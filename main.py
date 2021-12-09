#!/usr/bin/python 
# -*- coding: utf-8 -*- 

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2

def decode_str(s):
  for charset in [u'cp932', u'utf-8', u'euc-jp', u'shift-jis', u'iso2022-jp']:
    try:
      return s.decode(charset)
    except:
      pass

class SignalHandler: 
  def back_button_clicked(self, button):
    webview.go_back()

  def reload_button_clicked(self, button):
    webview.reload()
    search_bar.set_text(uri)
    
  def home_button_clicked(self, button):
    webview.load_uri(homepage)

  def enterkey_clicked(self, button):
    global search_text
    search_text = search_bar.get_text()
    webview.load_uri(search_text)

  def source_button_clicked(self, button):
    if(svs.get_property("visible")):
      sb_image.set_from_stock("gtk-media-previous", Gtk.IconSize.BUTTON)
      svs.hide()
    else:
      buffer = source_viewer.get_buffer()
      buffer.set_text(html)
      sb_image.set_from_stock("gtk-media-forward", Gtk.IconSize.BUTTON)
      svs.show()

  def bookmark_button_clicked(self, button):
    if uri in bookmarks:
      bookmarks.remove(uri)
      bookmark_image.set_from_icon_name("non-starred-symbolic", Gtk.IconSize.BUTTON)
    else:
      bookmarks.append(uri)
      bookmark_image.set_from_icon_name("starred-symbolic", Gtk.IconSize.BUTTON)

def load_changed(self, event, ud=None):
  if event == WebKit2.LoadEvent.FINISHED:
    resource = self.get_main_resource()
    if resource is not None:
      resource.get_data(None, grdata,None)
    else:
      webview.load_uri("https://www.google.com/search?q="+search_text)

def grdata(self, task, ud=None):
  global html
  html = self.get_data_finish(task)
  html = decode_str(html)
  if(svs.get_property("visible")):
    buffer = source_viewer.get_buffer()
    buffer.set_text(html)

def uri_changed(self, v):
  global uri
  uri = self.get_uri()
  search_bar.set_text(uri)
  if uri in bookmarks:
    bookmark_image.set_from_icon_name("starred-symbolic", Gtk.IconSize.BUTTON)
  else:
    bookmark_image.set_from_icon_name("non-starred-symbolic", Gtk.IconSize.BUTTON)
 
builder = Gtk.Builder() 
builder.add_from_file("ui.glade") 
builder.connect_signals(SignalHandler()) 

uri = ""
html = ""
search_text = ""
homepage = "https://www.google.com"
bookmarks = []

window = builder.get_object("window") 
search_bar = builder.get_object("search_bar")  
source_viewer = builder.get_object("source_viewer")
svs = builder.get_object("svs")
sb_image = builder.get_object("sb_image")
reload_image = builder.get_object("reload_image")
bookmark_image = builder.get_object("bookmark_image")
viewer = builder.get_object("viewer") 

webview = WebKit2.WebView() 
webview.set_editable(False)

webview.connect("notify::uri", uri_changed)
webview.connect("load-changed", load_changed)
webview.load_uri("https://www.google.com")

viewer.add(webview) 
webview.show()
 
window.connect("delete-event", Gtk.main_quit) 
window.show_all() 
Gtk.main()