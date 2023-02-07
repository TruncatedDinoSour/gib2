#!/usr/bin/env bash

set -eu

main() {
    ./scripts/stub.sh

    for d in gib gib_bot; do
        pushd "$d"
        pip install -e .
        popd
    done
}

main "$@"
