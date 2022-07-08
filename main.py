import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

import window as w

TITLE = "Tabs"
WIDTH = 800
HEIGHT = 500

window = w.Window(TITLE, WIDTH, HEIGHT)
window.connect("destroy", w.Window.quit)

Gtk.main()
