import sys, os
sys.path.append(os.path.abspath(os.pardir) + '\widgets')
sys.path.append(os.path.abspath(os.pardir))

from uiHandler22 import Window, AppWindow
from button import Buttonbox
from tableWidget2 import Table
from photoWidget2 import Photo


def multiple_match(table_data):
	def set_(student_id):
		window_.student_id = student_id
		top_window_.destroy()

	def close():
		window_.student_id = False
		top_window_.destroy()

	top_window_ = Window(top=True)
	top_window_.attributes('-fullscreen', False)
	top_window_.geometry('560x460')
	top_window_.resizable(0, 0)
	top_window_.grab_set()
	top_window_.focus_set()
	top_window_.titleFrame.pack_forget()

	window_ = AppWindow(top_window_.mainFrame)

	window_.newFrame("Table Frame", (0, 0))

	teacher_table = Table(repr='teachertable')
	teacher_table_headers = ['Barcode', 'First name', 'Last name', 'Chinese name']
	close_button = Buttonbox(text='Close', repr=None)

	window_.frames["Table Frame"].addWidget(teacher_table, (0, 0))
	window_.frames["Table Frame"].addWidget(close_button, (1, 0))

	teacher_table.canvas.config(widt=530, height=400)

	window_.student_id = False
	teacher_table.setData(
		headers=teacher_table_headers,
		data=table_data)

	for pos, cell in teacher_table.cells.items():
		cell.config(bind=('<Double-Button-1>', lambda event, pos=pos: set_(teacher_table.data[pos[0]-1][0])))
	
	close_button.config(cmd=close)
	top_window_.protocol('WM_DELETE_WINDOW', close)
	
	top_window_.wait_window()
	
	return window_.student_id