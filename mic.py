#!/usr/bin/python

import sys
import re

import pygtk
pygtk.require('2.0')

import gtk
import gnomeapplet
import gobject

import gnome.ui

from commands import *

class GnomeMicControl(gnomeapplet.Applet):

	def __init__(self, applet, iid):
		applet = applet

		xml = '<popup name="button3"><menuitem name="About Item" verb="About" stockid="gtk-about" /></popup>'
		verbs = [("About", self.menu)]
		applet.setup_menu(xml, verbs, None)

		hbox = gtk.VBox()
		applet.add(hbox)

		button = gtk.EventBox()

		self.image = gtk.Image()

		self.update_status()

		button.connect('button-press-event', self.click)
		button.add(self.image)
		hbox.add(button)
		# hbox.add(self.image)
	
		applet.show_all()
		gobject.timeout_add(100, self.update_status)

	def click(self, widget, event):
		if event.button == 1:
			self.change_status()
		elif event.button == 2:
			self.init_menu()

	def menu(self, event, data = None):
		gnome.ui.About('GNOME Microphone Control', '0.2', 'GNU GPLv3', '', ['p01nt <pasha@klets.name>',]).show()

	def change_status(self):
		getoutput('amixer set Capture toggle')
		self.update_status()

	def update_status(self):
		out = getoutput('amixer cget name="Capture Switch" | tail -1')
		result = re.findall('values=(on|off),', out);
		self.image.set_from_file('/usr/share/pixmaps/mic_' + result[0] + '.png')

		return True

def run_in_window():
	window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	window.set_title('Microphone Control')
	window.connect('destroy', gtk.main_quit)

	app = gnomeapplet.Applet()
	applet_factory(app, None)
	app.reparent(window)
	window.show_all()

	gtk.main()
	sys.exit()

def run_in_panel():
	gnomeapplet.bonobo_factory('OAFIID:MicControl_Factory', GnomeMicControl.__gtype__, 'Microphone Control', '0.1', applet_factory)

def applet_factory(applet, iid):
	GnomeMicControl(applet, iid)
	return True

def main(args):
	if len(args) == 2 and args[1] == '--debug':
		run_in_window()
	else:
		run_in_panel()

if __name__ == '__main__':
	main(sys.argv)
