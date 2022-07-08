import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gdk, Gio, Pango

from pathlib import Path
import os
import threading
from playsound import playsound
from gtts import gTTS

from dialogs import *
from tab import *

KEYWORDS = ["False", "class", "from", "or", "None", "continue", "global", "pass", "True", "def", "if", "raise", "and",
            "del", "import", "return", "as", "elif", "in", "try", "assert", "else", "is", "while", "async", "except",
            "lambda", "with", "await", "finally", "nonlocal", "yield", "break", "for", "not", "self", "-", "+", "*",
            "/", "**", "//", "%", ">", "<", "=", "==", "!", "(", ")", "[", "]", "{", "}"]

OPEN_FILES = []


class Window(Gtk.Window):
    def __init__(self, title, width, height):
        Gtk.Window.__init__(self, title=title)
        self.set_default_size(width, height)
        # icon_path = os.path.join(Path(__file__).parent, "tabs.png")
        # self.set_icon_from_file(icon_path)
        window_icon = self.render_icon("tabs.png", Gtk.IconSize.MENU)
        self.set_icon(window_icon)
        self.connect("key-press-event", self.key_press_event)

        self.set_up_header_bar()

        self.editors = []
        self.tab_num = 0
        self.current_tab = 0
        self.font = None
        self.wrap_mode = None
        self.first = True
        self.first_search = True
        self.highlight_syntax_bool = False
        self.read_aloud_language = "en: English"

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.vbox)

        self.scrolledwindow_tab_bar = Gtk.ScrolledWindow()
        self.tab_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.scrolledwindow_tab_bar.add(self.tab_bar)
        self.vbox.add(self.scrolledwindow_tab_bar)

        self.new_tab_btn = Gtk.Button()
        new_tab_btn_label = Gtk.Label(label="<span size='15000'>+</span>", use_markup=True)
        self.new_tab_btn.add(new_tab_btn_label)
        self.new_tab_btn.set_relief(Gtk.ReliefStyle.NONE)
        self.new_tab_btn.connect("clicked", self.new_tab)
        self.tab_bar.add(self.new_tab_btn)

        self.new_tab("")

        self.editors[0].editor.grab_focus()

        self.show_all()

    def key_press_event(self, widget, event):
        pass
        # keyval = event.keyval
        # keyval_name = Gdk.keyval_name(keyval)
        # state = event.state
        # ctrl = state and Gdk.ModifierType.CONTROL_MASK
        # alt = state and Gdk.ModifierType.META_MASK
        # editor_focus = False
        # for editor in self.editors:
        #     if editor.editor.has_focus():
        #         editor_focus = True
        #
        # if editor_focus:
        #     self.grab_focus()
        #     if ctrl and keyval_name == "n":
        #         self.new_tab("")
        #     if ctrl and keyval_name == "Tab":
        #         if self.current_tab == len(self.editors):
        #             self.switch_tab(0)
        #         else:
        #             print(self.current_tab, len(self.editors))
        #             self.switch_tab(self.current_tab+1)
        #     if ctrl and keyval_name == "s":
        #         self.save("")
        #     if ctrl and keyval_name == "o":
        #         print(state and Gdk.ModifierType.CONTROL_MASK)
        #         self.open("")
        #     if ctrl and keyval_name == "w":
        #         self.close_tab(self.current_tab)
        #     if alt and keyval_name == "s":
        #         self.open_preferences("")
        #     for editor in self.editors:
        #         print(editor.editor.has_focus())

    def set_up_header_bar(self):
        self.headerbar = Gtk.HeaderBar()
        self.headerbar.set_show_close_button(True)
        self.headerbar.props.title = "Tabs"
        self.set_titlebar(self.headerbar)

        self.save_btn = Gtk.Button(label="Save")
        self.save_btn.connect("clicked", self.save)
        self.headerbar.add(self.save_btn)

        self.open_btn = Gtk.Button(label="Open")
        self.open_btn.connect("clicked", self.open)
        self.headerbar.add(self.open_btn)

        self.popover = Gtk.Popover()
        self.popover.set_border_width(10)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        save_as_btn = Gtk.Button(label="Save As")
        save_as_btn.set_relief(Gtk.ReliefStyle.NONE)
        save_as_btn.connect("clicked", self.save_as)
        vbox.add(save_as_btn)

        # vbox.add(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

        save_all_btn = Gtk.Button(label="Save All")
        save_all_btn.set_relief(Gtk.ReliefStyle.NONE)
        save_all_btn.connect("clicked", self.save_all)
        vbox.add(save_all_btn)

        # vbox.add(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

        preferences_btn = Gtk.Button()
        preferences_btn_label = Gtk.Label(label="Preferences")
        preferences_btn.set_halign = 1
        preferences_btn.add(preferences_btn_label)
        preferences_btn.set_relief(Gtk.ReliefStyle.NONE)
        preferences_btn.connect("clicked", self.open_preferences)
        vbox.add(preferences_btn)

        # vbox.add(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

        find_btn = Gtk.Button(label="Find")
        find_btn.set_relief(Gtk.ReliefStyle.NONE)
        find_btn.connect("clicked", self.search)
        vbox.add(find_btn)

        # vbox.add(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

        clear_find_btn = Gtk.Button(label="Clear Find")
        clear_find_btn.set_relief(Gtk.ReliefStyle.NONE)
        clear_find_btn.connect("clicked", self.clear_search)
        vbox.add(clear_find_btn)

        # vbox.add(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

        read_btn = Gtk.Button(label="Read Aloud")
        read_btn.set_relief(Gtk.ReliefStyle.NONE)
        read_btn.connect("clicked", self.read_aloud)
        vbox.add(read_btn)
        vbox.show_all()

        # vbox.add(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

        keyboard_stortcuts_btn = Gtk.Button(label="Keyboard Shortcuts")
        keyboard_stortcuts_btn.set_relief(Gtk.ReliefStyle.NONE)
        keyboard_stortcuts_btn.connect("clicked", self.open_keyboard_shortcuts_window)
        vbox.add(keyboard_stortcuts_btn)

        # vbox.add(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

        quit_btn = Gtk.Button(label="Exit")
        quit_btn.set_relief(Gtk.ReliefStyle.NONE)
        quit_btn.connect("clicked", Gtk.main_quit)
        vbox.add(quit_btn)
        vbox.show_all()

        self.popover.add(vbox)
        self.popover.set_position(Gtk.PositionType.BOTTOM)

        self.popover_open_btn = Gtk.MenuButton(popover=self.popover)
        icon = Gio.ThemedIcon(name="open-menu-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.popover_open_btn.add(image)
        self.headerbar.pack_end(self.popover_open_btn)

        self.curpos_label = Gtk.Label(label="<span size='10000'>Ln 0, Col 0</span>", use_markup=True)
        self.curpos_label.set_opacity(0.75)
        self.headerbar.pack_end(self.curpos_label)

    def read_aloud(self, dummy):
        def say_text():
            for line in text.split("\n"):
                if line == "": continue
                try:
                    path = os.getcwd()
                    path = path + '/'
                    path = path + f'.{random.randint(0, 100000000000)}.mp3'
                    say = gTTS(text=line, lang=self.read_aloud_language[:2], slow=False, tld='co.uk')
                    say.save(path)
                    OPEN_FILES.append(path)
                    print(OPEN_FILES)
                    playsound(path)
                    os.remove(path)
                    OPEN_FILES.remove(path)
                except gtts.tts.gTTSError:
                    dialog = Gtk.MessageDialog(
                        transient_for=self,
                        message_type=Gtk.MessageType.ERROR,
                        buttons=Gtk.ButtonsType.OK,
                        text="No internet connection"
                    )
                    dialog.format_secondary_text("Unable to connect to the internet. \"Read Aloud\" cannot be performed. ")
                    dialog.run()

        text = self.editors[self.current_tab].buffer.get_text(self.editors[self.current_tab].buffer.get_start_iter(),
                                                              self.editors[self.current_tab].buffer.get_end_iter(),
                                                              False)
        if text != "":
            thread = threading.Thread(target=say_text, daemon=True)
            thread.start()

    def open_keyboard_shortcuts_window(self, _):
        keyboard_shortcuts_window = Gtk.ShortcutsWindow()
        section = Gtk.ShortcutsSection()
        section.show()
        group = Gtk.ShortcutsGroup(title="Shortcuts (THEY DON'T WORK YET)")
        group.show()

        shortcut = Gtk.ShortcutsShortcut(title="New Tab", accelerator="<Control>n")
        shortcut.show()
        group.add(shortcut)

        shortcut = Gtk.ShortcutsShortcut(title="Close Tab", accelerator="<Control>w")
        shortcut.show()
        group.add(shortcut)

        shortcut = Gtk.ShortcutsShortcut(title="Save File", accelerator="<Control>s")
        shortcut.show()
        group.add(shortcut)

        shortcut = Gtk.ShortcutsShortcut(title="Open File", accelerator="<Control>o")
        shortcut.show()
        group.add(shortcut)

        shortcut = Gtk.ShortcutsShortcut(title="Open Preferences", accelerator="<Alt>s")
        shortcut.show()
        group.add(shortcut)

        section.add(group)
        keyboard_shortcuts_window.add(section)
        keyboard_shortcuts_window.show()

        keyboard_shortcuts_window.show()

    def open_preferences(self, dummy):
        dialog = Preferences(self, self.font)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            font = dialog.font_btn.get_font_name()
            self.font = font
            for x in self.editors:
                x.editor.modify_font(Pango.FontDescription(font))

            wrap = dialog.wrap_mode_combobox.get_active_text()
            print(wrap)
            wrap_mode = Gtk.WrapMode.NONE
            if wrap == "None":
                wrap_mode = Gtk.WrapMode.NONE
            elif wrap == "Character":
                wrap_mode = Gtk.WrapMode.CHAR
                self.curpos_label.set_text("")
            elif wrap == "Word":
                wrap_mode = Gtk.WrapMode.WORD
                self.curpos_label.set_text("")
            elif wrap == "":
                wrap_mode = Gtk.WrapMode.NONE

            self.wrap_mode = wrap_mode

            for x in self.editors:
                x.editor.set_wrap_mode(wrap_mode)

            editable = dialog.editable.get_active()
            for x in self.editors:
                x.editor.set_editable(not editable)

            self.highlight_syntax_bool = dialog.syntax_highlighting.get_active()

            self.read_aloud_language = dialog.langs_combobox.get_active_text()

        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()

    def new_tab(self, dummy):
        tab_obj = Tab(self.tab_num, "Untitled" + str(self.tab_num + 1), self.switch_tab, self.close_tab)

        tab_obj.buffer.connect("notify::cursor-position", self.update_cursor_position)
        if self.font is not None:
            tab_obj.editor.modify_font(Pango.FontDescription(self.font))
        if self.wrap_mode is not None:
            tab_obj.editor.set_wrap_mode(self.wrap_mode)

        # tab_obj.buffer.set_text("Type some text here")
        self.tab_bar.add(tab_obj.hbox)
        self.editors.append(tab_obj)
        tab_obj.buffer.connect("changed", self.highlight_syntax)

        for x in range(len(self.editors)):
            self.vbox.remove(self.editors[x].scrolled_window)

        self.vbox.add(tab_obj.scrolled_window)
        self.set_title(tab_obj.name + " - Tabs")
        self.current_tab = self.tab_num
        self.switch_tab(self.current_tab)
        self.show_all()

        self.tab_num += 1

    def update_cursor_position(self, buffer, _):
        if self.editors[self.current_tab].editor.get_wrap_mode() in [Gtk.WrapMode.CHAR, Gtk.WrapMode.WORD]:
            return
        cursor_pos = buffer.props.cursor_position
        iter = buffer.get_iter_at_offset(cursor_pos)
        line = iter.get_line() + 1
        column = iter.get_line_offset() + 1
        self.curpos_label.set_text(f"Ln {line}, Col {column}")

    def highlight_syntax(self, dummy):
        # editor = self.editors[self.current_tab].editor
        # text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        # cursor_position = buffer.props.cursor_position
        # line_iter = buffer.get_iter_at_offset(cursor_position).get_line()
        # line = text.split("\n")[line_iter]
        # tag = buffer.create_tag("keyword", foreground="purple")
        # for x in range(len(line)):
        #     for y in line.split(" "):
        #         if y in KEYWORDS:
        #             buffer.apply_tag(tag, editor.get_iter_at_location(x, False), buffer.get_end_iter())
        #             print(x)
        if not self.highlight_syntax_bool:
            return

        def search_and_mark(text, start):
            end = buffer.get_end_iter()
            match = start.forward_search(text, 0, end)

            if match is not None:
                match_start, match_end = match
                buffer.apply_tag(self.tag_keyword, match_start, match_end)
                search_and_mark(text, match_end)

        buffer = self.editors[self.current_tab].buffer
        buffer.remove_all_tags(buffer.get_start_iter(), buffer.get_end_iter())
        if self.first:
            self.tag_keyword = buffer.create_tag("keyword", foreground="#d843e6")
            self.first = False
        cursor_mark = buffer.get_insert()
        start = buffer.get_iter_at_mark(cursor_mark)
        if start.get_offset() == buffer.get_char_count():
            start = buffer.get_start_iter()

        for keyword in KEYWORDS:
            search_and_mark(keyword, start)

    def switch_tab(self, index):
        self.curpos_label.set_text("Ln 0, Col 0")
        self.update_cursor_position(self.editors[index].buffer, "")
        for x in range(len(self.editors)):
            self.vbox.remove(self.editors[x].scrolled_window)

        self.vbox.add(self.editors[index].scrolled_window)
        for x in range(len(self.editors)):
            self.editors[x].name_button.set_opacity(0.5)
        self.editors[index].name_button.set_opacity(10.0)
        self.set_title(self.editors[index].name + " - Tabs")
        self.current_tab = index

    def close_tab(self, index):
        self.vbox.remove(self.editors[index].scrolled_window)
        self.tab_bar.remove(self.editors[index].hbox)
        self.set_title("Tabs")
        # if len(self.editors) != 0:
        #     self.switch_tab(0)

    def search(self, widget):
        buffer = self.editors[self.current_tab].buffer
        if self.first_search:
            self.tag_found = buffer.create_tag("found", background="yellow", foreground="black")
            self.first_search = False
        dialog = SearchDialog(self)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            cursor_mark = buffer.get_insert()
            start = buffer.get_iter_at_mark(cursor_mark)
            if start.get_offset() == buffer.get_char_count():
                start = buffer.get_start_iter()

            self.search_and_mark(dialog.entry.get_text(), start, buffer, self.tag_found)

        dialog.destroy()

    def clear_search(self, dummy):
        buffer = self.editors[self.current_tab].buffer
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        buffer.remove_all_tags(start, end)

    def search_and_mark(self, text, start, buffer, tag_found):
        end = buffer.get_end_iter()
        match = start.forward_search(text, 0, end)

        if match is not None:
            match_start, match_end = match
            buffer.apply_tag(tag_found, match_start, match_end)
            self.search_and_mark(text, match_end, buffer, tag_found)

    def save_as(self, dummy):
        current_tab = self.editors[self.current_tab]
        buffer = current_tab.buffer
        text = current_tab.buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        dialog = Gtk.FileChooserDialog(
            title="", parent=self, action=Gtk.FileChooserAction.SAVE
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                file = open(dialog.get_filename(), "w")
                self.editors[self.current_tab].file_path = dialog.get_filename()
                self.set_title(
                    str(dialog.get_filename()[dialog.get_filename().rfind("/") + 1:]) + " - Tabs")
                current_tab.name_button.set_label(str(dialog.get_filename()[dialog.get_filename().rfind("/") + 1:]))
                current_tab.name = str(dialog.get_filename()[dialog.get_filename().rfind("/") + 1:])
                file.write(str(text))
                file.close()
            except Exception as e:
                pass
        elif response == Gtk.ResponseType.CANCEL:
            pass
        dialog.destroy()

    def save(self, dummy, index=None):
        current_tab = self.editors[self.current_tab]
        if index is not None:
            current_tab = self.editors[index]
        buffer = current_tab.buffer
        text = current_tab.buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        if current_tab.file_path == "":
            dialog = Gtk.FileChooserDialog(
                title="", parent=self, action=Gtk.FileChooserAction.SAVE
            )
            dialog.add_buttons(
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN,
                Gtk.ResponseType.OK,
            )
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                try:
                    file = open(dialog.get_filename(), "w")
                    self.editors[self.current_tab].file_path = dialog.get_filename()
                    self.set_title(
                        str(dialog.get_filename()[dialog.get_filename().rfind("/") + 1:]) + " - Tabs")
                    current_tab.name_button.set_label(str(dialog.get_filename()[dialog.get_filename().rfind("/") + 1:]))
                    current_tab.name = str(dialog.get_filename()[dialog.get_filename().rfind("/") + 1:])
                    file.write(str(text))
                    file.close()
                except Exception as e:
                    pass
            elif response == Gtk.ResponseType.CANCEL:
                pass
            dialog.destroy()
        else:
            file = open(current_tab.file_path, "w")
            file.write(str(text))
            file.close()

    def save_all(self):
        for editor in self.editors:
            if editor.file_path != "":
                self.save("", index=editor.number)

    def open(self, dummy):
        current_tab = self.editors[self.current_tab]
        dialog = Gtk.FileChooserDialog(
            title="Select file to open", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                file = open(dialog.get_filename(), "r")
                current_tab.buffer.set_text(file.read())
                self.set_title(str(dialog.get_filename()[dialog.get_filename().rfind("/") + 1:]) + " - Tabs")
                current_tab.name_button.set_label(str(dialog.get_filename()[dialog.get_filename().rfind("/") + 1:]))
                current_tab.name = str(dialog.get_filename()[dialog.get_filename().rfind("/") + 1:])
                current_tab.file_path = dialog.get_filename()
                file.close()
            except Exception as e:
                pass
        elif response == Gtk.ResponseType.CANCEL:
            pass
        dialog.destroy()

    @staticmethod
    def quit(dummy):
        for x in OPEN_FILES:
            os.remove(x)

        Gtk.main_quit()
