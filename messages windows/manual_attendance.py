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
from textbox import Textbox
from date_textbox import Datebox
from button import Buttonbox
from simple_label import Labelbox
from tableWidget2 import Table
from photoWidget2 import Photo
from languages import languages
from translations import english_to_chinese, chinese_to_english
from translate_ import translate
from master_list import *


def manual_attendance(lang, database):
	def return_(value):
		if not value:
			message_box.root.destroy()
			return

		new_check_in = message_box.check_in_hour.get() + \
									':' + message_box.check_in_minute.get() + \
									' ' + message_box.check_in_ampm.get()
		new_check_out = message_box.check_out_hour.get() + \
								':' + message_box.check_out_minute.get() + \
								' ' + message_box.check_out_ampm.get()

		try:
			datetime.strptime(attendance_date.getData() + ' ' + new_check_in, '%m/%d/%Y %I:%M %p')
			datetime.strptime(attendance_date.getData() + ' ' + new_check_out, '%m/%d/%Y %I:%M %p')
		except ValueError:
			time_error(lang)
			return
		
		if value == 'overwrite':
			if message_box.attendance[1][2] != new_check_in:
				message_box.attendance[1][1] = ''
				message_box.attendance[1][2] = new_check_in
			if message_box.attendance[1][4] != new_check_out:
				message_box.attendance[1][3] = ''
				message_box.attendance[1][4] = new_check_out

		elif value == 'new':
			database.studentList[barcode.getData()].datapoints['attinfo'][1].append([
				attendance_date.getData(),
				'',
				new_check_in,
				'',
				new_check_out,
				database.school
			])

			database.sort_attendance(barcode.getData())

		database.saveData()

		message_box.change_made = True

		message_box.root.destroy()

	def check_attendance():
		if attendance_date.getData() == '01/01/1900':
			date_error(lang)
			return

		if datetime.strptime(attendance_date.getData(), '%m/%d/%Y') > datetime.now():
			deny_checkout_future(lang, attendance_date.getData())
			return

		message_box.attendance = database.search_attendance(barcode.getData(), attendance_date.getData())
		
		if message_box.attendance == 'no teacher':
			student_does_not_exist(lang)
			return

		elif message_box.attendance:
			final_table = [[] for x in range(0, len(message_box.attendance[0]))]
			for row in message_box.attendance:
				for index in range(0, len(row)):
					final_table[index].append(row[index])

			attendance_table.setData(
				data=final_table
			)

			for cell_id, cell_val in attendance_table.cells.items():
				if cell_id[0] == 1:
					cell_val.label.grid(pady=1)
				if cell_id[1] == 1:
					cell_val.label.grid(padx=1)
				if cell_id[0] == 0 or cell_id[1] == 0:
					cell_val.label.grid_forget()
			attendance_table.corner_cell.grid_forget()

			attendance_table.canvas.config(width=235, height=155)

			confirm_window.frames["Attendance Frame"].grid(row=1, column=0)
			confirm_window.frames["New Attendance Frame"].grid(row=1, column=1, sticky=N)
			check_button.widget_frame.grid_forget()

			check_in = message_box.attendance[1][2]
			check_out = message_box.attendance[1][4]

			if len(check_in) > 0:
				message_box.check_in_hour.set(check_in.split(':')[0])
				message_box.check_in_minute.set(check_in.split(':')[1].split(' ')[0])
				message_box.check_in_ampm.set(check_in.split(' ')[1])
			if len(check_out) > 0:
				message_box.check_out_hour.set(check_out.split(':')[0])
				message_box.check_out_minute.set(check_out.split(':')[1].split(' ')[0])
				message_box.check_out_ampm.set(check_out.split(' ')[1])

			return_button.config(cmd=lambda: return_('overwrite'))
		
		elif not message_box.attendance:
			confirm_window.frames["New Attendance Frame"].grid(row=1, column=0)
			check_button.widget_frame.grid_forget()

			return_button.config(cmd=lambda: return_('new'))

		barcode.entry.config(state=DISABLED, disabledbackground='white', disabledforeground='black')
		attendance_date.mEntry.config(state=DISABLED, disabledbackground='white', disabledforeground='black')
		attendance_date.dEntry.config(state=DISABLED, disabledbackground='white', disabledforeground='black')
		attendance_date.yEntry.config(state=DISABLED, disabledbackground='white', disabledforeground='black')
		return_button.widget_frame.grid(row=1, column=0, pady=1)

		if lang == 'chinese':
			translate(message_box.root, english_to_chinese)

	message_box = Mbox()
	message_box.root.resizable(0, 0)
	message_box.root.grab_set()
	message_box.root.focus_set()
	message_box.change_made = False
	message_box.check_in_hour = StringVar()
	message_box.check_in_minute = StringVar()
	message_box.check_in_ampm = StringVar()
	message_box.check_out_hour = StringVar()
	message_box.check_out_minute = StringVar()
	message_box.check_out_ampm = StringVar()

	confirm_window = AppWindow(message_box.mainFrame)

	barcode = Textbox(text='Barcode', lang=lang, repr='barcode')
	attendance_date = Datebox(text='Date', lang=lang, repr='a_date')
	check_button = Buttonbox(text='Check', lang=lang, repr='check_button')
	return_button = Buttonbox(text='Confirm', lang=lang, repr='rbutton')
	cancel_button = Buttonbox(text='Cancel', lang=lang, repr='cancelbutton')
	attendance_table = Table(repr='attendance_table', edit=False)
	new_check_in_label = Labelbox(repr='new_checkin', text='New Check-in')
	new_check_out_label = Labelbox(repr='new_checkout', text='New Check-out')

	confirm_window.newFrame("First Frame", (0, 0))
	confirm_window.newFrame("Attendance Frame", (1, 0))
	confirm_window.newFrame("New Attendance Frame", (1, 1))
	confirm_window.newFrame("Button Frame", (3, 0))

	confirm_window.frames["First Frame"].grid(columnspan=2)
	confirm_window.frames["Attendance Frame"].grid_forget()
	confirm_window.frames["New Attendance Frame"].grid_forget()
	confirm_window.frames["Button Frame"].grid(columnspan=2)

	check_in_hour = ttk.Combobox(
		confirm_window.frames["New Attendance Frame"],
		textvariable=message_box.check_in_hour, width=4, state='readonly')
	check_in_hour.grid(row=0, column=1)
	check_in_minute = ttk.Combobox(
		confirm_window.frames["New Attendance Frame"],
		textvariable=message_box.check_in_minute, width=4, state='readonly')
	check_in_minute.grid(row=0, column=2)
	check_in_ampm = ttk.Combobox(
		confirm_window.frames["New Attendance Frame"],
		textvariable=message_box.check_in_ampm, width=4, state='readonly')
	check_in_ampm.grid(row=0, column=3)
	check_out_hour = ttk.Combobox(
		confirm_window.frames["New Attendance Frame"],
		textvariable=message_box.check_out_hour, width=4, state='readonly')
	check_out_hour.grid(row=1, column=1)
	check_out_minute = ttk.Combobox(
		confirm_window.frames["New Attendance Frame"],
		textvariable=message_box.check_out_minute, width=4, state='readonly')
	check_out_minute.grid(row=1, column=2)
	check_out_ampm = ttk.Combobox(
		confirm_window.frames["New Attendance Frame"],
		textvariable=message_box.check_out_ampm, width=4, state='readonly')
	check_out_ampm.grid(row=1, column=3)
	confirm_window.frames["First Frame"].addWidget(barcode, (0, 0))
	confirm_window.frames["First Frame"].addWidget(attendance_date, (1, 0))
	confirm_window.frames["Attendance Frame"].addWidget(attendance_table, (0, 0))
	confirm_window.frames["Button Frame"].addWidget(check_button, (0, 0))
	confirm_window.frames["Button Frame"].addWidget(return_button, (1, 0))
	confirm_window.frames["Button Frame"].addWidget(cancel_button, (2, 0))
	confirm_window.frames["New Attendance Frame"].addWidget(new_check_in_label, (0, 0))
	confirm_window.frames["New Attendance Frame"].addWidget(new_check_out_label, (1, 0))

	check_in_hour['values'] = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
	check_in_minute['values'] = ('00', '30')
	check_in_ampm['values'] = ('AM', 'PM')
	check_out_hour['values'] = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
	check_out_minute['values'] = ('00', '30')
	check_out_ampm['values'] = ('AM', 'PM')

	return_button.widget_frame.grid_forget()
	check_button.config(cmd=check_attendance)
	cancel_button.config(cmd=lambda: return_(False))

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	barcode.setData('RYB-')

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()

	return message_box.change_made