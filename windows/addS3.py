import sys, os
sys.path.append(os.path.abspath(os.pardir) + '\widgets')
sys.path.append(os.path.abspath(os.pardir) + '\database')
sys.path.append(os.path.abspath(os.pardir) + '\miscellaneous')
sys.path.append(os.path.abspath(os.pardir) + '\messages windows')

from student import StudentInfo
from uiHandler22 import Window, AppWindow
from textbox import Textbox, TextboxNoEdit, IntTextbox, MoneyTextbox
from button import Buttonbox
from simple_label import Labelbox
from date_textbox import Datebox
from photoWidget2 import Photo
from multiline_textbox import LongTextbox
from translations import english_to_chinese
from translate_ import translate
from master_list import *


def main(lang, database):
	def return_(value):
		if not value:
			if confirm_return_to_main_window(window_.lang):
				top_window_.destroy()
				return
			return

		if not confirm_teacher_addition(window_.lang):
			return

		new_student = StudentInfo()
		new_student.datapoints.update(window_.collect(new_student.datapoints).items())
 
		database.addStudent(new_student.datapoints['bCode'], new_student)
		database.saveData()

		teacher_added(window_.lang)
		top_window_.destroy()

	top_window_ = Window(top=True)
	top_window_.attributes('-fullscreen', False)
	top_window_.geometry('1280x740+1+1')
	top_window_.resizable(0, 0)
	top_window_.grab_set()
	top_window_.focus_set()
	top_window_.titleFrame.config(height=1)
	top_window_.wintitle.place_forget()
	
	window_ = AppWindow(top_window_.mainFrame)
	window_.lang = lang

	window_.newFrame("Image Frame", (0, 0))
	window_.newFrame("General Info Frame", (0, 1))
	window_.newFrame("Contact Frame", (0, 2))
	window_.newFrame("Notes Frame", (1, 1))
	window_.newFrame("Button Frame", (2, 0))

	window_.frames["Image Frame"].grid(sticky=NW)
	window_.frames["Button Frame"].grid(columnspan=3)

	''' widgets '''
	general_header = Labelbox(text='General', lang=lang, repr='sinfo')
	address_header = Labelbox(text="Address", lang=lang, repr='ainfo')
	notes_header = Labelbox(text='Notes', lang=lang, repr='ninfo')
	first_name = Textbox(text="First name", lang=lang, repr='firstName')
	last_name = Textbox(text="Last name", lang=lang, repr='lastName')
	chinese_name = Textbox(text="Chinese name", lang=lang, repr='chineseName')
	date_of_birth = Datebox(text="Date of birth", lang=lang, repr='dob')
	card_print_status = Textbox(text="Card printed", lang=lang, repr='cp')
	barcode = TextboxNoEdit(text="Barcode", lang=lang, repr='bCode')
	address = Textbox(text="Address", lang=lang, repr='addr')
	city = Textbox(text="City", lang=lang, repr='city')
	state = Textbox(text="State", lang=lang, repr='state')
	email = Textbox(text="E-mail", lang=lang, repr='email')
	cell_phone = Textbox(text="Cell phone", lang=lang, repr='cPhone')
	cell_phone_2 = Textbox(text="Cell phone 2", lang=lang, repr='cPhone2')
	zipcode = IntTextbox(text="Zipcode", lang=lang, repr='zip')
	add_teacher_button = Buttonbox(text='Add teacher', lang=lang, repr='sadd')
	portrait = Photo(repr='portr', path=images + 'monet_sm.jpg')
	notes = LongTextbox(text="Notes", lang=lang, repr='notes')
	cancel_button = Buttonbox(text='Cancel', lang=lang, repr='cancelbutton')

	''' widget addition '''
	window_.frames["General Info Frame"].addWidget(general_header, (0, 0))
	window_.frames["General Info Frame"].addWidget(first_name, (1, 0))
	window_.frames["General Info Frame"].addWidget(last_name, (2, 0))
	window_.frames["General Info Frame"].addWidget(chinese_name, (3, 0))
	window_.frames["General Info Frame"].addWidget(date_of_birth, (4, 0))
	window_.frames["General Info Frame"].addWidget(barcode, (5, 0))
	window_.frames["General Info Frame"].addWidget(card_print_status, (6, 0)) #card printed
	window_.frames["Contact Frame"].addWidget(address_header, (0, 0))
	window_.frames["Contact Frame"].addWidget(address, (1, 0))
	window_.frames["Contact Frame"].addWidget(city, (2, 0))
	window_.frames["Contact Frame"].addWidget(state, (3, 0))
	window_.frames["Contact Frame"].addWidget(zipcode, (4, 0))
	window_.frames["Contact Frame"].addWidget(email, (5, 0))
	window_.frames["Contact Frame"].addWidget(cell_phone, (6, 0))
	window_.frames["Contact Frame"].addWidget(cell_phone_2, (7, 0))
	window_.frames["Image Frame"].addWidget(portrait, (0, 0))
	window_.frames["Notes Frame"].addWidget(notes_header, (0, 0))
	window_.frames["Notes Frame"].addWidget(notes, (1, 0))
	window_.frames["Button Frame"].addWidget(add_teacher_button, (0, 0))
	window_.frames["Button Frame"].addWidget(cancel_button, (1, 0))


	''' colors '''
	label_bg = '#B6F279'
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
	add_teacher_button.label.config(height=5)
	add_teacher_button.config(label_bg=label_bg, hover_bg=hover_bg, label_fg='black')
	notes.label.pack_forget()
	notes.config(height=8, width=30)
	portrait.label.config(bg='#73C1DE')
	window_.frames["General Info Frame"].grid(padx=(0, 10), pady=(0, 10))
	window_.frames["Contact Frame"].grid(padx=(0, 10), pady=(0, 10))

	database.loadData()
	barcode.setData(database.formatCode())

	add_teacher_button.config(cmd=lambda: return_(True))
	cancel_button.config(cmd=lambda: return_(False))

	if lang == 'chinese':
		translate(window_, english_to_chinese)