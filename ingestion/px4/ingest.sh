#!/usr/bin/env bash
# --- inputs (set by workflow or .env) ---
PX4="${PX4_VERSION:-latest}"
GITHUB_ORG="${GITHUB_ORG:-${GITHUB_REPOSITORY_OWNER:-github}}"
PLATFORM="linux/arm64"
SOURCE="px4io/px4-sitl:${PX4}"
TARGET="ghcr.io/${GITHUB_ORG}/third-party/px4-sitl:${PX4}"

# --- pull from upstream ---
echo "Pulling ${SOURCE} for ${PLATFORM}..."
docker pull --platform "${PLATFORM}" "${SOURCE}"

# --- push to internal registry ---
echo "Pushing to ${TARGET}..."
docker tag "${SOURCE}" "${TARGET}"
docker push "${TARGET}"