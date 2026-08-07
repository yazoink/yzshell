#!/usr/bin/env bash

v="$(grep -E '^VERSION=' /etc/os-release | sed 's/VERSION=//;s/\"//g')"
n="$(grep -E '^PRETTY_NAME=' /etc/os-release | sed 's/PRETTY_NAME=//;s/\"//g')"

echo "${n} ${v}"
