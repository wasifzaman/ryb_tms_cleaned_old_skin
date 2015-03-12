from tkinter import *
from datetime import time, date, datetime

from textbox import IntTextbox


class Datebox(IntTextbox):

	def config(self, **kwargs):
		if 'm' in kwargs and 'd' in kwargs and 'y' in kwargs:
			m, d, y = StringVar(), StringVar(), StringVar()
			m.set(kwargs['m'])
			d.set(kwargs['d'])
			y.set(kwargs['y'])
			self.mEntry.config(textvariable=m)
			self.dEntry.config(textvariable=d)
			self.yEntry.config(textvariable=y)
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
		self.mdy_frame = Frame(self.widget_frame, relief=FLAT)#, bg='#ADD6FF')
		self.mdy_container = Frame(self.mdy_frame, relief=FLAT, bg='#000000')
		self.label = Label(self.widget_frame, text=self.text, width=12, anchor=W)
		self.dLabel = Entry(self.mdy_container, relief=FLAT, width=1, disabledbackground='white', disabledforeground='black')
		self.yLable = Entry(self.mdy_container, relief=FLAT, width=1, disabledbackground='white', disabledforeground='black')
		self.mEntry = Entry(self.mdy_container, relief=FLAT, width=4, justify=CENTER)
		self.dEntry = Entry(self.mdy_container, relief=FLAT, width=4, justify=CENTER)
		self.yEntry = Entry(self.mdy_container, relief=FLAT, width=8, justify=CENTER)

		self.dLabel.insert(0, '/')
		self.dLabel.config(state=DISABLED)
		self.yLable.insert(0, '/')
		self.yLable.config(state=DISABLED)

		self.widget_frame.grid(row=self.row, column=self.column, stick=E+W, pady=(1, 0))
		self.label.pack(side=LEFT)
		self.mdy_frame.pack(padx=1, pady=1, fill=X, side=LEFT)
		self.mdy_container.pack(side=LEFT)
		self.mEntry.pack(side=LEFT, padx=(1, 0), pady=1)
		self.dLabel.pack(side=LEFT)
		self.dEntry.pack(side=LEFT)
		self.yLable.pack(side=LEFT)
		self.yEntry.pack(side=LEFT, padx=(0, 1))

		self.bind()

	def OnValidate(self, d, i, P, s, S, v, V, W, digit_type):
		if d == '0': return True
		if not S.isdigit(): return False
		if digit_type == 'date' or digit_type == 'month':
			if len(s) == 2: return False
		elif digit_type == 'year':
			if len(s) == 4: return False
		return True

	def bind(self):
		self.mEntry.config(validate="all", validatecommand=(self.parent.register(self.OnValidate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W', 'date'))
		self.dEntry.config(validate="all", validatecommand=(self.parent.register(self.OnValidate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W', 'month'))
		self.yEntry.config(validate="all", validatecommand=(self.parent.register(self.OnValidate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W', 'year'))

	def getData(self):
		try:
			date = self.mEntry.get() + '/' + self.dEntry.get() + '/' + self.yEntry.get()
			dt = datetime.strptime(date, '%m/%d/%Y')
			return datetime.strftime(dt, '%m/%d/%Y')
		except ValueError:
			return '01/01/1900'

	def setData(self, data):
		date = data.split('/')
		m, d, y = date[0], date[1], date[2]

		self.config(m=m, d=d, y=y)
