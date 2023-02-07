#!/usr/bin/env sh

set -eu

main() {
    . scripts/stub.sh

    git add -A
    git commit -sa
    git push -u origin main
}

main "$@"

