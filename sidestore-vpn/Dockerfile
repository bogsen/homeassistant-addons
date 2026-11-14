# Copy the original reflector without building or modifying its Rust source.
FROM ghcr.io/xddxdd/sidestore-vpn:latest@sha256:077de9af996cae9d63803715f2eb54596d6e48a37069f9b15656990459c4c9d4 AS reflector
FROM tailscale/tailscale:v1.104.7@sha256:72c1e19e0aedca96b8533bbb0b4368564410ff20b17e53b804eb6c1f04a31be4

# Home Assistant OS provides nftables rather than legacy iptables tables.
RUN apk add --no-cache bash jq \
    && test -x /usr/sbin/xtables-nft-multi \
    && ln -sf /usr/sbin/xtables-nft-multi /usr/sbin/iptables \
    && ln -sf /usr/sbin/xtables-nft-multi /usr/sbin/ip6tables
COPY --from=reflector /sidestore-vpn /usr/local/bin/sidestore-vpn
COPY rootfs /
RUN chmod +x /usr/local/bin/sidestore-vpn-run

ENV TS_USERSPACE=false \
    TS_STATE_DIR=/data/tailscale \
    TS_SOCKET=/tmp/tailscaled.sock \
    TS_ACCEPT_DNS=false \
    TS_ROUTES=10.7.0.1/32 \
    TS_EXTRA_ARGS="--snat-subnet-routes=false --stateful-filtering=false --accept-routes=false" \
    TS_TAILSCALED_EXTRA_ARGS="--port=41641 --verbose=-1"

ENTRYPOINT ["/usr/local/bin/sidestore-vpn-run"]
