import sys, os
sys.path.append(os.path.abspath(os.pardir))
sys.path.append(os.path.abspath(os.pardir) + '\miscellaneous')
sys.path.append(os.path.abspath(os.pardir) + '\widgets')

from tkinter import *
import pickle

from textbox import Textbox
from mbox2 import Mbox
from button import Buttonbox
from simple_label import Labelbox
from translations import english_to_chinese, chinese_to_english
from translate_ import translate


def password_prompt(lang, reset_pw):
	def get_return(value):
		if value == 'pw_mismatch':
			return
		message_box.value = value
		message_box.dw()

	message_box = Mbox()

	message_box.newFrame("Top Frame", (0, 0))
	message_box.newFrame("First Frame", (1, 0))
	message_box.newFrame("Second Frame", (2, 0))

	no_pw_detected = Labelbox(text="Password must be reset. Please enter the old password followed by the new password", lang=lang, repr='nopwsetpw')
	old_pw_textbox = Textbox(text="Old password", lang={"Old Password": "Old Password"}, repr='oldpwtextbox')
	new_pw_textbox = Textbox(text="New password", lang={"New Password": "New Password"}, repr='newpwtextbox')
	retype_new_pw_textbox = Textbox(text="Retype new password", lang={"Retype New Password": "Retype New Password"}, repr='retypenewpwtextbox')
	pw_textbox = Textbox(text="Password", lang={"Password": "Password"}, repr='oldpwtextbox')
	ok_button = Buttonbox(text='Ok', lang=None, repr='ok_button')
	save_button = Buttonbox(text='Save', lang=None, repr='save_button')
	cancel_button = Buttonbox(text='Cancel', lang=None, repr='cancel_button')


	if reset_pw:
		message_box.frames["Top Frame"].addWidget(no_pw_detected, (0, 0))
		message_box.frames["First Frame"].addWidget(old_pw_textbox, (1, 0))
		message_box.frames["First Frame"].addWidget(new_pw_textbox, (2, 0))
		message_box.frames["First Frame"].addWidget(retype_new_pw_textbox, (3, 0))
		message_box.frames["Second Frame"].addWidget(save_button, (0, 1))
		save_button.config(cmd=lambda: get_return((old_pw_textbox.getData(), new_pw_textbox.getData())) if new_pw_textbox.getData() == retype_new_pw_textbox.getData() else get_return('pw_mismatch'))
		save_button.label.config(width=10)
		save_button.widget_frame.grid(padx=5)
		old_pw_textbox.label.config(width=19)
		new_pw_textbox.label.config(width=19)
		retype_new_pw_textbox.label.config(width=19)
		no_pw_detected.label.config(wraplength=250, justify=LEFT)
	else:
		message_box.frames["First Frame"].addWidget(pw_textbox, (0, 0))
		message_box.frames["Second Frame"].addWidget(ok_button, (0, 1))
		pw_textbox.label.config(width=8)
		ok_button.config(cmd=lambda: get_return(pw_textbox.getData()))
		ok_button.label.config(width=10)
		ok_button.widget_frame.grid(padx=5)

	message_box.frames["Second Frame"].addWidget(cancel_button, (0, 0))
	
	cancel_button.label.config(width=10)
	cancel_button.widget_frame.grid(padx=5)
	
	cancel_button.config(cmd=lambda: get_return('cancel'))

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)

	message_box.root.wait_window()

	return message_box.value