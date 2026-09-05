# iOS text input composition synchronization

Follow-up to `ios-text-input-edit-batching`, applied after `ios-hardware-keyboard-native-repeat` in the 1.12.0 release.
The previously published patches are unchanged; this patch contains only the subsequent composition and native-edit synchronization fixes.

- Preserve the marked range while predicting edits. `EditProcessor.reset` commits the initial composition, so restore it before applying
  each callback. Continuing or committing marked text must be predicted as replacement, not insertion followed by a spurious external-change notification.
- Apply `setMarkedText`'s relative UTF-16 selection to the new marked text, preserving its internal caret and selection.
- Keep focus while Escape is handled by an active composition. Releasing the same key after composition ends must not blur the editor.
- Expose the synchronous Objective-C action `flushPendingTextInputEdits` on the Compose text input view. Cancel its scheduled flush,
  apply each pending command once, and retain newer state if the host replaces the input session or reenters native editing.

Ordinary IME callbacks retain their existing batching. The caller chooses an explicit native editing boundary; this patch neither detects
keyboard languages nor ends composition itself.

Consumers must apply commands in order: a `SetSelectionCommand` after `SetComposingTextCommand` refers to the updated text.
UTF-16 conversion must therefore use that updated text, not the snapshot at the beginning of the batch.

Regression coverage includes marked-text replacement within and across batches, final composition commit, marked-text selection with surrogate
pairs and empty replacement, real external-change notifications, Escape focus across key-down and key-up, synchronous flush without replay,
session replacement, and reentrant edits.
