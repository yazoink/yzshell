#!/usr/bin/env python

from sys import argv
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

if __name__ == "__main__":
    title = "Choose a file..."
    if len(argv) > 1:
        title = argv[1]

    filechooserdialog = Gtk.FileChooserDialog(
        title=title,
        parent=None,
        action=Gtk.FileChooserAction.OPEN
    )
    filechooserdialog.add_buttons("_Open", Gtk.ResponseType.OK)
    filechooserdialog.add_buttons("_Cancel", Gtk.ResponseType.CANCEL)
    filechooserdialog.set_default_response(Gtk.ResponseType.OK)

    response = filechooserdialog.run()

    if response == Gtk.ResponseType.OK:
        print(filechooserdialog.get_filename())

    filechooserdialog.destroy()
