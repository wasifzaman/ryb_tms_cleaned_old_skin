import sys, os
sys.path.append(os.path.abspath(os.pardir) + '\widgets')
sys.path.append(os.path.abspath(os.pardir) + '\miscellaneous')
sys.path.append(os.path.abspath(os.pardir) + '\windows')
images = os.path.abspath(os.pardir) + '\images\\'


from tkinter import *
from datetime import datetime
import tkinter.ttk as ttk

from mbox2 import Mbox
from uiHandler22 import *
from textbox import IntTextbox
from date_textbox import Datebox
from button import Buttonbox
from simple_label import Labelbox
from photoWidget2 import Photo
from languages import languages
from deny_messages import date_error
from translations import english_to_chinese, chinese_to_english
from translate_ import translate


def month_year(lang):
	def return_(value):
		if not value:
			message_box.month_input_stringvar, message_box.year_input = False, False
		else:
			message_box.month_input_stringvar = months.index(message_box.month_input_stringvar.get()) + 1
			message_box.year_input = year_input.getData()
		message_box.root.destroy()

	message_box = Mbox()
	message_box.root.resizable(0, 0)
	message_box.root.grab_set()
	message_box.root.focus_set()
	message_box.month_input_stringvar = StringVar()

	confirm_window = AppWindow(message_box.mainFrame)

	months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
	today = datetime.now()

	return_button = Buttonbox(text='Confirm', lang=lang, repr='rbutton')
	cancel_button = Buttonbox(text='Cancel', lang=lang, repr='cancelbutton')
	year_input = IntTextbox(text='', repr='yearinput')

	confirm_window.newFrame("First Frame", (0, 0))
	confirm_window.newFrame("Button Frame", (1, 0))

	month_input = ttk.Combobox(
		confirm_window.frames["First Frame"],
		textvariable=message_box.month_input_stringvar, width=11, state='readonly')
	month_input.grid(row=0, column=0)
	confirm_window.frames["First Frame"].addWidget(year_input, (0, 1))
	confirm_window.frames["Button Frame"].addWidget(return_button, (1, 0))
	confirm_window.frames["Button Frame"].addWidget(cancel_button, (2, 0))

	month_input['values'] = tuple(months)

	if today.month - 1 == 0:
		message_box.month_input_stringvar.set('December')
		year_input.setData(today.year - 1)
	else:
		message_box.month_input_stringvar.set(months[today.month - 2])
		year_input.setData(today.year)

	year_input.label.pack_forget()
	year_input.entry.config(width=6)
	year_input.widget_frame.grid(pady=0)
	return_button.widget_frame.grid(pady=(20, 1))

	return_button.config(cmd=lambda: return_(True))
	cancel_button.config(cmd=lambda: return_(False))

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()

	return message_box.month_input_stringvar, message_box.year_input