# Home Assistant Add-on: SideStore VPN

Use [SideStore](https://sidestore.io) while keeping Tailscale connected on your
iPhone or iPad. This add-on combines the original
[SideStore packet reflector](https://github.com/xddxdd/sidestore-vpn) with
Tailscale in its own network namespace. It advertises only `10.7.0.1/32` and
preserves the phone's source address. Your existing Tailscale add-on can continue
routing LAN subnets with its own settings.

Supports **aarch64** and **amd64**. Requires Home Assistant OS with `/dev/net/tun`
and IPv4 forwarding in the add-on's network namespace.

## Setup

1. Install and start the add-on. Optionally change its Tailscale `hostname` first.
2. Open the add-on logs and follow Tailscale's login link. Sign in to the same
   tailnet as your phone. This creates a separate machine named `sidestore-vpn`.
3. In the [Tailscale admin console](https://login.tailscale.com/admin/machines),
   approve this machine's **`10.7.0.1/32` subnet route**. If another machine
   advertises this same route, remove that advertisement to avoid ambiguity.
4. Connect Tailscale on your phone. In newer SideStore builds, open Settings →
   Connection Config, turn **Use Local VPN off**, and set **Device IP / Endpoint**
   to **`10.7.0.1`**. Keep your existing valid pairing file. Remote Pairing port
   requirements depend on your iOS and SideStore versions.
5. Check SideStore's Device Reachability, then test a refresh and installation.
   Start with the phone connected to Wi-Fi. Cellular use depends on SideStore and
   iOS; this add-on does not enable the phone's developer services itself.

Enable **Start on boot** and **Watchdog** in Home Assistant after setup.
Login state lives in private `/data` storage and survives restarts and upgrades.
Include the add-on in backups; cold backups briefly stop its connection.

## Networking and access rules

This node uses kernel networking with subnet SNAT and stateful filtering disabled,
as required by the reflector. No LAN static route or Tailscale exit node is
needed when the phone uses the advertised Tailscale route.

With a restrictive tailnet policy, allow the phone to connect to `10.7.0.1` and
allow `10.7.0.1` to initiate connections back to that phone. Reflection starts a
second connection with the ports preserved; allowing only normal return traffic
is insufficient. Scope access to your intended devices. The standard allow-all
tailnet policy already allows both directions.

The add-on maps its Tailscale UDP port to **41642** on Home Assistant. A router
port forward to this port is optional and may help establish direct connections;
Tailscale can also use relays. No application ports or web interface are exposed.

If connection checks pass but installs fail, inspect the pairing file, Remote
Pairing port, and SideStore logs. Reachability alone does not prove installation
works. See the [upstream issues](https://github.com/xddxdd/sidestore-vpn/issues)
for version-specific reports.

The reflector is provided by [xddxdd and contributors](https://github.com/xddxdd/sidestore-vpn)
under the Unlicense. Tailscale is provided by
[Tailscale and contributors](https://github.com/tailscale/tailscale) under BSD-3-Clause.
