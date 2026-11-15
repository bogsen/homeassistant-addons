"""Prepare add-on versions and release notes on a Renovate branch."""

import argparse
import re
import subprocess
from pathlib import Path


ADDONS = {
    "atvloadly": "ghcr.io/bitxeno/atvloadly",
    "sidestore-vpn": "tailscale/tailscale",
}
UPSTREAMS = {
    "ghcr.io/bitxeno/atvloadly": ("ATVLoadly", "https://github.com/bitxeno/atvloadly"),
    "tailscale/tailscale": ("Tailscale", "https://github.com/tailscale/tailscale"),
    "ghcr.io/xddxdd/sidestore-vpn": ("SideStore reflector", "https://github.com/xddxdd/sidestore-vpn"),
}
VERSION = re.compile(r'^version: "(\d+\.\d+\.\d+)(?:-(\d+))?"$', re.M)
RELEASE = re.compile(
    r"\A# Changelog\n\n<!-- renovate-release -->\n## ([\d.-]+)\n.*?"
    r"<!-- /renovate-release -->\n\n", re.S
)


def images(dockerfile):
    return dict(re.findall(r"^FROM (\S+?):(\S+)", dockerfile, re.M))


def upstream_version(image):
    match = re.fullmatch(r"v(\d+\.\d+\.\d+)@sha256:[a-f0-9]{64}", image)
    if not match:
        raise ValueError(f"Expected a pinned stable upstream image, got {image!r}")
    return match[1]


def upstream_links(repository, old_tag, tag):
    return (
        f"[Release notes]({repository}/releases/tag/{tag}) · "
        f"[All changes]({repository}/compare/{old_tag}...{tag})."
    )


def prepare(addon, before, after, base_config, config, changelog):
    if before == after:
        return config, changelog
    old, new = images(before), images(after)
    primary = ADDONS[addon]
    upstream = upstream_version(new[primary])
    base = VERSION.search(base_config)
    if not base or len(VERSION.findall(config)) != 1:
        raise ValueError("Expected one quoted add-on version")
    revision = int(base[2] or 0) + 1 if base[1] == upstream else 1
    version = f"{upstream}-{revision}"
    notes = []
    if old.keys() != new.keys():
        raise ValueError("The Docker build stages changed; review release notes manually")
    for image, value in new.items():
        if old[image] == value:
            continue
        old_tag, old_digest = old[image].split("@sha256:")
        tag, digest = value.split("@sha256:")
        label, repository = UPSTREAMS[image]
        if old_tag != tag:
            notes.append(
                f"- Update {label} from {old_tag.removeprefix('v')} to {tag.removeprefix('v')}. "
                + upstream_links(repository, old_tag, tag)
            )
        else:
            notes.append(
                f"- Update {label} image digest (`{old_digest[:12]}` → `{digest[:12]}`). "
                f"[Upstream]({repository})."
            )
    old_s6 = re.findall(r"^ARG S6_OVERLAY_VERSION=(\S+)$", before, re.M)
    new_s6 = re.findall(r"^ARG S6_OVERLAY_VERSION=(\S+)$", after, re.M)
    if old_s6 != new_s6:
        if len(old_s6) != 1 or len(new_s6) != 1:
            raise ValueError("s6-overlay version was added or removed")
        notes.append(
            f"- Update s6-overlay from {old_s6[0]} to {new_s6[0]}. "
            + upstream_links(
                "https://github.com/just-containers/s6-overlay",
                f"v{old_s6[0]}", f"v{new_s6[0]}",
            )
        )
    if not notes:
        raise ValueError("No recognized dependency changes in Dockerfile")
    config = VERSION.sub(f'version: "{version}"', config)
    changelog = changelog.replace("\r\n", "\n")
    previous = RELEASE.match(changelog)
    base_version = f"{base[1]}-{base[2]}" if base[2] else base[1]
    # Replace this PR's generated entry on reruns, preserving released history.
    if previous and previous[1] != base_version:
        changelog = "# Changelog\n\n" + changelog[previous.end():]
    if not changelog.startswith("# Changelog\n\n"):
        raise ValueError("Expected a '# Changelog' heading")
    entry = (
        f"<!-- renovate-release -->\n## {version}\n\n"
        + "\n".join(notes) + "\n<!-- /renovate-release -->\n\n"
    )
    return config, "# Changelog\n\n" + entry + changelog[len("# Changelog\n\n"):]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--base", required=True)
    args = parser.parse_args()
    # A stale PR must be rebased before calculating its next release revision.
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", args.base, "HEAD"],
        cwd=args.repository, check=True,
    )
    changes = {}
    for addon in ADDONS:
        def read_base(name):
            return subprocess.check_output(
                ["git", "show", f"{args.base}:{addon}/{name}"],
                cwd=args.repository, text=True,
            )

        directory = args.repository / addon
        config, changelog = prepare(
            addon, read_base("Dockerfile"), (directory / "Dockerfile").read_text(),
            read_base("config.yaml"), (directory / "config.yaml").read_text(),
            (directory / "CHANGELOG.md").read_text(),
        )
        changes[directory / "config.yaml"] = config
        changes[directory / "CHANGELOG.md"] = changelog
    for path, content in changes.items():
        path.write_text(content)


if __name__ == "__main__":
    main()
