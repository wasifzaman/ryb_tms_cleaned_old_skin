import sys, os
sys.path.append(os.path.abspath(os.pardir) + '\widgets')
sys.path.append(os.path.abspath(os.pardir) + '\database')
sys.path.append(os.path.abspath(os.pardir) + '\miscellaneous')
sys.path.append(os.path.abspath(os.pardir) + '\messages windows')
images = os.path.abspath(os.pardir) + '\images\\' #image directory

from uiHandler22 import AppWindow
from master_list import *
from student_picker import multiple_match
from textbox import Textbox
from button import Buttonbox
from toggle_option import Toggle_option
from tableWidget2 import Table
import edit_salary
from translations import english_to_chinese, chinese_to_english
from translate_ import translate


def main(parent_frame, lang, database, markerfile):
	database.loadData()

	if os.path.isfile(markerfile):
		print('found', markerfile)
	else:
		markerfile = False
		print('not found', markerfile)

	window_ = AppWindow(parent_frame)

	window_.newFrame("Search Frame", (0, 0))
	window_.newFrame("Table Frame", (1, 0))
	window_.newFrame("Button Frame", (2, 0))

	teacher_table = Table(repr='teachertable')
	teacher_table_headers = ['Barcode', 'First name', 'Last name', 'Chinese name', 'Date of birth']
	search_value = Textbox(text="Search", repr=None)
	search_options = Toggle_option(
		options=(('Barcode', 'bCode'),('First name', 'firstName'), \
		('Last name', 'lastName'), ('Chinese name', 'chineseName'), \
		('Phone number', 'phoneNumber')), repr=None)
	search_button = Buttonbox(text='Search', lang=lang, repr='searchbutton')
	first_page_button = Buttonbox(text='<<', repr='fpagebutton')
	next_page_button = Buttonbox(text='>', lang=lang, repr='>>')
	previous_page_button = Buttonbox(text='<', lang=lang, repr='<<')
	last_page_button = Buttonbox(text='>>', lang=lang, repr='>>>')

	window_.frames["Search Frame"].addWidget(search_value, (0, 0))
	window_.frames["Search Frame"].addWidget(search_options, (1, 0))
	window_.frames["Search Frame"].addWidget(search_button, (2, 0))
	window_.frames["Button Frame"].addWidget(first_page_button, (0, 0))
	window_.frames["Button Frame"].addWidget(previous_page_button, (0, 1))
	window_.frames["Button Frame"].addWidget(next_page_button, (0, 2))
	window_.frames["Button Frame"].addWidget(last_page_button, (0, 3))
	window_.frames["Table Frame"].addWidget(teacher_table, (0, 0))

	''' colors '''
	label_bg = '#4DBCE9'
	hover_bg = '#26ADE4'
	header_color = "#26ADE4"

	#window_.frames["Search Frame"].config(bg=header_color)
	search_value.label.config(width=7, height=2)#, bg=header_color, fg='white')
	search_value.label.pack(padx=(5, 0))
	search_value.entry_container.pack(padx=(0, 10))
	#search_value.widget_frame.config(bg=header_color)
	search_value.widget_frame.grid(sticky=E, pady=0)
	#search_button.label.config(width=1)
	search_button.widget_frame.grid(pady=0, columnspan=6)
	#search_button.config(image=images + 'search.png', image_resize=(28,28),\
	#					label_bg='#FF6B6B', hover_bg='#C44D58', label_fg='black')
	search_options.widget_frame.grid(columnspan=2)
	search_options.config(height=1, \
		inactive_bg='#FFFFFF')#width=15, active_bg='#8FBE00')
	first_page_button.config(label_bg=label_bg, hover_bg=hover_bg, width=5)
	previous_page_button.config(label_bg=label_bg, hover_bg=hover_bg, width=5)
	next_page_button.config(label_bg=label_bg, hover_bg=hover_bg, width=5)
	last_page_button.config(label_bg=label_bg, hover_bg=hover_bg, width=5)
	first_page_button.label.grid(padx=1)
	previous_page_button.label.grid(padx=(0, 1))
	next_page_button.label.grid(padx=(0, 1))
	last_page_button.label.grid(padx=(0, 1))

	teacher_list = [[]]
	for teacher in database.studentList.values():
		data_points = teacher.datapoints
		teacher_list[0].append([
			data_points['bCode'],
			data_points['firstName'],
			data_points['lastName'],
			data_points['chineseName'],
			data_points['dob']])

	teacher_list[0].sort()

	teacher_on_page = []
	for teacher in teacher_list[0]:
		teacher_on_page.append(teacher)
		if len(teacher_on_page) >= 15:
			teacher_list.append(teacher_on_page)
			teacher_on_page = []
	teacher_list.append(teacher_on_page)

	if len(teacher_list[-1]) == 0 and len(teacher_list) != 1: teacher_list.pop()

	window_.pNum = 1

	def toPage(to):
		if to == 'next':
			if window_.pNum == len(teacher_list) - 1: return
			window_.pNum = window_.pNum + 1
		elif to == 'previous':
			if window_.pNum == 1: return
			window_.pNum = window_.pNum - 1
		elif to == 'last':
			window_.pNum = len(teacher_list) - 1
		elif to == 'first':
			window_.pNum = 1

		teacher_table.setData(headers=teacher_table_headers,
			data=teacher_list[window_.pNum] if len(teacher_list[0]) >= 1 else [])
		teacher_table.canvas.config(width=700, height=350)
		teacher_table.set_width(1, 5, 14)
		def open_edit_window(pos):
			student_id = teacher_table.data[pos[0]-1][0]
			edit_salary.start_window(lang, database, markerfile=markerfile, student_id=student_id)
		for pos, cell in teacher_table.cells.items():
			if pos[0] == 0: continue
			cell.config(bind=('<Double-Button-1>', lambda event, pos=pos: open_edit_window(pos)))

	if len(teacher_list[0]) > 15:
		toPage(1)
		first_page_button.config(cmd=lambda: toPage('first'))
		next_page_button.config(cmd=lambda: toPage('next'))
		previous_page_button.config(cmd=lambda: toPage('previous'))
		last_page_button.config(cmd=lambda: toPage('last'))

	toPage('first')

	def search_student():
		window_.student_id = search_value.getData()

		if len(window_.student_id) == 0: return
		if search_options.stringvar.get() == 'bCode' and window_.student_id not in database.studentList:
			student_does_not_exist(lang)
			return

		if search_options.stringvar.get() != 'bCode':
			scan_type = search_options.stringvar.get()
			scan_value = search_value.getData()
			student_list = []

			for student in database.studentList:
				matched_student_data_points = False
				if scan_type == 'phoneNumber':
					if database.studentList[student].datapoints['hPhone'] == scan_value or \
						database.studentList[student].datapoints['cPhone'] == scan_value or \
						database.studentList[student].datapoints['cPhone2'] == scan_value:
						matched_student_data_points = database.studentList[student].datapoints
				elif database.studentList[student].datapoints[scan_type] == scan_value:
					matched_student_data_points = database.studentList[student].datapoints
				
				if matched_student_data_points:
					student_list.append([
						matched_student_data_points['bCode'],
						matched_student_data_points['firstName'],
						matched_student_data_points['lastName'],
						matched_student_data_points['chineseName']])

			if len(student_list) == 0:
				student_does_not_exist(lang)
				return

			if len(student_list) > 1:
				student_list.sort()
				window_.student_id = multiple_match(student_list)
				if not window_.student_id: return
			else:
				window_.student_id = student_list[0][0]

		edit_salary.start_window(lang, database=database, student_id=window_.student_id, markerfile=markerfile)
		search_options.config(set_=0)
		search_value.entry.delete(0, END) #reset search

	search_value.entry.bind("<Return>", lambda event: search_student())
	search_button.config(cmd=search_student)