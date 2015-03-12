import sys, os
sys.path.append(os.path.abspath(os.pardir) + '\windows')
sys.path.append(os.path.abspath(os.pardir) + '\widgets')
sys.path.append(os.path.abspath(os.pardir) + '\database')
sys.path.append(os.path.abspath(os.pardir) + '\miscellaneous')
sys.path.append(os.path.abspath(os.pardir) + '\messages windows')
sys.path.append(os.path.abspath(os.pardir))
images = os.path.abspath(os.pardir) + '\images\\' #image directory

from tkinter import *
from tkinter import filedialog
from datetime import datetime
import configparser

from master_list import *
from choose_school import choose_school
from password_prompt import password_prompt
from uiHandler22 import Window, AppWindow, AppFrame
from dataHandler import StudentDB
from translations import english_to_chinese, chinese_to_english
from translate_ import translate
from photoWidget2 import Photo
from find_all import find_all
import keeper
import print_reports
import scanS22
import scanOut
import tools2


def main():
	def switch_language():
		if window_.lang == 'english':
			window_.lang = 'chinese'
			translate(window_, english_to_chinese)
			change_language_button.label.config(text='English')
		else:
			window_.lang = 'english'
			translate(window_, chinese_to_english)
			change_language_button.label.config(text='中文')

	def showWindow(f, optional=False):
		#if optional and optional == 'add':
		#	main_window_.require_confirm = [True] #pass it as list to preserve reference
		if optional and optional == 'tools':
			if encr_config_file.files['resetpw']:
				new_pw = password_prompt(window_.lang, encr_config_file.files['dbpw'])
				if new_pw == 'cancel':
					return
				if encr_config_file.hashpw(new_pw[0]) != encr_config_file.files['dbpw']:
					wrong_password(window_.lang)
					return
				encr_config_file.files['dbpw'] = encr_config_file.hashpw(new_pw[1])
				encr_config_file.files['resetpw'] = False
				encr_config_file.save()
				pw_reset_confirm(window_.lang)
			else:
				pw_input = password_prompt(window_.lang, False)
				if pw_input == 'cancel':
					return
				if not encr_config_file.hashpw(pw_input) == encr_config_file.files['dbpw']:
					wrong_password(window_.lang)
					return

		if optional and optional == 'add':
			f(window_.frames["App Frame"], window_.lang, database, main_window_.require_confirm, return_to_main)
		else:	
			f(window_.frames["App Frame"], window_.lang, database)

		''' hide main window '''
		main_window_.titleFrame.config(height=1)
		main_window_.wintitle.place_forget()
		window_.frames["Button Frame"].grid_forget()
		window_.frames["Image Frame"].grid_forget()
		window_.frames["Dock Frame"].grid_forget()

		''' show opened window '''
		window_.frames["App Frame"].grid(row=1, padx=10, pady=10)
		window_.frames["Return Button Frame"].grid()

	def return_to_main():
		if hasattr(main_window_, 'require_confirm') and main_window_.require_confirm[0]:
			if not confirm_return_to_main_window(window_.lang): return
			main_window_.require_confirm = [False]

		app_window_widgets = []
		find_all(window_.frames['App Frame'], app_window_widgets, 'all')

		for widget in app_window_widgets:
			widget.destroy()

		window_.frames['App Frame'].grid_forget()
		main_window_.titleFrame.config(height=60)
		main_window_.wintitle.place(in_=main_window_.titleFrame, anchor="c", relx=.5, rely=.5)

		window_.frames['App Frame'].grid_forget()
		window_.frames["Button Frame"].grid(row=0, column=0, sticky=N+W)
		window_.frames["Image Frame"].grid(row=0, column=1, rowspan=2)
		window_.frames["Dock Frame"].grid(row=1, column=0, sticky=SE+W)
		window_.frames['Return Button Frame'].grid_forget()

		#encr_config_file.files['cfilepath'] = database.file
		#encr_config_file.save()

	def printPrompt():
		output_path = filedialog.askdirectory()
		if output_path != '':
			print_reports.exportreport(database, output_path, datetime.strftime(datetime.now(), '%m/%d/%Y'))
		else:
			return
		teacher_report_print_successful(window_.lang)
	
	def export_database():
		output_path = filedialog.askdirectory()
		if output_path == '':
			return
		today = datetime.now()
		date = today.strftime('%m.%d.%y')
		time = today.strftime('%I.%M.%p')
		database.exportdb(output_path + '/RYB Teacher Backup - ' + database.school + ' ' + date + ' ' + time + '.rybdb')			
		database_backup_successful(window_.lang)
	
	main_window_ = Window()
	main_window_.attributes('-fullscreen', False)
	main_window_.geometry('1280x740+1+1')
	main_window_.wm_title("RYB Teacher Attendance")

	window_ = AppWindow(main_window_.mainFrame)
	config = configparser.ConfigParser()
	config.read(os.path.abspath(os.pardir) + '\config.ini', encoding='utf-8')
	window_.lang = config['DEFAULT']['DEFAULT_LANGUAGE']

	window_.newFrame("Button Frame", (0, 0))
	window_.newFrame("Image Frame", (0, 1))
	window_.newFrame("Dock Frame", (1, 0))
	window_.newFrame("App Frame", (1, 0))
	window_.newFrame("Return Button Frame", (2, 0))

	window_.frames['App Frame'].grid_forget()
	window_.frames['Return Button Frame'].grid_forget()

	choose_school_button = Buttonbox(text='Choose school', repr='bcschool')	
	check_in_button = Buttonbox(text='Check-in teacher', repr='check_in_button') #Scan Student
	check_out_button = Buttonbox(text='Check-out teacher', repr='check_out_button') #Scan Student
	
	tools_button = Buttonbox(text='Tools', repr='tools_button') #Database Management
	back_to_main_menu_button = Buttonbox(text='Back to main menu', repr='back_to_main_menu_button') #Return to Main Menu
	exit_button = Buttonbox(text='Exit', repr='exit_button') #Exit
	print_report_button = Buttonbox(text='Print report', repr='print_report_button') #Print end of day report
	export_button = Buttonbox(text='Export database', repr='export_button')
	splash_image = Photo(repr='splash', path=os.path.abspath(images + 'background_IMG.jpg'))
	change_language_button = Buttonbox(text='E', repr='change_language_button') #Change Language
	
	window_.frames["Button Frame"].addWidget(check_in_button, (1, 0))
	window_.frames["Button Frame"].addWidget(check_out_button, (2, 0))
	window_.frames["Button Frame"].addWidget(export_button, (4, 0))
	window_.frames["Button Frame"].addWidget(print_report_button, (5, 0))
	window_.frames["Button Frame"].addWidget(change_language_button, (6, 0))
	window_.frames["Button Frame"].addWidget(exit_button, (7, 0))
	window_.frames["Image Frame"].addWidget(splash_image, (0, 0))
	window_.frames["Return Button Frame"].addWidget(back_to_main_menu_button, (0, 0))
	#window_.frames["Button Frame"].addWidget(tools_button, (4, 0))
	
	window_.frames["Image Frame"].grid(rowspan=2)
	window_.frames["Dock Frame"].config(bg='#B9B8E0')
	window_.frames["Button Frame"].config(bg='black')
	window_.frames["Button Frame"].grid(sticky=N+W)
	window_.frames["Dock Frame"].grid(sticky=SE+W)
	#window_.frames["Dock Frame"].addWidget(change_language_button, (0, 0))

	''' hover button colors '''
	label_bg = '#E3E9F9'
	hover_bg = '#405DB2'

	''' widget settings '''
	#add_teacher_button.config(label_bg=label_bg, hover_bg=hover_bg, label_fg='black')
	check_in_button.config(label_bg=label_bg, hover_bg=hover_bg, label_fg='black')
	check_out_button.config(label_bg=label_bg, hover_bg=hover_bg, label_fg='black')
	#teacher_database_button.config(label_bg=label_bg, hover_bg=hover_bg, label_fg='black')
	#tools_button.config(label_bg=label_bg, hover_bg=hover_bg, label_fg='black')
	export_button.config(label_bg=label_bg, hover_bg=hover_bg, label_fg='black')
	print_report_button.config(label_bg=label_bg, hover_bg=hover_bg, label_fg='black')
	change_language_button.config(label_bg=label_bg, hover_bg=hover_bg, label_fg='black')
	exit_button.config(label_bg=label_bg, hover_bg=hover_bg, label_fg='black')
	back_to_main_menu_button.config(label_bg=label_bg, hover_bg=hover_bg, label_fg='black')
	#export_button.config()#image=images + 'backup.png', image_resize=(28, 28))
	#print_report_button.config(label_bg='#366BFF', hover_bg='#4785FF')#, image=images + 'print.png', image_resize=(28, 28))
	#exit_button.config(label_bg='#FC354C', hover_bg='#CC0C39')#, image=images + 'close.png', image_resize=(28, 28))
	#change_language_button.config(label_bg='#C0D860', hover_bg='#789048')
	#change_language_button.label.config(width=4)
	#change_language_button.widget_frame.grid(pady=0)
	splash_image.label.config(bg='black')
	#tools_button.widget_frame.grid_forget()
	main_window_.titleFrame.config(bg='#353432')
	main_window_.wintitle.config(bg='#353432')
	main_window_.wintitle.config(text='RYB Student Management')
	main_window_.iconbitmap(os.path.abspath(images + 'RYB_Attendance.ico'))
	#export_button.label.config(width=4)
	#export_button.widget_frame.grid(pady=0)
	#print_report_button.label.config(width=4)
	#print_report_button.widget_frame.grid(pady=0)
	#exit_button.label.config(width=4)
	#exit_button.widget_frame.grid(pady=0)

	encr_config_file = keeper.Keeper('keeper.db')
	database = StudentDB(file=encr_config_file.files['cfilepath'], pwfile=encr_config_file.files['pwfile'], cfile=encr_config_file.fname)

	if 'school' not in encr_config_file.files:
		encr_config_file.files['school'] = choose_school(window_.lang)
		if encr_config_file.files['school'] == 'cancel': encr_config_file.files['school'] = 'Flushing'
		database.school = encr_config_file.files['school']
		encr_config_file.save()
	else:
		print(encr_config_file.files['school'])
		database.school = encr_config_file.files['school']
	
	#add_teacher_button.config(cmd=lambda: showWindow(addS3.main, 'add'))
	check_in_button.config(cmd=lambda: showWindow(scanS22.main))
	check_out_button.config(cmd=lambda: showWindow(scanOut.main))
	#tools_button.config(cmd=lambda: showWindow(tools2.main, 'tools'))
	back_to_main_menu_button.config(cmd=return_to_main)
	print_report_button.config(cmd=printPrompt)
	exit_button.config(cmd=main_window_.destroy)
	change_language_button.config(cmd=switch_language)
	export_button.config(cmd=export_database)
	splash_image.label.bind('<Control-Alt-Shift-D>', lambda event: showWindow(tools2.main, 'tools'))

	if window_.lang == 'chinese':
		translate(window_, english_to_chinese)
		change_language_button.label.config(text='E')
	else:
		change_language_button.label.config(text='中文')

	main_window_.mainloop()

main()