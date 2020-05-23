from tkinter import messagebox, scrolledtext, Label, Button, Tk, INSERT, END
from tkinter.ttk import Combobox
from os import listdir


def get_files_from_root(folder_name, file_extension):
    files = listdir(folder_name)
    files = list(filter(lambda x: x.endswith(file_extension), files))
    if file_extension=='.sav':
        files.insert(0, 'Choose model')
    elif file_extension=='.csv':
        files.insert(0, 'Choose file')
    return files


WIN_WIDTH = 750
WIN_HEIGHT = 650
FONT_NAME = 'Courier New'
FONT_SIZE = 14
DEFAULT_MODEL_LIST = get_files_from_root('Model', '.sav')
DEFAULT_FILE_LIST = get_files_from_root('Data', '.csv')
LBL_DEFAULT_TEXT = 'Neural network is waiting to start scanning'


# Создание и описание элементов экрана
window = Tk()
lbl = Label(window, text=LBL_DEFAULT_TEXT, font=(FONT_NAME,FONT_SIZE))
btn_scan = Button(window, width = 12, text='Scan', font=(FONT_NAME, FONT_SIZE), bg='#3333ff', fg='#ffffff')
btn_clear = Button(window, width = 12, text='Clear', font=(FONT_NAME, FONT_SIZE), bg='#3f3f3f', fg='#ffffff')
model_list = Combobox(window)
file_list = Combobox(window)
result_text_field = scrolledtext.ScrolledText(window, width=100, height=35)