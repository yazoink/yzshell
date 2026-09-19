#!/usr/bin/env python
# script deps: figlet, gum, git, python

import subprocess
import argparse
from sys import argv, exit
from os import path, getcwd, remove, unlink, geteuid, environ, listdir
from shutil import rmtree, copytree, copyfile
import json


COL_1 = "212" # primary gum text colour
COL_2 = "99" # secondary gum text colour
OMZ_DIR = path.expanduser("~/.oh-my-zsh")
# executables to be installed
EXES = [
    "yzconf",
    "yzshell",
    "yzwallpaper",
    "yzwidgets",
    "yzpicker",
    "yzrecorder",
    "yzshot",
    "yzctl",
    "iconfetch",
    "zenconf",
    "yzshell-install-hyprland-plugins",
    "base16-to-yzshell-scheme",
    "base16-to-yzshell-template"
]
# required directories in yzshell repo
DIRS = [
    "assets",
    "colourschemes",
    "dotfiles",
    "templates",
    "misc",
    "scripts",
    "lib"
]


def title_text(s):
    subprocess.run(
        f"""
        gum style \
            --foreground={COL_2} \
            --padding='2 4' \
            "$(figlet "{s}")"
        """,
        shell=True
    )


def announce(s):
    cmd = f'gum style --foreground {COL_1} "{s}"'
    subprocess.run(cmd, shell=True)


def choose(x, opts):
    cmd = f"gum choose --padding='1 1' --header 'select {x}...'"
    for o in opts:
        cmd += f" '{o}'"
    return subprocess.run(
        cmd, shell=True, text=True, stdout=subprocess.PIPE
    ).stdout.strip()


def backup_file(p):
    if path.isfile(p):
        dest = f"{p}-backup"
        delete_if_exists(dest)
        copyfile(p, dest)
        remove(p)
        announce(f"backed up conflicting file: {p} => {dest}")


def backup_dir(p):
    if path.exists(p):
        dest = f"{p}-backup"
        delete_if_exists(dest)
        copytree(p, dest)
        rmtree(p)
        announce(f"backed up conflicting directory: {p} => {dest}")


def copy_files(install_dir):
    target_dir = environ["YZSHELL_DATA_DIR"]
    delete_if_exists(target_dir)
    for d in DIRS:
        c = path.join(install_dir, d)
        v = path.join(target_dir, d)
        copytree(c, v)
        announce(f"copied directory: {c} => {v}")
    for e in EXES:
        c = path.join(install_dir, "bin", e)
        v = path.join("/usr/bin", e)
        subprocess.run(
            f"sudo install -Dm755 '{c}' '{v}'",
            shell=True
        )
        announce(f"installed binary: {c} => {v}")


def set_env_vars(env_vars):
    env_file = "/etc/environment"
    tmp_file = "/tmp/yzshell_env"
    lines = []

    if path.isfile(env_file) == False:
        subprocess.run(["sudo", "touch", env_file])

    for v in env_vars:
        environ[v] = env_vars[v]
        subprocess.run(
            f"""
            if grep "{v}" "{env_file}"; then
                sudo gawk -i inplace "!/{v}/" "{env_file}"
            fi
            echo "{v}={env_vars[v]}" \
                | sudo tee -a "{env_file}"
            """,
            shell=True,
            capture_output=True
        )


def configure_yzshell_env_vars():
    data_dir = path.expanduser("~/.local/share/yzshell")
    script_dir = path.join(data_dir, "scripts")
    lib_dir = path.join(data_dir, "lib")
    conf_dir = path.expanduser("~/.config/yzshell")
    cache_dir = path.expanduser("~/.cache/yzshell")
    env_vars = {
        "YZSHELL_DATA_DIR": data_dir,
        "YZSHELL_LIB_DIR": lib_dir,
        "YZSHELL_PYTHON_LIB_DIR": path.join(lib_dir, "python"),
        "YZSHELL_BASH_LIB_DIR": path.join(lib_dir, "bash"),
        "YZSHELL_STOW_DIR": path.expanduser("~/.dotfiles"),
        "YZSHELL_CONF_DIR": conf_dir,
        "YZSHELL_CONF_FILE": path.join(conf_dir, "config.json"),
        "YZSHELL_DEFAULT_CONF_FILE": path.join(data_dir, "misc/default-config.json"),
        "YZSHELL_EWW_DIR": path.expanduser("~/.config/eww"),
        "YZSHELL_SCRIPT_DIR": script_dir,
        "YZSHELL_EWW_SCRIPT_DIR": path.join(script_dir, "eww"),
        "YZSHELL_COLOURS_DIR": path.join(data_dir, "colourschemes"),
        "YZSHELL_TEMPLATES_DIR": path.join(data_dir, "templates"),
        "YZSHELL_CACHE_DIR": cache_dir,
        "YZSHELL_TEMPLATE_CACHE_DIR": path.join(cache_dir, "built_templates"),
        "YZSHELL_WALLPAPER_CACHE_DIR": path.join(cache_dir, "wallpapers"),
        "YZSHELL_WALLPAPER_LOCKFILE": path.join(cache_dir, "wallpapers.lock"),
    }
    set_env_vars(env_vars)
    announce("yzshell environment variables configured!")


def confirm(question):
    a = subprocess.run(
        f'gum confirm --padding="1 1" "{question}"', 
        shell=True
    )
    if a.returncode == 0:
        return True
    return False


def delete_if_exists(p):
    if path.isdir(p) == True:
        rmtree(p)
    elif path.isfile(p) == True:
        remove(p)
    elif path.islink(p) == True:
        unlink(p)


def enable_chaotic_aur():
    if confirm("enable chaotic-aur repo? (recommended)") == True:
        subprocess.run(
            """
            sudo pacman-key --init
            sudo pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com
            sudo pacman-key --lsign-key 3056513887B78AEB
            sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst'
            sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'
            echo "
[chaotic-aur]
Include = /etc/pacman.d/chaotic-mirrorlist
            " | sudo tee -a /etc/pacman.conf
            """,
            shell=True
        )
        update_pacman()
        announce("chaotic-aur repo enabled!")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-sd", "--skip-dependencies", 
        action="store_true", 
        default=False,
        help="skip dependency installation"
    )
    parser.add_argument(
        "-o", "--optional-dependencies", 
        action="store_true", 
        default=False,
        help="install optional dependencies"
    )
    parser.add_argument(
        "-d", "--directory", 
        default=None,
        help="specify directory of repo to install from"
    )
    return parser.parse_args(argv[1:])


def get_bin(b):
    r = subprocess.run(
        ["which", b],
        capture_output=True,
        text=True
    )
    if r.returncode == 0:
        return r.stdout
    else:
        return None


def get_full_path(p):
    if "~" in p:
        return path.expanduser(p)
    else:
        return path.abspath(p)


def get_install_dir(arg_directory):
    def validate_install_dir(install_dir):
        # ensure required dirs
        for d in DIRS:
            p = path.join(install_dir, d)
            if path.exists(p) == False:
                #print_err(
                #    "required directory not found: " + p, 
                #    level="warn", 
                #    exit_script=False
                #)
                return False
        # ensure executables
        for e in EXES:
            p = path.join(install_dir, "bin", e)
            if path.isfile(p) == False:
                #print_err(
                #    "require file not found: " + p, 
                #    level="warn", 
                #    exit_script=False
                #)
                return False
        return True

    cwd = getcwd()
    dir_valid = False

    if arg_directory != None: # dir specified
        install_dir = get_full_path(arg_directory)
        dir_valid = validate_install_dir(install_dir)
    else: # dir not specified
        install_dir = cwd
        dir_valid = validate_install_dir(install_dir)
        if dir_valid == False:
            install_dir = path.join(install_dir, "yzshell")
            if dir_valid == False:
                install_dir = "/tmp/yzshell"

    if dir_valid == True: # dir valid
        announce("installing from repo: " + install_dir)
    else: # dir invalid
        if path.exists(install_dir): # dir exists and is invalid
            print_err("path is not a valid yzshell repo: " + install_dir)
        # clone repo
        if confirm(f"clone yzshell repo to '{install_dir}'?"):
            announce("cloning yzshell repo to: " + install_dir)
            git_clone("https://github.com/yazoink/yzshell", install_dir)
        else:
            print_err("no yzshell repo found!")
    return install_dir


def git_clone(repo, dest):
    try:
        subprocess.run(["git", "clone", repo, dest])
        announce("repo successfully cloned: " + repo)
    except:
        print_err("failed to clone repo: " + repo)


def grep_file(s, f):
    r = subprocess.run(f"grep -q '{s}' '{f}'", shell=True)
    if r.returncode == 0:
        return True
    else:
        return False


def get_input(question):
    return subprocess.run(
        f"gum input --placeholder '{question}'", 
        shell=True, 
        text=True, 
        stdout=subprocess.PIPE
    ).stdout.strip()


def remove_pkgs(pkgs, aur=False):
    cmd = [
        "pacman", 
        "-Rns",
        "--noconfirm"
    ]
    if aur == True:
        cmd[0] = "yay"
    else:
        cmd.insert(0, "sudo")
    l = len(cmd)
    for p in pkgs:
        if pkg_installed(p, aur):
            cmd.append(p)
    if len(cmd) > l:
        subprocess.run(cmd)


def install_pkgs(pkgs, aur=False):
    cmd = [
        "pacman", 
        "-S",
        "--needed",
        "--noconfirm"
    ]
    if aur == True:
        cmd[0] = "yay"
        cmd.extend(["--norebuild", "--noredownload"])
    else:
        cmd.insert(0, "sudo")
    l = len(cmd)
    for p in pkgs:
        if pkg_installed(p, aur) == False:
            cmd.append(p)
    if len(cmd) > l:
        subprocess.run(cmd)


def install_yay():
    print("installing yay...")
    tmp_dir = "/tmp/yay"
    install_pkgs(["base-devel"])
    delete_if_exists(tmp_dir)
    git_clone("https://aur.archlinux.org/yay.git", tmp_dir)
    r = subprocess.run(
        f"cd '{tmp_dir}' && makepkg -si",
        shell=True
    )
    rmtree(tmp_dir)
    if r.returncode != 0:
        print_err("could not install yay")
    announce("yay installed!")


def install_zsh():
    if confirm("install and configure zsh with yzshell?"):
        omz_plugins = {
            "zsh-autosuggestions": "https://github.com/zsh-users/zsh-autosuggestions",
            "zsh-syntax-highlighting": "https://github.com/zsh-users/zsh-syntax-highlighting.git"
        }
        install_pkgs(["zsh", "zsh-completions"])
        backup_dir(OMZ_DIR)
        subprocess.run(
            """
            sh -c \
                "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)" \
                "" --unattended
            """,
            shell=True
        )
        for p in omz_plugins:
            announce("installing zsh plugin: "+ p)
            git_clone(omz_plugins[p], path.join(OMZ_DIR, "plugins", p))
        announce("zsh installed!")

        if confirm("set zsh as default shell?"):
            subprocess.run("chsh -s $(which zsh)", shell=True)
            announce("default shell set to zsh!")
        update_config("configure_zsh", "true")
    else:
        update_config("configure_zsh", "false")
    


def parse_json_file(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        print_err("could not parse file: " + path)


def pkg_installed(pkg, aur=False):
    mgr_cmd = "pacman"
    if aur == True:
        mgr_cmd = "yay"
    r = subprocess.run(
        [mgr_cmd, "-Qi", pkg],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    if r.returncode == 0:
        return True
    else:
        return False


def print_err(msg, level="fatal", exit_script=True, exit_code=1):
    subprocess.run(f"gum log --structured --level='{level}' '{msg}'", shell=True)
    if exit_script == True:
        exit(exit_code)


def update_pacman():
    try:
        subprocess.run(["sudo", "pacman", "-Syu"])
    except:
        print_err("failed to update pacman, please check your internet connection!")


def update_config(opt, val):
    subprocess.run(["yzconf", "set", opt, val])


def configure_default_apps():
    apps = parse_json_file(path.join(install_dir, "misc/apps.json"))
    for category in apps:
        title = apps[category]["title"]
        cmd = None
        a = apps[category]["apps"]
        a["other"] = {}
        c = choose(title, a)
        if c == "other":
            while True:
                cmd = get_input(f"enter {title} command...")
                if confirm(f"set {title} to '{cmd}'?"):
                    break
        else:
            cmd = c
            if "deps" in apps[category]["apps"][c]:
                install_pkgs(apps[category]["apps"][c]["deps"])
            if "aur_deps" in apps[category]["apps"][c]:
                install_pkgs(apps[category]["apps"][c]["aur_deps"], aur=True)
        update_config(category, cmd)
        announce(f"set {title} to '{cmd}'!")


def configure_gpu_drivers():
    c = choose("graphics drivers", ["amd", "intel", "none"])
    match c:
        case "amd":
            if confirm("this script does not support < Rx 2000, continue?"):
                env_vars = {
                    "LIBVA_DRIVER_NAME": "radeonsi",
                    "VDPAU_DRIVER": "va_gl"
                }
                install_pkgs([
                    "mesa", 
                    "libva-mesa-driver", 
                    "vulkan-radeon",
                    "libvdpau-va-gl"
                ])
                set_env_vars(env_vars)
        case "intel":
            d = choose("intel drivers", ["standard", "legacy (gen 2-7)", "none"])
            match d:
                case "standard":
                    env_vars = {
                        "LIBVA_DRIVER_NAME": "iHD",
                        "VDPAU_DRIVER": "va_gl"
                    }
                    install_pkgs([
                        "mesa",
                        "vulkan-intel",
                        "intel-media-driver",
                        "vpl-gpu-rt"
                    ])
                    set_env_vars(env_vars)
                case "legacy (gen 2-7)":
                    env_vars = {
                        "LIBVA_DRIVER_NAME": "i965",
                        "VDPAU_DRIVER": "va_gl"
                    }
                    remove_pkgs(["mesa"])
                    install_pkgs([
                        "mesa-amber",
                        "libva-intel-driver",
                        "intel-media-sdk"
                    ])
                    set_env_vars(env_vars)


def install_vscode():
    if confirm("install and configure vscodium with yzshell?"):
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
        announce("installing vscodium...")
        install_pkgs(["code"])
        announce("installing vscodium extensions...")
        for e in extensions:
            subprocess.run(["code", "--install-extension", e])
        update_config("configure_vscodium", "true")
        announce("installed vscodium!")
    else:
        update_config("configure_vscodium", "false")


def backup_dotfiles():
    backup_file(path.expanduser("~/.zshrc"))
    backup_file(path.expanduser("~/.zprofile"))
    omz_custom = path.join(OMZ_DIR, "custom")
    if path.exists(omz_custom):
        files = listdir(omz_custom)
        for f in files:
            if f.endswith("-backup") == False:
                backup_file(path.join(omz_custom, f))

    templates = parse_json_file(
        path.join(
            environ["YZSHELL_DATA_DIR"], 
            "templates/templates.json"
        )
    )
    for t in templates:
        backup_file(path.join(path.expanduser("~"), str(templates[t])))

if __name__ == "__main__":
    if geteuid() == 0:
        print_err("please do not run as root!")

    args = get_args()
    install_dir = get_install_dir(args.directory)

    configure_yzshell_env_vars()
    copy_files(install_dir)

    # install deps
    if args.skip_dependencies == False:
        update_pacman()

        # aur helper
        if get_bin("yay") == None:
            install_yay()

        # chaotic-aur
        if grep_file("chaotic-aur", "/etc/pacman.conf") == False:
            enable_chaotic_aur()

        # deps
        deps = parse_json_file(path.join(install_dir, "misc/deps.json"))
        announce("installing dependencies...")
        install_pkgs(deps["pacman"])
        install_pkgs(deps["yay"], aur=True)
        announce("installed dependencies!")

        configure_default_apps()
        configure_gpu_drivers()

        # zsh
        if environ["SHELL"].endswith("/zsh") == False:
            install_zsh()

        # vesktop
        if confirm("install and configure vesktop with yzshell?"):
            announce("installing vesktop...")
            install_pkgs(["vesktop-bin"], aur=True)
            update_config("configure_vesktop", "true")
            announce("installed vesktop!")
        else:
            update_config("configure_vesktop", "false")

        # nvim
        if confirm("install and configure nvim with yzshell?"):
            announce("installing nvim...")
            install_pkgs([
                "neovim",
                "python-isort",
                "python-black",
                "prettier",
                "shfmt",
                "yamllint",
                "yamlfmt",
                "uncrustify",
                "typstyle",
                "stylua",
            ])
            install_pkgs([
                #"alejandra",
                "beautysh",
                "mago-bin",
            ], aur=True)
            update_config("configure_nvim", "true")
            announce("installed nvim!")
        else:
            update_config("configure_nvim", "false")

        # vscode
        install_vscode()

        # misc
        subprocess.run(
            """
            sudo ln -sf /usr/share/fontconfig/conf.avail/10-nerd-font-symbols.conf \
                /etc/fonts/conf.d/
            sudo journalctl --vacuum-time=2weeks
            sudo systemctl enable --now fstrim.timer
            sudo systemctl enable --now systemd-oomd
            sudo systemctl enable --now swayosd-libinput-backend.service
            sudo systemctl enable --now bluetooth.service
            systemctl --user --now enable mpd
            """,
            shell=True
        )

    if args.optional_dependencies == True:
        deps = parse_json_file(path.join(install_dir, "misc/optional-deps.json"))
        announce("installing optional dependencies...")
        install_pkgs(deps["pacman"])
        install_pkgs(deps["yay"], aur=True)
        announce("installed optional dependencies!")

    backup_dotfiles()
    subprocess.Popen(
        """
        yzconf deploy_configs -r
        pgrep --quiet Hyprland && yzshell reload
        """,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT
    )

    title_text("yzshell")
    print("""a reboot is required after the initial installation!

to configure zen Browser: once there is at least one profile in '~/.config/zen', run 'zenconf --select-profile' to ensure its configuration.

make sure pipewire is installed and networkmanager is in use!

hyprland is configured to start on tty login from '~/.zprofile'; if you are not using zsh, it will need to be launched manually with 'exec dbus-run-session start-hyprland', or from a display manager."
    """)