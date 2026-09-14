import org.gradle.api.publish.maven.MavenPublication
import org.gradle.api.publish.PublishingExtension
import org.gradle.kotlin.dsl.configure

val localRepository = gradle.startParameter.projectProperties["composePatchesRepository"]
val githubActor = System.getenv("GITHUB_ACTOR")
val githubToken = System.getenv("GITHUB_TOKEN")
val patchProvenanceSha256 =
    System.getenv("PATCH_PROVENANCE_SHA256")
        ?.takeIf { it.matches(Regex("[0-9a-f]{64}")) }
        ?: error("PATCH_PROVENANCE_SHA256 must be a lowercase SHA-256")

gradle.beforeProject {
    pluginManager.withPlugin("maven-publish") {
        extensions.configure<PublishingExtension> {
            publications.withType(MavenPublication::class.java).configureEach {
                pom.properties.put("typie.patch.sha256", patchProvenanceSha256)
            }
            repositories {
                maven {
                    name = "GitHubPackages"
                    url = uri(localRepository ?: "https://maven.pkg.github.com/penxle/compose-patches")
                    if (localRepository == null) {
                        credentials {
                            username = githubActor ?: error("GITHUB_ACTOR is required")
                            password = githubToken ?: error("GITHUB_TOKEN is required")
                        }
                    }
                }
            }
        }
    }
}
