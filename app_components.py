from tkinter import messagebox, scrolledtext, Label, Button, Tk, INSERT, END, Entry
from tkinter.ttk import Combobox
from os import listdir


def get_files_from_root(folder_name, file_extension):
    files = listdir(folder_name)
    files = list(filter(lambda x: x.endswith(file_extension), files))
    return files


WIN_WIDTH = 680
WIN_HEIGHT = 620
FONT_NAME = 'Courier New'
FONT_SIZE = 14
DEFAULT_MODEL_LIST = get_files_from_root('DDoS-attack-detector\\models', '.sav')
DEFAULT_FILE_LIST = get_files_from_root('DDoS-attack-detector\\data', '.csv')
LBL_DEFAULT_TEXT = 'Choose file and model and press "Scan"'


# Создание и описание элементов экрана
window = Tk()
lbl = Label(window, text=LBL_DEFAULT_TEXT, font=(FONT_NAME,FONT_SIZE))
lbl_records_count = Label(window, text='Number of records:', font=(FONT_NAME, FONT_SIZE))
btn_scan = Button(window, width = 8, text='Scan', font=(FONT_NAME, FONT_SIZE), bg='#3333ff', fg='#ffffff')
btn_clear = Button(window, width = 8, text='Clear', font=(FONT_NAME, FONT_SIZE), bg='#3f3f3f', fg='#ffffff')
model_list = Combobox(window)
file_list = Combobox(window)
records_count = Entry(window, width=15)
result_text_field = scrolledtext.ScrolledText(window, width=65, height=35, font=(FONT_NAME, 12))