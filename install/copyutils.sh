function copy_data_dir() {
    local -; set -e
    src="${SRC_DIR}/${1}"
    target="${TARGET_DIR}/${1}"
    cp -rf "$src" "$target"
    echo ">> Copied '${src}' to '${target}'"
}

function copy_executable() {
    local -; set -e
    src="${SRC_DIR}/bin/${1}"
    target="/usr/bin/${1}"
    sudo install -Dm755 "$src" "$target"
    echo ">> Installed '${src}' to '${target}'"
}