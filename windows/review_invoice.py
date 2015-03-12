import sys, os
sys.path.append(os.path.abspath(os.pardir) + '\widgets')
sys.path.append(os.path.abspath(os.pardir) + '\database')
sys.path.append(os.path.abspath(os.pardir) + '\miscellaneous')
sys.path.append(os.path.abspath(os.pardir) + '\messages windows')

from datetime import datetime
import pickle

from uiHandler22 import Window, AppWindow
from textbox import TextboxNoEdit
from button import Buttonbox
from tableWidget2 import Table
from translations import english_to_chinese
from master_list import *
import print_reports

def main(lang, database, month, year, markerfile=False):
	def return_(value):
		if value:
			if not top_window_.data_valid:
				invoice_error(lang)
				return

			file_path = filedialog.askdirectory()
			today = datetime.now()
			date = today.strftime('%m.%d.%y')
			time = today.strftime('%I.%M.%p')

			for teacher_id, attendance in top_window_.invoice_teacher_data.items():
				print_reports.print_pay_entries(database, \
					file_path + '/Salary Report ' + teacher_id + ' ' + database.school + ' ' + date + ' ' + time + '.xlsx', \
					teacher_id,
					attendance,
					database.studentList[teacher_id].datapoints['pay_per_hour']
				)
				if markerfile:
					if teacher_id not in marker:
						marker[teacher_id] = {}
						marker[teacher_id]['paid_set'] = attendance
						marker[teacher_id]['color_set'] = ['tomato', 'cornflowerblue']
						marker[teacher_id]['current_color'] = 0
						marker[teacher_id]['row_color'] = {}
						for row_num in attendance:
							marker[teacher_id]['row_color'][row_num] = marker[teacher_id]['color_set'][marker[teacher_id]['current_color']]
					else:
						print(teacher_id, ' in marker file, appending..')
						marker[teacher_id]['current_color'] = (marker[teacher_id]['current_color'] + 1) % len(marker[teacher_id]['color_set'])
						print(marker[teacher_id]['current_color'])
						for row_num in attendance:
							marker[teacher_id]['row_color'][row_num] = marker[teacher_id]['color_set'][marker[teacher_id]['current_color']]
						marker[teacher_id]['paid_set'].update(attendance)
					print(marker)
					pickle.dump(marker, open(markerfile, "wb"))

			print_succesful(lang)

		top_window_.destroy()

	def find_issues():
		for cell_id, cell_val in invoice_table.cells.items():
			if cell_val.label.cget('text') == 'X':
				cell_val.label.config(bg='orange')
				top_window_.data_valid = False
			if cell_id[1] == 8:
				try:
					if (float(cell_val.getData()) > 12.0 or float(cell_val.getData()) == 0.0):
						cell_val.label.config(bg='orange')
						top_window_.data_valid = False
				except ValueError:
					continue

	def create_manual_attendance():
		if manual_attendance(lang, database):
			invoice_data = database.get_monthly_invoice(month, year)
			top_window_.invoice_table_data = invoice_data[0]
			top_window_.invoice_teacher_data = invoice_data[1]
			
			invoice_table.setData(
				headers=['' for i in range(0, len(top_window_.invoice_table_data[0]))],
				data=top_window_.invoice_table_data
			)

			invoice_table.remove_headers_numbers()
			find_issues()

	top_window_ = Window(top=True)
	top_window_.attributes('-fullscreen', False)
	top_window_.geometry('1280x740+1+1')
	top_window_.resizable(0, 0)
	top_window_.grab_set()
	top_window_.focus_set()
	top_window_.titleFrame.config(height=1)
	top_window_.wintitle.place_forget()

	window_ = AppWindow(top_window_.mainFrame)

	window_.newFrame("Table Frame", (0, 0))
	window_.newFrame("Button Frame", (1, 0))

	invoice_table = Table(repr='inv_table', edit=False)
	return_button = Buttonbox(text='Confirm', lang=lang, repr='rbutton')
	cancel_button = Buttonbox(text='Cancel', lang=lang, repr='cancelbutton')
	manual_attendance_button = Buttonbox(text='Manual Attendance', repr='test')
	
	invoice_data = database.get_monthly_invoice(month, year)
	top_window_.invoice_table_data = invoice_data[0]
	top_window_.invoice_teacher_data = invoice_data[1]
	top_window_.data_valid = True

	marker = pickle.load(open(markerfile, "rb")) if markerfile else False

	window_.frames["Table Frame"].addWidget(invoice_table, (0, 0))
	window_.frames["Button Frame"].addWidget(manual_attendance_button, (0, 0))
	window_.frames["Button Frame"].addWidget(return_button, (1, 0))
	window_.frames["Button Frame"].addWidget(cancel_button, (2, 0))

	manual_attendance_button.widget_frame.grid(sticky=E)

	invoice_table.setData(
		headers=['' for i in range(0, len(top_window_.invoice_table_data[0]))],
		data=top_window_.invoice_table_data
	)

	invoice_table.remove_headers_numbers()
	for cell_id, cell_val in invoice_table.cells.items():
		if cell_id[0] == 7:
				cell_val.label.config(bg='lightblue')
	invoice_table.cells[(1, 1)].label.config(bg='lightgreen')
	invoice_table.cells[(1, 2)].label.config(bg='lightgreen')
	invoice_table.cells[(3, 1)].label.config(bg='lightgreen')
	invoice_table.cells[(3, 2)].label.config(bg='lightgreen')
	invoice_table.cells[(4, 1)].label.config(bg='lightgreen')
	invoice_table.cells[(4, 2)].label.config(bg='lightgreen')
	invoice_table.cells[(5, 1)].label.config(bg='lightgreen')
	invoice_table.cells[(5, 2)].label.config(bg='lightgreen')

	find_issues()

	return_button.config(cmd=lambda: return_(True))
	cancel_button.config(cmd=lambda: return_(False))
	manual_attendance_button.config(cmd=create_manual_attendance)

	invoice_table.canvas.config(width=900, height=550)