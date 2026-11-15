import importlib.util
import unittest
from pathlib import Path


spec = importlib.util.spec_from_file_location(
    "release", Path(__file__).with_name("prepare-renovate-release.py")
)
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)
ROOT = Path(__file__).resolve().parents[2]


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.addon = "atvloadly"
        self.docker = (ROOT / self.addon / "Dockerfile").read_text()
        self.config = (ROOT / self.addon / "config.yaml").read_text()
        self.history = (ROOT / self.addon / "CHANGELOG.md").read_text()

    def prepare(self, after, config=None, changelog=None):
        return release.prepare(
            self.addon, self.docker, after, self.config,
            config or self.config, changelog or self.history,
        )

    def test_grouped_upstream_and_s6_update(self):
        after = self.docker.replace("v0.7.4@", "v0.8.3@").replace("=3.2.1.0", "=3.2.3.2")
        config, changelog = self.prepare(after)
        self.assertIn('version: "0.8.3-1"', config)
        self.assertIn("## 0.8.3-1", changelog)
        self.assertIn("Update ATVLoadly from 0.7.4 to 0.8.3.", changelog)
        self.assertIn("Update s6-overlay from 3.2.1.0 to 3.2.3.2.", changelog)
        self.assertIn("https://github.com/bitxeno/atvloadly/releases/tag/v0.8.3", changelog)
        self.assertIn("https://github.com/bitxeno/atvloadly/compare/v0.7.4...v0.8.3", changelog)
        self.assertIn("https://github.com/just-containers/s6-overlay/releases/tag/v3.2.3.2", changelog)
        self.assertIn("https://github.com/just-containers/s6-overlay/compare/v3.2.1.0...v3.2.3.2", changelog)
        self.assertTrue(changelog.endswith(self.history.removeprefix("# Changelog\n\n")))
        self.assertEqual(self.prepare(after, config, changelog), (config, changelog))

    def test_s6_only_bumps_revision(self):
        config, changelog = self.prepare(self.docker.replace("=3.2.1.0", "=3.2.3.2"))
        self.assertIn('version: "0.7.4-2"', config)
        self.assertNotIn("Update ATVLoadly", changelog.split("## 0.7.4-1")[0])

    def test_corrects_the_existing_pr_version(self):
        after = self.docker.replace("v0.7.4@", "v0.8.3@")
        config, _ = self.prepare(after, config=self.config.replace("0.7.4-1", "0.7.4-2"))
        self.assertIn('version: "0.8.3-1"', config)

    def test_digest_update_preserves_primary_version(self):
        after = self.docker.replace("c613dcbfa1a6638e1c02a2820b1abbe1f65c8dd71ec9904ee53ba410886b63cf", "a" * 64)
        config, changelog = self.prepare(after)
        self.assertIn('version: "0.7.4-2"', config)
        self.assertIn("Update ATVLoadly image digest", changelog)
        self.assertIn("[Upstream](https://github.com/bitxeno/atvloadly)", changelog)

    def test_sidestore_upstream_and_reflector(self):
        addon = "sidestore-vpn"
        docker = (ROOT / addon / "Dockerfile").read_text()
        config = (ROOT / addon / "config.yaml").read_text()
        history = (ROOT / addon / "CHANGELOG.md").read_text()
        after = docker.replace("v1.104.7@", "v1.106.0@")
        result, notes = release.prepare(addon, docker, after, config, config, history)
        self.assertIn('version: "1.106.0-1"', result)
        self.assertIn("Update Tailscale from 1.104.7 to 1.106.0.", notes)
        self.assertIn("https://github.com/tailscale/tailscale/releases/tag/v1.106.0", notes)
        self.assertIn("https://github.com/tailscale/tailscale/compare/v1.104.7...v1.106.0", notes)
        after = docker.replace("077de9af996cae9d63803715f2eb54596d6e48a37069f9b15656990459c4c9d4", "b" * 64)
        result, notes = release.prepare(addon, docker, after, config, config, history)
        self.assertIn('version: "1.104.7-2"', result)
        self.assertIn("Update SideStore reflector image digest", notes)
        self.assertIn("[Upstream](https://github.com/xddxdd/sidestore-vpn)", notes)
        self.assertNotIn("/commit/", notes)

    def test_released_generated_notes_are_preserved(self):
        after = self.docker.replace("=3.2.1.0", "=3.2.3.2")
        generated = "# Changelog\n\n<!-- renovate-release -->\n## 0.7.4-1\n\n- A released change.\n<!-- /renovate-release -->\n\n## 0.7.1-1\n"
        _, notes = self.prepare(after, changelog=generated)
        self.assertEqual(notes.count("## 0.7.4-1"), 1)
        self.assertIn("- A released change.", notes)
        self.assertIn("## 0.7.4-2", notes)

    def test_no_change_and_unrecognized_change(self):
        self.assertEqual(self.prepare(self.docker), (self.config, self.history))
        with self.assertRaisesRegex(ValueError, "No recognized"):
            self.prepare(self.docker + "\n# unrelated edit\n")
        with self.assertRaisesRegex(ValueError, "pinned stable"):
            self.prepare(self.docker.replace("v0.7.4@", "latest@"))


if __name__ == "__main__":
    unittest.main()
