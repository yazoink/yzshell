#!/usr/bin/env bash

tmp_dir=/tmp/yay

if [ ! -n "${tmp_dir}" ]; then
    rm -rf "${tmp_dir}"
fi

git clone "https://aur.archlinux.org/yay.git" "${tmp_dir}"
(cd '{tmp_dir}' && makepkg -si)