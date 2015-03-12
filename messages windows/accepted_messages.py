import sys, os
sys.path.append(os.path.abspath(os.pardir) + '\widgets')
sys.path.append(os.path.abspath(os.pardir) + '\miscellaneous')
images = os.path.abspath(os.pardir) + '\images\\'

from tkinter import *

from mbox2 import Mbox
from button import Buttonbox
from simple_label import Labelbox
from photoWidget2 import Photo
from translations import english_to_chinese, chinese_to_english
from translate_ import translate


def teacher_added(lang):
	message_box = Mbox()

	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	teacher_added_text = Labelbox(text='Teacher has been added to the database', lang=lang, repr='tatext')
	ok_button = Buttonbox(text='Ok', lang=lang, repr='ok_button')
	confirm_image = Photo(repr='confirm_image', path=images + 'check_mark_sm.png')
	
	message_box.frames["First Frame"].addWidget(teacher_added_text, (0, 1))
	message_box.frames["Second Frame"].addWidget(ok_button, (0, 0))
	message_box.frames["First Frame"].addWidget(confirm_image, (0, 0))

	confirm_image.label.config(width=80)
	teacher_added_text.label.config(wraplength=200, justify=LEFT)
	ok_button.config(cmd=message_box.dw, width=10)

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()

def print_succesful(lang):
	def return_(value):
		message_box.value = value
		message_box.dw()

	message_box = Mbox()

	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	print_succesful_text = Labelbox(text='Print successful', lang=lang, repr='printsuccesful')
	ok_button = Buttonbox(text='Ok', lang=lang, repr='ok_button')
	confirm_image = Photo(repr='confirm_image', path=images + 'check_mark_sm.png')

	message_box.frames["First Frame"].addWidget(print_succesful_text, (0, 1))
	message_box.frames["Second Frame"].addWidget(ok_button, (0, 0))
	message_box.frames["First Frame"].addWidget(confirm_image, (0, 0))
	
	confirm_image.label.config(width=80)
	print_succesful_text.label.config(wraplength=200, justify=LEFT)
	ok_button.config(cmd=lambda: return_(True), width=10)

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()

	return message_box.value

def teacher_report_print_successful(lang):
	def return_(value):
		message_box.value = value
		message_box.dw()

	message_box = Mbox()
	
	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	teacher_report_printed_text = Labelbox(text='Teacher print successful', lang=lang, repr='teacherreportprinted')
	ok_button = Buttonbox(text='Ok', lang=lang, repr='ok_button')
	confirm_image = Photo(repr='confirm_image', path=images + 'check_mark_sm.png')

	message_box.frames["First Frame"].addWidget(teacher_report_printed_text, (0, 1))
	message_box.frames["Second Frame"].addWidget(ok_button, (0, 0))
	message_box.frames["First Frame"].addWidget(confirm_image, (0, 0))
	
	confirm_image.label.config(width=80)
	teacher_report_printed_text.label.config(wraplength=200, justify=LEFT)
	ok_button.config(cmd=lambda: return_(True), width=10)

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()

	return message_box.value

def pw_reset_confirm(lang):
	message_box = Mbox()
	
	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	confirmed_reset_text = Labelbox(text='Password has been reset', lang=lang, repr='confirmedreset')
	ok_button = Buttonbox(text='Ok', lang=lang, repr='ok_button')
	confirm_image = Photo(repr='confirm_image', path=images + 'check_mark_sm.png')

	message_box.frames["First Frame"].addWidget(confirmed_reset_text, (0, 1))
	message_box.frames["Second Frame"].addWidget(ok_button, (0, 0))
	message_box.frames["First Frame"].addWidget(confirm_image, (0, 0))

	confirm_image.label.config(width=80)
	confirmed_reset_text.label.config(wraplength=200, justify=LEFT)
	ok_button.config(cmd=message_box.dw, width=10)

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()

def database_backup_successful(lang):
	def return_(value):
		message_box.value = value
		message_box.dw()

	message_box = Mbox()
	
	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	db_backup_success_text = Labelbox(text='Database backup successful', lang=lang, repr='dbbackupsuccess')
	ok_button = Buttonbox(text='Ok', lang=lang, repr='ok_button')
	confirm_image = Photo(repr='confirm_image', path=images + 'check_mark_sm.png')

	message_box.frames["First Frame"].addWidget(db_backup_success_text, (0, 1))
	message_box.frames["Second Frame"].addWidget(ok_button, (0, 0))
	message_box.frames["First Frame"].addWidget(confirm_image, (0, 0))
	
	confirm_image.label.config(width=80)
	db_backup_success_text.label.config(wraplength=200, justify=LEFT)
	ok_button.config(cmd=lambda: return_(True), width=10)

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()

	return message_box.value

def reset_confirmation(lang, value):
	if value != True: return

	message_box = Mbox()
	
	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	early_checkin_reset_text = Labelbox(text='Early Check-ins have been reset', lang=lang, repr='earlycheckinreset')
	ok_button = Buttonbox(text='Ok', lang=lang, repr='ok_button')
	confirm_image = Photo(repr='confirm_image', path=images + 'check_mark_sm.png')

	message_box.frames["First Frame"].addWidget(early_checkin_reset_text, (0, 1))
	message_box.frames["Second Frame"].addWidget(ok_button, (0, 0))
	message_box.frames["First Frame"].addWidget(confirm_image, (0, 0))

	confirm_image.label.config(width=80)
	early_checkin_reset_text.label.config(wraplength=200, justify=LEFT)
	ok_button.config(cmd=message_box.dw, width=10)

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)
		
	message_box.root.wait_window()