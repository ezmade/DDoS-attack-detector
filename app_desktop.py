import ddos_detector
from app_components import *
from pandas import read_csv


def btn_scan_clicked(key):
    if (model_list.get() == DEFAULT_MODEL_LIST[0]) and (file_list.get() == DEFAULT_FILE_LIST[0]):
        messagebox.showwarning('Warning!', 'Choose model and file to start scanning!')
    elif (model_list.get() == DEFAULT_MODEL_LIST[0]):
        messagebox.showwarning('Warning!', 'Choose model to start scanning!')
    elif (file_list.get() == DEFAULT_FILE_LIST[0]):
        messagebox.showwarning('Warning!', 'Choose file to start scanning!')
    else:
        try:
            numbers_of_count = int(records_count.get())
            scanning(numbers_of_count)
        except:
            messagebox.showwarning('Warning!', "Incorrect value of records' number!")


def btn_clear_clicked(key):
    result_text_field.delete(1.0, END)


def scanning(number_of_records):
    model = ddos_detector.load_model(f'DDoS-attack-detector\Model\{model_list.get()}')
    data = read_csv(f'DDoS-attack-detector\Data\{file_list.get()}')
    dataset = data.iloc[:,:8]
    data = ddos_detector.label_encoding(data)
    if number_of_records > 10000 or number_of_records == 0:
        number_of_records = 10000
    for record in range (0, number_of_records):
        prediction = ddos_detector.predict_ddos_attack(model, data.iloc[record])
        if prediction != -1:
            result_text_field.insert(INSERT, f'{dataset.iloc[record]} \nAttack Status: {prediction} \n \n')
        else:
            result_text_field.insert(INSERT, "Something goes wrong! Check your dataset!\n")


if __name__ == '__main__':
    window.title("DDoS Attacks Detector")
    window.geometry(f'{WIN_WIDTH}x{WIN_HEIGHT}')

    btn_scan.bind('<ButtonPress>', btn_scan_clicked)
    btn_clear.bind('<ButtonPress>', btn_clear_clicked)

    model_list['values'] = DEFAULT_MODEL_LIST
    model_list.current(0)

    file_list['values'] = DEFAULT_FILE_LIST
    file_list.current(0)

    records_count.insert(0, 15)


    lbl.grid(columnspan=4, row=0)
    btn_scan.grid(column=2, row=4)
    btn_clear.grid(column=3, row=4)
    model_list.grid(column=0, row=1)
    file_list.grid(column=1, row=1)
    records_count.grid(column=3, row=1)
    lbl_records_count.grid(column=2, row=1)
    result_text_field.grid(columnspan=4, row=8)

    window.mainloop()
