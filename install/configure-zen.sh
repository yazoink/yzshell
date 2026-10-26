function configure_zen() {
    zen_dir="${HOME}/.config/zen"
    zen_profile="$(yzconf get zen_profile)"
    # yzconf set web_browser "zen-browser -P ${zen_profile}"
    zen_profile_dir="${zen_dir}/${zen_profile}"

    if [ -d "${zen_profile_dir}" ]; then
        announce "Zen profile already exists, skipping creation..."
        return 0
    fi

    # [ -z "${zen_dir}" ] && mkdir -p "${zen_dir}"
    # chmod og-rwx -R "${zen_dir}"

    zen-browser -CreateProfile "${zen_profile} ${zen_profile_dir}" \
        --headless \
        --screenshot /dev/null
    # cp "${REPO_DIR}/misc/zen/profiles.ini" "${zen_dir}/profiles.ini"
    announce "Created Zen profile: ${zen_profile_dir}"
    python "${REPO_DIR}/install/install-zen-extensions.py" "${zen_profile_dir}"
}

configure_zen
announce "Configured Zen browser!"
