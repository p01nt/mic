#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys
import gtk
import gtk.gdk
import gnome.ui
import gnomeapplet
from commands import *

class GnomeMicControl(gnomeapplet.Applet):
	def __init__(self, applet, iid):
		self.applet = applet
		self.__init_core_widgets()
		self.init_additional_widgets()
		self.init_ppmenu()
		self.__connect_events()
		"""self.applet.connect("destroy", self._cleanup)"""
		"""self.after_init()"""
		self.applet.show_all()

	def __init_core_widgets(self):
		self.hbox = gtk.HBox()
		self.ev_box = gtk.EventBox()
		self.applet.add(self.hbox)
		self.hbox.add(self.ev_box)

	def init_additional_widgets(self):
		self.update_status()
		self.image = gtk.Image()
		self.update_image()

		self.button = gtk.Button()
		self.button.connect("clicked", self.change_status)
		self.button.set_image(self.image)
		self.ev_box.add(self.button)
	
	def update_image(self):
		self.image.set_from_file('/server/mic/img/mic_' + self.status + '_ico.png')

	def update_status(self):
		out = getoutput('amixer cget name="Capture Switch" | tail -1')
		result = re.findall('values=(on|off),', out);
		self.status = result[0];

	def change_status(self, data):
		getoutput('amixer set Capture toggle')
		self.update_status()
		self.update_image()

	def init_ppmenu(self):
		self.ppmenu_xml = """<popup name="button3"><menuitem name="About Item" verb="About" stockid="gtk-about" /></popup>"""
		self.ppmenu_verbs = [("About", self.on_ppm_about)]

	def on_ppm_about(self, event, data=None):
		gnome.ui.About("GNOME Microphone Control", "0.1", "GNU General Public License v.2", "", ["p01nt <pasha@klets.name>, areign <areign@yandex.ru>",]
		).show()

	def __connect_events(self):
		self.ev_box.connect("button-press-event", self.on_button)
		self.button_actions = {
			1: lambda: None,
			2: lambda: None,
			3: self._show_ppmenu,
		}

	def on_button(self, widget, event):
		if event.type == gtk.gdk.BUTTON_PRESS:
			self.button_actions[event.button]()

	def _show_ppmenu(self):
		self.applet.setup_menu(self.ppmenu_xml, self.ppmenu_verbs, None)

def applet_factory(applet, iid):
	GnomeMicControl(applet, iid)
	return True

def run_in_window():
	main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	main_window.set_title("Microphone Control")
	main_window.connect("destroy", gtk.main_quit)
	app = gnomeapplet.Applet()
	applet_factory(app, None)
	app.reparent(main_window)
	main_window.show_all()
	gtk.main()
	sys.exit()

def run_in_panel():
	gnomeapplet.bonobo_factory("OAFIID:MicControl_Factory", GnomeMicControl.__gtype__, "Microphone Control", "0.1", applet_factory)



def main(args):
	if len(args) == 2 and args[1] == 'debug':
		run_in_window()
	else:
		run_in_panel()

if __name__ == '__main__':
	main(sys.argv)

