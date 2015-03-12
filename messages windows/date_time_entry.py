import sys, os
sys.path.append(os.path.abspath(os.pardir) + '\widgets')
sys.path.append(os.path.abspath(os.pardir) + '\miscellaneous')
sys.path.append(os.path.abspath(os.pardir) + '\windows')
sys.path.append(os.path.abspath(os.pardir) + '\messages windows')
images = os.path.abspath(os.pardir) + '\images\\'


from tkinter import *
from datetime import datetime
import tkinter.ttk as ttk

from mbox2 import Mbox
from uiHandler22 import *
from date_textbox import Datebox
from button import Buttonbox
from simple_label import Labelbox
from photoWidget2 import Photo
from translations import english_to_chinese, chinese_to_english
from translate_ import translate
from master_list import *


def date_time_entry(lang):
	def return_():
		if date_input.getData() == '01/01/1900':
			date_error(lang)
			return
		time_input = hour_input_stringvar.get() + ':' + minute_input_stringvar.get() + ' ' + am_pm_stringvar.get()
		dt = datetime.strftime(datetime.strptime(time_input, '%I:%M %p'), '%I:%M %p')
		message_box.time_input_confirmed = dt
		message_box.date_input = date_input.getData()
		message_box.root.destroy()

	message_box = Mbox()
	message_box.root.resizable(0, 0)
	message_box.root.grab_set()
	message_box.root.focus_set()
	message_box.date_input = False
	message_box.time_input_confirmed = False

	confirm_window = AppWindow(message_box.mainFrame)

	date_input = Datebox(text='Date', lang=lang, repr='dateinput')
	hour_input_stringvar = StringVar()
	minute_input_stringvar = StringVar()
	am_pm_stringvar = StringVar()
	hour_input_stringvar.set(datetime.strftime(datetime.now(), '%I'))
	minute_input_stringvar.set('00')
	am_pm_stringvar.set(datetime.strftime(datetime.now(), '%p'))
	return_button = Buttonbox(text='Confirm', lang=lang, repr='rbutton')
	cancel_button = Buttonbox(text='Cancel', lang=lang, repr='cancelbutton')

	confirm_window.newFrame("First Frame", (0, 0))

	confirm_window.frames["First Frame"].addWidget(date_input, (0, 0))
	Label(confirm_window.frames["First Frame"], text='Time').grid(row=1, column=0, sticky=E)
	hour_input = ttk.Combobox(
		confirm_window.frames["First Frame"],
		textvariable=hour_input_stringvar, width=2, state='readonly')
	hour_input.grid(row=1, column=1)
	minute_input = ttk.Combobox(
		confirm_window.frames["First Frame"],
		textvariable=minute_input_stringvar, width=2, state='readonly')
	minute_input.grid(row=1, column=2)
	am_pm_input = ttk.Combobox(
		confirm_window.frames["First Frame"],
		textvariable=am_pm_stringvar, width=3, state='readonly')
	am_pm_input.grid(row=1, column=3, padx=(2, 0))
	confirm_window.frames["First Frame"].addWidget(return_button, (2, 0))
	confirm_window.frames["First Frame"].addWidget(cancel_button, (3, 0))

	hour_input['values'] = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
	minute_input['values'] = ('00', '30')
	am_pm_input['values'] = ('AM', 'PM')

	return_button.widget_frame.grid(columnspan=6, pady=(20, 1))
	cancel_button.widget_frame.grid(columnspan=6)
	date_input.label.config(width=6)
	date_input.widget_frame.grid(columnspan=7, pady=15)

	return_button.config(cmd=return_)
	cancel_button.config(cmd=message_box.root.destroy)

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()

	return message_box.date_input, message_box.time_input_confirmed