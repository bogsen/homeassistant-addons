# Home Assistant Add-on: atvloadly

[atvloadly](https://github.com/bitxeno/atvloadly) installs and automatically
refreshes sideloaded apps on Apple TV. This add-on brings its web interface into
Home Assistant, with Apple TV discovery and persistent storage included.

Supports **aarch64** and **amd64**, using the official upstream image.

Install and start the add-on, then open it using **Open Web UI** or the Home
Assistant sidebar. Configure the application in its own interface.

- Enable **Start on boot** to keep scheduled refreshes running after restarts.
- Settings, credentials, and apps persist in private add-on storage.
- Include the add-on in Home Assistant backups. Backups briefly stop it, so take
  them between installation or refresh jobs.

From v0.7.4, Apple ID signing requires a remote anisette server. You can select
the server and reset anisette data for an individual account in the application's
advanced settings. If installation or refresh fails because the remote server
is unavailable, retry later or select another server.

See the [upstream documentation](https://github.com/bitxeno/atvloadly/tree/v0.7.4#readme)
for pairing, Apple login, installing apps, and refresh settings.

Application and artwork by the [upstream contributors](https://github.com/bitxeno/atvloadly),
licensed under [AGPL-3.0](https://github.com/bitxeno/atvloadly/blob/v0.7.4/LICENSE).
