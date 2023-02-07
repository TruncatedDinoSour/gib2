#!/usr/bin/env sh

set -eu

main() {
    for d in gib/ gib_bot/; do
        cd "$d"
        rm -f ./*.pyi
        stubgen "$d"/ -o .
        mv "$d"/*.pyi .
        cd ..
    done
}

main "$@"
