import sys, os
sys.path.append(os.path.abspath(os.pardir) + '\widgets')
sys.path.append(os.path.abspath(os.pardir) + '\miscellaneous')
sys.path.append(os.path.abspath(os.pardir) + '\messages windows')

from tkinter import *

from mbox2 import Mbox
from button import Buttonbox
from simple_label import Labelbox
from translations import english_to_chinese, chinese_to_english
from translate_ import translate


def choose_school(lang):
	def return_(value):
		message_box.value = value
		message_box.dw()

	message_box = Mbox()
	message_box.root.protocol('WM_DELETE_WINDOW', lambda: False)

	message_box.newFrame("First Frame", (0, 0))

	button_brooklyn = Buttonbox(text='Brooklyn', lang=lang, repr='bklyn')
	button_elmhurst = Buttonbox(text='Elmhurst', lang=lang, repr='el')
	button_flushing = Buttonbox(text='Flushing', lang=lang, repr='flu')
	button_chinatown = Buttonbox(text='Chinatown', lang=lang, repr='ct')
	bcancel = Buttonbox(text='Cancel', lang=lang, repr='bcancel')

	message_box.frames["First Frame"].addWidget(button_flushing, (0, 0))
	message_box.frames["First Frame"].addWidget(button_chinatown, (1, 0))
	message_box.frames["First Frame"].addWidget(button_elmhurst, (2, 0))
	message_box.frames["First Frame"].addWidget(button_brooklyn, (3, 0))
	message_box.frames["First Frame"].addWidget(bcancel, (4, 0))

	button_brooklyn.config(cmd=lambda: return_('Brooklyn'), lang=lang)
	button_elmhurst.config(cmd=lambda: return_('Elmhurst'), lang=lang)
	button_flushing.config(cmd=lambda: return_('Flushing'), lang=lang)
	button_chinatown.config(cmd=lambda: return_('Chinatown'), lang=lang)
	bcancel.config(cmd=lambda: return_('cancel'), lang=lang)

	bcancel.idlebg = 'tomato'
	bcancel.fg = 'black'
	bcancel.hoverfg = 'white'
	bcancel.hoverbg = 'crimson'
	#bcancel.button.config(bg=bcancel.idlebg, fg=bcancel.fg)

	if lang == 'chinese':
		translate(message_box.root, english_to_chinese)
		
	message_box.root.wait_window()
	
	return message_box.value