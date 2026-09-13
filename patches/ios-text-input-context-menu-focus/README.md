# iOS text input context menu focus

Upstream: `JetBrains/compose-multiplatform-core` at
`f29d2f99f3beafc60992c6a73dbbaa9f841c5d4c` (Compose 1.12.0).

## Problem

With the default iOS context-menu implementation (`isNewContextMenuEnabled = false`),
every composed `BasicTextField` publishes system copy, paste, cut, and select-all
callbacks into the scene's shared `UIKitNativeTextInputContext`, including unfocused
fields. A custom editor can therefore receive a UIKit input view whose system paste
callback belongs to an unfocused title or subtitle. The custom editor's own Command-V
handler can paste into the body while UIKit's system action modifies the other field.

## Change

Only the focused field publishes system editing actions. Each action also checks
focus when executed, so a callback installed before a focus transition cannot modify
the previous field. This covers both `TextFieldValue` and `TextFieldState` fields.
The latter's existing focus property becomes snapshot-observable so changing focus
updates system actions even when the text and selection stay unchanged.

The opt-in new context-menu implementation is unchanged. No public API is added.

## Verification

The iOS regression tests compose real text fields and a separate focus target, with
a test clipboard and a recording implementation of the native menu context. They
verify unfocused fields cannot receive system paste, paste follows focus between
fields, and an installed callback becomes ineffective immediately after focus moves.
Each scenario runs with both text-field APIs.

Before the fix, all three tests failed; the first inserted `pasted` into the unfocused
subtitle. After the fix, the three regressions and four existing focus/input tests
pass, and the iOS arm64 library compiles. The tests exercise callback ownership;
a physical iPad Command-V event has not been replayed.
Both iOS foundation publications were also generated in a temporary local Maven
repository, with their coordinates and patched source archives verified.

Commands are recorded in `patch.json` and run through the Compose warm verifier.
Untouched upstream formatting is preserved; the changed code and new test were
checked with `ktCheckFile --format`.

## Integration

This patch is independent of the UI patch stack. Apply it at the recorded upstream
commit and publish `foundation-iosarm64` and `foundation-iossimulatorarm64` alongside
the existing UI artifacts. Typie's `apps/mobile/settings.gradle.kts` must include both
foundation artifacts in the patch repository's exclusive-content filter.

Removing this patch restores the original foundation implementation. Remove the two
foundation publication entries and the matching consumer repository filters when
returning to the unpatched foundation artifacts.
