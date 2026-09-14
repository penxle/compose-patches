# Android text input focus transfer

Backport AndroidX commit [f3d1e163](https://github.com/androidx/androidx/commit/f3d1e1632c81ceeec2a0cd5f14a3ef985d0f8f80),
"Avoid keyboard flicker during focus transfers across text fields" (issue 530704636),
to the Compose UI 1.12.0 release commit `963bf914f78b389bdddef0da7f36bee19d897274`.

StartInput and ShowKeyboard keep the low-latency out-of-frame executor. StopInput
and HideKeyboard wait for the next animation frame, allowing the incoming field's
start request to supersede cleanup. A queued immediate dispatch is demoted when
cleanup arrives; the superseded runnable cannot execute the queue.

The backport retains the upstream implementation and regression tests. The only
adaptation is import context in PlatformTextInputViewIntegrationTest, where the
1.12.0 release still imports StandardTestDispatcher.

The separate `androidx-ui-playground.patch` adds a standalone Compose UI build
using AndroidX's existing playground support. It selects `:compose:ui:ui` and lets
AndroidX include its dependency graph. This avoids requiring an AOSP repo checkout
and does not change library source or Android behavior.

Run the commands in `patch.json` from `playground-projects/compose/ui-playground`
with JDK 21 and ANDROID_HOME pointing to an Android SDK. The regression suite
checks deferred cleanup, immediate startup, command coalescing, and stale runnable
invalidation. All 25 host tests pass against the complete patch set.

Cleanup is deferred until the next frame. A custom editor still needs to enqueue
its new input session before that frame to keep the keyboard visible across a
focus transfer; asynchronous state preparation can outlast this batching window.

This patch publishes `androidx.compose.ui:ui-android:1.12.0`. JetBrains' Android
variant redirects to AndroidX, so patching or publishing the iOS variants cannot
apply this fix to Android. Keep `isOutOfFrameSchedulerForTextInputEventsEnabled`
at its default true value when using the patched artifact.

Typie device verification on an LG LM_Q920N running Android 12 passed 12 body/header
round trips across normal and zero-duration animation settings. System Back and
the reading-mode button both dismissed the keyboard. Typie retains undispatched
session startup and synchronous initial IME-state preparation; the global
scheduler fallback and its R8 override are removed.
