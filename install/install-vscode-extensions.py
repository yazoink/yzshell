#!/usr/bin/env python

import subprocess

extensions = [
    "pkief.material-icon-theme",
    "pkief.material-product-icons",
    "meta.pyrefly",
    "ms-python.python",
    "pinage404.bash-extension-pack",
    "eww-yuck.yuck",
    "devsense.phptools-vscode",
    "redhat.vscode-yaml",
    "redhat.vscode-xml",
    "ecmel.vscode-html-css",
    "yzhang.markdown-all-in-one",
    "tamasfe.even-better-toml",
    "sumneko.lua"
]
for e in extensions:
    subprocess.run(["code", "--install-extension", e])