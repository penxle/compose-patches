# AndroidX Compose UI 1.12.0

Upstream: `androidx/androidx` at `963bf914f78b389bdddef0da7f36bee19d897274`, the
[Compose UI 1.12.0 release](https://developer.android.com/jetpack/androidx/releases/compose-ui#1.12.0).

This release builds the Android text-input focus-transfer fix separately from the
JetBrains Compose Multiplatform release in `../1.12.0`. The source repositories,
commits, patch provenance, and publications are independent.

Only `androidx.compose.ui:ui-android:1.12.0` is published. Consumers must resolve
that exact module from the patch repository; the root `ui` metadata and the other
AndroidX libraries continue to come from Google Maven.

`gradle_project_directory` selects the standalone UI playground added by the
patch. AndroidX already declares version 1.12.0 in libraryversions.toml, so no
JetBrains version override property is needed.

To roll back, remove the consumer's repository override and resolve the original
Google Maven artifact. Updating to a later release requires checking whether it
contains the upstream fix; 1.12.1 disables the scheduler instead of backporting it.
