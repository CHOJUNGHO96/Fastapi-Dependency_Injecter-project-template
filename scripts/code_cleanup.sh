#!/usr/bin/env bash
set -eo pipefail

# shellcheck disable=SC2006
COLOR_GREEN=`tput setaf 2;`
# shellcheck disable=SC2006
COLOR_NC=`tput sgr0;` # No Color

echo "Starting black"
poetry run black ..
echo "OK"

echo "Starting isort"
poetry run isort ..
echo "OK"


echo "Sort pyproject.toml"
poetry run toml-sort ../pyproject.toml --all --in-place
echo "OK"


echo "${COLOR_GREEN}All tests passed successfully!${COLOR_NC}"
