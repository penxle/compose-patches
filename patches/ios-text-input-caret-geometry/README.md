# iOS text input caret and range geometry

Apply after `ios-text-input-view-lifecycle` in the Compose 1.12.0 patch stack.

## Behavior

The Compose-rendered UIKit input view previously returned a fixed caret at `(1, 1, 0, 1)`
and no rectangle for text ranges. Moving the hidden input view near the caret could not
supply the composing range or the caret's actual height to the Japanese IME.

- Observe the focused rectangle and unclipped text origin alongside the field and clipping geometry.
- Add an optional `UIKitTextInputMethodRequest.firstRectForRangeInRoot` callback for custom editors.
  It accepts a UTF-16 range and returns its first visual line, or the caret for an empty range, in root pixels.
- Apply pending native edits before answering a synchronous geometry query, so the requested
  text and the host layout agree. Recheck text and session identity after the custom callback,
  which can wait for another editor operation or reenter input attachment. Other input callbacks remain batched.
- Answer UIKit's range and position queries from that callback, converting current root coordinates
  through the actual input view frame into local UIKit points.
- A missing callback retains focused-caret support. A callback that returns no geometry does not
  fall back to a different or stale caret. Rectangles outside the clipping region are unavailable.
- Notify UIKit when the unclipped text origin moves, even after a text edit with unchanged geometry.
  A custom editor supplies `unclippedTextOffsetInRoot` to expose scrolling independently of the caret.
  Keep suppressing other layout changes caused by IME edits, including delayed field resizing,
  so native caret movement does not receive duplicate selection notifications.

Geometry queries preserve the existing edit commands and marked ranges; they do not change
keyboard routing or fabricate a Compose text layout. The native text-input rendering path is unchanged.

## Typie integration

Typie supplies the requested range from its Rust layout and converts it through the displayed
page's current scroll position, zoom, and density. IME text and range geometry use the same applied
state, including before its rendered frame is published. The revision and UTF-16 window offsets
are read under the editor lock and converted to flat character offsets before querying Rust.
A collapsed query at the current caret preserves its affinity at soft-wrap boundaries.
The iOS request wrapper forwards the callback through its existing platform bridge. The first
page's root position supplies the unclipped document origin; every page retains layout coordinates
even offscreen, so changing the selected page does not look like a scroll.

Remove Typie's `fixedLocalCaretTextFieldRectInRoot` workaround with this patch, regenerate its FFI
bindings, and build against the patched Compose artifacts. Roll back the new request integration
and restore the field-frame workaround together if removing this patch.

## Verification

Regression coverage includes requested ranges and arbitrary caret positions, caret-only updates,
field-origin changes, zero-width carets, unavailable or clipped geometry, a single scroll after an
equal-width marked-text replacement, delayed native caret/field updates, callback-time text or
session replacement,
queries made before pending edits are flushed or rendered frames are published, and preservation
of Japanese marked text without duplicate edit dispatch. The initial range test returned `CGRectNull`; the
initial scroll test received no UIKit geometry notifications.

Physical-device candidate alignment and scroll behavior require separate confirmation; these
unit tests do not render the system IME candidate window.

As with the lifecycle patch, this fork does not register the generic `updateApi` or
`compileDebugKotlinAndroid` tasks. Typie's Android target is compiled separately.
