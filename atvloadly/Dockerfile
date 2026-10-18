# Both Supervisor and the repository builder supply --platform for this index.
# Do not use BUILD_FROM: newer Supervisors override it with the HA base image.
FROM ghcr.io/bitxeno/atvloadly:v0.7.1@sha256:1ade1ac88b9dbd2e687111437d196827729b1b525f9ec6d59e6ec9938aa04cbc

ARG S6_OVERLAY_VERSION=3.2.1.0
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        nginx dbus avahi-daemon jq xz-utils iproute2 \
    && rm -rf /var/lib/apt/lists/* \
    && case "$(dpkg --print-architecture)" in arm64) s6_arch=aarch64 ;; amd64) s6_arch=x86_64 ;; *) exit 1 ;; esac \
    && cd /tmp \
    && for arch in noarch "$s6_arch"; do \
        url="https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-${arch}.tar.xz"; \
        curl -fsSLO "$url" && curl -fsSLO "$url.sha256" \
        && sha256sum -c "s6-overlay-${arch}.tar.xz.sha256" \
        && tar -C / -Jxpf "s6-overlay-${arch}.tar.xz" || exit 1; \
    done \
    && rm -f /tmp/s6-overlay-*.tar.xz* \
    && rm -f /etc/nginx/sites-enabled/default

# Keep upstream's initialization, but let S6 own both foreground processes.
RUN test "$(grep -c '^/etc/init.d/usbmuxd start' /entrypoint.sh)" = 1 \
    && test "$(grep -c '^/usr/bin/atvloadly server' /entrypoint.sh)" = 1 \
    && sed '/^\/etc\/init.d\/usbmuxd start/d; /^\/usr\/bin\/atvloadly server/d' \
        /entrypoint.sh > /usr/local/bin/atvloadly-bootstrap \
    && chmod +x /usr/local/bin/atvloadly-bootstrap \
    && sed -i '/^server:$/a\  listen_addr: 127.0.0.1' /keep/config.yaml

COPY rootfs /
RUN chmod +x /usr/local/bin/atvloadly-init /etc/s6-overlay/s6-rc.d/*/run
ENV S6_BEHAVIOUR_IF_STAGE2_FAILS=2
ENTRYPOINT ["/init"]
