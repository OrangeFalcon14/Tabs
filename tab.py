import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk


class Tab:
    def __init__(self, number, name, switch_tab_func, close_tab_func, file_path="", saved=False, ):
        self.scrolled_window = Gtk.ScrolledWindow()
        self.editor = Gtk.TextView()
        self.editor.set_vexpand(True)
        self.editor.set_hexpand(True)
        self.editor.set_left_margin(5)
        self.editor.set_right_margin(5)
        self.editor.set_top_margin(5)
        self.editor.set_bottom_margin(5)

        self.buffer = self.editor.get_buffer()
        self.scrolled_window.add(self.editor)

        self.name = name
        self.number = number
        self.saved = saved
        self.file_path = file_path

        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.name_button = Gtk.Button(label=self.name)
        self.name_button.set_relief(Gtk.ReliefStyle.NONE)
        self.name_button.set_name("padding_right")
        self.name_button.connect("clicked", lambda dummy: switch_tab_func(self.number))
        self.hbox.add(self.name_button)

        close_button_label = Gtk.Label(label="<span size='15000'>&#215;</span>", use_markup=True)

        self.close_button = Gtk.Button()
        self.close_button.set_relief(Gtk.ReliefStyle.NONE)
        self.close_button.set_name("padding_left")
        self.close_button.add(close_button_label)
        self.close_button.connect("clicked", lambda dummy: close_tab_func(self.number))
        self.hbox.add(self.close_button)
