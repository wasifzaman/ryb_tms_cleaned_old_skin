import sys, os
images = os.path.abspath(os.pardir) + '\images\\' #image directory

from tkinter import *
import os.path
from PIL import Image, ImageTk


class AppFrame(Frame):

	def __init__(self, parent, *args, **kwargs):
		Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.curRow = 0
		self.curColumn = 0
		self.widgets = {}

	def addWidget(self, widget, pos):
		self.widgets[widget.repr] = widget
		self.widgets[widget.repr].place(parent=self, row=pos[0], column=pos[1])


class AppWindow(Frame):

	def __init__(self, parent, *args, **kwargs):
		Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		self.oframe = Frame(self)
		self.mainFrame = Frame(self.oframe, bg='white')
		self.oframe.pack(fill="both", expand=True)
		self.mainFrame.place(in_=self.oframe, anchor="c", relx=.5, rely=.5)

		self.option_add("*Frame.Background", "white")
		self.option_add("*Label.Background", "white")
		self.option_add("*Font", "Verdana 11")

		self.pack(side=LEFT)
		self.oframe.grid()
		self.mainFrame.grid()
		
		self.frames = {}
		self.framePadding = (1, 1)

	def newFrame(self, frameName, gridpos=(0,0)):
		self.frames[frameName] = AppFrame(self.mainFrame)

		self.frames[frameName].grid(
			row=gridpos[0], column=gridpos[1], sticky=N)
			#padx=self.framePadding[0], pady=self.framePadding[1], sticky=N)

	def collect(self, keys):
		collected_data = {}

		for frame in self.frames.values():
			for widget in frame.widgets.values():
				if widget.repr in keys:
					collected_data[widget.repr] = widget.getData()

		return collected_data

	def populate(self, data):
		for frame in self.frames.values():
			for widget in frame.widgets.values():
				if widget.repr in data:
					widget.setData(data[widget.repr])

	def dw(self):
		self.destroy()
		

class Window(Tk):

	def __init__(self, top=False, *args, **kwargs):
		if top: Toplevel.__init__(self, *args, **kwargs)
		else: Tk.__init__(self, *args, **kwargs)
		
		self.attributes('-fullscreen', True)

		self.pic = Image.open(images + 'bigbl.jpg')
		self.img = ImageTk.PhotoImage(self.pic)
		self.oframe = Frame(self)
		Label(self.oframe, image=self.img).place(x=-2, y=-5, in_=self.oframe)
		self.mainFrame = Frame(self.oframe)#, bd=1, bg='lightgrey')
		self.titleFrame = Frame(self.mainFrame, height=60)
		self.titleFrame.pack(fill=X)
		self.wintitle = Label(self.titleFrame, fg='white', font=('Arial', 15, 'bold'))

		self.wintitle.place(in_=self.titleFrame, anchor="c", relx=.5, rely=.5)
		self.oframe.pack(fill="both", expand=True)#, padx=20, pady=20)
		self.mainFrame.place(in_=self.oframe, anchor="c", relx=.5, rely=.5)

		self.update_idletasks()
		self.after_idle(lambda: self.minsize(self.winfo_width(), self.winfo_height()))