from tkinter import *

class Toggle_option:

	def __init__(self, **kwargs):
		self.repr = None
		self.options = kwargs['options']
		self.stringvar = StringVar()
		self.stringvar.set(self.options[0][1])
		self.labels = []
		self.current_label = None

	def set_up_single_option(self, option):
		def set_(event):
			self.stringvar.set(option['value'])
			if hasattr(self, 'active_bg'):
				self.current_label.config(bg=self.inactive_bg)
				option['label'].config(bg=self.active_bg)
			self.current_label = option['label']

		option = {
			'label': Radiobutton(self.widget_frame, text=option[0],
									variable=self.stringvar, value=option[1]),
			'value': option[1]
		}

		option['label'].bind('<Button-1>', set_)
		option['label'].pack(side=LEFT)
		self.labels.append(option['label'])

	def place(self, **kwargs):
		self.widget_frame = Frame(kwargs['parent'])

		for option in self.options:
			self.set_up_single_option(option)

		self.current_label = self.labels[0]
		self.widget_frame.grid(row=kwargs['row'], column=kwargs['column'])

	def config(self, **kwargs):
		if 'inactive_bg' in kwargs:
			self.inactive_bg = kwargs['inactive_bg']
			for label in self.labels:
				label.config(bg=self.inactive_bg)
		if 'active_bg' in kwargs:
			self.active_bg = kwargs['active_bg']
			self.labels[0].config(bg=self.active_bg)
		if 'width' in kwargs:
			for label in self.labels:
				label.config(width=kwargs['width'])
		if 'height' in kwargs:
			for label in self.labels:
				label.config(height=kwargs['height'])
		if 'fg' in kwargs:
			for label in self.labels:
				label.config(fg=kwargs['fg'])
		if 'set_' in kwargs:
			self.current_label.config(bg=self.inactive_bg)
			self.current_label = self.labels[kwargs['set_']]
			if hasattr(self, 'active_bg'):
				self.current_label.config(bg=self.active_bg)
			label_text = self.current_label.cget('text')
			for option in self.options:
				if option[0] == label_text: self.stringvar.set(option[1])