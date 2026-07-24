from os import environ
from sys import argv
from lib.utils.config import Config
from lib.utils.colourscheme import Colourscheme, MustacheTemplate


def main():
    argc = len(argv)
    c = Config()
    s = c.current["colourscheme"]

    if argc > 1:
        s = argv[1]

    cs = Colourscheme(s)

    templates = [
        MustacheTemplate("eww.scss.mustache", f"{environ["CONFIG_DIR"]}/eww/scss/_colours.scss"),
        MustacheTemplate("foot.ini.mustache", f"{environ["CONFIG_DIR"]}/foot/foot.ini"),
        MustacheTemplate("gtk.css.mustache", f"{environ["CONFIG_DIR"]}/gtk-3.0/gtk.css"),
        MustacheTemplate("gtk.css.mustache", f"{environ["CONFIG_DIR"]}/gtk-4.0/gtk.css"),
        MustacheTemplate("kvantum.kvconfig.mustache", f"{environ["CONFIG_DIR"]}/Kvantum/KvRecolour/KvRecolour.kvconfig"),
        MustacheTemplate("kvantum.svg.mustache", f"{environ["CONFIG_DIR"]}/Kvantum/KvRecolour/KvRecolour.svg"),
        MustacheTemplate("labwc_themerc.mustache", f"{environ["CONFIG_DIR"]}/labwc/themerc-override"),
        MustacheTemplate("mako.mustache", f"{environ["CONFIG_DIR"]}/mako/config"),
        MustacheTemplate("waybar.css.mustache", f"{environ["CONFIG_DIR"]}/waybar/colours.css"),
        MustacheTemplate("wofi.css.mustache", f"{environ["CONFIG_DIR"]}/wofi/style.css"),
        MustacheTemplate("yazi.toml.mustache", f"{environ["CONFIG_DIR"]}/yazi/theme.toml"),
        MustacheTemplate("swayosd.css.mustache", f"{environ["CONFIG_DIR"]}/swayosd/style.css"),
        MustacheTemplate("zen_userchrome.css.mustache", f"{environ["CONFIG_DIR"]}/zen/userChrome.css"),
        MustacheTemplate("zen_usercontent.css.mustache", f"{environ["CONFIG_DIR"]}/zen/userContent.css"),
    ]

    for t in templates:
        t.apply(cs)

    c.change("colourscheme", s)


main()