from tkinter import *

from textbox import Textbox


class Picker(Textbox):
	def __init__(self, **kwargs):
		self.repr = kwargs['repr']
		self.text = kwargs['text']
		self.rads = kwargs['rads']

	def config(self, **kwargs):
		self.lang = kwargs['lang']
		self.label.config(text=self.lang[self.text])
		i = 0
		for rad in self.brads:
			rad.config(text=self.lang[self.rads[i][0]])
			i += 1

	def place(self, **kwargs):

		self.parent = kwargs['parent']
		self.row = kwargs['row']
		self.column = kwargs['column']

		self.selfframe = Frame(self.parent)
		self.label = Label(self.selfframe, text=self.text)
		self.entry = Entry(self.selfframe, relief=SOLID)

		self.b, r = StringVar(), []
		self.b.set(self.rads[0][1])
		for rad in self.rads:
			r.append(Radiobutton(self.selfframe, text=rad[0], variable=self.b, \
				value=rad[1], indicatoron=10))#, offrelief=GROOVE, overrelief=SOLID))

		self.brads = r

		self.selfframe.grid()
		self.label.pack()
		self.entry.pack()
		for rad in self.brads:
			rad.pack(side=LEFT)

	def getData(self):
		return self.b.get(), self.entry.get()