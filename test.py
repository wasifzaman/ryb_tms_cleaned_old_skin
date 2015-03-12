from tkinter import *


t = Tk()

#f = Frame(t, bg='red', width=200, height=200)
#f2 = Frame(f, bg='blue', width=200, height=200)

#f.pack()
#f2.pack()


'''
b = Button(text='test', command=lambda: t.state('zoomed'))
b2 = Button(text='test2', command=lambda: t.state('normal'))
b2.pack()
b.pack()
'''

tup = (0, 0, 5, 5)
f = Frame(t)
c = Canvas(f, bg='red', width=30, height=300)
c.config(scrollregion=(0, 0, 0, 0))
f2 = Frame(c)
yscroll = Scrollbar(f, orient="vertical", command=c.yview)
b1 = Button(f, text='Up')
b2 = Button(f, text='Down')

b1.pack()
b2.pack()

c.create_window((0, 0), window=f2, anchor=NW)

Label(f2, text='test').pack()
Label(f2, text='test2').pack()


f.pack(side=LEFT)
yscroll.pack(side=RIGHT, fill=Y)
c.pack()

def move_up():
	c.yview_scroll(1, UNITS)
	return

def move_down():
	c.yview_scroll(-1, UNITS)

b1.config(command=move_up)
b2.config(command=move_down)

x = 'abcdef'
x = str.encode(x)
print(bytearray(x))


#t.mainloop()