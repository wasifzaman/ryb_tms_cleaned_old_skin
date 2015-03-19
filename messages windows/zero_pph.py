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
from button import Buttonbox
from tableWidget2 import Table
from simple_label import Labelbox
from translations import english_to_chinese, chinese_to_english
from translate_ import translate


def zero_pph(lang, zero_pph_teachers, valid_pph_teachers):
	def return_(value):
		message_box.value = value
		message_box.dw()

	message_box = Mbox()

	message_box.newFrame("Zero PPH Label Frame", (0, 0))
	message_box.newFrame("Valid PPH Label Frame", (0, 1))
	message_box.newFrame("Zero PPH Table Frame", (1, 0))
	message_box.newFrame("Valid PPH Table Frame", (1, 1))
	message_box.newFrame("Button Frame", (2, 0))

	message_box.frames["Button Frame"].grid(columnspan=2)

	zero_pph_label = Labelbox(text='Invalid pay per hour', repr='zpphlabel')
	valid_pph_label = Labelbox(text='Valid pay per hour', repr='vpphlabel')
	warning_label = Labelbox(text='Warning: teachers in the invalid table will be printed with $0.00 pay per hour', repr='warninglabel')
	zero_pph_table = Table(repr='zp_table', edit=False)
	valid_pph_table = Table(repr='vp_table', edit=False)
	print_all = Buttonbox(text='Yes, print all', lang=lang, repr='printall')
	print_valid = Buttonbox(text='Print valid only', lang=lang, repr='printvalid')
	no_button = Buttonbox(text='Cancel', lang=lang, repr='no_button')

	message_box.frames["Zero PPH Label Frame"].addWidget(zero_pph_label, (0, 0))
	message_box.frames["Valid PPH Label Frame"].addWidget(valid_pph_label, (0, 0))
	message_box.frames["Zero PPH Table Frame"].addWidget(zero_pph_table, (0, 0))
	message_box.frames["Valid PPH Table Frame"].addWidget(valid_pph_table, (0, 0))
	message_box.frames["Button Frame"].addWidget(warning_label, (0, 0))
	message_box.frames["Button Frame"].addWidget(print_all, (1, 0))
	message_box.frames["Button Frame"].addWidget(print_valid, (1, 1))
	message_box.frames["Button Frame"].addWidget(no_button, (1, 2))

	if len(zero_pph_teachers) > 0:
		zero_pph_table.setData(
			headers=['Barcode', 'First name', 'Last name', 'Chinese name'],
			data=zero_pph_teachers
		)
		zero_pph_table.set_width(1, 4, 14)

	if len(valid_pph_teachers) > 0:
		valid_pph_table.setData(
			headers=['Barcode', 'First name', 'Last name', 'Chinese name'],
			data=valid_pph_teachers
		)
		valid_pph_table.set_width(1, 4, 14)

	zero_pph_table.canvas.config(width=550, height=300)
	valid_pph_table.canvas.config(width=550, height=300)
	warning_label.widget_frame.grid(columnspan=3)
	print_all.widget_frame.grid(sticky=E+W, padx=5)
	print_valid.widget_frame.grid(sticky=E+W, padx=5)
	no_button.widget_frame.grid(sticky=E+W, padx=5)
	print_all.config(cmd=lambda: return_('all'))
	print_valid.config(cmd=lambda: return_('valid_only'))
	no_button.config(cmd=lambda: return_(False))
	no_button.label.focus_set()

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)
		
	message_box.root.wait_window()

	return message_box.value