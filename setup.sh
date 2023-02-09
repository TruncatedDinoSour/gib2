#!/usr/bin/env bash

set -eu

main() {
    ./scripts/stub.sh

    for d in gib gib_bot; do
        pushd "$d"
        python3 -m pip install -e .
        python3 -m pip install -r requirements.txt
        popd
    done
}

main "$@"
