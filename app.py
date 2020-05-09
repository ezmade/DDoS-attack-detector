from tkinter import messagebox, scrolledtext, Label, Button, Tk, INSERT, END
from tkinter.ttk import Combobox
from random import randint
from ddos_detector import *


def btn_scan_clicked():
    if (proto_list.get() == DEFAULT_PROTO_LIST[0]):
        messagebox.showwarning('Warning!', 'Choose protocol to start scanning!')
    else:
        lbl.configure(text='Scanning has been started.')
        scanning()


def btn_stop_clicked():
    lbl.configure(text=LBL_DEFAULT_TEXT)
    result_text_field.delete(1.0, END)


def scanning():
    for i in range(0, 15):
        result_text_field.insert(INSERT, '%s port scanning in process: Packages get: %d,\t Packages sent: %d \n' %(proto_list.get(), randint(0, 20), randint(0, 20)))


WIN_WIDTH = 800
WIN_HEIGHT = 600
FONT_NAME = 'Courier New'
FONT_SIZE = 14
IS_SCAN = False
DEFAULT_PROTO_LIST= ('Choose protocol to scan', 'UDP', 'TCP', 'HTTP', 'All')
LBL_DEFAULT_TEXT = 'Neural network is waiting to start scanning your system'


# Создание и описание элементов экрана
window = Tk()
lbl = Label(window, text=LBL_DEFAULT_TEXT, font=(FONT_NAME,FONT_SIZE))
btn_scan = Button(window, text='Scan', font=(FONT_NAME, FONT_SIZE), bg='#3f3f3f', fg='#ffffff', command=btn_scan_clicked)
btn_stop = Button(window, text='Stop', font=(FONT_NAME, FONT_SIZE), bg='#ff3333', fg='#ffffff', command=btn_stop_clicked)
proto_list = Combobox(window)
result_text_field = scrolledtext.ScrolledText(window, width=100, height=35)


if __name__ == '__main__':
    window.title("DDoS Attacks Detector")
    window.geometry('%sx%s' % (WIN_WIDTH, WIN_HEIGHT))

    proto_list['values'] = DEFAULT_PROTO_LIST
    proto_list.current(0)

    # Сетка отображения элементов на экране
    # TODO Использовать метод place или pack вместо grid

    lbl.grid(column=0, row=0)
    btn_scan.grid(column=0, row=2)
    btn_stop.grid(column=1, row=2)
    proto_list.grid(column=0, row=1)
    result_text_field.grid(column=0, row=5)

    window.mainloop()
