from tkinter import *

from PIL import Image, ImageTk
from textbox import Textbox


class Buttonbox(Textbox):

	def __init__(self, **kwargs):
		self.text = kwargs['text']
		self.repr = kwargs['repr']
		self.width = 30
		self.label_bg = '#4DBCE9'
		self.label_fg = 'black'
		self.hover_bg = '#26ADE4'
		self.hover_fg = 'white'
		
	def set_hover(self):
		def set_hover_bg(event):
			self.label.config(bg=self.hover_bg, fg=self.hover_fg)
			self.img.config(bg=self.hover_bg, fg=self.hover_fg)

		def remove_hover_bg(event):
			self.label.config(bg=self.label_bg, fg=self.label_fg)
			self.img.config(bg=self.label_bg, fg=self.label_fg)

		if hasattr(self, 'img'):
			self.widget_frame.bind('<Enter>', set_hover_bg)
			self.widget_frame.bind('<Leave>', remove_hover_bg)
		else:
			self.widget_frame.bind('<Enter>', lambda event: self.label.config(bg=self.hover_bg, fg=self.hover_fg))
			self.widget_frame.bind('<Leave>', lambda event: self.label.config(bg=self.label_bg, fg=self.label_fg))

	def config(self, **kwargs):
		if 'lang' in kwargs:
			pass
			#self.lang = kwargs['lang']
			#self.label.config(text=self.lang[self.text])
		if 'cmd' in kwargs:
			self.command = kwargs['cmd']
			self.label.bind('<Button-1>', lambda event: self.command())
			if hasattr(self, 'img'):
				self.img.bind('<Button-1>', lambda event: self.command())
		if 'width' in kwargs:
			self.width = kwargs['width']
			self.label.config(width=self.width)
		if 'label_bg' in kwargs:
			self.label_bg = kwargs['label_bg']
			self.label.config(bg=self.label_bg)
		if 'label_fg' in kwargs:
			self.label_fg = kwargs['label_fg']
			self.label.config(fg=self.label_fg)
		if 'hover_bg' in kwargs:
			self.hover_bg = kwargs['hover_bg']
			self.hover_fg = self.label_fg if self.hover_fg == None else self.hover_fg
			self.set_hover()
		if 'hover_fg' in kwargs:
			self.hover_fg = kwargs['hover_fg']
			self.hover_bg = self.label_bg if self.hover_bg == None else self.hover_bg
			self.set_hover()
		if 'image' in kwargs:
			self.img_path = kwargs['image']
			self.picture = Image.open(self.img_path)
			self.image = ImageTk.PhotoImage(self.picture)
			self.img = Label(self.widget_frame, bg=self.label_bg, fg=self.label_fg)
			self.img.grid(row=0, column=0, ipadx=5, ipady=5, columnspan=2, sticky=W)
			self.img.config(image=self.image)
			self.set_hover()
			if hasattr(self, 'command'):
				self.img.bind('<Button-1>', lambda event: self.command())
		if 'image_resize' in kwargs:
			self.picture = self.picture.resize(kwargs['image_resize'], Image.ANTIALIAS)
			self.image = ImageTk.PhotoImage(self.picture)
			self.img.config(image=self.image)
		
	def setData(self, data):
		self.config(text=data)

	def place(self, **kwargs):
		self.parent = kwargs['parent']
		self.row = kwargs['row']
		self.column = kwargs['column']

		self.widget_frame = Frame(self.parent)
		self.label = Label(self.widget_frame, text=self.text, \
			width=self.width, bg=self.label_bg, fg=self.label_fg, \
			font=('Verdana', 11), height=2)

		self.label.grid(row=0, column=1)
		self.widget_frame.grid(row=self.row, column=self.column, pady=(0, 1))

		self.set_hover()