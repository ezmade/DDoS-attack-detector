import ddos_detector
from app_components import *
import time

SCAN = False

def btn_scan_clicked(key):
    if (model_list.get() == DEFAULT_MODEL_LIST[0]) and (file_list.get() == DEFAULT_FILE_LIST[0]):
        messagebox.showwarning('Warning!', 'Choose model and file to start scanning!')
    elif (model_list.get() == DEFAULT_MODEL_LIST[0]):
        messagebox.showwarning('Warning!', 'Choose model to start scanning!')
    elif (file_list.get() == DEFAULT_FILE_LIST[0]):
        messagebox.showwarning('Warning!', 'Choose file to start scanning!')
    elif SCAN:
        messagebox.showwarning('Warning!', 'Scanning is in process!')
    else:
        lbl.configure(text='Scanning has been started.')
        time.sleep(10)
        scanning(15)


def btn_clear_clicked(key):
    result_text_field.delete(1.0, END)


def scanning(records_count):
    SCAN = True
    predictions = ddos_detector.predict_ddos_attack(model_list.get(), file_list.get())
    if predictions:
        for i in range(0, records_count):
            result_text_field.insert(INSERT, predictions[records_count])
    else:
        result_text_field.insert(INSERT, "Something goes wrong! Check your dataset!")

    SCAN = False
    # lbl.configure(text=LBL_DEFAULT_TEXT)


if __name__ == '__main__':
    window.title("DDoS Attacks Detector")
    window.geometry(f'{WIN_WIDTH}x{WIN_HEIGHT}')

    btn_scan.bind('<ButtonPress>', btn_scan_clicked)
    btn_clear.bind('<ButtonPress>', btn_clear_clicked)

    model_list['values'] = DEFAULT_MODEL_LIST
    model_list.current(0)

    file_list['values'] = DEFAULT_FILE_LIST
    file_list.current(0)

    # Сетка отображения элементов на экране
    # TODO Использовать метод place или pack вместо grid

    lbl.grid(column=0, row=0)
    btn_scan.grid(column=0, row=3)
    btn_clear.grid(column=0, row=5)
    model_list.grid(column=0, row=1)
    file_list.grid(column=0, row=2)
    result_text_field.grid(column=0, row=7)

    window.mainloop()
