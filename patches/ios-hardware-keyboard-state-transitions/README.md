# iOS hardware keyboard state transitions

Apply after `ios-text-input-composition-sync` in the 1.12.0 patch stack.
Previously published patches remain unchanged.

- Read current modifier flags from the UIKit press event. If UIKit supplies further repeat callbacks
  after Shift changes, application commands use the latest modifiers rather than the initial state.
- Observe every physical key before routing it to the application or UIKit. A new non-modifier
  key ends the previous repeat bridge, so its native selection or deletion cannot replay an old key.
- End a repeat only when its own key is released. Releasing an earlier arrow does not stop a newer
  arrow's repeat, and finishing a press still happens after UIKit handles its final callbacks.

Native callbacks still supply the repeat cadence; this patch adds no timers or key-history tracker.
Initial native echoes, forward-delete preludes, composition ownership, and reentrant callback guards
retain their existing behavior. When UIKit provides no press event, key conversion keeps its existing
modifier fallback.

Regression tests cover Shift changes during a held arrow, overlapping editing keys, out-of-order
key release, and native selection reaching the text input connection after repeat ownership ends.
Focused iOS simulator tests and iOS arm64 compilation were verified. On the tested iPhone and hardware
keyboard, changing Shift during a held arrow stopped repeat; this behavior was accepted. Pressing
another arrow replaced the previous repeat, including repeating Up while Down remained held. These
observations do not establish identical event ordering on every iOS version or keyboard.
