#!/usr/bin/env bash
# deploy.sh - Build and sideload OpenBible-TV to Roku (Linux/macOS)
# Usage: ./deploy.sh
# Or with overrides: ./deploy.sh --host 192.168.0.5 --password mypassword

set -euo pipefail

ROKU_HOST="${ROKU_HOST:-}"
ROKU_PASSWORD="${ROKU_PASSWORD:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_ENV_FILE="${SCRIPT_DIR}/../.env"

load_env_file() {
    local env_file="$1"
    if [[ ! -f "$env_file" ]]; then
        return
    fi

    while IFS='=' read -r raw_key raw_value; do
        # Skip blank lines and comments
        [[ -z "${raw_key// }" ]] && continue
        [[ "${raw_key}" =~ ^[[:space:]]*# ]] && continue

        local key
        key="$(echo "$raw_key" | sed -E 's/^[[:space:]]+|[[:space:]]+$//g')"
        local value
        value="$(echo "${raw_value:-}" | sed -E 's/^[[:space:]]+|[[:space:]]+$//g')"

        # Strip optional surrounding quotes
        value="${value%\"}"
        value="${value#\"}"

        if [[ "$key" == "ROKU_HOST" && -z "$ROKU_HOST" ]]; then
            ROKU_HOST="$value"
        elif [[ "$key" == "ROKU_PASSWORD" && -z "$ROKU_PASSWORD" ]]; then
            ROKU_PASSWORD="$value"
        fi
    done < "$env_file"
}

usage() {
    cat <<EOF
Usage: ./deploy.sh [--host <ip>] [--password <password>]

Reads ROKU_HOST and ROKU_PASSWORD from ../.env by default.
Command-line flags override values from .env.
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --host)
            ROKU_HOST="${2:-}"
            shift 2
            ;;
        --password)
            ROKU_PASSWORD="${2:-}"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "ERROR: Unknown argument: $1"
            usage
            exit 1
            ;;
    esac
done

load_env_file "$ROOT_ENV_FILE"

if [[ -z "$ROKU_HOST" || -z "$ROKU_PASSWORD" ]]; then
    echo "ERROR: ROKU_HOST and ROKU_PASSWORD must be set in ../.env or passed as flags."
    echo "Copy .env.example to .env and fill in your Roku IP and developer password."
    exit 1
fi

if ! command -v curl >/dev/null 2>&1; then
    echo "ERROR: curl is required but not found in PATH."
    exit 1
fi

cd "$SCRIPT_DIR"

echo "Building with BrighterScript..."
if npx bsc --project bsconfig.json >/dev/null 2>&1; then
    # Run again to show user-friendly compiler output after capability check.
    npx bsc --project bsconfig.json
else
    npx -y brighterscript --project bsconfig.json
fi

ZIP_PATH="${SCRIPT_DIR}/out/roku.zip"
if [[ ! -f "$ZIP_PATH" ]]; then
    echo "ERROR: Build completed but package not found at $ZIP_PATH"
    exit 1
fi

echo "Built: $ZIP_PATH"
echo "Deploying to Roku at $ROKU_HOST ..."

response="$(curl --digest --silent --show-error \
    -u "rokudev:${ROKU_PASSWORD}" \
    -F "mysubmit=Install" \
    -F "archive=@${ZIP_PATH}" \
    "http://${ROKU_HOST}/plugin_install")"

if [[ "$response" == *"Install Success"* ]]; then
    echo "Deployed successfully!"
else
    echo "Deploy response:"
    echo "$response"
fi
