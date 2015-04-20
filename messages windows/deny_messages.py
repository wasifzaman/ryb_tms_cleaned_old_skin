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


def student_does_not_exist(lang):
	message_box = Mbox()
	
	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	nostext = Labelbox(text='Teacher not found', lang=lang, repr='nostext')
	ok_button = Buttonbox(text='ok', lang=lang, repr='ok_button')
	warning_image = Photo(repr='warning_image', path=images + 'ws_sm.png')

	message_box.frames["First Frame"].addWidget(nostext, (0, 1))
	message_box.frames["Second Frame"].addWidget(ok_button, (2, 0))
	message_box.frames["First Frame"].addWidget(warning_image, (0, 0))
	
	warning_image.label.config(width=80)
	nostext.label.config(wraplength=200, justify=LEFT)
	ok_button.config(cmd=message_box.dw, width=10)

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()

def date_error(lang):
	def return_(value):
		message_box.value = value
		message_box.dw()

	message_box = Mbox()
	
	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	nostext = Labelbox(text='Invalid date', lang=lang, repr='invaliddate')
	return_button = Buttonbox(text='Return', lang=lang, repr='ok_')
	warning_image = Photo(repr='warning_image', path=images + 'ws_sm.png')

	message_box.frames["First Frame"].addWidget(nostext, (0, 1))
	message_box.frames["Second Frame"].addWidget(return_button, (0, 0))
	message_box.frames["First Frame"].addWidget(warning_image, (0, 0))
	
	warning_image.label.config(width=80)
	nostext.label.config(wraplength=200, justify=LEFT)
	return_button.config(cmd=lambda: return_(True), width=10)

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()

def time_error(lang):
	def return_(value):
		message_box.value = value
		message_box.dw()

	message_box = Mbox()
	
	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	nostext = Labelbox(text='Invalid time', lang=lang, repr='invaliddate')
	return_button = Buttonbox(text='Return', lang=lang, repr='ok_')
	warning_image = Photo(repr='warning_image', path=images + 'ws_sm.png')

	message_box.frames["First Frame"].addWidget(nostext, (0, 1))
	message_box.frames["Second Frame"].addWidget(return_button, (0, 0))
	message_box.frames["First Frame"].addWidget(warning_image, (0, 0))
	
	warning_image.label.config(width=80)
	nostext.label.config(wraplength=200, justify=LEFT)
	return_button.config(cmd=lambda: return_(True), width=10)

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()

def invalid_path(lang):
	def return_(value):
		message_box.value = value
		message_box.dw()

	message_box = Mbox()
	
	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	nostext = Labelbox(text='Invalid Path', lang={'Invalid Path': 'Invalid Path'}, repr='invaliddate')
	return_button = Buttonbox(text='Return', lang=lang, repr='ok_')
	warning_image = Photo(repr='warning_image', path=images + 'ws_sm.png')

	message_box.frames["First Frame"].addWidget(nostext, (0, 1))
	message_box.frames["Second Frame"].addWidget(return_button, (2, 0))
	message_box.frames["First Frame"].addWidget(warning_image, (0, 0))
	
	warning_image.label.config(width=80)
	nostext.label.config(wraplength=200, justify=LEFT)
	return_button.config(cmd=lambda: return_(True), width=10)

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()

def checkout_earlier_checkin(lang):
	message_box = Mbox()
	
	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	checkout_earlier_checkin_ = Labelbox(text='Check-Out Cannot be earlier than Check-In',
		lang=lang, 
		repr='fimport')
	ok_button = Buttonbox(text='ok', lang=lang, repr='ok_button')
	warning_image = Photo(repr='warning_image', path=images + 'ws_sm.png')

	message_box.frames["First Frame"].addWidget(checkout_earlier_checkin_, (0, 1))
	message_box.frames["Second Frame"].addWidget(ok_button, (2, 0))
	message_box.frames["First Frame"].addWidget(warning_image, (0, 0))

	warning_image.label.config(width=80)
	checkout_earlier_checkin_.label.config(wraplength=200, justify=LEFT)
	ok_button.config(cmd=message_box.dw, width=10)

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()

def entry_not_found(lang, date):
	message_box = Mbox()
	
	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	entry_not_found_ = Labelbox(text='No Check-In on that Date',
		lang=lang, 
		repr='fimport')
	ok_button = Buttonbox(text='ok', lang=lang, repr='ok_button')
	warning_image = Photo(repr='warning_image', path=images + 'ws_sm.png')

	message_box.frames["First Frame"].addWidget(entry_not_found_, (0, 1))
	message_box.frames["Second Frame"].addWidget(ok_button, (2, 0))
	message_box.frames["First Frame"].addWidget(warning_image, (0, 0))

	warning_image.label.config(width=80)
	entry_not_found_.label.config(wraplength=200, justify=LEFT)
	entry_not_found_.label.config(text=entry_not_found_.label.cget('text') + ' ' + date)
	ok_button.config(cmd=message_box.dw, width=10)

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()

def deny_checkout_future(lang, date):
	message_box = Mbox()
	
	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	entry_not_found_ = Labelbox(text='Cannot Check-in a future time',
		lang=lang, 
		repr='fimport')
	ok_button = Buttonbox(text='ok', lang=lang, repr='ok_button')
	warning_image = Photo(repr='warning_image', path=images + 'ws_sm.png')

	message_box.frames["First Frame"].addWidget(entry_not_found_, (0, 1))
	message_box.frames["Second Frame"].addWidget(ok_button, (2, 0))
	message_box.frames["First Frame"].addWidget(warning_image, (0, 0))
	
	warning_image.label.config(width=80)
	entry_not_found_.label.config(wraplength=200, justify=LEFT)
	entry_not_found_.label.config(text=entry_not_found_.label.cget('text') + ' ' + date)
	ok_button.config(cmd=message_box.dw, width=10)

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()

def wrong_password(lang):
	message_box = Mbox()
	
	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	wrong_pw_label = Labelbox(text='wrong password try again', lang=lang, repr='wrongpwtryagain')
	ok_button = Buttonbox(text='ok', lang=lang, repr='ok_button')
	warning_image = Photo(repr='warning_image', path=images + 'ws_sm.png')

	message_box.frames["First Frame"].addWidget(wrong_pw_label, (0, 1))
	message_box.frames["Second Frame"].addWidget(ok_button, (0, 0))
	message_box.frames["First Frame"].addWidget(warning_image, (0, 0))

	warning_image.label.config(width=80)
	wrong_pw_label.label.config(wraplength=200, justify=LEFT)
	ok_button.config(cmd=message_box.dw, width=10)

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()

def invalid_file_type(lang):
	''' **obsolete**? '''
	
	message_box = Mbox()
	
	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	fimport = Labelbox(text='Invalid File Type', lang=lang, repr='fimport')
	ok_button = Buttonbox(text='ok', lang=lang, repr='ok_button')
	warning_image = Photo(repr='warning_image', path=images + 'ws_sm.png')

	message_box.frames["First Frame"].addWidget(fimport, (0, 1))
	message_box.frames["Second Frame"].addWidget(ok_button, (2, 0))
	message_box.frames["First Frame"].addWidget(warning_image, (0, 0))

	warning_image.label.config(width=80)
	fimport.label.config(wraplength=200, justify=LEFT)
	ok_button.config(cmd=message_box.dw, width=10)

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()

def no_checkin_today(lang):
	message_box = Mbox()
	
	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	fimport = Labelbox(text='No Check-in today', lang=lang, repr='fimport')
	ok_button = Buttonbox(text='ok', lang=lang, repr='ok_button')
	warning_image = Photo(repr='warning_image', path=images + 'ws_sm.png')

	message_box.frames["First Frame"].addWidget(fimport, (0, 1))
	message_box.frames["Second Frame"].addWidget(ok_button, (2, 0))
	message_box.frames["First Frame"].addWidget(warning_image, (0, 0))

	warning_image.label.config(width=80)
	fimport.label.config(wraplength=200, justify=LEFT)
	ok_button.config(cmd=message_box.dw, width=10)

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()

def invoice_error(lang):
	message_box = Mbox()
	
	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	fimport = Labelbox(text='Invoice errors found! Please review the invoice.', lang=lang, repr='fimport')
	ok_button = Buttonbox(text='Yes, I will review', lang=lang, repr='ok_button')
	warning_image = Photo(repr='warning_image', path=images + 'ws_sm.png')

	message_box.frames["First Frame"].addWidget(fimport, (0, 1))
	message_box.frames["Second Frame"].addWidget(ok_button, (2, 0))
	message_box.frames["First Frame"].addWidget(warning_image, (0, 0))

	warning_image.label.config(width=80)
	fimport.label.config(wraplength=200, justify=LEFT)
	ok_button.config(cmd=message_box.dw, width=15)

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()

def decryption_error(lang):
	message_box = Mbox()
	
	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	message = Labelbox(text='Unable to decrypt database with the chosen key! The key was not changed.', lang=lang, repr='fimport')
	ok_button = Buttonbox(text='ok', lang=lang, repr='ok_button')
	warning_image = Photo(repr='warning_image', path=images + 'ws_sm.png')

	message_box.frames["First Frame"].addWidget(message, (0, 1))
	message_box.frames["Second Frame"].addWidget(ok_button, (2, 0))
	message_box.frames["First Frame"].addWidget(warning_image, (0, 0))

	warning_image.label.config(width=80)
	message.label.config(wraplength=200, justify=LEFT)
	ok_button.config(cmd=message_box.dw, width=15)

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()

def already_running_(lang):
	message_box = Mbox(stand_alone=True)
	
	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Second Frame", (1, 0))

	message = Labelbox(text='Another instance of this program is running. Please close all instances of this program and try running again.', lang=lang, repr='fimport')
	ok_button = Buttonbox(text='ok', lang=lang, repr='ok_button')
	warning_image = Photo(repr='warning_image', path=images + 'ws_sm.png')

	message_box.frames["First Frame"].addWidget(message, (0, 1))
	message_box.frames["Second Frame"].addWidget(ok_button, (2, 0))
	message_box.frames["First Frame"].addWidget(warning_image, (0, 0))

	warning_image.label.config(width=80)
	message.label.config(wraplength=200, justify=LEFT)
	ok_button.config(cmd=message_box.dw, width=15)

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()