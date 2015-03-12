import sys, os
sys.path.append(os.path.abspath(os.pardir) + '\widgets')
sys.path.append(os.path.abspath(os.pardir) + '\messages windows')
images = os.path.abspath(os.pardir) + '\images\\' #image directory

from textbox import Textbox, TextboxNoEdit, IntTextbox, MoneyTextbox
from date_textbox import Datebox
from seek_category import Picker
from multiline_textbox import LongTextbox
from simple_label import Labelbox
from button import Buttonbox
from tableWidget2 import Table
from photoWidget2 import Photo

from languages import *
from mbox2 import *
from tkinter import filedialog
import pickle
from datetime import datetime
import tkinter.ttk as ttk

language = languages["english"]

firstName = Textbox(text="First Name", lang=language, repr='firstName')
lastName = Textbox(text="Last Name", lang=language, repr='lastName')
chineseName = Textbox(text="Chinese Name", lang=language, repr='chineseName')
schoolLoc = Textbox(text="School Location", lang=language, repr='schoolLoc')
bCode = Textbox(text="Barcode", lang=language, repr='bCode')
bCodeNE = TextboxNoEdit(text="Barcode", lang=language, repr='bCode')
gender = Textbox(text="Gender", lang=language, repr='gender')
parentName = Textbox(text="Parent Name", lang=language, repr='parentName')
pup = Textbox(text="Pick up Person", lang=language, repr='pup')
addr = Textbox(text="Address", lang=language, repr='addr')
state = Textbox(text="State", lang=language, repr='state')
city = Textbox(text="City", lang=language, repr='city')
wkdwknd = Textbox(text="Weekday/Weekend", lang=language, repr='wkdwknd')
ctime = Textbox(text="Class time", lang=language, repr='ctime')
email = Textbox(text="E-mail", lang=language, repr='email')
sType = Textbox(text="Service Type", lang=language, repr='sType')
hPhone = Textbox(text="Home Phone", lang=language, repr='hPhone')
cPhone = Textbox(text="Cell Phone", lang=language, repr='cPhone')
cPhone2 = Textbox(text="Cell Phone 2", lang=language, repr='cPhone2')
cp = Textbox(text="Card Printed", lang=language, repr='cp')
age = IntTextbox(text="Age", lang=language, repr='age')
sid = IntTextbox(text="Old Student ID", lang=language, repr='sid')
zip = IntTextbox(text="Zipcode", lang=language, repr='zip')
cAwarded = IntTextbox(text="Classes Awarded", lang=language, repr='cAwarded')
cRemaining = IntTextbox(text="Classes Remaining", lang=language, repr='cRemaining')
dob = Datebox(text="Date of Birth", lang=language, repr='dob')
tpd = Datebox(text="Tuition Paid Day", lang=language, repr='tpd')
tpa = MoneyTextbox(text="Tuition Pay Amount", lang=language, repr='tpa')
tpo = MoneyTextbox(text="Amount Owed", lang=language, repr='tpo')
tp = MoneyTextbox(text="Already Paid", lang=language, repr='tp')
attinfo = Table(repr='attinfo', edit=True)
portr = Photo(repr='portr', path=images + 'monet_sm.jpg')


attinfoh = [language['Date'], language['Check-In Time'], language['Class Time']]
#attinfo.build(headers=attinfoh, data=[[]])
attinfo.clast = '#FF99FF'




sby = Picker(repr='sby', text=language['Search By'], rads=[(language['Barcode'], 'bCode'), \
	(language['First Name'], 'firstName'), \
	(language['Last Name'], 'lastName'), \
	(language['Chinese Name'], 'chineseName'), \
	(language['Phone Number'], 'phoneNumber')])

#info titles
sinfo = Labelbox(text='Student information', lang=language, repr='sinfo')
ainfo = Labelbox(text='Address information', lang=language, repr='ainfo')
cinfo = Labelbox(text='Contact information', lang=language, repr='cinfo')
pinfo = Labelbox(text='Payment information', lang=language, repr='pinfo')
ninfo = Labelbox(text='Notes', lang=language, repr='ninfo')

#early checkin
checkin25 = TextboxNoEdit(text='25s', lang=language, repr='25s')
checkin50 = TextboxNoEdit(text='50s', lang=language, repr='50s')
checkin100 = TextboxNoEdit(text='100s', lang=language, repr='100s')
early_checkin = TextboxNoEdit(text='Early Check-in', lang=language, repr='inrow')


notes = LongTextbox(text="Notes", lang=language, repr='notes')
ws = Photo(repr='ws', path=images + 'ws_sm.png')
hs = Photo(repr='hs', path=images + 'halt_sm.png')
cm = Photo(repr='cm', path=images + 'check_mark_sm.png')
bok = Buttonbox(text='ok', lang=language, repr='bok')
byes = Buttonbox(text='yes', lang=language, repr='byes')
bno = Buttonbox(text='no', lang=language, repr='bno')
bcancel = Buttonbox(text='Cancel', lang=language, repr='bcancel')
imp = Labelbox(text='impdb', lang=language, repr='imp', bold=True)
impt = Labelbox(text='impt', lang=language, repr='impt', bold=True)
exp = Labelbox(text='expdb', lang=language, repr='exp', bold=True)
curfile = Labelbox(text='curfile', lang=language, repr='curfile', bold=True)
curdbs = Labelbox(text='', lang=language, repr='curdb')
saveto = Labelbox(text='saveto', lang=language, repr='saveto')
bimp = Buttonbox(text='impxls', lang=language, repr='bimp')
bimpt = Buttonbox(text='imptxls', lang=language, repr='bimpt')
bexp = Buttonbox(text='expxls', lang=language, repr='bexp')
bsav = Buttonbox(text='Save', lang=language, repr='bsav')
bcdb = Buttonbox(text='choosedb', lang=language, repr='bcdb')
bsalrep = Buttonbox(text='salrep', lang=language, repr='bsrep')
bclang = Buttonbox(text='changelanguage', lang=language, repr='bclang')
bsearch = Buttonbox(text='Search', lang=language, repr='bsearch')
back = Buttonbox(text='Back', lang=language, repr='back')
next_ = Buttonbox(text='Next', lang=language, repr='bimp')
brw = Buttonbox(text='browse', lang=language, repr='brw')
fpath = Textbox(text='filepath', lang=language, repr='fpath')
brw2 = Buttonbox(text='browse', lang=language, repr='brw2')
fpath2 = Textbox(text='filepath', lang=language, repr='fpath2')
brwp = Buttonbox(text='browsephoto', lang=language, repr='brwp')

bok.width = 10
byes.width = 10
bno.width = 10
bcancel.width = 10

def clang():
	if w.lang['self'] == 'english':
		w.lang = languages['chinese']
	else:
		w.lang = languages['english']
	for frame in w.frames.values():
		for widget in frame.widgets.values():
			widget.config(lang=w.lang)
