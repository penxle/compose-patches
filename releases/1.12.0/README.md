# Compose 1.12.0 patch composition

Upstream: `f29d2f99f3beafc60992c6a73dbbaa9f841c5d4c`.

## August source baseline

The last patch-repository commit before September 2026 is
`81f3b27999ca8efa727e3a7fa694c0a7fff71526` (August 31).
Its four patch directories and their order are preserved byte-for-byte:

1. `ios-velocity-tracker`
2. `ios-text-input-edit-batching`
3. `ios-compose-text-input-initial-frame`
4. `ios-zero-duration-keyboard-frame`

This is a source baseline, not an assertion that a particular shipped app binary
was built from this exact commit.

## September follow-ups

Apply these after the August baseline, in order:

1. `ios-text-input-composition-sync`: composition synchronization and reentrant
   flush handling, previously split between `ios-text-input-composition-sync`
   and `ios-text-input-reentrant-flush`.
2. `ios-hardware-keyboard-native-repeat`: hardware-key ownership and repetition,
   previously split between `ios-hardware-keyboard-native-repeat`
   and `ios-hardware-keyboard-state-transitions`.
3. `ios-text-input-view-lifecycle`: explicit UIKit input-view attachment and
   detachment callbacks, including cancellation and reentrant request replacement.
   Typie uses these callbacks to install its bridges without first-responder
   traversal or delayed retries.
4. `ios-text-input-caret-geometry`: deliver actual caret and text-range rectangles
   to the Compose-rendered UIKit input view and notify UIKit about scrolling.
   Typie supplies range geometry from its Rust layout and removes its field-frame workaround.

The first follow-up can be applied without the second. The second patch is based
on the first, including its input-test fixture. The lifecycle patch is
based on both. Remove caret geometry before removing lifecycle support and
Typie's request wrapper that consumes its API.

The caret-geometry patch can be removed independently, together with reverting
Typie's range callback and restoring its field-frame workaround.

The consolidation of the first two follow-ups produced exactly the same source
files and tests as the previous seven-patch release plus the reviewed,
uncommitted reentrant-flush patch.
No implementation changes or tests are dropped during consolidation. Earlier
published patch revisions remain in Git history; they are not rewritten.

## Source rollback

To restore the August source baseline, remove all four September follow-up IDs from
`release.json`, leaving the first four IDs unchanged. When reversing patches in
an already-patched checkout, reverse caret geometry first, then lifecycle and hardware handling,
then IME synchronization.
After removing lifecycle handling, hardware handling can also be removed while
leaving the IME fixes available.

Verified Git source-tree IDs at the consolidation boundary:

- August baseline: `fc5f1ffa0058f26a8f6be4ceb7fc162414f06bed`
- August plus IME follow-up: `f0dcec98500f949549dc2b7bc66e2994226aff83`
- Complete September stack: `14c7316b55c68d93f872d13362502690566a705a`

The publication workflow replaces artifacts at the same Maven version when patch
provenance changes. A source rollback therefore requires rebuilding and
republishing; it does not select or preserve an old binary. This consolidation
does not change that publication policy.
