# compose-patches

Compose patches used by [Typie](https://github.com/penxle/typie).

- `patches/`: patches, provenance, and release configuration
- `.github/workflows/publish.yml`: publishes missing or changed releases after a push to `main`
- Maven registry: `https://maven.pkg.github.com/penxle/compose-patches`

## Adding a patch

Add a directory under `patches/` containing the patch files, a short README, and a `release.json`. Copy an existing `release.json` and update:

- the upstream repository, commit, version property, and version;
- `patches`, in application order;
- `verify_args`, passed to the upstream Gradle wrapper;
- `publications`, with each Maven coordinate and its GitHub Packages publication task.

Merge the change into `main`. The workflow publishes missing publications and replaces publications whose release configuration or patch contents have
changed.
