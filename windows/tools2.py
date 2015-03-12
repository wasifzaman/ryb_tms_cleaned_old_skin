import sys, os
sys.path.append(os.path.abspath(os.pardir) + '\database')
sys.path.append(os.path.abspath(os.pardir) + '\widgets')
sys.path.append(os.path.abspath(os.pardir) + '\miscellaneous')
sys.path.append(os.path.abspath(os.pardir) + '\messages windows')
sys.path.append(os.path.abspath(os.pardir) + '\windows')
sys.path.append(os.path.abspath(os.pardir))

from datetime import datetime

from master_list import *
from uiHandler22 import Window, AppWindow
from preBuilts2 import *
from textbox import TextboxNoEdit, IntTextbox
from button import Buttonbox
from simple_label import Labelbox
from choose_school import choose_school
from create_new_db import create_new_db
from convert_to_encrypted import convert_to_encrypted
from password_prompt import password_prompt
from date_to_date import date_to_date
from find_all import find_all
from translations import english_to_chinese, chinese_to_english
from translate_ import translate
import addS3
import sDb22
import keeper
import importwiz
import sdb_salrep
import print_reports
import review_invoice


def main(parent_frame, lang, database):
	encr_config_file = keeper.Keeper('keeper.db')

	def change_database():
		file_path = filedialog.askopenfilename(filetypes=[('RYB database file', '.rybdb')])
		if len(file_path) == 0: return

		curdb.config(text=file_path)
		database.file = file_path
		encr_config_file.files['cfilepath'] = file_path
		encr_config_file.save()

	def ctdb():
		file_path = filedialog.askopenfilename(filetypes=[('Excel 97-2003 Workbook', '.xls'), ('Excel Workbook', '.xlsx')])
		if len(file_path) == 0: return

		database.loadData()
		ns, nt = database.importtimexlsx(file_path)
		ctimp(window_.lang, ns, nt)

	def set_pwfile():
		file_path = filedialog.askopenfilename(filetypes=[('RYB database file', '.rybdb')])
		if len(file_path) == 0: return

		file_ = open(file_path, 'rb')
		curpwfile.config(text=file_path)
		database.pwfile = file_path
		encr_config_file.files['pwfile'] = file_path
		encr_config_file.save()

	def set_markerfile(label):
		file_path = filedialog.askopenfilename(filetypes=[('RYB database file', '.rybdb')])
		if len(file_path) == 0: return

		label.config(text=file_path)
		encr_config_file.files['markerfile'] = file_path
		encr_config_file.save()

	def print_report_by_range():
		start_date, end_date = date_to_date(window_.lang)
		if not start_date: return

		dest_path = filedialog.askdirectory()
		if dest_path == None: return
		
		print_reports.print_teacher_attendance(database, dest_path, start_date, end_date)

	def print_report_by_range_simple():
		start_date, end_date = date_to_date(window_.lang)
		if not start_date: return

		dest_path = filedialog.askdirectory()
		if dest_path == None: return

		print_reports.print_teacher_attendance_simple(database, dest_path, start_date, end_date)

	def show_salrep():
		hide_tools()
		window_.frames["Table Frame"].grid(row=0, column=0)
		window_.frames["Button Frame"].grid(row=1, column=0)

	def show_teacher_database():
		hide_tools()
		window_.frames["Teacher Database Frame"].grid(row=0, column=0)
		window_.frames["Button Frame"].grid(row=1, column=0)

	def show_tools():
		window_.frames["Table Frame"].grid_forget()
		window_.frames["Teacher Database Frame"].grid_forget()
		window_.frames["Button Frame"].grid_forget()
		window_.frames["Toggle0 Frame"].grid(row=0, column=0, padx=10, sticky=N)
		window_.frames["Toggle Frame"].grid(row=0, column=1, padx=10, sticky=N)
		window_.frames["Toggle2 Frame"].grid(row=0, column=2, padx=10, sticky=N)

	def hide_tools():
		window_.frames["Toggle0 Frame"].grid_forget()
		window_.frames["Toggle Frame"].grid_forget()
		window_.frames["Toggle2 Frame"].grid_forget()		
	
	def choose_school_(event):
		school = choose_school(window_.lang)
		if school == 'cancel': return

		encr_config_file.files['school'] = school
		database.school = encr_config_file.files['school']
		current_school.setData(database.school)
		encr_config_file.save()

	def reset_dbmanager_pw(lang):
		new_pw = password_prompt(lang, encr_config_file.files['dbpw'])
		if new_pw == 'cancel': return
		if encr_config_file.hashpw(new_pw[0]) != encr_config_file.files['dbpw']:
			wrong_password(window_.lang)
			return
		encr_config_file.files['dbpw'] = encr_config_file.hashpw(new_pw[1])
		encr_config_file.files['resetpw'] = False
		encr_config_file.save()
		pw_reset_confirm(window_.lang)

	def create_new_markerfile():
		out_file = filedialog.asksaveasfilename()
		if len(out_file) == 0: return
		pickle.dump({}, open(out_file + '.rybdb', "wb"))

	def review_invoice_():
		month_year_ = month_year(window_.lang)
		if not month_year_[0]:
			return
		review_invoice.main(window_.lang, database, month_year_[0], month_year_[1], encr_config_file.files['markerfile'])


	window_ = AppWindow(parent_frame)

	window_.lang = lang

	window_.newFrame("Teacher Database Frame", (0, 0))
	window_.newFrame("Table Frame", (0, 0))
	window_.newFrame("Button Frame", (0, 0))
	window_.newFrame("Toggle0 Frame", (0, 0))
	window_.newFrame("Toggle Frame", (0, 1))
	window_.newFrame("Toggle2 Frame", (0, 2))
	
	window_.frames["Teacher Database Frame"].grid_forget()
	window_.frames["Table Frame"].grid_forget()
	window_.frames["Button Frame"].grid_forget()
	window_.frames["Toggle0 Frame"].grid(padx=10)
	window_.frames["Toggle Frame"].grid(padx=10)
	window_.frames["Toggle2 Frame"].grid(padx=10)
	
	teacher_database_button = Buttonbox(text='Teacher database', repr='teacher_database_button') #Student Database
	add_teacher_button = Buttonbox(text='Add teacher', repr='add_teacher_button') #Add Student
	import_export_toggle = Buttonbox(text='Import/export', repr=None)
	print_reports_toggle = Buttonbox(text='Print reports', repr=None)
	school_toggle = Buttonbox(text='School', repr=None)
	database_toggle = Buttonbox(text='Database', repr=None)
	password_toggle = Buttonbox(text='Passwords', repr=None)
	bchoose_school = Buttonbox(text='Choose school', lang=window_.lang, repr='bcschool')
	reset_db_manager_pw = Buttonbox(text='Reset DB manager PW', lang=window_.lang, repr='resetdbmanagerpw')
	print_report_button = Buttonbox(text='Print report', lang=window_.lang, repr='printreport')
	curdb = TextboxNoEdit(text='Database', repr=None)
	curpwfile = TextboxNoEdit(text='PW file', repr=None)
	curmarkerfile = TextboxNoEdit(text='Marker', repr=None)
	current_school = TextboxNoEdit(text='School', repr=None)
	choose_pwfile = Buttonbox(text='Choose PW file', lang=window_.lang, repr='cpwfile')
	choose_markerfile = Buttonbox(text='Choose Marker File', lang=window_.lang, repr='cmarkerfile')
	create_db = Buttonbox(text='Create new database', lang=window_.lang, repr='createdb')
	create_markerfile = Buttonbox(text='Create new markerfile', lang=window_.lang, repr='createmfile')
	import_data_button = Buttonbox(text='Import data', repr=None)
	import_time_data_button = Buttonbox(text='Import time data', repr=None)
	salary_report_button = Buttonbox(text='Salary report', repr=None)
	change_database_button = Buttonbox(text='Change database', repr=None)
	back_to_tools = Buttonbox(text='Back to tools', repr=None)
	review_invoice_button = Buttonbox(text='Review invoice', repr='test')
	#print_simple_attendance = Buttonbox(text='Print simple report', lang=window_.lang, repr='simplereport')
	#convert_db = Buttonbox(text='Convert to encrypted DB', lang=window_.lang, repr='convertdb')

	window_.frames["Toggle0 Frame"].addWidget(add_teacher_button, (0, 0))
	window_.frames["Toggle0 Frame"].addWidget(teacher_database_button, (1, 0))
	window_.frames["Toggle Frame"].addWidget(review_invoice_button, (0, 0))
	window_.frames["Toggle Frame"].addWidget(salary_report_button, (1, 0))
	window_.frames["Toggle Frame"].addWidget(print_report_button, (2, 0))
	window_.frames["Toggle Frame"].addWidget(bchoose_school, (4, 0))
	window_.frames["Toggle Frame"].addWidget(reset_db_manager_pw, (5, 0))
	window_.frames["Toggle Frame"].addWidget(import_data_button, (7, 0))
	window_.frames["Toggle Frame"].addWidget(import_time_data_button, (8, 0))
	window_.frames["Toggle2 Frame"].addWidget(curdb, (0, 0))
	window_.frames["Toggle2 Frame"].addWidget(curpwfile, (1, 0))
	window_.frames["Toggle2 Frame"].addWidget(curmarkerfile, (2, 0))
	window_.frames["Toggle2 Frame"].addWidget(change_database_button, (3, 0))
	window_.frames["Toggle2 Frame"].addWidget(choose_pwfile, (4, 0))
	window_.frames["Toggle2 Frame"].addWidget(choose_markerfile, (5, 0))
	window_.frames["Toggle2 Frame"].addWidget(create_markerfile, (6, 0))
	window_.frames["Toggle2 Frame"].addWidget(create_db, (7, 0))
	window_.frames["Button Frame"].addWidget(back_to_tools, (0, 0))
	#window_.frames["Toggle Frame"].addWidget(print_simple_attendance, (3, 0))
	#window_.frames["Toggle Frame"].addWidget(convert_db, (6, 0))

	''' hover button colors '''
	label_bg = 'tomato'
	hover_bg = 'crimson'

	''' widget settings '''
	salary_report_button.config(label_bg=label_bg, hover_bg=hover_bg, label_fg='black')
	review_invoice_button.config(label_bg=label_bg, hover_bg=hover_bg, label_fg='black')
	change_database_button.config(label_bg=label_bg, hover_bg=hover_bg, label_fg='black')
	curdb.label.config(width=8)
	curpwfile.label.config(width=8)
	curmarkerfile.label.config(width=8)
	curdb.entry.config(width=19)
	curpwfile.entry.config(width=19)
	curmarkerfile.entry.config(width=19)
	
	curdb.setData(encr_config_file.files['cfilepath'])
	curpwfile.setData(encr_config_file.files['pwfile'])
	curmarkerfile.setData(encr_config_file.files['markerfile'])

	bchoose_school.config(cmd=lambda: choose_school_(window_.lang))
	import_data_button.config(cmd=lambda: importwiz.main(window_.lang, database))
	change_database_button.config(cmd=lambda: change_database())
	import_time_data_button.config(cmd=ctdb)
	salary_report_button.config(cmd=show_salrep)
	teacher_database_button.config(cmd=show_teacher_database)
	choose_pwfile.config(cmd=lambda: set_pwfile())
	create_db.config(cmd=lambda: create_new_db(window_.lang, database))
	create_markerfile.config(cmd=create_new_markerfile)
	choose_markerfile.config(cmd=lambda: set_markerfile(curmarkerfile))
	reset_db_manager_pw.config(cmd=lambda: reset_dbmanager_pw(window_.lang))
	print_report_button.config(cmd=print_report_by_range)
	back_to_tools.config(cmd=show_tools)
	review_invoice_button.config(cmd=review_invoice_)
	add_teacher_button.config(cmd=lambda: addS3.main(window_.lang, database))
	#print_simple_attendance.config(cmd=print_report_by_range_simple)
	#convert_db.config(cmd=lambda: convert_to_encrypted(window_.lang, database))

	sdb_salrep.main(window_.frames["Table Frame"], window_.lang, database, encr_config_file.files['markerfile'])
	sDb22.main(window_.frames["Teacher Database Frame"], window_.lang, database)
	
	if lang == 'chinese':
		translate(window_, english_to_chinese)