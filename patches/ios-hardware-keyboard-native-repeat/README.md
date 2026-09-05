# iOS hardware keyboard native repeat

Routes each hardware-key press to either UIKit or Compose once, while using UIKit's native callback cadence to repeat application-owned
vertical navigation and forward deletion.

Plain horizontal navigation and active text composition remain UIKit-owned. Native callback echoes are consumed without becoming duplicate
document edits.
