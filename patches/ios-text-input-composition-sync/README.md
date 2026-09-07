# iOS text input composition synchronization

September 2026 follow-up to the unchanged August patch stack, including `ios-text-input-edit-batching`.
Apply before `ios-hardware-keyboard-native-repeat` in the 1.12.0 release.
This combines composition synchronization and reentrant flush handling into one patch; it does not replace the August batching patch.

- Preserve the marked range while predicting edits. `EditProcessor.reset` commits the initial composition, so restore it before applying
  each callback. Continuing or committing marked text must be predicted as replacement, not insertion followed by a spurious external-change notification.
- Apply `setMarkedText`'s relative UTF-16 selection to the new marked text, preserving its internal caret and selection.
- Keep focus while Escape is handled by an active composition. Releasing the same key after composition ends must not blur the editor.
- Expose the synchronous Objective-C action `flushPendingTextInputEdits` on the Compose text input view. Cancel its scheduled flush,
  apply each pending command once, and retain newer state if the host replaces the input session or reenters native editing.
- Tie snapshot-notification suppression to the native edit generation being applied. A completed nested flush supersedes the outer
  prediction, and a subsequent host change must still notify UIKit whether its snapshot arrives synchronously or later.
- Reconcile host transformations through the existing value-update callback, preserving both delegate notifications and native-view
  geometry updates.

Ordinary IME callbacks retain their existing batching. The caller chooses an explicit native editing boundary; this patch neither detects
keyboard languages nor ends composition itself.

Consumers must apply commands in order: a `SetSelectionCommand` after `SetComposingTextCommand` refers to the updated text.
UTF-16 conversion must therefore use that updated text, not the snapshot at the beginning of the batch.

Regression coverage includes marked-text replacement within and across batches, final composition commit, marked-text selection with surrogate
pairs and empty replacement, real external-change notifications, Escape focus across key-down and key-up, synchronous flush without replay,
session replacement, nested native edits, synchronous snapshot echoes, and host changes after nested flushes.

The patch and its input tests also apply without the hardware-keyboard patch. For the August source baseline and rollback order,
see [the release notes](../../releases/1.12.0/README.md).
