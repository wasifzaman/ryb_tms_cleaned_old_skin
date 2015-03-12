import sys, os
sys.path.append(os.path.abspath(os.pardir) + '\widgets')
sys.path.append(os.path.abspath(os.pardir) + '\database')
sys.path.append(os.path.abspath(os.pardir) + '\miscellaneous')
sys.path.append(os.path.abspath(os.pardir) + '\messages windows')
images = os.path.abspath(os.pardir) + '\images\\' #image directory

from uiHandler22 import AppWindow
from master_list import *
from student_picker import multiple_match
from textbox import Textbox, TextboxNoEdit
from button import Buttonbox
from simple_label import Labelbox
from date_textbox import Datebox
from multiline_textbox import LongTextbox
from toggle_option import Toggle_option
from tableWidget2 import Table
from translations import english_to_chinese, chinese_to_english
from translate_ import translate


def main(parent_frame, lang, database):
	database.loadData()

	window_ = AppWindow(parent_frame)

	window_.newFrame("Search Frame", (0, 0))
	window_.newFrame("General Info Frame", (1, 0))
	window_.newFrame("Notes Frame", (2, 0))
	window_.newFrame("Button Frame", (3, 0))
	window_.newFrame("Table Frame", (1, 1))

	window_.frames["Search Frame"].grid(columnspan=2)
	window_.frames["Button Frame"].grid(columnspan=2)
	window_.frames["Table Frame"].grid(rowspan=2)

	attendance_table = Table(repr='attinfox', edit=True)
	attendance_table_headers = ['Date', 'Check-in time', 'Start time', 'Check-out time', 'Confirm time']
	search_value = Textbox(text="Search", repr=None)
	search_options = Toggle_option(
		options=(('Barcode', 'bCode'),('First name', 'firstName'), \
		('Last name', 'lastName'), ('Chinese name', 'chineseName'), \
		('Phone number', 'phoneNumber')), repr=None)
	general_header = Labelbox(text='General', lang=lang, repr='sinfo')
	notes_header = Labelbox(text='Notes', lang=lang, repr='ninfo')
	first_name = Textbox(text="First name", lang=lang, repr='firstName')
	last_name = Textbox(text="Last name", lang=lang, repr='lastName')
	chinese_name = Textbox(text="Chinese name", lang=lang, repr='chineseName')
	date_of_birth = Datebox(text="Date of birth", lang=lang, repr='dob')
	barcode = TextboxNoEdit(text="Barcode", lang=lang, repr='bCode')
	notes = LongTextbox(text="Notes", lang=lang, repr='notes')
	search_button = Buttonbox(text='Search', lang=lang, repr='searchbutton')
	save_button = Buttonbox(text='Save', lang=lang, repr='save_button')
	manual_entry_button = Buttonbox(text='Manual entry', repr='manualentrybutton')

	window_.frames["Search Frame"].addWidget(search_value, (0, 0))
	window_.frames["Search Frame"].addWidget(search_options, (1, 0))
	window_.frames["Search Frame"].addWidget(search_button, (2, 0))
	window_.frames["General Info Frame"].addWidget(general_header, (0, 0))
	window_.frames["General Info Frame"].addWidget(first_name, (1, 0))
	window_.frames["General Info Frame"].addWidget(last_name, (2, 0))
	window_.frames["General Info Frame"].addWidget(chinese_name, (3, 0))
	window_.frames["General Info Frame"].addWidget(date_of_birth, (4, 0))
	window_.frames["General Info Frame"].addWidget(barcode, (7, 0))
	window_.frames["Notes Frame"].addWidget(notes_header, (8, 0))
	window_.frames["Notes Frame"].addWidget(notes, (9, 0))
	window_.frames["Table Frame"].addWidget(attendance_table, (0, 0))
	window_.frames["Button Frame"].addWidget(save_button, (0, 0))
	window_.frames["Button Frame"].addWidget(manual_entry_button, (0, 1))
	#window_.frames["Fourth Frame"].addWidget(early_checkin, (0, 0))

	window_.frames["General Info Frame"].grid(padx=(0, 10), pady=10)
	window_.frames["Notes Frame"].grid(padx=(0, 10), pady=(0, 10))
	window_.frames["Table Frame"].grid(padx=(0, 10), pady=10)

	''' colors '''
	label_bg = '#4DBCE9'
	hover_bg = '#26ADE4'
	header_color = "#3B5C8D"

	#window_.frames["Search Frame"].config(bg=header_color)
	search_value.label.config(width=7, height=2)#, bg=header_color, fg='white')
	search_value.label.pack(padx=(5, 0))
	search_value.entry_container.pack(padx=(0, 10))
	#search_value.widget_frame.config(bg=header_color)
	search_value.widget_frame.grid(sticky=E, pady=0)
	#search_button.label.config(width=1)
	search_button.widget_frame.grid(pady=0, columnspan=6)
	#search_button.config(image=images + 'search.png', image_resize=(28,28),\
	#					label_bg='#FF6B6B', hover_bg='#C44D58')
	search_options.widget_frame.grid(columnspan=2)
	search_options.config(height=1, \
		inactive_bg='#FFFFFF')#width=15, active_bg='#8FBE00')
	notes.label.pack_forget()
	notes.config(height=6, width=30)
	attendance_table.canvas.config(width=695, height=300)
	general_header.widget_frame.grid(columnspan=2, sticky=EW)
	general_header.config(bg=header_color, fg='white')
	general_header.label.pack(side=LEFT)
	notes_header.widget_frame.grid(columnspan=2, sticky=EW)
	notes_header.config(bg=header_color, fg='white')
	notes_header.label.pack(side=LEFT)
	save_button.config(label_bg=label_bg, hover_bg=hover_bg, label_fg='black')
	save_button.widget_frame.grid(padx=(0, 10))
	manual_entry_button.config(label_bg=label_bg, hover_bg=hover_bg, label_fg='black')

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

		search_value.entry.delete(0, END) #reset search

		data_points = database.studentList[window_.student_id].datapoints
		window_.populate(data_points)
		window_.original_data_points = window_.collect(database.studentList[window_.student_id].datapoints)

		dt = datetime.now()
		date = datetime.strftime(dt, '%m/%d/%Y')
		time = datetime.strftime(dt, '%I:%M %p')
		timelot = database.findTimeSlot(dt)
		overwrite = False
		data = False
		for row in data_points['attinfo'][1]:
			if row[0] == date:
				data = row
				break

		if not data:
			no_checkin_today(lang)
			search_options.config(set_=0) #reset search bar
			return
		if len(data[4]) != 0:
			if confirm_overwrite_checkout(lang):
				overwrite = True
			else:
				search_options.config(set_=0) #reset search bar
				return

		confirm_status = confirm_check_out_time(lang, database)
		if confirm_status == 'manual':
			time_ = time_entry(lang)
			print(time_, type(time_))
			if not time_: return
			data[3] = time
			data[4] = time_
		elif confirm_status:
			data[3] = time
			data[4] = timelot
		else:
			search_options.config(set_=0) #reset search bar
			return

		if datetime.strptime(date + ' ' + data[4], '%m/%d/%Y %I:%M %p') < datetime.strptime(date + ' ' + data[2], '%m/%d/%Y %I:%M %p'):
			checkout_earlier_checkin(lang)
			search_options.config(set_=0) #reset search bar
			data[3] = ''
			data[4] = ''
			return

		database.saveData()
		attendance_table.setData(
			headers=attendance_table_headers,
			data=[data[:5]]) #display entry being scanned out
		search_options.config(set_=0) #reset search bar
		attendance_table.canvas.yview_moveto(1.0)
		attendance_table.set_width(1, 1, 13)
		attendance_table.set_width(2, 5, 14)

	def manual_scan():
		if (len(barcode.getData())) == 0: return

		dt = date_time_entry(lang)
		if not dt[0]: return
		date = dt[0]
		time = dt[1]
		time_entry = '' if datetime.strptime(date, '%m/%d/%Y').date() != datetime.now().date() else datetime.strftime(datetime.now(), '%I:%M %p')

		data_points = database.studentList[barcode.getData()].datapoints

		for row in data_points['attinfo'][1]:
			if row[0] == date:
				if len(row[4]) == 0 or confirm_overwrite_checkout(lang):
					if datetime.strptime(date + ' ' + time, '%m/%d/%Y %I:%M %p') < datetime.strptime(date + ' ' + row[2], '%m/%d/%Y %I:%M %p'):
						checkout_earlier_checkin(lang)
						return
					row[3] = time_entry
					row[4] = time
					database.saveData()
					attendance_table.setData(
						headers=attendance_table_headers,
						data=[[date, row[1], row[2], row[3], row[4]]])
					attendance_table.set_width(1, 1, 13)
					attendance_table.set_width(2, 5, 14)
					return

		entry_not_found(lang, date)

	def collect():
		if not altered(): return
		if not confirm_save_teacher_data(lang): return
		student = database.studentList[window_.student_id]
		student.datapoints.update(window_.collect(student.datapoints))
		window_.original_data_points = window_.collect(student.datapoints)
		database.saveData()
		
	def altered():
		current_data_points = window_.collect(window_.original_data_points)
		for key in current_data_points.keys():
			if current_data_points[key] != window_.original_data_points[key]:
				return True
		return False

	search_button.config(cmd=search_student)
	manual_entry_button.config(cmd=lambda: manual_scan())
	search_value.entry.bind("<Return>", lambda x: search_student())
	save_button.config(cmd=collect)

	if lang == 'chinese':
		translate(window_, english_to_chinese)