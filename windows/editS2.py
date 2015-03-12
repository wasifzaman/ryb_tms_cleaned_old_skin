import sys, os
sys.path.append(os.path.abspath(os.pardir) + '\widgets')
sys.path.append(os.path.abspath(os.pardir) + '\database')
sys.path.append(os.path.abspath(os.pardir) + '\miscellaneous')
sys.path.append(os.path.abspath(os.pardir) + '\messages windows')

from uiHandler22 import Window, AppWindow
from textbox import Textbox, TextboxNoEdit, IntTextbox, MoneyTextbox
from button import Buttonbox
from simple_label import Labelbox
from date_textbox import Datebox
from photoWidget2 import Photo
from multiline_textbox import LongTextbox
from translations import english_to_chinese
from translate_ import translate
from tableWidget2 import Table
from student import StudentInfo
from master_list import *

def main(lang, database, i=0):
	database.loadData()

	top_window_ = Window(top=True)
	top_window_.attributes('-fullscreen', False)
	top_window_.geometry('1280x740+1+1')
	top_window_.resizable(0, 0)
	top_window_.grab_set()
	top_window_.focus_set()
	top_window_.titleFrame.config(height=1)
	top_window_.wintitle.place_forget()

	window_main = AppWindow(top_window_.mainFrame)
	window_1 = AppWindow(top_window_.mainFrame)
	window_2 = AppWindow(top_window_.mainFrame)

	window_main.pack(anchor=N)
	window_2.pack_forget()

	window_1.newFrame("Image Frame", (0, 0))
	window_1.newFrame("General Info Frame", (0, 1))
	window_1.newFrame("Contact Frame", (0, 2))
	window_1.newFrame("Notes Frame", (1, 1))
	window_1.newFrame("Button Frame", (2, 0))
	window_1.newFrame("Table Frame", (0, 2))

	window_1.frames["Image Frame"].grid(sticky=NW)
	window_1.frames["Button Frame"].grid(columnspan=3)
	#window_1.frames["Table Frame"].grid(rowspan=2)
	
	general_header = Labelbox(text='General', lang=lang, repr='sinfo')
	address_header = Labelbox(text="Address", lang=lang, repr='ainfo')
	notes_header = Labelbox(text='Notes', lang=lang, repr='ninfo')
	first_name = Textbox(text="First name", lang=lang, repr='firstName')
	last_name = Textbox(text="Last name", lang=lang, repr='lastName')
	chinese_name = Textbox(text="Chinese name", lang=lang, repr='chineseName')
	date_of_birth = Datebox(text="Date of birth", lang=lang, repr='dob')
	card_print_status = Textbox(text="Card printed", lang=lang, repr='cp')
	pay_per_hour = MoneyTextbox(text="Pay/hour", lang=lang, repr='pay_per_hour')
	barcode = TextboxNoEdit(text="Barcode", lang=lang, repr='bCode')
	address = Textbox(text="Address", lang=lang, repr='addr')
	city = Textbox(text="City", lang=lang, repr='city')
	state = Textbox(text="State", lang=lang, repr='state')
	email = Textbox(text="E-mail", lang=lang, repr='email')
	cell_phone = Textbox(text="Cell phone", lang=lang, repr='cPhone')
	cell_phone_2 = Textbox(text="Cell phone 2", lang=lang, repr='cPhone2')
	zipcode = IntTextbox(text="Zipcode", lang=lang, repr='zip')
	add_student_button = Buttonbox(text='Add Teacher', lang=lang, repr='sadd')
	portrait = Photo(repr='portr', path=images + 'monet_sm.jpg')
	notes = LongTextbox(text="Notes", lang=lang, repr='notes')
	save_teacher_button = Buttonbox(text='Save', lang=lang, repr='save_teacher_button')
	close_button = Buttonbox(text='Close', lang=lang, repr='close_button')
	attendance_table = Table(repr='attinfox', edit=False)
	attendance_table_headers = ['Date', 'Check-In Time', 'Start Time', 'Check-Out Time', 'Confirm Time']
	#switch_frame_button = Buttonbox(text='Attendance', lang=lang, repr='showstudentinfo')
	
	window_1.frames["General Info Frame"].addWidget(general_header, (0, 0))
	window_1.frames["General Info Frame"].addWidget(first_name, (1, 0))
	window_1.frames["General Info Frame"].addWidget(last_name, (2, 0))
	window_1.frames["General Info Frame"].addWidget(chinese_name, (3, 0))
	window_1.frames["General Info Frame"].addWidget(date_of_birth, (4, 0))
	window_1.frames["General Info Frame"].addWidget(barcode, (5, 0))
	window_1.frames["General Info Frame"].addWidget(card_print_status, (6, 0))
	window_1.frames["General Info Frame"].addWidget(pay_per_hour, (7, 0))
	window_1.frames["Contact Frame"].addWidget(address_header, (0, 0))
	window_1.frames["Contact Frame"].addWidget(address, (1, 0))
	window_1.frames["Contact Frame"].addWidget(city, (2, 0))
	window_1.frames["Contact Frame"].addWidget(state, (3, 0))
	window_1.frames["Contact Frame"].addWidget(zipcode, (4, 0))
	window_1.frames["Contact Frame"].addWidget(email, (5, 0))
	window_1.frames["Contact Frame"].addWidget(cell_phone, (6, 0))
	window_1.frames["Contact Frame"].addWidget(cell_phone_2, (7, 0))
	window_1.frames["Image Frame"].addWidget(portrait, (0, 0))
	window_1.frames["Notes Frame"].addWidget(notes_header, (0, 0))
	window_1.frames["Notes Frame"].addWidget(notes, (1, 0))
	window_1.frames["Button Frame"].addWidget(save_teacher_button, (0, 0))
	window_1.frames["Button Frame"].addWidget(close_button, (0, 1))	
	#window_1.frames["Table Frame"].addWidget(attendance_table, (0, 0))
	#window_1.frames["Fourth Frame"].addWidget(early_checkin, (0, 0))
	#window_1.frames["Button Frame"].addWidget(switch_frame_button, (0, 2))

	''' colors '''
	label_bg = '#4DBCE9'
	hover_bg = '#26ADE4'
	header_color = "#3B5C8D"
	
	'''
	widget settings
	must be placed after widget has been added
	'''
	general_header.widget_frame.grid(columnspan=2, sticky=EW)
	general_header.config(bg=header_color, fg='white')
	general_header.label.pack(side=LEFT)
	address_header.widget_frame.grid(columnspan=2, sticky=EW)
	address_header.config(bg=header_color, fg='white')
	address_header.label.pack(side=LEFT)
	notes_header.widget_frame.grid(columnspan=2, sticky=EW)
	notes_header.config(bg=header_color, fg='white')
	notes_header.label.pack(side=LEFT)
	notes.label.pack_forget()
	notes.config(height=8, width=30)
	portrait.label.config(bg='#73C1DE')
	window_1.frames["General Info Frame"].grid(padx=(0, 10), pady=(0, 10))
	window_1.frames["Contact Frame"].grid(padx=(0, 10), pady=(0, 10))
	#window_1.frames["Image Frame"].grid(padx=(0, 10), pady=10)
	#window_1.frames["Notes Frame"].grid(padx=(0, 10), pady=(0, 10))
	#attendance_table.canvas.config(width=580, height=300)
	#switch_frame_button.config(lang=lang)
	#switch_frame_button.selfframe.grid_forget()

	top_window_.current_shown = 'window_1'
	def switch_frame():
		if top_window_.current_shown == 'window_1':
			window_1.pack_forget()
			window_2.pack(side=LEFT)
			top_window_.current_shown = 'window_2'
			switch_frame_button.label.config(text='Teacher info')
		elif top_window_.current_shown == 'window_2':
			window_2.pack_forget()
			window_1.pack(side=LEFT)
			top_window_.current_shown = 'window_1'
			switch_frame_button.label.config(text='Attendance')
		return

	data_points = StudentInfo().datapoints
	data_points.update(database.studentList[i].datapoints)
	window_1.populate(data_points)
	window_2.populate(data_points)
	pay_per_hour.entry.config(validate="all", validatecommand=pay_per_hour.vcmd)
	'''
	attendance_table.setData(
		headers=attendance_table_headers,
		data=[row[:5] for row in data_points['attinfo'][1]])
	'''

	def collect():
		if not altered():
			top_window_.destroy()
			return
		if not confirm_save_teacher_data(lang): return

		data_points.update(window_1.collect(data_points))
		database.studentList[i].datapoints = data_points
		database.saveData()
		top_window_.destroy()

	def altered():
		current_data_points = window_1.collect(data_points)
		for key in current_data_points.keys():
			if current_data_points[key] != data_points[key]:
				return True
		return False

	def quit():
		if not altered():
			top_window_.destroy()
		elif confirm_return_without_saving(lang):
			top_window_.destroy()
	
	save_teacher_button.widget_frame.grid(padx=5)
	close_button.widget_frame.grid(padx=5)
	
	save_teacher_button.config(cmd=collect)
	close_button.config(cmd=quit)
	#switch_frame_button.config(cmd=switch_frame)

	for frame in window_1.frames.values():
		for widget in frame.widgets.values():
			widget.config(lang=lang)