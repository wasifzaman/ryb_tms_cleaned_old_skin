import sys, os, shutil
sys.path.append(os.path.abspath(os.pardir) + '\widgets')
sys.path.append(os.path.abspath(os.pardir) + '\database')
sys.path.append(os.path.abspath(os.pardir) + '\messages windows')
temp = os.path.abspath(os.pardir) + '\\temp\\'

from dataHandler import StudentDB
from uiHandler22 import Window, AppWindow
from textbox import Textbox, TextboxNoEdit
from tableWidget2 import Table
from tkinter import filedialog
from random import randrange
from master_list import *

def main(lang, database):
	def open_excel():
		excel_file = filedialog.askopenfile(mode='r')
		if excel_file != None:
			source_path.setData(excel_file.name)
		
	def preview_database():
		if hasattr(window_, 'randfile') and os.path.exists(window_.randfile):
			os.remove(window_.randfile)
		if hasattr(window_, 'randpwfile') and os.path.exists(window_.randpwfile):
			os.remove(window_.randpwfile)

		if len(source_path.getData()) == 0: return

		rand_int = str(randrange(0, 100000))
		window_.randfile = temp + '\\temp' + rand_int + '.rybdb'
		window_.randpwfile = temp + '\\temp_pw_file' + rand_int + '.rybdb'
		new_database = StudentDB(file=window_.randfile, cfile='', pwfile=window_.randpwfile)
		
		try:
			new_database.importxlsx(source_path.getData())
		except xlrd.biffh.XLRDError:
			invalid_file_type(window_.lang)
			os.remove(window_.randfile)
			os.remove(window_.randpwfile)

		student_list = []
		for student in new_database.studentList.values():
			data_points = student.datapoints
			student_list.append([data_points['bCode'], data_points['firstName'], data_points['lastName'], data_points['chineseName'], data_points['dob']])

		student_list.sort()
		student_table.canvas.config(width=600, height=280)
		student_table.setData(
			headers=student_table_headers,
			data=student_list)
		student_table.canvas.yview_moveto(1.0)

	def set_file(textbox):
		out_file = filedialog.asksaveasfilename()
		if len(out_file) != 0:
			textbox.setData(out_file + '.rybdb')
		out_file = out_file.split('/')
		file_name = out_file[-1]
		dest_path = '/'.join(out_file[:-1])

	def save_():
		if len(dest_path.getData()) == 0 or \
			len(source_path.getData()) == 0 or \
			len(pw_file_path.getData()) == 0 or \
			not hasattr(window_, 'randfile'):
			return
		out_file = dest_path.getData().split('/')
		file_name = temp + out_file[-1]
		dest_path_ = '/'.join(out_file[:-1])
		pw_out_file = pw_file_path.getData().split('/')
		pw_file_name = temp + pw_out_file[-1]
		pw_dest_path = '/'.join(out_file[:-1])

		os.rename(window_.randfile, file_name)
		os.rename(window_.randpwfile, pw_file_name)
		shutil.move(file_name, dest_path_)
		shutil.move(pw_file_name, pw_dest_path)

		top_window_.destroy()

	def exit_():
		if hasattr(window_, 'randfile') and os.path.exists(window_.randfile):
			os.remove(window_.randfile)
		if hasattr(window_, 'randpwfile') and os.path.exists(window_.randpwfile):
			os.remove(window_.randpwfile)

		top_window_.destroy()

	database.loadData()

	top_window_ = Window(top=True)
	top_window_.geometry('900x500')
	top_window_.attributes('-fullscreen', False)
	top_window_.focus_set()
	top_window_.grab_set()
	top_window_.titleFrame.pack_forget()

	window_ = AppWindow(top_window_.mainFrame)
	window_.lang = lang

	student_table = Table(repr='stable', edit=False)
	student_table_headers = ['Barcode', 'First Name', 'Last Name', 'Chinese Name', 'Date of Birth']
	
	window_.newFrame("Open Excel Frame", (0, 0))
	window_.newFrame("Table Frame", (1, 0))
	window_.newFrame("Password File Frame", (2, 0))
	window_.newFrame("Confirm Frame", (3, 0))

	window_.frames["Table Frame"].grid(sticky=EW)

	save_button = Buttonbox(text='Save', lang=window_.lang, repr='savebutton')
	source_path = TextboxNoEdit(text='Source excel', lang=window_.lang, repr='sourceexcel')
	source_path_browse_button = Buttonbox(text='Browse', lang=window_.lang, repr='sourcefilebrw')
	dest_path = TextboxNoEdit(text='Output file', lang=window_.lang, repr='outputfile')
	dest_path_browse_button = Buttonbox(text='Browse', lang=window_.lang, repr='outputfilebrw')
	pw_file_path = TextboxNoEdit(text='Password file', lang=window_.lang, repr='pwfilepath')
	pw_file_path_browse_button = Buttonbox(text='Browse', lang=window_.lang, repr='pwfilebrw')
	preview_button = Buttonbox(text='Preview', lang=window_.lang, repr='previewbutton')
	cancel_button = Buttonbox(text='Cancel', lang=window_.lang, repr='cancel')
	
	window_.frames["Open Excel Frame"].addWidget(source_path, (0, 0))
	window_.frames["Open Excel Frame"].addWidget(source_path_browse_button, (0, 1))
	window_.frames["Open Excel Frame"].addWidget(preview_button, (0, 2))
	window_.frames["Table Frame"].addWidget(student_table, (0, 0))
	window_.frames["Password File Frame"].addWidget(dest_path, (0, 0))
	window_.frames["Password File Frame"].addWidget(dest_path_browse_button, (0, 1))
	window_.frames["Password File Frame"].addWidget(pw_file_path, (1, 0))
	window_.frames["Password File Frame"].addWidget(pw_file_path_browse_button, (1, 1))
	window_.frames["Confirm Frame"].addWidget(save_button, (0, 0))
	window_.frames["Confirm Frame"].addWidget(cancel_button, (0, 1))

	student_table.canvas.config(width=600, height=280)
	
	for frame in window_.frames.values():
		for widget in frame.widgets.values():
			widget.config(lang=window_.lang)
	
	source_path_browse_button.config(width=7)
	dest_path_browse_button.config(width=7)
	pw_file_path_browse_button.config(width=7)
	preview_button.config(width=7)
	source_path_browse_button.label.config(height=1)
	dest_path_browse_button.label.config(height=1)
	pw_file_path_browse_button.label.config(height=1)
	preview_button.label.config(height=1)
	source_path_browse_button.widget_frame.grid(padx=5)
	dest_path_browse_button.widget_frame.grid(padx=5)
	pw_file_path_browse_button.widget_frame.grid(padx=5)
	preview_button.widget_frame.grid(padx=5)
	save_button.widget_frame.grid(padx=5)
	cancel_button.widget_frame.grid(padx=5)
	window_.frames["Confirm Frame"].grid(pady=(10, 0))

	source_path_browse_button.config(cmd=open_excel)
	dest_path_browse_button.config(cmd=lambda: set_file(dest_path))
	pw_file_path_browse_button.config(cmd=lambda: set_file(pw_file_path))
	preview_button.config(cmd=preview_database)
	save_button.config(cmd=save_)
	cancel_button.config(cmd=exit_)
	
	top_window_.mainloop()