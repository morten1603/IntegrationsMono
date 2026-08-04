#!/usr/bin/env bash

# --- inputs (set by workflow or .env) ---
REDIS_VERSION="${REDIS_VERSION:-7.2.4}"
PLATFORM="linux/arm64"
SOURCE="docker.io/library/redis:${REDIS_VERSION}"
TARGET="ghcr.io/${{ github.repository_owner }}/third-party/redis:${REDIS_VERSION}"

# --- pull from upstream ---
echo "Pulling ${SOURCE} for ${PLATFORM}..."
docker pull --platform "${PLATFORM}" "${SOURCE}"

# --- push to internal registry ---
echo "Pushing to ${TARGET}..."
docker tag "${SOURCE}" "${TARGET}"
docker push "${TARGET}"
