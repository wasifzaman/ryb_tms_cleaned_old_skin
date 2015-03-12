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
from translations import english_to_chinese
from translate_ import translate


def convert_to_encrypted(lang, database):
	def return_(value):
		message_box.value = value
		message_box.to_encrypt_file = to_encrypt_file_textbox.getData()
		message_box.db_file = db_file_textbox.getData()
		message_box.pw_file = pw_file_textbox.getData()
		message_box.pw = pw_textbox.getData()
		message_box.dw()

	def set_file(textbox):
		out_file = filedialog.asksaveasfilename()
		if len(out_file) != 0:
			textbox.setData(out_file + '.rybdb')

	def open_file(textbox):
		out_file = filedialog.askopenfile()
		if out_file != None:
			textbox.setData(out_file.name)

	message_box = Mbox()

	message_box.newFrame("First Frame", (0, 0))
	message_box.newFrame("Button Frame", (1, 0))

	to_encrypt_file_textbox = Textbox(text='Unencrypted', lang={'Unencrypted File': 'Unencrypted File'}, repr='unc_db_file')
	db_file_textbox = Textbox(text='Encrypt file', lang={'Encrypt File To': 'Encrypt File To'}, repr='db_file')
	pw_file_textbox = Textbox(text='Password file', lang={'Password File': 'Password File'}, repr='pw_file')
	pw_textbox = Textbox(text='Password', lang={'Password': 'Password'}, repr='pw')
	brw1 = Buttonbox(text='Browse', lang=lang, repr='brw1')
	brw2 = Buttonbox(text='Browse', lang=lang, repr='brw2')
	brw3 = Buttonbox(text='Browse', lang=lang, repr='brw3')
	save_button = Buttonbox(text='Save', lang=lang, repr='save_button')
	cancel_button = Buttonbox(text='Cancel', lang=lang, repr='cancel_button')

	message_box.frames["First Frame"].addWidget(to_encrypt_file_textbox, (0, 0))
	message_box.frames["First Frame"].addWidget(db_file_textbox,(1, 0))
	message_box.frames["First Frame"].addWidget(pw_file_textbox,(2, 0))
	message_box.frames["First Frame"].addWidget(brw3, (0, 1))
	message_box.frames["First Frame"].addWidget(brw1, (1, 1))
	message_box.frames["First Frame"].addWidget(brw2, (2, 1))
	message_box.frames["First Frame"].addWidget(pw_textbox, (3, 0))
	message_box.frames["Button Frame"].addWidget(save_button, (0, 0))
	message_box.frames["Button Frame"].addWidget(cancel_button, (1, 0))

	db_file_textbox.label.config(width=12)
	pw_file_textbox.label.config(width=12)
	to_encrypt_file_textbox.config(width=12)
	pw_textbox.label.config(width=12)
	brw1.config(width=7)
	brw2.config(width=7)
	brw3.config(width=7)
	brw1.label.config(height=1)
	brw2.label.config(height=1)
	brw3.label.config(height=1)
	brw1.widget_frame.grid(padx=5)
	brw2.widget_frame.grid(padx=5)
	brw3.widget_frame.grid(padx=5)
	#save_button.button.config(width=22)

	brw1.config(cmd=lambda: set_file(db_file_textbox))
	brw2.config(cmd=lambda: set_file(pw_file_textbox))
	brw3.config(cmd=lambda: open_file(to_encrypt_file_textbox))
	save_button.config(cmd=lambda: return_('success'))
	cancel_button.config(cmd=lambda: return_('cancel'), lang=lang)

	message_box.root.wait_window()

	if message_box.value == 'cancel':
		return

	key = str.encode(message_box.pw)
	studentList = pickle.load(open(message_box.to_encrypt_file, 'rb'))
	cipher = AES.new(key, AES.MODE_CFB, database.iv)
	binary_string = pickle.dumps(studentList)
	encrypted = cipher.encrypt(binary_string)

	f = open(message_box.db_file, 'wb')
	f.write(bytearray(encrypted))
	f.close()

	f = open(message_box.pw_file, 'wb')
	f.write(bytearray(str.encode(message_box.pw)))
	f.close()