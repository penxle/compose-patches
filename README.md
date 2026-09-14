# compose-patches

Compose patches used by [Typie](https://github.com/penxle/typie).

- `patches/`: independent patch files and provenance
- `releases/`: ordered patch sets and publication configuration; release IDs may differ from Maven versions
- `.github/workflows/publish.yml`: publishes missing or changed releases after a push to `main`
- Maven registry: `https://maven.pkg.github.com/penxle/compose-patches`

## Adding a patch

Add `patches/<patch-id>` containing a short README, `patch.json`, and the patch files. `patch.json` records the upstream repository, commit, version,
files, and focused verification commands.

Adding a patch does not publish it. Add its ID to `releases/<version>/release.json` in application order when it should be included in the published
artifacts.

Merge the change into `main`. The workflow publishes missing publications and replaces publications whose release configuration or patch contents have
changed.

Verification commands use one fully qualified Gradle task followed by optional `--tests PATTERN` pairs.
CI merges repeated tasks and test patterns into one Gradle invocation; an unfiltered task retains full test coverage.
It prepares all publication files in a local Maven repository before deleting replaced package versions, so compilation and metadata generation
finish before the registry is changed. The final step publishes those prepared build outputs through Gradle.

## Android and iOS releases

`releases/1.12.0` builds the JetBrains iOS patches. `releases/androidx-1.12.0` builds
AndroidX Compose UI from its own release commit. A release may set
`gradle_project_directory` to use a standalone upstream build, and
`version_property` only when its upstream needs a publication-version override.

For local verification, the publication init script accepts
`-PcomposePatchesRepository=/absolute/path/to/maven-repository`. It uses the same
publication tasks and provenance property without GitHub credentials.
