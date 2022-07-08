import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gdk


class Preferences(Gtk.Dialog):
    def __init__(self, parent, font):
        super().__init__(title="Preferences", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        self.set_border_width(10)
        self.set_default_size(500, 200)

        self.box = self.get_content_area()

        self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.hbox1.set_margin_bottom(10)
        self.box.add(self.hbox1)

        self.font_btn = Gtk.FontButton()
        if font is not None:
            self.font_btn.set_font_name(font)
        self.hbox1.pack_start(Gtk.Label(label="<span size='11000'>Font</span>", use_markup=True), False, False, 0)
        self.hbox1.pack_end(self.font_btn, False, False, 0)

        self.hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.hbox2.set_margin_bottom(10)
        self.box.add(self.hbox2)

        wrap_modes = [
            "None",
            "Character",
            "Word"
        ]
        self.wrap_mode_combobox = Gtk.ComboBoxText()
        # self.wrap_mode_combobox.set_entry_text_column(0)
        for x in wrap_modes:
            self.wrap_mode_combobox.append_text(x)
        self.hbox2.pack_start(Gtk.Label(label="<span size='11000'>Wrap</span>", use_markup=True), False, False, 0)
        self.hbox2.pack_end(self.wrap_mode_combobox, False, False, 0)

        self.hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.hbox3.set_margin_bottom(10)
        self.box.add(self.hbox3)

        self.editable = Gtk.Switch()
        self.editable.set_active(False)

        self.hbox3.pack_start(Gtk.Label(label="<span size='11000'>Read-Only</span>", use_markup=True), False, False, 0)
        self.hbox3.pack_end(self.editable, False, False, 0)

        self.hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.hbox4.set_margin_bottom(10)
        self.box.add(self.hbox4)

        self.syntax_highlighting = Gtk.Switch()
        self.syntax_highlighting.set_active(False)

        self.hbox4.pack_start(Gtk.Label(label="<span size='11000'>Syntax Highlighting</span>", use_markup=True), False,
                              False, 0)
        self.hbox4.pack_end(self.syntax_highlighting, False, False, 0)

        self.hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.hbox5.set_margin_bottom(10)
        self.box.add(self.hbox5)

        langs = [
            "af: Afrikaans",
            "ar: Arabic",
            "bg: Bulgarian",
            "bn: Bengali",
            "bs: Bosnian",
            "ca: Catalan",
            "cs: Czech",
            "cy: Welsh",
            "da: Danish",
            "de: German",
            "el: Greek",
            "en: English",
            "eo: Esperanto",
            "es: Spanish",
            "et: Estonian",
            "fi: Finnish",
            "fr: French",
            "gu: Gujarati",
            "hi: Hindi",
            "hr: Croatian",
            "hu: Hungarian",
            "hy: Armenian",
            "id: Indonesian",
            "is: Icelandic",
            "it: Italian",
            "iw: Hebrew",
            "ja: Japanese",
            "jw: Javanese",
            "km: Khmer",
            "kn: Kannada",
            "ko: Korean",
            "la: Latin",
            "lv: Latvian",
            "mk: Macedonian",
            "ml: Malayalam"
            "mr: Marathi",
            "ms: Malay",
            "my: Myanmar (Burmese)",
            "ne: Nepali",
            "nl: Dutch",
            "no: Norwegian",
            "pl: Polish",
            "pt: Portuguese",
            "ro: Romanian",
            "ru: Russian",
            "si: Sinhala",
            "sk: Slovak",
            "sq: Albanian",
            "sr: Serbian",
            "su: Sundanese",
            "sv: Swedish",
            "sw: Swahili",
            "ta: Tamil",
            "te: Telugu",
            "th: Thai",
            "tl: Filipino",
            "tr: Turkish",
            "uk: Ukrainian",
            "ur: Urdu",
            "vi: Vietnamese",
            "zh-CN: Chinese",
            "zh-TW: Chinese (Mandarin/Taiwan)",
            "zh: Chinese (Mandarin)"
        ]
        self.langs_combobox = Gtk.ComboBoxText()
        # self.langs_combobox.set_wrap_width(-1)
        # self.wrap_mode_combobox.set_entry_text_column(0)
        for x in langs:
            self.langs_combobox.append_text(x)

        self.hbox5.pack_start(Gtk.Label(label="<span size='11000'>Read Aloud Language</span>", use_markup=True), False,
                              False, 0)
        self.hbox5.pack_end(self.langs_combobox, False, False, 0)

        self.show_all()