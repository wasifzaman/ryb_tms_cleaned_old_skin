from tkinter import *
from tkinter.scrolledtext import ScrolledText

from textbox import Textbox


class LongTextbox(Textbox):

	def config(self, **kwargs):
		if 'height' in kwargs:
			self.entry.config(height=kwargs['height'])
		if 'width' in kwargs:
			self.entry.config(width=kwargs['width'])
		if 'text' in kwargs:	
			self.entry.insert(END, kwargs['text'])
		if 'lang' in kwargs:
			pass
			#self.lang = kwargs['lang']
			#self.label.config(text=self.lang[self.text])
		if 'bg' in kwargs:
			self.widget_frame.config(bg=kwargs['bg'])
			self.label.config(bg=kwargs['bg'])
		
	def place(self, **kwargs):
		self.parent = kwargs['parent']
		self.row = kwargs['row']
		self.column = kwargs['column']

		self.widget_frame = Frame(self.parent)
		self.entry_container = Frame(self.widget_frame, bg='#000000')
		self.label = Label(self.widget_frame, text=self.text)
		self.entry = ScrolledText(self.entry_container, relief=FLAT)

		self.widget_frame.grid(row=self.row, column=self.column, pady=(1, 0))
		self.label.pack(side=LEFT)
		self.entry_container.pack(side=LEFT)
		self.entry.pack(padx=1, pady=1)

	def getData(self):
		return self.entry.get('1.0', END + '-1c')

	def setData(self, data):
		self.entry.delete('1.0', END)
		self.config(text=data)