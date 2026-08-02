class WindowManager():
    def __init__(self, name, launch_cmd, reload_cmd, deps, config):
        self.name = name
        self.launch_cmd = launch_cmd
        self.reload_cmd = reload_cmd
        self.deps = deps
        self._config = config

    def reload(self):
        import subprocess
        subprocess.Popen(
            self.reload_cmd, 
            shell=True,
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )

    def uninstall(self):
        self.deps.uninstall()

    def install(self):
        from os import environ
        self.deps.install()
        self._config.change("window_manager", self.name)

        src = f"{environ["TEMPLATES_DIR"]}/zprofile.mustache"
        dest = f"{environ["HOME"]}/.zprofile"
        with open(src, "r") as f:
            cfg = f.read()
        cfg = cfg.replace("{{window_manager}}", self.launch_cmd)
        with open(dest, "w") as f:
            f.write(cfg)