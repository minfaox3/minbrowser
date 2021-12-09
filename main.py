#!/usr/bin/python 
# -*- coding: utf-8 -*- 

## Here we imported both Gtk library and the WebKit engine. 
import gi
from requests import exceptions
from requests.sessions import Request
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2

class Handler: 
  
  def back_button_clicked(self, button):
    webview.go_back()

  def reload_button_clicked(self, button):
    webview.reload()
    
  def home_button_clicked(self, button):
    webview.load_uri("https://www.google.com")

  def enterkey_clicked(self, button):
    webview.load_uri(search_bar.get_text())

  def source_button_clicked(self, button):
    if(svs.get_property("visible")):
      sb_image.set_from_stock("gtk-media-forward", Gtk.IconSize.BUTTON)
      svs.hide()
    else:
      buffer = source_viewer.get_buffer()
      buffer.set_text(html.encode('utf-8'))
      sb_image.set_from_stock("gtk-media-previous", Gtk.IconSize.BUTTON)
      svs.show()

def load_changed(self, event, ud=None):
  if event == WebKit2.LoadEvent.FINISHED:
    self.get_main_resource().get_data(None, grdata,None)

def grdata(self, task, ud=None):
  global html
  html = self.get_data_finish(task)
  if(svs.get_property("visible")):
    buffer = source_viewer.get_buffer()
    for charset in [u'cp932', u'utf-8', u'euc-jp', u'shift-jis', u'iso2022-jp']:
        try:
          html = html.decode(charset)
          break
        except:
          pass
    buffer.set_text(html)

def uri_changed(self, v):
  search_bar.set_text(self.get_uri())

## Nothing new here.. We just imported the 'ui.glade' file. 
builder = Gtk.Builder() 
builder.add_from_file("ui.glade") 
builder.connect_signals(Handler()) 

html = ""

window = builder.get_object("window") 

## Here's the new part.. We created a global object called 'browserholder' which will contain the WebKit rendering engine, and we set it to 'WebKit.WebView()' which is the default thing to do if you want to add a WebKit engine to your program. 
webview = WebKit2.WebView() 

## To disallow editing the webpage. 
webview.set_editable(False) 

webview.connect("notify::uri", uri_changed)
webview.connect("load-changed", load_changed)

search_bar = builder.get_object("search_bar")  
source_viewer = builder.get_object("source_viewer")
svs = builder.get_object("svs")
sb_image = builder.get_object("sb_image")

## The default URL to be loaded, we used the 'load_uri()' method. 
webview.load_uri("https://www.google.com")

## Here we imported the scrolledwindow1 object from the ui.glade file. 
viewer = builder.get_object("viewer") 

## We used the '.add()' method to add the 'browserholder' object to the scrolled window, which contains our WebKit browser. 
viewer.add(webview) 

## And finally, we showed the 'browserholder' object using the '.show()' method. 
webview.show() 
 
## Give that developer a cookie ! 
window.connect("delete-event", Gtk.main_quit) 
window.show_all() 
Gtk.main()