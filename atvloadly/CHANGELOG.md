# Changelog

## 0.7.4-1

- Update the upstream ATVLoadly image from v0.7.1 to v0.7.4.
- Include PlumeImpactor v2.7.1-patch.4 with fixes for Apple login and expired sessions.
- Add upstream anisette server settings and per-account anisette resets.
- Apple ID signing now requires a remote anisette server. If installation or
  refresh fails because the server is unavailable, retry later or select another
  server in the application's advanced settings.
- Include upstream fixes for pairing, IPA icon parsing, and log rotation.

## 0.7.1-1

- Initial wrapper around the upstream ATVLoadly v0.7.1 image.
- Home Assistant ingress, private discovery services, and supervised processes.
- Persistent add-on data and cold backups; ARM64 and AMD64 builds.
