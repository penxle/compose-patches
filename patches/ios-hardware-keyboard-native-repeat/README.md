# iOS hardware keyboard native repeat

September 2026 hardware-keyboard routing and repeat handling. Apply after `ios-text-input-composition-sync`.
This combines native repeat support and its key/modifier state-transition fixes into one patch.

Routes each hardware-key press to either UIKit or Compose once, while using UIKit's native callback cadence to repeat application-owned
vertical navigation and forward deletion.

Plain horizontal navigation and active text composition remain UIKit-owned. Native callback echoes are consumed without becoming duplicate
document edits.

- Read current modifier flags from the UIKit press event so subsequent repeats do not retain an earlier Shift state.
- Observe physical keys before routing them. A new non-modifier key ends the previous repeat, so its native callback cannot replay an old key.
- End a repeat only when its own key is released. Releasing an earlier arrow does not stop a newer arrow's repeat.
- Preserve initial native-echo suppression, forward-delete preludes, composition ownership, and reentrant callback guards.

Native callbacks provide the repeat cadence; there are no timers or key-history trackers. Regression tests cover repeat routing,
Shift changes, overlapping editing keys, out-of-order release, and native selection after repeat ownership ends.

On the tested iPhone and hardware keyboard, changing Shift during a held arrow stopped repeat; this behavior was accepted. Pressing
another arrow replaced the previous repeat, including repeating Up while Down remained held. These observations do not establish
identical event ordering on every iOS version or keyboard.

Removing this patch leaves the IME follow-up intact. For the August source baseline and rollback order,
see [the release notes](../../releases/1.12.0/README.md).
