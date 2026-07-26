from os import environ, path, makedirs
import json

class Colourscheme:
    def __init__(self, scheme_name):
        self.scheme = {}
        self.scheme_name = scheme_name

        try:
            with open(f"{environ["COLOURS_DIR"]}/{scheme_name}.json", "r") as f:
                j = f.read()
                self.scheme = json.loads(j)
        except:
            print(f"Error: colourscheme '{scheme_name}' not recognised")
            exit(1)
        
        self.scheme["surface1"] = self._overlay_colour(self.scheme["base00"], self.scheme["base05"], 0.1)
        self.scheme["surface2"] = self._overlay_colour(self.scheme["base00"], self.scheme["base05"], 0.2)
        self.scheme["surface3"] = self._overlay_colour(self.scheme["base00"], self.scheme["base05"], 0.3)
        self.scheme["surface4"] = self._overlay_colour(self.scheme["base00"], self.scheme["base05"], 0.4)

    def _hex_to_rgb(self, hex_colour):
        return tuple(int(hex_colour[i : i + 2], 16) for i in (0, 2, 4))

    def _rgb_to_hex(self, rgb):
        return "{:02X}{:02X}{:02X}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
        
    def _overlay_colour(self, base, overlay, amount):
        base = self._hex_to_rgb(base)
        overlay = self._hex_to_rgb(overlay)
        r = base[0] + (overlay[0] - base[0]) * amount
        g = base[1] + (overlay[1] - base[1]) * amount
        b = base[2] + (overlay[2] - base[2]) * amount
        return self._rgb_to_hex((r, g, b))

class MustacheTemplate:
    def __init__ (self, src, out):
        self.src = f"{environ["TEMPLATES_DIR"]}/{src}"
        self.out = out

    def apply(self, scheme): # MustacheTemplate(<template>, <output>).apply(Colourscheme("<scheme name>"))
        s = path.split(self.out)
        try:
            makedirs(s[0])
        except:
            pass
        cfg = ""
        with open(self.src, "r") as f:
            cfg = f.read()
        for s in scheme.scheme:
            cfg = cfg.replace(f"{{{{{s}}}}}", str(scheme.scheme[s]))
        with open(self.out, "w") as f:
            f.write(cfg)
        print(f"Applied colourscheme '{scheme.scheme_name}' to '{self.out}'")