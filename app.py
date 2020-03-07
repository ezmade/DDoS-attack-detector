from tkinter import messagebox, scrolledtext, Label, Button, Tk, INSERT, END
from tkinter.ttk import Combobox
from random import randint

isScan = False

def btnStartClicked():
    if (protoList.get() == defaultProtoList[0]):
        messagebox.showwarning('Warning!', 'Choose protocol to start scanning!')
    else:
        lbl.configure(text='Scanning has been started.')
        scanning()


def btnStopClicked():
    lbl.configure(text='Neural network is waiting to start scanning your system.')
    resultTextField.delete(1.0, END)


def scanning():
    for i in range(0, 15):
        resultTextField.insert(INSERT, '%s port scanning in process: Packages get: %d,\t Packages sent: %d \n' %(protoList.get(), randint(0, 20), randint(0, 20)))


win_width = 800
win_height = 600
defaultProtoList = ('Choose protocol to scan', 'UDP', 'TCP', 'HTTP', 'All')


# Создание и описание элементов экрана
window = Tk()
lbl = Label(window, text='Neural network is waiting to start scanning your system', font=('JetBrains Mono',15))
btnStart = Button(window, text='Start', font=('JetBrains Mono', 14), bg='#3f3f3f', fg='#ffffff', command=btnStartClicked)
btnStop = Button(window, text='Stop', font=('JetBrains Mono', 14), bg='#ff3333', fg='#ffffff', command=btnStopClicked)
protoList = Combobox(window)
resultTextField = scrolledtext.ScrolledText(window, width=100, height=35)


if __name__ == '__main__':
    window.title("DDoS Attacks Detector")
    window.geometry('%sx%s' % (win_width, win_height))

    protoList['values'] = defaultProtoList
    protoList.current(0)

    # Сетка отображения элементов на экране
    # TODO Использовать метод place или pack вместо grid

    lbl.grid(column=0, row=0)
    btnStart.grid(column=0, row=2)
    btnStop.grid(column=1, row=2)
    protoList.grid(column=0, row=1)
    resultTextField.grid(column=0, row=5)

    window.mainloop()
