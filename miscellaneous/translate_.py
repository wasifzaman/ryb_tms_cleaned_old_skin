from tkinter import *
from find_all import find_all

def translate(root, translation_lib):
	label_lib = []
	find_all(root, label_lib, Label)
	find_all(root, label_lib, Radiobutton)

	for label in label_lib:
		if label.cget('text') in translation_lib:
			label.config(text=translation_lib[label.cget('text')])