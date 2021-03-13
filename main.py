# main.py
# A little GUI for its own sake
#
# By Gavin
# March 13th 2021


import gi
from twitterRSS import *
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk


class Window(Gtk.Window):
	def __init__(self):
		self.shadowbanned = False
		Gtk.Window.__init__(self, title="TwitteRSS")
		Gtk.Window.set_default_size(self, 300,300)
		Gtk.Window.set_resizable(self, False)
		border = Gtk.Frame(shadow_type=Gtk.ShadowType.IN, border_width=6)
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6) #entry & spinner
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
		self.add(border)
		border.add(vbox) #primary container
		
		label = Gtk.Label(label="Enter Twitter Username")
		
		self.entry = Gtk.Entry()
		self.entry.connect("key-press-event", self.submission)
		
		self.spinner = Gtk.Spinner()
		
		banButton = Gtk.CheckButton(label="Shadowbanned User")
		banButton.connect("toggled", self.on_banButton_toggled, "1")
		
		aboutButton = Gtk.LinkButton.new_with_label(
            uri="https://www.github.com/gavosb",
            label="Github"
        )
		
		separator = Gtk.Separator()
		label2 = Gtk.Label(label="Default location: /feeds")
		fileopener = Gtk.FileChooserButton(title="Change save location", action=Gtk.FileChooserAction.SELECT_FOLDER)
		
		vbox.pack_start(label, True, True, 0)
		vbox.pack_start(hbox, True, True, 0)
		hbox.pack_start(self.entry, True, True, 0)
		hbox.pack_end(self.spinner, True, True, 0)
		vbox.pack_start(banButton, True, True, 0)
		vbox.pack_start(separator, True, True, 0)
		vbox.pack_start(label2, True, True, 0)
		vbox.pack_start(fileopener, True, True, 0)
		vbox.pack_start(aboutButton, True, True, 0)
		
	def submission(self, button, event): #self, widget, event
		if Gdk.keyval_name (event.keyval) == "Return":
			self.spinner.start()
			twiddle = twitter_feed(button.get_text(), 400, self.shadowbanned)
			twiddle.convert_RSS()
			#self.spinner.stop() #uncomment this if you want it to not spin constantly idk i dont care
	
	def on_banButton_toggled():
		self.shadowbanned = !self.shadowbanned

win = Window()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
