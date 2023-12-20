import atexit
import json
import os
import time
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import csv

import pyperclip
import keyboard


def format_input(value):
    # Return '00' if the input is empty, otherwise prepend '0' if single digit
    return '00' if value == '' else (value if len(value) > 1 else '0' + value)


class LawApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("Reg Form Demo")
        self.master.attributes("-topmost", 1)

        # FILE PROPERTY
        self.user_home_dir = os.path.expanduser("~")
        self.csv_file_path = os.path.join(self.user_home_dir, "Desktop")
        self.csv_file_name = "huuli.csv"
        self.recovery_file_path = os.path.join(self.user_home_dir, "Documents")
        self.recovery_file_name = "giz-huuli-recovery"

        # instance attributes
        self.law_parent_id = 0
        self.law_list_order = 0
        self.law_index = ''
        self.chapter = 0
        self.section = 0
        self.article = 0
        self.sub_article = 0
        self.article_code = ''
        self.action_code = 0
        self.action_list_order = 0
        self.subject_code = 0
        self.subject_list_order = 0
        self.data = {}

        # Initialize UI components
        self.padx = 5
        self.pady = 5
        self.inputList = []
        self.large_text_inputList = []
        self.code_textbox = None
        self.article_textbox = None

        # checkbox variables
        self.isNegj = tk.BooleanVar()
        self.isErhHasah = tk.BooleanVar()
        self.isBarivchlah = tk.BooleanVar()
        self.isAlbadlaga = tk.BooleanVar()
        self.isTusgaiJuram = tk.BooleanVar()
        self.isTusgaiSungalt = tk.BooleanVar()
        self.isPublished = tk.BooleanVar(value=True)

        # radiobutton
        self.radio_var = tk.StringVar(value="LAW")
        self.setup_styles()
        self.setup_inputs()
        self.setup_large_text_inputs()
        self.setup_checkboxes()
        self.setup_radio_buttons()
        self.setup_result_and_buttons()
        self.setup_shortcut()

        atexit.register(lambda: self.save_to_file())

    def setup_shortcut(self):
        keyboard.add_hotkey("ctrl+n", lambda: self.copy_and_paste_into_name(), suppress=True)
        keyboard.add_hotkey("ctrl+i", lambda: self.copy_and_paste_into_info(), suppress=True)
        keyboard.add_hotkey("ctrl+1", lambda: self.toggle_checkbox(1), suppress=True)
        keyboard.add_hotkey("ctrl+2", lambda: self.toggle_checkbox(2), suppress=True)
        keyboard.add_hotkey("ctrl+3", lambda: self.toggle_checkbox(3), suppress=True)
        keyboard.add_hotkey("ctrl+4", lambda: self.toggle_checkbox(4), suppress=True)
        keyboard.add_hotkey("ctrl+5", lambda: self.toggle_checkbox(5), suppress=True)
        keyboard.add_hotkey("ctrl+6", lambda: self.toggle_checkbox(6), suppress=True)
        keyboard.add_hotkey("ctrl+enter", lambda: self.on_save_button_clicked(), suppress=True)
        keyboard.add_hotkey("ctrl+shift+enter", lambda: self.on_set_button_clicked())
        keyboard.add_hotkey("ctrl+q", lambda: self.toggle_radio_button(), suppress=True)
        keyboard.add_hotkey("ctrl+right", lambda: self.on_generate_next_button_clicked(), suppress=True)

    def setup_styles(self):
        self.master.style = ttk.Style()
        self.master.style.configure('TCheckbutton', font=('Arial', 12))
        self.master.style.configure('TRadiobutton', font=('Arial', 12))
        self.master.style.configure('TEntry', font=('Arial', 12))
        self.master.style.configure('TButton', font=('Arial', 12))
        self.master.style.configure('TLabel', font=('Arial', 12, "bold"))
        self.master.columnconfigure(0, minsize=50, weight=0)
        self.master.columnconfigure(1, minsize=50, weight=0)
        self.master.columnconfigure(2, minsize=50, weight=0)
        self.master.columnconfigure(3, minsize=50, weight=0)

    def setup_inputs(self):
        align = 'nw'
        # PARENT_ID and LIST_ORDER input fields
        ttk.Label(self.master, width=20, text="Parent Id").grid(row=0, column=0, padx=self.padx, pady=self.pady,
                                                                sticky=align)
        parent_id_input = ttk.Entry(self.master)
        parent_id_input.grid(row=0, column=1, padx=self.padx, pady=self.pady, sticky=align)
        self.inputList.append(parent_id_input)

        ttk.Label(self.master, width=20, text="List order").grid(row=0, column=2, padx=self.padx, pady=self.pady,
                                                                 sticky=align)
        list_order_input = ttk.Entry(self.master)
        list_order_input.grid(row=0, column=3, padx=self.padx, pady=self.pady, sticky=align)
        self.inputList.append(list_order_input)

        # Chapter, Section, Article, sub_article inputs
        labels_text = ["Chapter", "Section", "Article", "sub_article"]
        for i, text in enumerate(labels_text):
            ttk.Label(self.master, width=20, text=text).grid(row=1, column=i)
            entry = ttk.Entry(self.master)
            entry.grid(row=2, column=i)
            self.inputList.append(entry)

        ttk.Label(self.master, text="Torguuli").grid(row=8, column=0, padx=self.padx, pady=self.pady, sticky=align)
        penalty_min_input = ttk.Entry(self.master)
        penalty_min_input.grid(row=8, column=1, padx=self.padx, pady=self.pady, sticky=align)  # index 6
        self.inputList.append(penalty_min_input)

        penalty_max_input = ttk.Entry(self.master)
        penalty_max_input.grid(row=8, column=2, padx=self.padx, pady=self.pady, sticky=align)
        self.inputList.append(penalty_max_input)  # index 7

        ttk.Label(self.master, text="Limitations").grid(row=9, column=0, padx=self.padx, pady=self.pady, sticky=align)
        statute_of_limitation_input = ttk.Entry(self.master)
        statute_of_limitation_input.grid(row=9, column=1, padx=self.padx, pady=self.pady, sticky=align)
        self.inputList.append(statute_of_limitation_input)  # index 8

    def setup_large_text_inputs(self):
        # NAME and INFO large text inputs
        large_text_labels = ["NAME", "INFO"]
        for i, text in enumerate(large_text_labels):
            ttk.Label(self.master, text=text).grid(row=3 + 2 * i, column=0, sticky='nw')
            text_input = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, height=5, width=40,
                                                   font=("Arial Unicode MS", 12))
            text_input.grid(row=4 + 2 * i, column=0, columnspan=4, sticky='ew')
            self.large_text_inputList.append(text_input)

    def setup_checkboxes(self):
        # Setup for Checkboxes
        checkbox_align = 'w'
        self.checkbox_negj = ttk.Checkbutton(self.master, text="1: Negj", variable=self.isNegj)
        self.checkbox_erh_hasah = ttk.Checkbutton(self.master, text="2: Erh hasah", variable=self.isErhHasah)
        self.checkbox_barivchlah = ttk.Checkbutton(self.master, text="3: Barivchlah", variable=self.isBarivchlah)
        self.checkbox_albadlaga = ttk.Checkbutton(self.master, text="4: Albadlaga", variable=self.isAlbadlaga)
        self.checkbox_TusgaiJuram = ttk.Checkbutton(self.master, text="5: Tusgai Juram", variable=self.isTusgaiJuram)
        self.checkbox_TusgaiSungalt = ttk.Checkbutton(self.master, text="6: Sungalt", variable=self.isTusgaiSungalt)
        self.checkbox_published = ttk.Checkbutton(self.master, text="Published", variable=self.isPublished)
        self.checkbox_erh_hasah.grid(row=11, column=0, padx=self.padx, pady=self.pady, sticky=checkbox_align)
        self.checkbox_barivchlah.grid(row=11, column=1, padx=self.padx, pady=self.pady, sticky=checkbox_align)
        self.checkbox_albadlaga.grid(row=11, column=2, padx=self.padx, pady=self.pady, sticky=checkbox_align)
        self.checkbox_TusgaiJuram.grid(row=11, column=3, padx=self.padx, pady=self.pady, sticky=checkbox_align)
        self.checkbox_TusgaiSungalt.grid(row=12, column=0, padx=self.padx, pady=self.pady, sticky=checkbox_align)
        self.checkbox_negj.grid(row=8, column=3, padx=self.padx, pady=self.pady, sticky=checkbox_align)
        self.checkbox_published.grid(row=16, column=0, padx=self.padx, pady=self.pady, sticky=checkbox_align)
        self.position_window_bottom_right()

    def position_window_bottom_right(self):
        self.master.update_idletasks()  # Update the window
        window_width = self.master.winfo_width()
        window_height = self.master.winfo_height()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculate x and y coordinates
        x = screen_width - window_width
        y = screen_height - window_height

        # Position the window in the bottom right corner
        self.master.geometry(f'+{x}+{y}')

    def setup_radio_buttons(self):
        # Setup for Radio Buttons
        align = 'w'
        self.radio_var = tk.StringVar(value="LAW")  # Default value

        ttk.Radiobutton(self.master, text="LAW", variable=self.radio_var,
                        value="LAW", command=self.on_radio_change).grid(row=14, column=0, padx=self.padx,
                                                                        pady=self.pady, sticky=align)

        ttk.Radiobutton(self.master, text="Action", variable=self.radio_var,
                        value="Action", command=self.on_radio_change).grid(row=14, column=1, padx=self.padx,
                                                                           pady=self.pady, sticky=align)

        ttk.Radiobutton(self.master, text="Subject", variable=self.radio_var,
                        value="Subject", command=self.on_radio_change).grid(row=14, column=2, padx=self.padx,
                                                                            pady=self.pady, sticky=align)
    def setup_result_and_buttons(self):
        # Code result display
        align = 'nw'
        ttk.Label(self.master, text="Code: ").grid(row=15, column=0, sticky=align)
        self.code_textbox = ttk.Entry(self.master)
        self.code_textbox.grid(row=15, column=1, padx=self.padx, pady=self.pady)

        # Article/Prefix display
        ttk.Label(self.master, text="Article/Prefix: ").grid(row=15, column=2, sticky=align)
        self.article_textbox = ttk.Entry(self.master)
        self.article_textbox.grid(row=15, column=3, padx=self.padx, pady=self.pady)

        # Buttons
        ttk.Button(self.master, width=20, text="Next", command=self.on_generate_next_button_clicked).grid(row=16,
                                                                                                          column=3,
                                                                                                          padx=self.padx,
                                                                                                          pady=self.pady)
        ttk.Button(self.master, width=20, text="Save", command=self.on_save_button_clicked).grid(row=16, column=2,
                                                                                                 padx=self.padx,
                                                                                                 pady=self.pady)
        ttk.Button(self.master, width=20, text="Set", command=self.on_set_button_clicked).grid(row=16, column=1,
                                                                                               padx=self.padx,
                                                                                               pady=self.pady)

    def on_generate_next_button_clicked(self):
        selected_radio = self.radio_var.get()
        if selected_radio == "Action":
            self.set_next_action_data()
        elif selected_radio == "Subject":
            self.set_next_subject_data()
        else:
            self.set_next_law_data()

    def on_save_button_clicked(self):
        self.construct_data()
        self.upload_data_to_file()

    def on_set_button_clicked(self):
        selected_radio = self.radio_var.get()
        if selected_radio == "Action":
            self.set_action_data()
        elif selected_radio == "Subject":
            self.set_subject_data()
        else:
            self.set_law_data()

    def set_law_data(self):
        self.law_parent_id = int(self.inputList[0].get()) if self.inputList[0].get() else 0
        self.law_list_order = int(self.inputList[1].get()) if self.inputList[1].get() else 0
        self.chapter = int(self.inputList[2].get()) if self.inputList[2].get() else 0
        self.section = int(self.inputList[3].get()) if self.inputList[3].get() else 0
        self.article = int(self.inputList[4].get()) if self.inputList[4].get() else 0
        self.sub_article = int(self.inputList[5].get()) if self.inputList[5].get() else 0
        self.generate_law_index()
        self.show_law_code()
        self.article_code = self.code_textbox.get()

    def set_action_data(self):
        self.action_code = int(self.code_textbox.get()) if self.code_textbox.get() else 0
        self.action_list_order = int(self.inputList[1].get()) if self.inputList[1].get() else 0

    def set_subject_data(self):
        self.subject_code = int(self.code_textbox.get()) if self.code_textbox.get() else 0
        self.subject_list_order = int(self.inputList[1].get()) if self.inputList[1].get() else 0

    def generate_law_index(self):
        self.law_index = ''.join([
            self.inputList[2].get() if self.inputList[2].get() else '',
            '.' + self.inputList[3].get() if self.inputList[3].get() else '',
            '-' + self.inputList[4].get() if self.inputList[4].get() else '',
            '.' + self.inputList[5].get() if self.inputList[5].get() else ''
        ])
        return self.law_index

    def show_law_code(self):
        fn_chapter = format_input(self.inputList[2].get())
        fn_section = format_input(self.inputList[3].get())
        fn_article = format_input(self.inputList[4].get())
        fn_sub_article = format_input(self.inputList[5].get())
        fn_law_index = self.generate_law_index()
        fn_law_code = "11" + fn_chapter + fn_section + fn_article + fn_sub_article
        # Display LawCode in the result field
        if self.large_text_inputList[0].get("1.0", "end-1c"):
            self.large_text_inputList[0].delete("1.0", "end-1c")
        self.large_text_inputList[0].insert("1.0", fn_law_index)
        self.code_textbox.delete(0, tk.END)  # Clear existing content
        self.code_textbox.insert(0, fn_law_code)  # Insert the LawCode

    def on_radio_change(self):
        self.clear_form()
        selected_radio = self.radio_var.get()
        if selected_radio == "Action":
            self.recall_prev_action_data()
            self.disable_law_attributes()
        elif selected_radio == "Subject":
            self.recall_prev_sub_data()
            self.disable_law_attributes()
        else:
            self.enable_law_attributes()
            self.recall_prev_law_data()

    def clear_form(self):
        self.inputList[0].delete(0, tk.END)
        self.inputList[1].delete(0, tk.END)
        self.inputList[2].delete(0, tk.END)
        self.inputList[3].delete(0, tk.END)
        self.inputList[4].delete(0, tk.END)
        self.inputList[5].delete(0, tk.END)
        for text_input in self.large_text_inputList:
            text_input.delete("1.0", tk.END)
        self.code_textbox.delete(0, tk.END)
        self.article_textbox.delete(0, tk.END)

    def disable_law_attributes(self):
        self.checkbox_barivchlah.config(state="disabled")
        self.checkbox_negj.config(state="disabled")
        self.checkbox_erh_hasah.config(state="disabled")
        self.checkbox_TusgaiSungalt.config(state="disabled")
        self.checkbox_albadlaga.config(state="disabled")
        self.checkbox_TusgaiJuram.config(state="disabled")
        self.inputList[6].config(state="disabled")
        self.inputList[7].config(state="disabled")
        self.inputList[8].config(state="disabled")
        self.large_text_inputList[1].config(state="disabled")

    def enable_law_attributes(self):
        # Enable checkboxes and other inputs
        self.checkbox_barivchlah.config(state="normal")
        self.checkbox_negj.config(state="normal")
        self.checkbox_erh_hasah.config(state="normal")
        self.checkbox_TusgaiSungalt.config(state="normal")
        self.checkbox_albadlaga.config(state="normal")
        self.checkbox_TusgaiJuram.config(state="normal")
        self.inputList[6].config(state="normal")
        self.inputList[7].config(state="normal")
        self.inputList[8].config(state="normal")
        self.large_text_inputList[1].config(state="normal")

    def recall_prev_action_data(self):
        self.code_textbox.insert(0, str(self.action_code))
        self.inputList[1].insert(0, str(self.action_list_order))
        self.inputList[0].insert(0, "52704")
        self.article_textbox.insert(0, str(self.article_code))

    def recall_prev_sub_data(self):
        self.code_textbox.insert(0, str(self.subject_code))
        self.inputList[0].insert(0, "52703")
        self.inputList[1].insert(0, str(self.subject_list_order))
        self.article_textbox.insert(0, str(self.article_code))

    def recall_prev_law_data(self):
        self.inputList[0].insert(0, str(self.law_parent_id) if self.law_parent_id > 0 else '')
        self.inputList[1].insert(0, str(self.law_list_order) if self.law_list_order > 0 else '')
        self.inputList[2].insert(0, str(self.chapter) if self.chapter > 0 else '')
        self.inputList[3].insert(0, str(self.section) if self.section > 0 else '')
        self.inputList[4].insert(0, str(self.article) if self.article > 0 else '')
        self.inputList[5].insert(0, str(self.sub_article) if self.sub_article > 0 else '')
        self.show_law_code()

    def set_next_action_data(self):
        self.action_list_order += 10
        self.action_code += 1
        self.inputList[1].delete(0, tk.END)
        self.inputList[1].insert(0, str(self.action_list_order))
        self.code_textbox.delete(0, tk.END)
        self.code_textbox.insert(0, str(self.action_code))
        self.set_action_data()

    def set_next_subject_data(self):
        self.subject_list_order += 10
        self.subject_code += 1
        self.inputList[1].delete(0, tk.END)
        self.inputList[1].insert(0, str(self.subject_list_order))
        self.code_textbox.delete(0, tk.END)
        self.code_textbox.insert(0, str(self.subject_code))
        self.set_subject_data()

    def set_next_law_data(self):
        if self.law_parent_id > 0:
            self.inputList[0].delete(0, tk.END)
            self.inputList[0].insert(0, str(self.law_parent_id))
        if self.law_list_order > 0:
            self.law_list_order += 10
            self.inputList[1].delete(0, tk.END)
            self.inputList[1].insert(0, str(self.law_list_order))
        if self.sub_article > 0:
            self.sub_article += 1
            self.inputList[5].delete(0, tk.END)
            self.inputList[5].insert(0, str(self.sub_article))
        elif self.article > 0:
            self.article += 1
            self.inputList[4].delete(0, tk.END)
            self.inputList[4].insert(0, str(self.article))
        elif self.section > 0:
            self.section += 1
            self.inputList[3].delete(0, tk.END)
            self.inputList[3].insert(0, str(self.section))
        elif self.chapter > 0:
            self.chapter += 1
            self.inputList[2].delete(0, tk.END)
            self.inputList[2].insert(0, str(self.chapter))
        self.show_law_code()
        self.set_law_data()

    def construct_data(self):
        selected_radio = self.radio_var.get()
        if selected_radio == "Action":
            self.data["TYPE"] = 3
        elif selected_radio == "Subject":
            self.data["TYPE"] = 2
        else:
            self.data["TYPE"] = 1

        self.data["PARENT_ID"] = int(self.inputList[0].get())
        self.data["CODE"] = self.code_textbox.get()
        self.data["NAME"] = self.large_text_inputList[0].get("1.0", "end-1c")
        self.data["INFO"] = self.large_text_inputList[1].get("1.0", "end-1c")
        self.data["LIST_ORDER"] = int(self.inputList[1].get())
        self.data["ATTRIBUTE_TORGUULI_MIN"] = int(self.inputList[6].get()) if (self.inputList[6].get()
                                                                               and selected_radio == "LAW") else ''
        self.data["ATTRIBUTE_TORGUULI_MAX"] = int(self.inputList[7].get()) if (self.inputList[7].get()
                                                                               and selected_radio == "LAW") else ''
        self.data["ATTRIBUTE_NEGJ"] = int(self.isNegj.get()) if selected_radio == "LAW" else ''
        self.data["ATTRIBUTE_ERH_HASAH"] = int(self.isErhHasah.get()) if selected_radio == "LAW" else ''
        self.data["ATTRIBUTE_BARIVCHLAH"] = int(self.isBarivchlah.get()) if selected_radio == "LAW" else ''
        self.data["ATTRIBUTE_ALBADLAGA"] = int(self.isAlbadlaga.get()) if selected_radio == "LAW" else ''
        self.data["ATTRIBUTE_TUSGAI_JURAM"] = int(self.isTusgaiJuram.get()) if selected_radio == "LAW" else ''
        self.data["ATTRIBUTE_TUSGAI_SUNGALT"] = int(self.isTusgaiSungalt.get()) if selected_radio == "LAW" else ''
        self.data["ATTRIBUTE_STATUTE_OF_LIMITATIONS"] = int(self.inputList[8].get()) if (self.inputList[8].get()
                                                                                         and selected_radio == "LAW") else ''
        self.data["ATTRIBUTE_ARTICLE_CODE"] = self.article_textbox.get() if self.article_textbox.get() and selected_radio == "Action" else ''
        self.data["ATTRIBUTE_CODE_PREFIX"] = self.article_textbox.get() if self.article_textbox.get() and selected_radio == "Subject" else ''
        self.data["PUBLISHED"] = int(self.isPublished.get())

    def upload_data_to_file(self):
        csv_file_path = os.path.join(self.csv_file_path, self.csv_file_name)
        if not os.path.exists(csv_file_path):
            with open(csv_file_path, mode='w', newline='', encoding="UTF-8") as file:
                writer = csv.DictWriter(file, fieldnames=self.data.keys())
                writer.writeheader()

        try:
            with open(csv_file_path, mode='a', newline='', encoding="UTF-8") as file:
                writer = csv.DictWriter(file, fieldnames=self.data.keys())
                writer.writerow(self.data)
            messagebox.showinfo(title="success")
            isNext = messagebox.askyesno("Saved", "generate next?")
            if isNext:
                self.on_generate_next_button_clicked()
            self.clear_form()
            self.on_radio_change()
        except PermissionError:
            messagebox.showerror(title="File Error", message="The CSV file is open in another application.")

    def copy_and_paste_into_name(self):
        keyboard.press_and_release('ctrl+c')
        time.sleep(0.3)
        copied_text = pyperclip.paste()
        if copied_text:
            current_text = self.large_text_inputList[0].get("1.0",
                                                            tk.END)
            if current_text.endswith("\n"):
                current_text = current_text[:-1]
            self.large_text_inputList[0].delete("1.0", tk.END)
            combined_text = current_text + " " if len(current_text) > 0 else ''
            combined_text += copied_text
            self.large_text_inputList[0].insert("1.0", combined_text)

    def copy_and_paste_into_info(self):
        keyboard.press_and_release('ctrl+c')
        time.sleep(0.3)
        copied_text = pyperclip.paste()
        if copied_text:
            current_text = self.large_text_inputList[1].get("1.0", tk.END)
            if current_text.endswith("\n"):
                current_text = current_text[:-1]
            self.large_text_inputList[1].delete("1.0", tk.END)
            combined_text = current_text + " " if len(current_text) > 0 else ''
            combined_text += copied_text
            self.large_text_inputList[1].insert("1.0", combined_text)

    def toggle_checkbox(self, param):
        if param == 1:
            self.isNegj.set(not self.isNegj.get())
        elif param == 2:
            self.isErhHasah.set(not self.isErhHasah.get())
        elif param == 3:
            self.isBarivchlah.set(not self.isBarivchlah.get())
        elif param == 4:
            self.isAlbadlaga.set(not self.isAlbadlaga.get())
        elif param == 5:
            self.isTusgaiJuram.set(not self.isTusgaiJuram.get())
        elif param == 6:
            self.isTusgaiSungalt.set(not self.isTusgaiSungalt.get())

    def toggle_radio_button(self):
        current_radio = self.radio_var.get()
        if current_radio == "LAW":
            self.radio_var.set("Action")
        elif current_radio == "Action":
            self.radio_var.set("Subject")
        else:
            self.radio_var.set("LAW")
        self.on_radio_change()

    def on_closing(self):
        self.save_to_file()
        self.master.destroy()

    def save_to_file(self):
        data = {
            "law_parent_id": self.law_parent_id,
            "law_list_order": self.law_list_order,
            "law_index": self.law_index,
            "chapter": self.chapter,
            "section": self.section,
            "article": self.article,
            "sub_article": self.sub_article,
            "article_code": self.article_code,
            "action_code": self.action_code,
            "action_list_order": self.action_list_order,
            "subject_code": self.subject_code,
            "subject_list_order": self.subject_list_order
        }
        print(data)
        file_path = os.path.join(self.recovery_file_path, self.recovery_file_name)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def read_recovery_file(self):
        print("trying to recall")
        file_path = os.path.join(self.recovery_file_path, self.recovery_file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                loaded_data = json.load(file)
                self.law_parent_id = loaded_data["law_parent_id"]
                self.law_list_order = loaded_data["law_list_order"]
                self.law_index = loaded_data["law_index"]
                self.chapter = loaded_data["chapter"]
                self.section = loaded_data["section"]
                self.article = loaded_data["article"]
                self.action_code = loaded_data["action_code"]
                self.action_list_order = loaded_data["action_list_order"]
                self.subject_code = loaded_data["subject_code"]
                self.subject_list_order = loaded_data["subject_list_order"]
                self.on_radio_change()
                print("recall success")
        else:
            print("recall failed")

    def __del__(self):
        self.on_closing()


def main():
    root = tk.Tk()
    app = LawApplication(root)
    app.read_recovery_file()
    root.mainloop()


if __name__ == "__main__":
    main()
