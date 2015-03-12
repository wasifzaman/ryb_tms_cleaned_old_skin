import sys, os
sys.path.append(os.path.abspath(os.pardir))
sys.path.append(os.path.abspath(os.pardir) + '\widgets')
sys.path.append(os.path.abspath(os.pardir) + '\messages windows')

from tkinter import *
from Crypto.Cipher import AES
import pickle

from textbox import Textbox, TextboxNoEdit, IntTextbox, MoneyTextbox
from mbox2 import Mbox
from button import Buttonbox
from simple_label import Labelbox


def create_new_markerfile(lang):
	def return_(value):
		message_box.value = value
		message_box.marker_file = marker_file_textbox.getData()
		message_box.dw()

	def set_file(textbox):
		out_file = filedialog.asksaveasfilename()
		if len(out_file) != 0:
			textbox.setData(out_file + '.rybdb')

	message_box = Mbox()

	message_box.newFrame("First Frame", (0, 0))

	marker_file_textbox = TextboxNoEdit(text='Marker File', lang={'Marker File': 'Marker File'}, repr='marker_file')
	brw3 = Buttonbox(text='browse', lang=lang, repr='brw3')
	save_button = Buttonbox(text='Save', lang=lang, repr='save_button')
	cancel_button = Buttonbox(text='Cancel', lang=lang, repr='cancel_button')

	message_box.frames["First Frame"].addWidget(marker_file_textbox,(2, 0))
	message_box.frames["First Frame"].addWidget(brw3,(2, 2))
	message_box.frames["First Frame"].addWidget(save_button, (4, 1))
	message_box.frames["First Frame"].addWidget(cancel_button, (5, 1))

	marker_file_textbox.label.config(width=12)
	#brw3.button.config(width=7)
	#save_button.button.config(width=22)

	brw3.config(cmd=lambda: set_file(marker_file_textbox))
	save_button.config(cmd=lambda: return_('success'))
	cancel_button.config(cmd=lambda: return_('cancel'), lang=lang)

	message_box.root.wait_window()

	if message_box.value == 'cancel':
		return

	if message_box.marker_file.strip() != "":
		pickle.dump({}, open(message_box.marker_file, "wb"))

	print(message_box.value)
