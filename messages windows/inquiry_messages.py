import sys, os
sys.path.append(os.path.abspath(os.pardir) + '\widgets')
sys.path.append(os.path.abspath(os.pardir) + '\miscellaneous')
images = os.path.abspath(os.pardir) + '\images\\'

from tkinter import *
from datetime import datetime

from mbox2 import Mbox
from textbox import Textbox, TextboxNoEdit, IntTextbox, MoneyTextbox
from button import Buttonbox
from simple_label import Labelbox
from photoWidget2 import Photo
from languages import languages
from translations import english_to_chinese, chinese_to_english
from translate_ import translate


def confirm_teacher_addition(lang):
	def return_(value):
		message_box.value = value
		message_box.dw()

	message_box = Mbox()

	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	context = Labelbox(text='Are you sure you would like to add this teacher?', lang=lang, repr='context')
	yes_button = Buttonbox(text='Yes', lang=lang, repr='yes_button')
	no_button = Buttonbox(text='No', lang=lang, repr='no_button')
	verify_image = Photo(repr='verify_image', path=images + 'halt_sm.png')

	message_box.frames["First Frame"].addWidget(context, (0, 1))
	message_box.frames["Second Frame"].addWidget(yes_button, (0, 0))
	message_box.frames["Second Frame"].addWidget(no_button, (0, 1))
	message_box.frames["First Frame"].addWidget(verify_image, (0, 0))

	yes_button.widget_frame.grid(sticky=E+W, padx=5)
	no_button.widget_frame.grid(sticky=E+W, padx=5)
	yes_button.config(cmd=lambda: return_(True), width=10)
	no_button.config(cmd=lambda: return_(False), width=10)
	no_button.label.focus_set()

	verify_image.label.config(width=80)
	context.label.config(wraplength=200, justify=LEFT)
	
	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)
		
	message_box.root.wait_window()

	return message_box.value

def confirm_save_teacher_data(lang):
	def return_(value):
		message_box.value = value
		message_box.dw()

	message_box = Mbox()

	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	constext = Labelbox(text='Save Teacher', lang=lang, repr='constext')
	yes_button = Buttonbox(text='Yes', lang=lang, repr='yes_button')
	no_button = Buttonbox(text='No', lang=lang, repr='no_button')
	verify_image = Photo(repr='verify_image', path=images + 'halt_sm.png')

	message_box.frames["First Frame"].addWidget(constext, (0, 1))
	message_box.frames["Second Frame"].addWidget(yes_button, (0, 0))
	message_box.frames["Second Frame"].addWidget(no_button, (0, 1))
	message_box.frames["First Frame"].addWidget(verify_image, (0, 0))

	yes_button.widget_frame.grid(sticky=E+W, padx=5)
	no_button.widget_frame.grid(sticky=E+W, padx=5)
	yes_button.config(cmd=lambda: return_(True), width=10)
	no_button.config(cmd=lambda: return_(False), width=10)

	verify_image.label.config(width=80)
	constext.label.config(wraplength=200, justify=LEFT)
	
	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)
		
	message_box.root.wait_window()

	return message_box.value

def confirm_overwrite_teacher(lang):
	def return_(value):
		message_box.value = value
		message_box.dw()

	message_box = Mbox()

	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	asetext = Labelbox(text='Teacher with this barcode already exists. Adding this teacher will overwrite the existing teacher. Would you like to overwrite?', lang=lang, repr='asetext')
	yes_button = Buttonbox(text='Yes', lang=lang, repr='yes_button')
	no_button = Buttonbox(text='No', lang=lang, repr='no_button')
	verify_image = Photo(repr='verify_image', path=images + 'halt_sm.png')

	message_box.frames["First Frame"].addWidget(asetext, (0, 1))
	message_box.frames["First Frame"].addWidget(verify_image, (0, 0))
	message_box.frames["Second Frame"].addWidget(yes_button, (0, 0))
	message_box.frames["Second Frame"].addWidget(no_button, (0, 1))

	yes_button.widget_frame.grid(sticky=E+W, padx=5)
	no_button.widget_frame.grid(sticky=E+W, padx=5)
	yes_button.config(cmd=lambda: return_(True), width=10)
	no_button.config(cmd=lambda: return_(False), width=10)
	no_button.label.focus_set()

	verify_image.label.config(width=80)
	asetext.label.config(wraplength=200, justify=LEFT)
	
	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)
		
	message_box.root.wait_window()

	return message_box.value

def confirm_check_in_time(lang, database):
	def return_(value):
		message_box.value = value
		message_box.dw()

	message_box = Mbox()

	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	timeslot = database.findTimeSlot(datetime.now())

	cstext = Labelbox(text='Check in the teacher?', lang=lang, repr='creset')
	yes_button_current_time = Buttonbox(text='Check-in time', lang=lang, repr='bok')
	yes_button_enter_time = Buttonbox(text='Yes, enter time', lang=lang, repr='no_buttonk')
	cancel_button = Buttonbox(text='Cancel', lang=lang, repr='cancel_button')
	verify_image = Photo(repr='verify_image', path=images + 'halt_sm.png')

	message_box.frames["First Frame"].addWidget(cstext, (0, 1))
	message_box.frames["Second Frame"].addWidget(yes_button_current_time, (0, 0))
	message_box.frames["Second Frame"].addWidget(yes_button_enter_time, (1, 0))
	message_box.frames["Second Frame"].addWidget(cancel_button, (2, 0))
	message_box.frames["First Frame"].addWidget(verify_image, (0, 0))

	yes_button_current_time.config(cmd=lambda: return_(True))
	yes_button_enter_time.config(cmd=lambda: return_('manual'))
	cancel_button.config(cmd=lambda: return_(False))
	
	verify_image.label.config(width=80)
	cstext.label.config(wraplength=200, justify=LEFT)
	
	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	yes_button_current_time_text = yes_button_current_time.label.cget('text')
	yes_button_current_time.label.config(
		text=yes_button_current_time_text + ' ' + timeslot)
		
	message_box.root.wait_window()

	return message_box.value

def confirm_check_out_time(lang, database):
	def return_(value):
		message_box.value = value
		message_box.dw()

	message_box = Mbox()

	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	timeslot = database.findTimeSlot(datetime.now())

	cstext = Labelbox(text='Check out the teacher?', lang=lang, repr='creset')
	yes_button_current_time = Buttonbox(text='Check-out time', lang=lang, repr='currenttimebutton')
	yes_button_enter_time = Buttonbox(text='Yes, enter time', lang=lang, repr='entertimebutton')
	cancel_button = Buttonbox(text='Cancel', lang=lang, repr='cancel_button')
	verify_image = Photo(repr='verify_image', path=images + 'halt_sm.png')

	message_box.frames["First Frame"].addWidget(cstext, (0, 1))
	message_box.frames["Second Frame"].addWidget(yes_button_current_time, (0, 0))
	message_box.frames["Second Frame"].addWidget(yes_button_enter_time, (1, 0))
	message_box.frames["Second Frame"].addWidget(cancel_button, (2, 0))
	message_box.frames["First Frame"].addWidget(verify_image, (0, 0))

	yes_button_current_time.config(cmd=lambda: return_(True))
	yes_button_enter_time.config(cmd=lambda: return_('manual'))
	cancel_button.config(cmd=lambda: return_(False))

	verify_image.label.config(width=80)
	cstext.label.config(wraplength=200, justify=LEFT)
	
	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)
		
	yes_button_current_time_text = yes_button_current_time.label.cget('text')
	yes_button_current_time.label.config(
		text=yes_button_current_time_text + ' ' + timeslot)
		
	message_box.root.wait_window()

	return message_box.value

def confirm_overwrite_checkout(lang):
	def return_(value):
		message_box.value = value
		message_box.dw()

	message_box = Mbox()

	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	cstext = Labelbox(text='Teacher checked-out today. Overwrite check-out?', lang=lang, repr='cprint')
	yes_button = Buttonbox(text='Yes', lang=lang, repr='yes_button')
	no_button = Buttonbox(text='No', lang=lang, repr='no_button')
	verify_image = Photo(repr='verify_image', path=images + 'halt_sm.png')

	message_box.frames["First Frame"].addWidget(cstext, (0, 1))
	message_box.frames["Second Frame"].addWidget(yes_button, (0, 0))
	message_box.frames["Second Frame"].addWidget(no_button, (0, 1))
	message_box.frames["First Frame"].addWidget(verify_image, (0, 0))

	yes_button.widget_frame.grid(sticky=E+W, padx=5)
	no_button.widget_frame.grid(sticky=E+W, padx=5)
	yes_button.config(cmd=lambda: return_(True), width=10)
	no_button.config(cmd=lambda: return_(False), width=10)
	yes_button.label.focus_set()

	verify_image.label.config(width=80)
	cstext.label.config(wraplength=200, justify=LEFT)
	
	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)
		
	message_box.root.wait_window()

	return message_box.value

def confirm_print(lang):
	def return_(value):
		message_box.value = value
		message_box.dw()

	message_box = Mbox()

	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	cstext = Labelbox(text='Confirm print', lang=lang, repr='cprint')
	yes_button = Buttonbox(text='Yes', lang=lang, repr='yes_button')
	no_button = Buttonbox(text='No', lang=lang, repr='no_button')
	verify_image = Photo(repr='verify_image', path=images + 'halt_sm.png')

	message_box.frames["First Frame"].addWidget(cstext, (0, 1))
	message_box.frames["Second Frame"].addWidget(yes_button, (0, 0))
	message_box.frames["Second Frame"].addWidget(no_button, (0, 1))
	message_box.frames["First Frame"].addWidget(verify_image, (0, 0))

	yes_button.widget_frame.grid(sticky=E+W, padx=5)
	no_button.widget_frame.grid(sticky=E+W, padx=5)
	yes_button.config(cmd=lambda: return_(True), width=10)
	no_button.config(cmd=lambda: return_(False), width=10)
	yes_button.label.focus_set()

	verify_image.label.config(width=80)
	cstext.label.config(wraplength=200, justify=LEFT)
	
	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)
		
	message_box.root.wait_window()

	return message_box.value

def confirm_reset(lang):
	def return_(value):
		message_box.value = value
		message_box.dw()

	message_box = Mbox()

	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	cstext = Labelbox(text='Confirm reset', lang=lang, repr='creset')
	yes_button = Buttonbox(text='Yes', lang=lang, repr='yes_button')
	no_button = Buttonbox(text='No', lang=lang, repr='no_button')
	cancel_button = Buttonbox(text='Cancel', lang=lang, repr='cancel_button')
	verify_image = Photo(repr='verify_image', path=images + 'halt_sm.png')

	message_box.frames["First Frame"].addWidget(cstext, (0, 1))
	message_box.frames["Second Frame"].addWidget(yes_button, (0, 0))
	message_box.frames["Second Frame"].addWidget(no_button, (0, 1))
	message_box.frames["Second Frame"].addWidget(cancel_button, (0, 2))
	message_box.frames["First Frame"].addWidget(verify_image, (0, 0))

	yes_button.widget_frame.grid(sticky=E+W, padx=5)
	no_button.widget_frame.grid(sticky=E+W, padx=5)
	cancel_button.widget_frame.grid(sticky=E+W, padx=5)
	yes_button.config(cmd=lambda: return_(True), width=10)
	no_button.config(cmd=lambda: return_(False), width=10)
	cancel_button.config(cmd=lambda: d('cancel'), width=10)

	verify_image.label.config(width=80)
	cstext.label.config(wraplength=200, justify=LEFT)
	
	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)
		
	message_box.root.wait_window()

	return message_box.value

def confirm_return_to_main_window(lang):
	def return_(value):
		message_box.value = value
		message_box.dw()

	message_box = Mbox()

	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	rettext = Labelbox(text='Return to main window?', lang=lang, repr='rettext')
	yes_button = Buttonbox(text='Yes', lang=lang, repr='yes_button')
	no_button = Buttonbox(text='No', lang=lang, repr='no_button')
	verify_image = Photo(repr='verify_image', path=images + 'halt_sm.png')

	message_box.frames["First Frame"].addWidget(rettext, (0, 1))
	message_box.frames["Second Frame"].addWidget(yes_button, (0, 0))
	message_box.frames["Second Frame"].addWidget(no_button, (0, 1))
	message_box.frames["First Frame"].addWidget(verify_image, (0, 0))

	yes_button.widget_frame.grid(sticky=E+W, padx=5)
	no_button.widget_frame.grid(sticky=E+W, padx=5)
	yes_button.config(cmd=lambda: return_(True), width=10)
	no_button.config(cmd=lambda: return_(False), width=10)
	no_button.label.focus_set()

	verify_image.label.config(width=80)
	rettext.label.config(wraplength=200, justify=LEFT)
	
	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)
		
	message_box.root.wait_window()

	return message_box.value

def confirm_return_without_saving(lang):
	def return_(value):
		message_box.value = value
		message_box.dw()

	message_box = Mbox()

	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	rettext = Labelbox(text='Return to main window without saving?', lang=lang, repr='rettext')
	yes_button = Buttonbox(text='Yes', lang=lang, repr='yes_button')
	no_button = Buttonbox(text='No', lang=lang, repr='no_button')
	verify_image = Photo(repr='verify_image', path=images + 'halt_sm.png')

	message_box.frames["First Frame"].addWidget(rettext, (0, 1))
	message_box.frames["Second Frame"].addWidget(yes_button, (0, 0))
	message_box.frames["Second Frame"].addWidget(no_button, (0, 1))
	message_box.frames["First Frame"].addWidget(verify_image, (0, 0))

	yes_button.widget_frame.grid(sticky=E+W, padx=5)
	no_button.widget_frame.grid(sticky=E+W, padx=5)
	yes_button.config(cmd=lambda: return_(True), width=10)
	no_button.config(cmd=lambda: return_(False), width=10)
	no_button.label.focus_set()

	verify_image.label.config(width=80)
	rettext.label.config(wraplength=200, justify=LEFT)
	
	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)
		
	message_box.root.wait_window()

	return message_box.value

def confirm_overwrite_checkin(lang):
	def return_(value):
		message_box.value = value
		message_box.dw()

	message_box = Mbox()

	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	cstext = Labelbox(text='Teacher checked-in today. Overwrite check-in?', lang=lang, repr='cprint')
	yes_button = Buttonbox(text='Yes', lang=lang, repr='yes_button')
	no_button = Buttonbox(text='No', lang=lang, repr='no_button')
	verify_image = Photo(repr='verify_image', path=images + 'halt_sm.png')

	message_box.frames["First Frame"].addWidget(cstext, (0, 1))
	message_box.frames["Second Frame"].addWidget(yes_button, (0, 0))
	message_box.frames["Second Frame"].addWidget(no_button, (0, 1))
	message_box.frames["First Frame"].addWidget(verify_image, (0, 0))

	yes_button.widget_frame.grid(sticky=E+W, padx=5)
	no_button.widget_frame.grid(sticky=E+W, padx=5)
	yes_button.config(cmd=lambda: return_(True), width=10)
	no_button.config(cmd=lambda: return_(False), width=10)
	yes_button.label.focus_set()

	verify_image.label.config(width=80)
	cstext.label.config(wraplength=200, justify=LEFT)
	
	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)
		
	message_box.root.wait_window()

	return message_box.value