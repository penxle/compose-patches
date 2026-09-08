# iOS text input view lifecycle

Follow-up to the existing 1.12.0 patch stack. Apply after `ios-hardware-keyboard-native-repeat`.
This is a separate, reversible patch; it does not modify the August or earlier September patches.

## Behavior

- Add the optional, experimental `UIKitTextInputMethodRequest` interface. A request receives the actual UIKit input view when Compose connects it and when the request stops using it.
- Attach session integration before Compose requests keyboard presentation. The Compose-rendered input view is not yet the first responder at that point; native-rendered text views may already be focused.
- Release the previous request's integration when replacing a request on the same connection, without detaching the reused UIKit view or scheduling its removal.
- Notify attachment only while the request still owns the connection after UIKit view setup. A request stopped or replaced during that setup receives neither attachment nor detachment.
- Release completed integration after a stopped connection has cleared its input state. If a connection ends inside the attachment callback, wait for that callback to return before cleanup. Repeated stops do not repeat cleanup.
- Preserve a newer request started reentrantly during old integration cleanup, and do not show the keyboard for a superseded request.

Callbacks configure and release integration only. The view remains owned by Compose; callbacks must not remove it or change its input connection.
The iOS sample is linked from the interface KDoc. This upstream revision's samples module is Android-only, so the `iosMain` sample is documentation source, not part of a compiled sample target.

## Typie integration

Typie decorates only its iOS editor request and installs its text-input and floating-cursor bridges directly on the supplied view. Cleanup belongs to that request, with generation checks protecting a later installation from older cleanup.
This replaces first-responder tree traversal and delayed installation retries; it does not change composition termination, keyboard-repeat policy, document navigation, or text-coordinate conversion.

Typie requires the artifact containing this patch before its new iOS request wrapper can compile. For local verification, publish both iOS architectures into an isolated Maven repository and pass that repository using Typie's `composePatchesRepository` property.
The 1.12.0 release manifest includes this patch after `ios-hardware-keyboard-native-repeat`. Roll back the Typie wrapper together with removing this patch from the artifact.

## Verification

The focused input-connection suite covers attach/show and stop/detach order, actual view identity, repeated stops, replacement without physical detachment, stop/replacement during UIKit view setup, replacement during old cleanup, and cleanup after attachment finishes, alongside the existing composition and reentrant-edit cases.
Typie additionally verifies direct pre-focus installation, stale cleanup, and floating-cursor callback ownership with Swift tests, and compiles against locally published iOS device and simulator artifacts.

Local reentrancy verification observed four failures against the previous implementation, then all 26 tests passed after the fix. The iOS device target compiled, and both device and simulator artifacts were published locally. Verification used `--no-configuration-cache` after the warm checkout initially ran an old 23-test executable despite updated source; build and compilation caches were retained. Check the executed test names and XML report when reusing an existing warm checkout.

The generic upstream instructions mention `updateApi` and `compileDebugKotlinAndroid`, but this fork revision does not register those tasks. No API dump or upstream Android verification is claimed; Typie's Android compilation is checked separately.
Physical-device keyboard/IME verification remains necessary before release.
