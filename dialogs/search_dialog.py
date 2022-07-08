import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gdk


class SearchDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Search", transient_for=parent, modal=True)
        self.add_buttons(
            Gtk.STOCK_FIND,
            Gtk.ResponseType.OK,
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
        )

        self.set_border_width(10)

        box = self.get_content_area()

        label = Gtk.Label(label="Enter the text you want to search for:")
        label.set_margin_bottom(5)
        box.add(label)

        self.entry = Gtk.Entry()
        self.entry.set_margin_bottom(5)
        box.add(self.entry)

        self.show_all()
