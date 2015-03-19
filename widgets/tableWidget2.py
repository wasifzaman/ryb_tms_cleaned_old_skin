from tkinter import *


class Cell:

	def __init__(self, **kwargs):
		self.text = kwargs['text']
		self.pos = kwargs['pos']
		self.bgcolor = 'white'
		self.altbgcolor = 'white'
	
	def config(self, **kwargs):
		if 'width' in kwargs:
			self.label.config(width=kwargs['width'])
		if 'text' in kwargs:
			self.label.config(text=kwargs['text'])
		if 'bgcolor' in kwargs:
			self.bgcolor = kwargs['bgcolor']
			self.label.config(bg=self.bgcolor)
		if 'bind' in kwargs:
			event = kwargs['bind'][0]
			command = kwargs['bind'][1]
			self.label.bind(event, command)
		
	def getData(self):
		return self.label.cget('text')
		
	def place(self, **kwargs):
		self.parent = kwargs['parent']
		self.label = Label(self.parent, text=self.text, bg=self.bgcolor)

		self.label.grid(row=self.pos[0], column=self.pos[1], sticky=E+W)


class Table:

	def __init__(self, **kwargs):
		self.repr = kwargs['repr']
		self.cells = {}
		self.data = {}
		self.clast = False

	def config(self, **kwargs):
		if 'lang' in kwargs:
			pass
			'''
			for cell_id, cell_val in self.cells.items():
				if cell_id[0] == 0:
					cur_text = cell_val.label.cget('text')
					if cur_text in kwargs['lang']:
						cell_val.label.config(text=lang[cur_text])
			'''
		if 'header_color' in kwargs:
			return

	def set_width(self, start_column, end_column, width):
		for column in range(start_column, end_column + 1):
			row = 0 if not hasattr(self, 'headers') or len(self.data) == 0 else 1
			self.cells[(row, column)].label.config(width=width)
		
	def place(self, **kwargs):
		self.parent = kwargs['parent']
		self.row = kwargs['row']
		self.column = kwargs['column']

		self.widget_frame = Frame(self.parent)
		self.canvas = Canvas(self.widget_frame, bg='white')
		self.table_frame = Frame(self.canvas, bg='lightgrey')

		self.xscrollbar = Scrollbar(self.widget_frame, orient="horizontal", command=self.canvas.xview)
		self.yscrollbar = Scrollbar(self.widget_frame, orient="vertical", command=self.canvas.yview)
		self.canvas.create_window((0,0), window=self.table_frame, anchor=NW, tags="table_frame")
		
		for cell_id, cell in self.cells.items():
			cell.place(parent=self.table_frame, pos=cell.pos)
			if cell_id[0] == 0:
				cell.label.grid(padx=(0, 1), pady=(1, 0))
			elif cell_id[1] == 0:
				cell.label.grid(padx=1, pady=(0, 1))	

		self.widget_frame.grid(row=0, column=0)
		self.canvas.grid(row=0, column=0)
		self.yscrollbar.grid(row=0, column=1, sticky=NS)
		self.xscrollbar.grid(row=1, column=0, sticky=EW)
		
		self.widget_frame.bind("<Configure>", self.makeScroll)

		'''
		** for custom scroll bar **
		self.scroll_up_button = Button(self.parent, text='Up')
		self.scroll_down_button = Button(self.parent, text='Down')
		self.scroll_up_button.grid(row=0, column=1)
		self.scroll_down_button.grid(row=0, column=2)
		self.scroll_down_button.config(command=lambda: self.canvas.yview_scroll(1, UNITS))
		self.scroll_up_button.config(command=lambda: self.canvas.yview_scroll(-1, UNITS))
		'''
	
	def setData(self, **kwargs):
		olddata = self.data
		newdata = kwargs['data']

		if newdata == [[]]: return

		#delete extra cells
		last_row = len(newdata)
		for row in range(last_row, len(olddata) + 1):
			for col in range(0, len(self.headers) + 1):
				self.cells[(row, col)].label.grid_forget()
				del self.cells[(row, col)]

		row, col = 1, 1
		for row_ in newdata:
			for text in row_:
				if (row, col) not in self.cells:
					self.cells[(row, col)] = Cell(text=text, pos=(row, col))
					self.cells[(row, col)].place(parent=self.table_frame)
					self.cells[(row, col)].label.grid(padx=(0, 1), pady=(0, 1))
				else:
					self.cells[(row, col)].label.config(text=text)
					self.cells[(row, col)].label.grid(padx=(0, 1), pady=(0, 1))
				col += 1

			#numbering
			self.cells[(row, 0)] = Cell(text=row, pos=(row, 0))
			self.cells[(row, 0)].place(parent=self.table_frame)
			self.cells[(row, 0)].label.grid(padx=1, pady=(0, 1))
			row += 1
			col = 1

		self.data = newdata

		if 'headers' in kwargs:
			self.headers = kwargs['headers']
			row, col = 0, 1
			for data in self.headers:
				self.cells[(row, col)] = Cell(text=data, pos=(row, col))
				self.cells[(row, col)].place(parent=self.table_frame, \
													pos=self.cells[(row, col)].pos)
				self.cells[(row, col)].label.grid(padx=(0, 1), pady=1)
				col += 1

		self.corner_cell = Label(self.table_frame, text='', bg='white', width=3)
		self.corner_cell.grid(row=0, column=0, padx=1, pady=1, sticky=E+W)

		self.table_frame.update_idletasks()
		self.canvas.config(scrollregion=self.canvas.bbox(ALL))
		self.canvas.config(xscrollcommand=self.xscrollbar.set)
		self.canvas.config(yscrollcommand=self.yscrollbar.set)

	def makeScroll(self, event):
		self.canvas.config(scrollregion=self.canvas.bbox(ALL))

	def getData(self):
		return self.headers, self.data

	def remove_headers_numbers(self):
		for cell_id, cell_val in self.cells.items():
			if cell_id[0] == 1:
				cell_val.label.grid(pady=1)
			if cell_id[1] == 1:
				cell_val.label.grid(padx=1)
			if cell_id[0] == 0 or cell_id[1] == 0:
				cell_val.label.grid_forget()
		self.corner_cell.grid_forget()

	'''
	** rewrite **
	def edit(self, pos):
		if not self.editwidget: return

		row = pos[0]
		col = pos[1]
		
		if row == 0 or col == 0: return

		def kill(event):
			self.data[row-1][col-1] = self.temp.get()
			self.update(data=self.data, headers=self.headers)
			self.temp.destroy()

		stringvar = StringVar()
		stringvar.set(self.cells[pos].getData())

		self.temp = Entry(self.innerframe,
			textvariable=stringvar,
			width=self.column_width_of[pos[1]])
		self.temp.grid(row=pos[0], column=pos[1])
		self.temp.focus_set()
		self.temp.grab_set()
		self.temp.bind("<Return>", kill)
	'''