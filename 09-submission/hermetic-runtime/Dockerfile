FROM ghcr.io/foundry-rs/foundry@sha256:7ec8952cc5322dce65091768e9efab8641ea9b54105f21fd71d4ae3dc3da05a8 AS foundry
FROM ghcr.io/argotorg/solc@sha256:e56ef5e376ae846f06b919d7ca4ed0c271f7fb0900daa6c660d53451f5bfd9db AS solidity
FROM texlive/texlive@sha256:bd551dda2195c6830bb714f731d74c4f71cda812178abae15a206fd68b5dbb7c

ARG DEBIAN_FRONTEND=noninteractive

ENV FORCE_SOURCE_DATE=1 \
    TZ=UTC \
    LC_ALL=C \
    LANG=C

RUN apt-get update \
    && apt-get install -y --no-install-recommends poppler-utils=26.07.0-2 \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

COPY --from=foundry /usr/local/bin/forge /usr/local/bin/forge
COPY --from=solidity /usr/bin/solc /usr/local/bin/solc

# Match the local macOS workspace owner so the isolated output bind mount does
# not receive root-owned artifacts. The runtime remains capability-free and
# read-only when invoked by build_submission_package.py.
USER 501:20
WORKDIR /workdir

LABEL org.opencontainers.image.title="PoI ALR hermetic TeX and Solidity runtime" \
      org.opencontainers.image.description="Digest-pinned TeX Live 2026, Foundry 1.5.1, Solidity 0.8.24, and version-locked Poppler PDF QA tools" \
      org.opencontainers.image.base.name="texlive/texlive@sha256:bd551dda2195c6830bb714f731d74c4f71cda812178abae15a206fd68b5dbb7c"
