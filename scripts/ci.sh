#!/bin/sh
### ci convenience shell script.
### Usage: ./ci.sh [command]
### If no command is provided, the script will run the following commands:
### ruff format --check
### ruff check
### pytest
### pyright
### Otherwise, the script will run `uv run --all-packages $command`.

UV="uv run --all-packages"

if [ -n "$1" ]; then
  $UV $@
  exit $?
fi

set -ex
$UV ruff format --check
$UV ruff check
$UV pytest
$UV pyright
