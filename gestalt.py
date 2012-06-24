from gi.repository import GObject, Gedit, Gtk
from GESTALTDocument import GESTALTDocument
from GESTALTCompletionWindow import GESTALTCompletionWindow

class GESTALTWindowActivatable(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "GESTALTWindowActivatable"
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self):
        GObject.Object.__init__(self)
        self.popup = None
    
    # Called when the plugin is activated.  Setup should be done here
    def do_activate(self):
        print "Starting GESTALT..."

        #######################################
        # PLUGIN SETUP
        handlers = []; # An array to hold handlers for adding and removing tabs
        # ADD TAB HANDLER
        handler_id = self.window.connect("tab-added", self.on_tab_added);
        handlers.append(handler_id);
        # REMOVE TAB HANDLER
        handler_id = self.window.connect("tab-removed", self.on_tab_removed);
        handlers.append(handler_id);
        # KEYPRESS HANDLER
        handler_id = self.window.connect("key-press-event", self.on_keypress);
        handlers.append(handler_id);
        # Set the handlers array so it can be accessed later
        self.window.set_data("handlers",handlers);
        print "Window ", self.window, " activated."
        #######################################

        #######################################
        # GESTALT Setup
        open_documents = []; # An array to hold all of the currently open documents

        self.window.set_data("open_documents",open_documents);

        self.popup = GESTALTCompletionWindow(self.window, self.complete_callback);
        #######################################

    # Called when the plugin is deactivated.  Any cleanup should be done here
    def do_deactivate(self):
        handlers = self.window.get_data("handlers")
        for handler_id in handlers:
            self.window.disconnect(handler_id)
            print "Disconnected handler %s" % handler_id

        print "Window ", self.window, " deactivated"

    # Called on several events when using the window.  Here is an incomplete list
    #   File saves
    #   Newline after a pause
    def do_update_state(self):
        a = 0; # Dummy line
        #print "Window %s state updated." % self.window

    # The handler callback for when a tab is added
    def on_tab_added(self, window, tab, data=None):
        print "Added tab"

        ### GET DATA
        open_documents = self.window.get_data("open_documents");
        ###

        # TODO Check if the opened tab is a new document or an opened file
        location = tab.get_document().get_uri_for_display();
        doc = GESTALTDocument(location,tab);
        
        open_documents.append(doc);

        ### SET DATA
        self.window.set_data("open_documents",open_documents);
        ###

        print "Tab added"

    # The handler callback for when a tab is removed
    def on_tab_removed(self, window, tab, data=None):
        print "Removing Tab"
        
        ### GET DATA
        open_documents = self.window.get_data("open_documents");
        ###

        for doc in open_documents:
            if doc.tab == tab:
                open_documents.remove(doc)
                break

        ### SET DATA
        self.window.set_data("open_documents",open_documents);
        ###

        print "Removed tab"

    def complete_callback(self):
        print "COMPLETION CALLBACK!!"

    def on_keypress(self,window,event):
#        print "Keypress",event.keyval,"  ", event.string

#        doc = window.get_active_document()
#        path = doc.get_uri_for_display()
#        f = open(path);
#        print f.read()

#        a = dir(Gedit.View);
#        f = open('Gedit.View','w');
#        for b in a:
#            f.write(b+'\n');

        # Find the current location of the cursor so that we can place the popup box at the right spot
        view = window.get_active_view()
        doc = view.get_buffer()
        insert = doc.get_iter_at_mark(doc.get_insert())
        rect = view.get_iter_location(insert)
        x, y = view.buffer_to_window_coords(Gtk.TextWindowType.TEXT, rect.x, rect.y)
        x, y = window.translate_coordinates(self.window, x, y)

        root_x, root_y = self.window.get_position()
        self.popup.move(root_x + x + 40, root_y + y + 120)
        if event.keyval == 96:
            self.popup.show_all()

