import sys, os
sys.path.append(os.path.abspath(os.pardir) + '\database')
sys.path.append(os.path.abspath(os.pardir) + '\widgets')
sys.path.append(os.path.abspath(os.pardir) + '\miscellaneous')
sys.path.append(os.path.abspath(os.pardir) + '\messages windows')

import pickle

from textbox import Textbox, TextboxNoEdit, IntTextbox, MoneyTextbox
from button import Buttonbox
from simple_label import Labelbox
from date_textbox import Datebox
from multiline_textbox import LongTextbox
from tableWidget2 import Table
from uiHandler22 import Window, AppWindow
from translations import english_to_chinese
from translate_ import translate
from master_list import *
import print_reports


def start_window(lang, database, student_id, markerfile=False):
	database.loadData()

	top_window_ = Window(top=True)
	top_window_.attributes('-fullscreen', False)
	top_window_.geometry('1280x720')
	top_window_.resizable(0, 0)
	top_window_.grab_set()
	top_window_.focus_set()
	top_window_.titleFrame.pack_forget()

	window_ = AppWindow(top_window_.mainFrame)
	window_.lang = lang
	window_.picked = {}

	marker = pickle.load(open(markerfile, "rb")) if markerfile else False

	window_.newFrame("First Frame", (0, 0))
	window_.newFrame("Button Frame", (1, 0))
	window_.newFrame("Table Frame", (0, 1))

	window_.frames["Table Frame"].grid(rowspan=2, sticky=N)
	#window_.frames["Table Frame"].columnconfigure(0, weight=5, minsize=720)

	today = TextboxNoEdit(text="Today's date", lang=window_.lang, repr='today_date')
	last_payment = TextboxNoEdit(text="Last payment", lang=window_.lang, repr='last_pay_date')
	pay_per_hour = TextboxNoEdit(text="Pay/hour", lang=window_.lang, repr='pay_per_hour')
	general_header = Labelbox(text='Student information', lang=lang, repr='general_header')
	firstName_noedit = TextboxNoEdit(text="First name", lang=lang, repr='firstName')
	lastName_noedit = TextboxNoEdit(text="Last name", lang=lang, repr='lastName')
	chineseName_noedit = TextboxNoEdit(text="Chinese name", lang=lang, repr='chineseName')
	max_hours = IntTextbox(text="Max hours", lang=window_.lang, repr='max_hours')
	b_print_to_file = Buttonbox(text='Print to file', lang=window_.lang, repr='print_to_file')
	close_button = Buttonbox(text='Close', lang=window_.lang, repr='close_button')
	notes_header = Labelbox(text='Notes', lang=None, repr='notes_header')
	notes = LongTextbox(text="Notes", lang=lang, repr='notes')
	attendance_table = Table(repr='attinfox', edit=True)
	attendance_table_headers = ['Date', 'Check-In Time', 'Start Time', 'Check-Out Time', 'Confirm Time']
	#b_reset_checkin = Buttonbox(text='resetcheckin', lang=lang, repr='bresetcheckin')

	window_.frames["First Frame"].addWidget(today, (0, 0))
	window_.frames["First Frame"].addWidget(last_payment, (1, 0))
	window_.frames["First Frame"].addWidget(pay_per_hour, (2, 0))
	window_.frames["First Frame"].addWidget(general_header, (4, 0))
	window_.frames["First Frame"].addWidget(firstName_noedit, (5, 0))
	window_.frames["First Frame"].addWidget(lastName_noedit, (6, 0))
	window_.frames["First Frame"].addWidget(chineseName_noedit, (7, 0))
	window_.frames["First Frame"].addWidget(notes_header, (8, 0))
	window_.frames["First Frame"].addWidget(notes, (9, 0))
	window_.frames["Button Frame"].addWidget(b_print_to_file, (0, 0))
	window_.frames["Button Frame"].addWidget(close_button, (1, 0))
	window_.frames["Table Frame"].addWidget(attendance_table, (0, 0))
	window_.frames["Table Frame"].grid(rowspan=3, sticky=W)
	
	''' colors '''
	label_bg = '#4DBCE9'
	hover_bg = '#26ADE4'
	header_color = "#3B5C8D"
	
	'''
	widget settings
	must be placed after widget has been added
	'''
	general_header.widget_frame.grid(columnspan=2, sticky=EW, pady=(10, 0))
	general_header.config(bg=header_color, fg='white')
	general_header.label.pack(side=LEFT)
	notes_header.widget_frame.grid(columnspan=2, sticky=EW, pady=(10, 0))
	notes_header.config(bg=header_color, fg='white')
	notes_header.label.pack(side=LEFT)
	today.config(text=str(datetime.strftime(datetime.now().date(), '%m/%d/%Y')))
	notes.label.pack_forget()
	notes.config(height=8, width=30)
	attendance_table.canvas.config(width=720, height=500)
	window_.frames["First Frame"].grid(padx=10, pady=10)
	window_.frames["Table Frame"].grid(padx=10, pady=10)	
	if database.studentList[student_id].datapoints['last_payment']:
		last_payment.config(text=datetime.strftime(database.studentList[student_id].datapoints['last_payment'], '%m/%d/%Y'))

	data_points = database.studentList[student_id].datapoints
	window_.populate(data_points)
	attendance_table.setData(
		headers=attendance_table_headers,
		data=[row[:5] for row in data_points['attinfo'][1]])
	attendance_table.set_width(1, 1, 13)
	attendance_table.set_width(2, 5, 14)

	def pick_cell(p, student_id):
		first_cell = attendance_table.cells[p]
		if p[0] == 0: return
		if marker and first_cell.bgcolor in marker[student_id]['color_set']:
			print('already printed')
			pickRow(p, True)
			window_.picked[p[0]] = attendance_table.data[p[0]-1]
		elif first_cell.bgcolor == first_cell.altbgcolor:
			print('picked!')
			pickRow(p)
			window_.picked[p[0]] = attendance_table.data[p[0]-1]
			print(window_.picked)
		else:
			print('unpicked!')
			unpickRow(p)
			del window_.picked[p[0]]
			print(window_.picked)

	for pos, cell in attendance_table.cells.items():
		cell.config(bind=('<Button-1>', lambda event, pos=pos: pick_cell(pos, student_id)))
		if marker and (pos[0] in marker[student_id]['paid_set']):
			cell.config(bgcolor=marker[student_id]['row_color'][pos[0]])

	def pickRow(entry, printed=False):
		x, y = entry[0], entry[1]
		for cell in attendance_table.cells.values():
			if cell.pos[0] == x:
				cell.altbgcolor = cell.bgcolor
				if not printed:
					cell.config(bgcolor='lightblue')
				else:
					cell.config(bgcolor='pink')

	def unpickRow(entry):
		x, y = entry[0], entry[1]
		for cell in attendance_table.cells.values():
			if cell.pos[0] == x:
				cell.config(bgcolor=cell.altbgcolor)

	def print_to_file():
		if not confirm_print(window_.lang): return
		file_path = filedialog.askdirectory()
		today = datetime.now()
		date = today.strftime('%m.%d.%y')
		time = today.strftime('%I.%M.%p')
		file_name = file_path + '/Salary Report ' + database.school + ' ' + date + ' ' + time + '.xlsx'
		printed = print_reports.print_pay_entries(database, file_name, student_id, window_.picked, pay_per_hour.getData(), False) #false is for max_hours
		if markerfile:
			if student_id not in marker:
				marker[student_id] = {}
				marker[student_id]['paid_set'] = window_.picked
				marker[student_id]['color_set'] = ['tomato', 'cornflowerblue']
				marker[student_id]['current_color'] = 0
				marker[student_id]['row_color'] = {}
				for row_num in window_.picked:
					marker[student_id]['row_color'][row_num] = marker[student_id]['color_set'][marker[student_id]['current_color']]
			else:
				print(student_id, ' in marker file, appending..')
				marker[student_id]['current_color'] = (marker[student_id]['current_color'] + 1) % len(marker[student_id]['color_set'])
				print(marker[student_id]['current_color'])
				for row_num in window_.picked:
					marker[student_id]['row_color'][row_num] = marker[student_id]['color_set'][marker[student_id]['current_color']]
				marker[student_id]['paid_set'].update(window_.picked)
			print(marker)
			pickle.dump(marker, open(markerfile, "wb"))
		if printed:
			print_succesful(window_.lang)
			top_window_.destroy()

	for frame in window_.frames.values():
		for widget in frame.widgets.values():
			widget.config(lang=window_.lang)

	b_print_to_file.config(cmd=print_to_file)
	close_button.config(cmd=top_window_.destroy)
	
	top_window_.mainloop()