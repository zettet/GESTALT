from gi.repository import GObject, Gedit
        
class GESTALTWindowActivatable(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "GESTALTWindowActivatable"
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self):
        GObject.Object.__init__(self)
    
    # Called when the plugin is activated.  Setup should be done here
    def do_activate(self):
        print "Starting GESTALT..."
        handlers = []; # An array to hold handlers for adding and removing tabs

        # ADD TAB HANDLER
        handler_id = self.window.connect("tab-added", self.on_tab_added);
        handlers.append(handler_id);

        # REMOVE TAB HANDLER
        handler_id = self.window.connect("tab-removed", self.on_tab_removed);
        handlers.append(handler_id);

        # Set the handlers array so it can be accessed later
        self.window.set_data("tab_handlers",handlers);
        print "Window ", self.window, " activated."

    # Called when the plugin is deactivated.  Any cleanup should be done here
    def do_deactivate(self):
        handlers = self.window.get_data("tab_handlers")
        for handler_id in handlers:
            self.window.disconnect(handler_id)
            print "Disconnected handler %s" % handler_id

        print "Window ", self.window, " deactivated."

    # Called on several events when using the window.  Here is an incomplete list
    #   File saves
    #   Newline after a pause
    def do_update_state(self):
        print "Window %s state updated." % self.window

    # The handler callback for when a tab is added
    def on_tab_added(self, window, tab, data=None):
        print "Added tab"

    # The handler callback for when a tab is removed
    def on_tab_removed(self, window, tab, data=None):
        print "Removed tab" 
