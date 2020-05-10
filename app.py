from tkinter import messagebox, scrolledtext, Label, Button, Tk, INSERT, END
from tkinter.ttk import Combobox
from os import listdir
import ddos_detector



def btn_scan_clicked():
    if (model_list.get() == DEFAULT_MODEL_LIST[0]) and (file_list.get() == DEFAULT_FILE_LIST[0]):
        messagebox.showwarning('Warning!', 'Choose model and file to start scanning!')
    elif (model_list.get() == DEFAULT_MODEL_LIST[0]):
        messagebox.showwarning('Warning!', 'Choose model to start scanning!')
    elif (file_list.get() == DEFAULT_FILE_LIST[0]):
        messagebox.showwarning('Warning!', 'Choose file to start scanning!')
    else:
        lbl.configure(text='Scanning has been started.')
        scanning()


def btn_stop_clicked():
    lbl.configure(text=LBL_DEFAULT_TEXT)
    result_text_field.delete(1.0, END)


def scanning():
    predictions = ddos_detector.predict_ddos_attack(model_list.get(), 'Combined.csv')
    for i in range(0, 15):
        result_text_field.insert(INSERT, predictions[i]) #(INSERT, f'{proto_list.get()} file scanning in process: Packages get: %d,\t Packages sent: %d \n' %(proto_list.get(), randint(0, 20), randint(0, 20)))


def get_files_from_root(folder_name, file_extension):
    files = listdir(folder_name)
    files = filter(lambda x: x.endswith(file_extension), files)
    return files


WIN_WIDTH = 800
WIN_HEIGHT = 600
FONT_NAME = 'Courier New'
FONT_SIZE = 14
IS_SCAN = False
DEFAULT_MODEL_LIST = list(get_files_from_root('Model', '.sav'))
DEFAULT_FILE_LIST = list(get_files_from_root('Data', '.csv'))
LBL_DEFAULT_TEXT = 'Neural network is waiting to start scanning'


# Создание и описание элементов экрана
window = Tk()
lbl = Label(window, text=LBL_DEFAULT_TEXT, font=(FONT_NAME,FONT_SIZE))
btn_scan = Button(window, text='Scan', font=(FONT_NAME, FONT_SIZE), bg='#3f3f3f', fg='#ffffff', command=btn_scan_clicked)
btn_stop = Button(window, text='Stop', font=(FONT_NAME, FONT_SIZE), bg='#ff3333', fg='#ffffff', command=btn_stop_clicked)
model_list = Combobox(window)
file_list = Combobox(window)
result_text_field = scrolledtext.ScrolledText(window, width=100, height=35)


if __name__ == '__main__':
    window.title("DDoS Attacks Detector")
    window.geometry('%sx%s' % (WIN_WIDTH, WIN_HEIGHT))

    model_list['values'] = DEFAULT_MODEL_LIST
    model_list.current(0)

    file_list['values'] = DEFAULT_FILE_LIST
    file_list.current(0)

    # Сетка отображения элементов на экране
    # TODO Использовать метод place или pack вместо grid

    lbl.grid(column=0, row=0)
    btn_scan.grid(column=0, row=3)
    btn_stop.grid(column=1, row=3)
    model_list.grid(column=0, row=1)
    file_list.grid(column=0, row=2)
    result_text_field.grid(column=0, row=5)

    window.mainloop()
