# compose-patches

Compose patches used by [Typie](https://github.com/penxle/typie).

- `patches/`: independent patch files and provenance
- `releases/`: ordered patch sets and publication configuration
- `.github/workflows/publish.yml`: publishes missing or changed releases after a push to `main`
- Maven registry: `https://maven.pkg.github.com/penxle/compose-patches`

## Adding a patch

Add `patches/<patch-id>` containing a short README, `patch.json`, and the patch files. `patch.json` records the upstream repository, commit, version,
files, and focused verification commands.

Adding a patch does not publish it. Add its ID to `releases/<version>/release.json` in application order when it should be included in the published
artifacts.

Merge the change into `main`. The workflow publishes missing publications and replaces publications whose release configuration or patch contents have
changed.
