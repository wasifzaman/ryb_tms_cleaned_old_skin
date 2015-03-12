from tkinter import *

from textbox import Textbox


class Labelbox(Textbox):
	def __init__(self, **kwargs):
		Textbox.__init__(self, **kwargs)
		self.bold = False
		if 'bold' in kwargs: self.bold = kwargs['bold']

	def config(self, **kwargs):
		if 'text' in kwargs:
			self.text=kwargs['text']
			self.label.config(text=self.text)
		if 'lang' in kwargs:
			pass
			#self.lang = kwargs['lang']
			#self.label.config(text=self.lang[self.text])
		if 'bg' in kwargs:
			self.widget_frame.config(bg=kwargs['bg'])
			self.label.config(bg=kwargs['bg'])
		if 'fg' in kwargs:
			self.label.config(fg=kwargs['fg'])

	def getData(self):
		return self.text

	def place(self, **kwargs):
		self.parent = kwargs['parent']
		self.row = kwargs['row']
		self.column = kwargs['column']

		self.widget_frame = Frame(self.parent)
		self.label = Label(self.widget_frame, text=self.text)
		
		self.widget_frame.grid(row=self.row, column=self.column)
		self.label.pack()

	def hide(self):
		self.label.grid_forget()

	def show(self):
		self.label.grid()