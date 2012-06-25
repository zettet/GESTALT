from gi.repository import GObject, Gtk, Gedit
import re

class GESTALTCompletionWindow(Gtk.Window):

    """Window for displaying a list of completions."""

    def __init__(self, parent, callback):
        print "Initializing Window"
        Gtk.Window.__init__(self,Gtk.WindowType.TOPLEVEL)
        self.set_decorated(False)
        self.store = None
        self.view = None
        self.completions = None
        self.complete_callback = callback
        self.set_transient_for(parent)
        self.set_border_width(1)
        self.text = Gtk.TextView()
        self.text_buffer = Gtk.TextBuffer()
        self.text.set_buffer(self.text_buffer)
        self.text.set_size_request(300, 200)
        self.text.set_sensitive(False)
        self.init_tree_view()
        self.init_frame()
        self.set_completions([]);
        self.connect('focus-out-event', self.focus_out_event)
        self.connect('key-press-event', self.key_press_event)
        self.grab_focus()
    
    def key_press_event(self, widget, event):
        print "Key_press",event.keyval
        if event.keyval == 65307: # Escape
           self.hide()
        elif event.keyval == 65288: # Backspace
           self.hide()
        elif event.keyval in [65293,65289]: # Return or tab
           self.complete()
        elif event.keyval == 65362: # Up arrow
           self.select_previous()
        elif event.keyval == 65364: # Down arrow
           self.select_next()

    def complete(self):
        print "Complete"
        #self.complete_callback(self.completions[self.get_selected()]['completion'])

    def focus_out_event(self, *args):
        print "Focus out"
        self.hide()
    
    def get_selected(self):
        """Get the selected row."""
        print "Get_selected"
        selection = self.view.get_selection()
        return selection.get_selected_rows()[1][0].get_indices()[0]

    def init_frame(self):
        """Initialize the frame and scroller around the tree view."""
        
        print "init_frame"
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)
        scroller.add(self.view)
        frame = Gtk.Frame()
        frame.set_shadow_type(Gtk.ShadowType.OUT)
        hbox = Gtk.HBox()
        hbox.add(scroller)

        scroller_text = Gtk.ScrolledWindow() 
        scroller_text.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroller_text.add(self.text)
        hbox.add(scroller_text)
        frame.add(hbox)
        self.add(frame)
        print "init_frame finished"

    def init_tree_view(self):
        """Initialize the tree view listing the completions."""

        print "init_tree_view"
        self.store = Gtk.ListStore(str,str) # If the list store should hold more fields, include them here.  This can also take a GObject
        self.view = Gtk.TreeView(self.store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("", renderer, text=0)
        self.view.append_column(column)
        self.view.set_enable_search(False)
        self.view.set_headers_visible(False)
        self.view.set_rules_hint(True)
        selection = self.view.get_selection()
        selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.view.set_size_request(300, 200)
        self.view.connect('row-activated', self.row_activated)
        print "init_tree_view_finished"

    def row_activated(self, tree, path, view_column, data = None):
        print "row activated"
        #self.complete()

    def select_next(self):
        """Select the next completion."""

        print "select next"
        row = min(self.get_selected() + 1, len(self.store) - 1)
        selection = self.view.get_selection()
        selection.unselect_all()
        selection.select_path(row)
        self.view.scroll_to_cell(row)
      
        self.text_buffer.set_text(self.completions[self.get_selected()][1])

    def select_previous(self):
        """Select the previous completion."""

        print "select previous"
        row = max(self.get_selected() - 1, 0)
        selection = self.view.get_selection()
        selection.unselect_all()
        selection.select_path(row)
        self.view.scroll_to_cell(row)
        
        self.text_buffer.set_text(self.completions[self.get_selected()][1])

    def set_completions(self, completions):
        """Set the completions to display."""

        print "set completions"

        self.completions = [["add","ADD"],
                            ["the","THE"],
                            ["completion","COMPLETION"],
                            ["candidates","CANDIDATES"],
                            ["here","HERE"]];

        #self.completions = completions
        self.resize(1, 1)
        self.store.clear()
        for completion in self.completions:
           self.store.append(completion)
           #self.store.append([unicode(completion['abbr'])])

        self.view.columns_autosize()
        self.view.get_selection().select_path(0)
        self.text_buffer.set_text(self.completions[0][1]);

    def set_font_description(self, font_desc):
        """Set the label's font description."""
        print "set font description"
        #self.view.modify_font(font_desc)

