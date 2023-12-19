import tkinter as tk
from tkinter import scrolledtext

def format_input(value):
    # Return '00' if the input is empty, otherwise prepend '0' if single digit
    return '00' if value == '' else (value if len(value) > 1 else '0' + value)


class LawApplication:
    def __init__(self, master):
        self.checkbox_barivchlah = None
        self.master = master
        self.master.title("Reg Form Demo")

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

        # Initialize UI components
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

        # radiobutton
        self.radio_var = tk.StringVar(value="LAW")

        self.setup_inputs()
        self.setup_large_text_inputs()
        self.setup_checkboxes()
        self.setup_radio_buttons()
        self.setup_result_and_buttons()

    def setup_inputs(self):
        # PARENT_ID and LIST_ORDER input fields
        tk.Label(self.master, text="PARENT_ID").grid(row=0, column=0)
        parent_id_input = tk.Entry(self.master)
        parent_id_input.grid(row=0, column=1)
        self.inputList.append(parent_id_input)

        tk.Label(self.master, text="LIST_ORDER").grid(row=0, column=2)
        list_order_input = tk.Entry(self.master)
        list_order_input.grid(row=0, column=3)
        self.inputList.append(list_order_input)

        # Chapter, Section, Article, sub_article inputs
        labels_text = ["Chapter", "Section", "Article", "sub_article"]
        for i, text in enumerate(labels_text):
            tk.Label(self.master, text=text).grid(row=1, column=i)
            entry = tk.Entry(self.master)
            entry.grid(row=2, column=i)
            self.inputList.append(entry)

        tk.Label(self.master, text="TORGUULI_MIN/MAX").grid(row=8, column=0)
        penalty_min_input = tk.Entry(self.master)
        penalty_min_input.grid(row=8, column=1) # index 6
        self.inputList.append(penalty_min_input)

        penalty_max_input = tk.Entry(self.master)
        penalty_max_input.grid(row=8, column=2)
        self.inputList.append(penalty_max_input) # index 7

        tk.Label(self.master, text="STATUTE OF LIMITATION").grid(row=9, column=0)
        statute_of_limitation_input = tk.Entry(self.master)
        statute_of_limitation_input.grid(row=9, column=1)
        self.inputList.append(statute_of_limitation_input)  # index 8


    def setup_large_text_inputs(self):
        # NAME and INFO large text inputs
        large_text_labels = ["NAME", "INFO"]
        for i, text in enumerate(large_text_labels):
            tk.Label(self.master, text=text).grid(row=3 + 2 * i, column=0, sticky='nw')
            text_input = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, height=5, width=40,
                                                   font=("Arial Unicode MS", 12))
            text_input.grid(row=4 + 2 * i, column=0, columnspan=4, sticky='ew')
            self.large_text_inputList.append(text_input)

    def setup_checkboxes(self):
        # Setup for Checkboxes
        self.checkbox_erh_hasah = tk.Checkbutton(self.master, text="Erh hasah", variable=self.isErhHasah)
        self.checkbox_barivchlah = tk.Checkbutton(self.master, text="Barivchlah", variable=self.isBarivchlah)
        self.checkbox_albadlaga = tk.Checkbutton(self.master, text="Albadlaga", variable=self.isAlbadlaga)
        self.checkbox_TusgaiJuram = tk.Checkbutton(self.master, text="Tusgai Juram", variable=self.isTusgaiJuram)
        self.checkbox_TusgaiSungalt = tk.Checkbutton(self.master, text="Sungalt", variable=self.isTusgaiSungalt)
        self.checkbox_negj = tk.Checkbutton(self.master, text="Negj", variable=self.isNegj)
        self.checkbox_erh_hasah.grid(row=11, column=0)
        self.checkbox_barivchlah.grid(row=11, column=1)
        self.checkbox_albadlaga.grid(row=11, column=2)
        self.checkbox_TusgaiJuram.grid(row=11, column=3)
        self.checkbox_TusgaiSungalt.grid(row=12, column=0)
        self.checkbox_negj.grid(row=8, column=3)

    def setup_radio_buttons(self):
        # Setup for Radio Buttons
        self.radio_var = tk.StringVar(value="LAW")  # Default value

        tk.Radiobutton(self.master, text="LAW", variable=self.radio_var,
                       value="LAW", command=self.on_radio_change).grid(row=14, column=0)
        tk.Radiobutton(self.master, text="Subject", variable=self.radio_var,
                       value="Subject", command=self.on_radio_change).grid(row=14, column=1)
        tk.Radiobutton(self.master, text="Action", variable=self.radio_var,
                       value="Action", command=self.on_radio_change).grid(row=14, column=2)

    def setup_result_and_buttons(self):
        # Code result display
        tk.Label(self.master, text="Code: ").grid(row=15, column=0, sticky='e')
        self.code_textbox = tk.Entry(self.master)
        self.code_textbox.grid(row=15, column=1)

        # Article/Prefix display
        tk.Label(self.master, text="Article/Prefix: ").grid(row=15, column=2, sticky='e')
        self.article_textbox = tk.Entry(self.master)
        self.article_textbox.grid(row=15, column=3)

        # Buttons
        tk.Button(self.master, text="Next", command=self.on_generate_next_button_clicked).grid(row=16, column=4)
        tk.Button(self.master, text="Save", command=self.on_save_button_clicked).grid(row=16, column=3)
        tk.Button(self.master, text="Set", command=self.on_set_button_clicked).grid(row=16, column=2)

    def on_generate_next_button_clicked(self):
        # Logic for handling 'Next' button click
        # You can add your logic here
        pass

    def on_save_button_clicked(self):
        # Logic for handling 'Save' button click
        # You can add your logic here
        pass

    def on_set_button_clicked(self):
        selected_radio = self.radio_var.get()
        if selected_radio == "Action":
            self.set_action_data()
        elif selected_radio == "Subject":
            self.set_subject_data()
        else:
            self.set_law_data()

    def set_law_data(self):
        # Assuming inputList is a list of Entry widgets
        self.law_parent_id = int(self.inputList[0].get()) if self.inputList[0].get() else 0
        self.law_list_order = int(self.inputList[1].get()) if self.inputList[1].get() else 0
        self.chapter = int(self.inputList[2].get()) if self.inputList[2].get() else 0
        self.section = int(self.inputList[3].get()) if self.inputList[3].get() else 0
        self.article = int(self.inputList[4].get()) if self.inputList[4].get() else 0
        self.sub_article = int(self.inputList[5].get()) if self.inputList[5].get() else 0
        self.article_code = self.code_textbox.get()
        self.generate_law_index()
        self.show_law_code()

        # ... [rest of the code for setting law data] ...
        self.article_code = self.code_textbox.get()
        # Call build_law_index and show_law_code here or their logic can be included directly

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
        for entry in self.inputList:
            entry.delete(0, tk.END)
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


# Main function to run the application
def main():
    root = tk.Tk()
    LawApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
