import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import csv

law_parent_id = 0
law_list_order = 0
law_index = ''
article_code = ''
chapter = 0
section = 0
article = 0
sub_article = 0
action_code = 0
action_list_order = 0
subject_code = 0
subject_list_order = 0
data = {}
csvFilePath = "C:\\Users\\Akhjarkhyn\\Desktop\\demoReg\\demoReg.csv"


def build_law_index():
    global law_index
    law_index = ''.join([
        inputList[2].get() if inputList[2].get() else '',
        '.' + inputList[3].get() if inputList[3].get() else '',
        '-' + inputList[4].get() if inputList[4].get() else '',
        '.' + inputList[5].get() if inputList[5].get() else ''
    ])
    return law_index

def construct_data():
    selected_radio = radio_var.get()
    if selected_radio == "Action":
        data["TYPE"] = 3
    elif selected_radio == "Subject":
        data["TYPE"] = 2
    else:
        data["TYPE"] = 1

    data["PARENT_ID"] = int(inputList[0].get())
    data["CODE"] = code_textbox.get()
    data["NAME"] = large_text_inputList[0].get("1.0", "end-1c")
    data["INFO"] = large_text_inputList[1].get("1.0", "end-1c")
    data["LIST_ORDER"] = int(inputList[1].get())
    data["ATTRIBUTE_TORGUULI_MIN"] = int(inputList[6].get()) if inputList[6].get() is not '' else ''
    data["ATTRIBUTE_TORGUULI_MAX"] = int(inputList[7].get()) if inputList[7].get() is not '' else ''
    data["ATTRIBUTE_NEGJ"] = int(isNegj.get())
    data["ATTRIBUTE_ERH_HASAH"] = int(isErhHasah.get())
    data["ATTRIBUTE_BARIVCHLAH"] = int(isBarivchlah.get())
    data["ATTRIBUTE_ALBADLAGA"] = int(isAlbadlaga.get())
    data["ATTRIBUTE_TUSGAI_JURAM"] = int(isTusgaiJuram.get())
    data["ATTRIBUTE_TUSGAI_SUNGALT"] = int(isTusgaiSungalt.get())
    data["ATTRIBUTE_STATUTE_OF_LIMITATIONS"] = int(inputList[8].get()) if inputList[8].get() is not '' else ''
    data["ATTRIBUTE_ARTICLE_CODE"] = article_code if selected_radio == "Action" else ''
    data["ATTRIBUTE_CODE_PREFIX"] = article_code if selected_radio == "Subject" else ''
    print(data)
    with open(csvFilePath, mode='a', newline='', encoding="UTF-8") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        writer.writerow(data)

    print("Data appended to the CSV file.")


def on_radio_change(*args):
    clear_form()
    selected_radio = radio_var.get()
    if selected_radio == "Action":
        recall_prev_action_data()
        disable_law_attributes()
    elif selected_radio == "Subject":
        recall_prev_sub_data()
        disable_law_attributes()
    else:
        enable_law_attributes()
        recall_prev_law_data()


def disable_law_attributes():
    checkbox_barivchlah.config(state="disabled")
    checkbox_is_negj.config(state="disabled")
    checkbox__erh_hasah.config(state="disabled")
    checkbox_TusgaiSungalt.config(state="disabled")
    checkbox_albadlaga.config(state="disabled")
    checkbox_TusgaiJuram.config(state="disabled")
    inputList[6].config(state="disabled")
    inputList[7].config(state="disabled")
    inputList[8].config(state="disabled")
    large_text_inputList[1].config(state="disabled")


def enable_law_attributes():
    checkbox_barivchlah.config(state="normal")
    checkbox_is_negj.config(state="normal")
    checkbox__erh_hasah.config(state="normal")
    checkbox_TusgaiSungalt.config(state="normal")
    checkbox_albadlaga.config(state="normal")
    checkbox_TusgaiJuram.config(state="normal")
    inputList[6].config(state="normal")
    inputList[7].config(state="normal")
    inputList[8].config(state="normal")
    large_text_inputList[1].config(state="normal")


def clear_form():
    for entry in inputList:  # Clear all input fields except the first one (PARENT_ID)
        entry.delete(0, tk.END)
    for text_input in large_text_inputList:
        text_input.delete("1.0", tk.END)
    code_textbox.delete(0, tk.END)
    article_textbox.delete(0, tk.END)

def format_input(value):
    # Return '00' if the input is empty, otherwise prepend '0' if single digit
    return '00' if value == '' else (value if len(value) > 1 else '0' + value)


def recall_prev_law_data():
    global law_list_order, law_parent_id
    global chapter, section, article, sub_article
    inputList[0].insert(0, str(law_parent_id) if law_parent_id > 0 else '')
    inputList[1].insert(0, str(law_list_order) if law_list_order > 0 else '')
    inputList[2].insert(0, str(chapter) if chapter > 0 else '')
    inputList[3].insert(0, str(section) if section > 0 else '')
    inputList[4].insert(0, str(article) if article > 0 else '')
    inputList[5].insert(0, str(sub_article) if sub_article > 0 else '')
    show_law_code()


def recall_prev_action_data():
    global action_code, action_list_order, article_code
    code_textbox.insert(0, str(action_code))
    inputList[1].insert(0, str(action_list_order))
    inputList[0].insert(0, "52704")
    article_textbox.insert(0, str(article_code))


def recall_prev_sub_data():
    global subject_code, subject_list_order, article_code
    code_textbox.insert(0, str(subject_code))
    inputList[0].insert(0, "52703")
    inputList[1].insert(0, str(subject_list_order))
    article_textbox.insert(0, str(article_code))


def show_law_code():
    fn_chapter = format_input(inputList[2].get())
    fn_section = format_input(inputList[3].get())
    fn_article = format_input(inputList[4].get())
    fn_sub_article = format_input(inputList[5].get())
    fn_law_index = build_law_index()
    fn_law_code = "11" + fn_chapter + fn_section + fn_article + fn_sub_article
    # Display LawCode in the result field
    if large_text_inputList[0].get("1.0", "end-1c"):
        large_text_inputList[0].delete("1.0", "end-1c")
    large_text_inputList[0].insert("1.0", fn_law_index)
    code_textbox.delete(0, tk.END)  # Clear existing content
    code_textbox.insert(0, fn_law_code)  # Insert the LawCode


def on_set_button_clicked():
    selected_radio = radio_var.get()
    if selected_radio == "Action":
        set_action_data()
    elif selected_radio == "Subject":
        set_subject_data()
    else:
        set_law_data()


def set_law_data():
    global law_list_order, law_parent_id, article_code
    global chapter, section, article, sub_article
    law_parent_id = int(inputList[0].get()) if inputList[0].get() else 0
    law_list_order = int(inputList[1].get()) if inputList[1].get() else 0
    chapter = int(inputList[2].get()) if inputList[2].get() else 0
    section = int(inputList[3].get()) if inputList[3].get() else 0
    article = int(inputList[4].get()) if inputList[4].get() else 0
    sub_article = int(inputList[5].get()) if inputList[5].get() else 0
    article_code = code_textbox.get()
    build_law_index()
    show_law_code()

def set_action_data():
    global action_code, action_list_order
    action_code = int(code_textbox.get()) if code_textbox.get() else 0
    action_list_order = int(inputList[1].get()) if inputList[1].get() else 0


def set_subject_data():
    global subject_code, subject_list_order
    subject_code = int(code_textbox.get()) if code_textbox.get() else 0
    subject_list_order = int(inputList[1].get()) if inputList[1].get() else 0


def on_save_button_clicked():
    construct_data()
    messagebox.showinfo(title="success")
    selected_radio = radio_var.get()
    if selected_radio == "Action":
        set_next_action_data()
    elif selected_radio == "Subject":
        set_next_subject_data()
    else:
        set_next_law_data()

def on_generate_next_button_clicked():
    selected_radio = radio_var.get()
    if selected_radio == "Action":
        set_next_action_data()
    elif selected_radio == "Subject":
        set_next_subject_data()
    else:
        set_next_law_data()


def set_next_law_data():
    global chapter, section, article, sub_article, law_list_order
    if law_list_order > 0:
        law_list_order += 10
        inputList[1].delete(0, tk.END)
        inputList[1].insert(0, str(law_list_order))
    if sub_article > 0:
        sub_article += 1
        inputList[5].delete(0, tk.END)
        inputList[5].insert(0, str(sub_article))
    elif article > 0:
        article += 1
        inputList[4].delete(0, tk.END)
        inputList[4].insert(0, str(article))
    elif section > 0:
        section += 1
        inputList[3].delete(0, tk.END)
        inputList[3].insert(0, str(section))
    elif chapter > 0:
        chapter += 1
        inputList[2].delete(0, tk.END)
        inputList[2].insert(0, str(chapter))
    show_law_code()
    set_law_data()


def set_next_action_data():
    global action_list_order, action_code
    action_list_order += 10
    action_code += 1
    inputList[1].delete(0, tk.END)
    inputList[1].insert(0, str(action_list_order))
    code_textbox.delete(0, tk.END)
    code_textbox.insert(0, str(action_list_order))
    set_action_data()


def set_next_subject_data():
    global subject_list_order, subject_code
    subject_list_order += 10
    subject_code += 1
    inputList[1].delete(0, tk.END)
    inputList[1].insert(0, str(subject_list_order))
    code_textbox.delete(0, tk.END)
    code_textbox.insert(0, str(subject_code))
    set_subject_data()

# Initialize Tkinter and create the main window
frame = tk.Tk()
frame.title("Reg Form Demo")
frame.attributes("-topmost", 1)

# Creating and placing 'PARENT_ID' and 'LIST_ORDER' input fields
parent_id_label = tk.Label(frame, text="PARENT_ID")
parent_id_label.grid(row=0, column=0)
parent_id_input = tk.Entry(frame)
parent_id_input.grid(row=0, column=1)

list_order_label = tk.Label(frame, text="LIST_ORDER")
list_order_label.grid(row=0, column=2)
list_order_input = tk.Entry(frame)
list_order_input.grid(row=0, column=3)

# Labels names for Chapter, Section, Article, sub_article
labels_text = ["Chapter", "Section", "Article", "sub_article"]
inputList = [parent_id_input, list_order_input]  # index 1, 2

# Creating and placing labels and input fields for Chapter, Section, Article, sub_article
for i, text in enumerate(labels_text):
    label = tk.Label(frame, text=text)
    label.grid(row=1, column=i)
    entry = tk.Entry(frame)
    entry.grid(row=2, column=i)
    inputList.append(entry)

# Creating and placing large text input fields for NAME and INFO
large_text_inputList = []
large_text_labels = ["NAME", "INFO"]
for i, text in enumerate(large_text_labels):
    label = tk.Label(frame, text=text)
    label.grid(row=3 + 2 * i, column=0, sticky='nw')  # Adjust the row index
    text_input = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=5, width=40, font=("Arial Unicode MS", 12))
    text_input.grid(row=4 + 2 * i, column=0, columnspan=4, sticky='ew')  # Span across all columns
    large_text_inputList.append(text_input)

penalty_min_label = tk.Label(frame, text="TORGUULI_MIN/MAX")
penalty_min_label.grid(row=8, column=0)
penalty_min_input = tk.Entry(frame)
penalty_min_input.grid(row=8, column=1)
inputList.append(penalty_min_input)  # index 6
penalty_max_input = tk.Entry(frame)
penalty_max_input.grid(row=8, column=2)
inputList.append(penalty_max_input)  # index 7
isNegj = tk.BooleanVar()
checkbox_is_negj = tk.Checkbutton(frame, text="HUWI", variable=isNegj)
checkbox_is_negj.grid(row=8, column=3)

statute_of_limitation_label = tk.Label(frame, text="STATUTE OF LIMITATION")
statute_of_limitation_label.grid(row=9, column=0)
statute_of_limitation_input = tk.Entry(frame)
statute_of_limitation_input.grid(row=9, column=1)
inputList.append(statute_of_limitation_input)  # index 8

isErhHasah = tk.BooleanVar()
isBarivchlah = tk.BooleanVar()
isAlbadlaga = tk.BooleanVar()
isTusgaiJuram = tk.BooleanVar()
isTusgaiSungalt = tk.BooleanVar()

# Create and pack the checkboxes
checkbox__erh_hasah = tk.Checkbutton(frame, text="Erh hasah", variable=isErhHasah)
checkbox_barivchlah = tk.Checkbutton(frame, text="Barivchlah", variable=isBarivchlah)
checkbox_albadlaga = tk.Checkbutton(frame, text="Albadlaga", variable=isAlbadlaga)
checkbox_TusgaiJuram = tk.Checkbutton(frame, text="Tusgai Juram", variable=isTusgaiJuram)
checkbox_TusgaiSungalt = tk.Checkbutton(frame, text="Sungalt", variable=isTusgaiSungalt)

checkbox__erh_hasah.grid(row=11, column=0)
checkbox_barivchlah.grid(row=11, column=1)
checkbox_albadlaga.grid(row=11, column=2)
checkbox_TusgaiJuram.grid(row=11, column=3)
checkbox_TusgaiSungalt.grid(row=12, column=0)

radio_var = tk.StringVar(value="LAW")  # Set the initial value to "LAW"
radio_var.trace_add("write", on_radio_change)  # Bind the function to the variable

law_radio = tk.Radiobutton(frame, text="LAW", variable=radio_var, value="LAW")
law_radio.grid(row=14, column=0)

subject_radio = tk.Radiobutton(frame, text="Subject", variable=radio_var, value="Subject")
subject_radio.grid(row=14, column=1)

action_radio = tk.Radiobutton(frame, text="Action", variable=radio_var, value="Action")
action_radio.grid(row=14, column=2)

# Result field and button
code_label = tk.Label(frame, text="Code: ")
code_label.grid(row=15, column=0, sticky='e')
code_textbox = tk.Entry(frame, state='normal')
code_textbox.grid(row=15, column=1)

article_label = tk.Label(frame, text="Article/Prefix: ")
article_label.grid(row=15, column=2, sticky='e')
article_textbox = tk.Entry(frame, state='normal')
article_textbox.grid(row=15, column=3)

generate_button = tk.Button(frame, text="next", command=on_generate_next_button_clicked)
generate_button.grid(row=16, column=4)
save_button = tk.Button(frame, text="save", command=on_save_button_clicked)
save_button.grid(row=16, column=3)
set_button = tk.Button(frame, text="set", command=on_set_button_clicked)
set_button.grid(row=16, column=2)
# Start the Tkinter event loop
frame.mainloop()
