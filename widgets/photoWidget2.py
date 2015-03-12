from tkinter import Label, N
from PIL import Image, ImageTk


class Photo:

	def __init__(self, **kwargs):
		self.repr = kwargs['repr']
		self.path = kwargs['path']

	def config(self, **kwargs):
		if 'path' in kwargs:
			self.path = kwargs['path']
			self.picture = Image.open(self.path)
			self.picture = self.picture.resize((200, 200), Image.ANTIALIAS)
			self.image = ImageTk.PhotoImage(self.picture)
			self.label.config(image=self.image)

	def place(self, **kwargs):
		self.parent = kwargs['parent']
		self.row = kwargs['row']
		self.column = kwargs['column']

		self.picture = Image.open(self.path)
		self.image = ImageTk.PhotoImage(self.picture)

		self.label = Label(self.parent, image=self.image)
		self.label.grid(row=self.row, column=self.column)
		self.label.bind('<Button-1>', lambda e: self.label.focus_set())

	def getData(self):
		return self.path

	def setData(self, data):
		#le sigh
		if data == '' or 'N/A': return
		self.config(path=data)

	def hide(self):
		self.label.grid_forget()