# Home Assistant Add-on: iSponsorBlockTV Legacy

Automatically skip sponsor segments in YouTube videos on Apple TV. This add-on
preserves the May 31, 2023 upstream build (`1aa06e6`), using direct Apple TV
control through pyatv instead of v2's YouTube remote sessions.

Supports **aarch64** and **amd64**, using the exact upstream image pinned in the
[Dockerfile](./Dockerfile). The application and its dependencies are unchanged.

Before starting, fill in the add-on's **Configuration**:

- `apikey`: your YouTube Data API v3 key, used to identify the playing video.
- `atvs`: each Apple TV's `identifier` and `airplay_credentials` from legacy
  iSponsorBlockTV pairing.
- `skip_categories`: SponsorBlock categories to skip; defaults to `sponsor`.
- `channel_whitelist`: channels to leave untouched, using `id` and an optional
  `name`; defaults to an empty list.

When migrating a legacy installation, copy these values from its `config.json`.
YouTube TV linking codes from v2 are not compatible with this version.

For fresh pairing, run the pinned upstream setup on a Linux Docker host on the
same network as the TVs, from a new empty directory:

```sh
printf '{}\n' > config.json
docker run --rm -it --network=host -v "$PWD:/setup" \
  ghcr.io/dmunozv04/isponsorblocktv@sha256:15f150c2ca6360af579952ac695ff6f92669e6c1fb5a28f2fc256fd9916470ed \
  --setup --file /setup/config.json
```

Follow the pairing and API-key prompts, then copy the generated `config.json`
values into the add-on's Configuration. The upstream wiki now describes v2;
use the pinned image above for legacy setup.

Home Assistant and the Apple TVs must be on the same network for discovery.
Stop the old instance before starting this add-on against the same TVs.
Enable **Start on boot** to keep skipping after Home Assistant restarts.
There is no web interface; use the add-on's Configuration and Log tabs.

Settings and pairing credentials stay in Home Assistant's private add-on storage
and are included in add-on backups. Restart the add-on after changing settings.
This is a frozen legacy release: it retains the old behavior and does not receive
new upstream fixes or v2's YouTube ad muting/skipping features.

Application by the [upstream contributors](https://github.com/dmunozv04/iSponsorBlockTV),
licensed under [GPL-3.0](https://github.com/dmunozv04/iSponsorBlockTV/blob/1aa06e677f4d1f30da11f86f5ba30cc91b019efc/LICENSE.md).
