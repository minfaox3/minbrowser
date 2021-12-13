#!/usr/bin/python 
# -*- coding: utf-8 -*- 

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2
import json

#decode webpage's html to view sourcecode
def decode_str(s):
  for charset in [u'cp932', u'utf-8', u'euc-jp', u'shift-jis', u'iso2022-jp']:
    try:
      return s.decode(charset)
    except:
      pass

class TabContent(Gtk.Box):
  def __init__(self) -> None:
      super().__init__(homogeneous=Gtk.Orientation.HORIZONTAL, spacing=3)
      self.view_window = Gtk.ScrolledWindow.new(None, None)
      self.source_view_window = Gtk.ScrolledWindow.new(None, None)
      self.source_view_button_icon = Gtk.Image.new_from_icon_name("go-last-symbolic-rtl", Gtk.IconSize.BUTTON)
      self.source_view_button = Gtk.Button.new()
      self.source_view = Gtk.TextView.new()
      self.webview = WebKit2.WebView()
      self.source_view_button.set_image(self.source_view_button_icon)
      self.source_view_button.connect("clicked", source_view_button_clicked)
      self.source_view_window.add(self.source_view)
      self.pack_start(self.view_window, True, True, 0)
      self.pack_start(self.source_view_button, False, True, 0)
      self.pack_start(self.source_view_window, True, True, 0)
      self.webview.connect("notify::uri", uri_changed)
      self.webview.connect("notify::title", title_changed)
      self.webview.connect("load-changed", load_changed)
      self.webview.connect("create", create)
      self.webview.load_uri(homepage)
      self.webview.set_editable(False)
      self.view_window.add(self.webview)
      self.source_view_window.hide()
      self.webview.show()

  def destroy(self):
    self.webview.destroy()
    self.view_window.destroy()
    self.source_view_button.destroy()
    self.source_view_button_icon.destroy()
    self.source_view.destroy()
    self.source_view_window.destroy()
    self.destroy()

  def hide_source_view_window(self):
    self.source_view_window.hide()
    self.source_view_button_icon.set_from_icon_name("go-last-symbolic-rtl", Gtk.IconSize.BUTTON)

  def switch_source_view(self):
    if(self.source_view_window.get_property("visible")):
      self.source_view_button_icon.set_from_icon_name("go-last-symbolic-rtl", Gtk.IconSize.BUTTON)
      self.source_view_window.hide()
    else:
      self.source_view.get_buffer().set_text(htmls[operate_page])
      self.source_view_button_icon.set_from_icon_name("go-last-symbolic", Gtk.IconSize.BUTTON)
      self.source_view_window.show()

  def go_back(self):
    self.webview.go_back()

  def reload(self):
    self.webview.reload()
  
  def load_uri(self, uri):
    self.webview.load_uri(uri)

class TabLabel(Gtk.Box):
  def __init__(self) -> None:
      super().__init__(homogeneous=Gtk.Orientation.HORIZONTAL, spacing=2)
      self.label = Gtk.Label.new("new tab")
      self.image = Gtk.Image.new_from_icon_name("edit-delete-symbolic", Gtk.IconSize.BUTTON)
      self.button = Gtk.Button.new()
      self.button.set_image(self.image)
      self.button.set_relief(Gtk.ReliefStyle.NONE)
      self.pack_start(self.label, True, True, 0)
      self.pack_start(self.button, False, False, 0)
      self.show_all()

class BrowseTab():
  def __init__(self, page_num) -> None:
    self.page_num = page_num
    self.label = TabLabel()
    self.content = TabContent()
    self.label.button.connect("clicked", self.close_tab)
  
  def close_tab(self, button):
    note_book.remove_page(self.page_num)
    tabs.pop(note_book.get_current_page())


#this handle connect to gobject's signal
class SignalHandler: 
  #MainWindowSignals
  def mw_back_button_clicked(self, button):
    tabs[operate_page].content.go_back()

  def mw_reload_button_clicked(self, button):
    tabs[operate_page].content.reload()
    search_bar.set_text(uris[operate_page])
    
  def mw_home_button_clicked(self, button):
    tabs[operate_page].content.load_uri(homepage)

  def mw_enterkey_clicked(self, button):
    global search_text
    search_text = search_bar.get_text()
    tabs[operate_page].content.load_uri(search_text)

  def mw_bookmark_button_clicked(self, button):
    if uris[operate_page] in bookmarks:
      bookmarks.remove(uris[operate_page])
      bookmark_image.set_from_icon_name("non-starred-symbolic", Gtk.IconSize.BUTTON)
    else:
      bookmarks.append(uris[operate_page])
      bookmark_image.set_from_icon_name("starred-symbolic", Gtk.IconSize.BUTTON)
  
  #pvmSignals
  def pvm_open_button_clicked(self, button):
    print("SIGNAL DETECTED:OPEN BOOKMARK")

  def pvm_config_button_clicked(self, button):
    print("SIGNAL DETECTED:OPEN CONFIG")
  
  def pvm_about_button_clicked(self, button):
    about_dialog.show_all()
  
  def pvm_quit_button_clicked(self, button):
    Gtk.main_quit()
  

  #AboutMenuSignal
  def about_dialog_delete_event(self, event, ud):
    about_dialog.hide()
    return True
  
  def ad_quit_button_clicked(self, button):
    about_dialog.hide()

  #Signals in Tab
  def t_add_tab_button_clicked(self, button):
    global uris
    global htmls
    global search_bar_texts
    global tabs
    global operate_page
    recent_op = operate_page
    search_bar_texts[operate_page] = search_bar.get_text()
    operate_page = note_book.get_n_pages()
    uris.append("")
    htmls.append("")
    search_bar_texts.append("")
    tabs.append(BrowseTab(operate_page))
    note_book.append_page(tabs[len(tabs)-1].content, tabs[len(tabs)-1].label)
    note_book.show_all()
    note_book.do_change_current_page(note_book, note_book.get_n_pages()-(note_book.get_current_page()+1))
    tabs[recent_op].content.hide_source_view_window()
    tabs[note_book.get_current_page()].content.hide_source_view_window()

def source_view_button_clicked(button):
  tabs[operate_page].content.switch_source_view()


#these functions connect to webkit::webview
def load_changed(self, event, ud=None):
  global tabs
  if event == WebKit2.LoadEvent.FINISHED:
    resource = self.get_main_resource()
    if resource is not None:
      resource.get_data(None, get_data,None)
    else:
      tabs[operate_page].content.load_uri("https://www.google.com/search?q="+search_text)

def get_data(self, task, ud=None):
  global htmls
  htmls[operate_page] = decode_str(self.get_data_finish(task))
  if(tabs[operate_page].content.source_view_window.get_property("visible")):
    buffer = tabs[operate_page].content.source_view.get_buffer()
    buffer.set_text(htmls[operate_page])

def uri_changed(self, v):
  global uris
  global search_bar_texts
  uris[operate_page] = self.get_uri()
  search_bar_texts[operate_page] = uris[operate_page]
  search_bar.set_text(uris[operate_page])
  if uris[operate_page] in bookmarks:
    bookmark_image.set_from_icon_name("starred-symbolic", Gtk.IconSize.BUTTON)
  else:
    bookmark_image.set_from_icon_name("non-starred-symbolic", Gtk.IconSize.BUTTON)

def title_changed(self, v):
  tabs[operate_page].label.label.set_text(self.get_title())

def create(self, n):
  global uris
  global htmls
  global search_bar_texts
  global tabs
  global operate_page
  recent_op = operate_page
  search_bar_texts[operate_page] = search_bar.get_text()
  operate_page = note_book.get_n_pages()
  uris.append("")
  htmls.append("")
  search_bar_texts.append("")
  tabs.append(BrowseTab(len(tabs)))
  note_book.append_page(tabs[len(tabs)-1].content, tabs[len(tabs)-1].label)
  note_book.show_all()
  note_book.do_change_current_page(note_book, note_book.get_n_pages()-(note_book.get_current_page()+1))
  tabs[recent_op].content.hide_source_view_window()
  tabs[note_book.get_current_page()].content.hide_source_view_window()
  tabs[note_book.get_current_page()].content.load_uri(n.get_request().get_uri())

def switch_page(self, page, page_num):
  global operate_page
  global search_bar_texts
  search_bar_texts[operate_page] = search_bar.get_text()
  operate_page = page_num
  search_bar.set_text(search_bar_texts[page_num])

#Main logic
builder = Gtk.Builder()
builder.add_from_file("ui.glade")
builder.connect_signals(SignalHandler())

#global variables
homepage = "https://www.google.com"
operate_page = 0
bookmarks = []
uris = []
tabs = []
labels = []
htmls = []
search_bar_texts = []

#get gobjects
window = builder.get_object("window")
about_dialog = builder.get_object("about_dialog")
search_bar = builder.get_object("mw_search_bar")
reload_image = builder.get_object("mw_reload_image")
bookmark_image = builder.get_object("mw_bookmark_image")
note_book = builder.get_object("mw_note_book")

note_book.connect("switch-page", switch_page)

uris.append("")
htmls.append("")
search_bar_texts.append("")
tabs.append(BrowseTab(0))
note_book.append_page(tabs[len(tabs)-1].content, tabs[len(tabs)-1].label)

window.connect("delete-event", Gtk.main_quit)
window.show_all()
tabs[0].content.hide_source_view_window()
Gtk.main()