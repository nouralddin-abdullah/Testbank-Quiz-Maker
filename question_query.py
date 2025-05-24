import tkinter as tk
from tkinter import ttk, messagebox
import os

class QuestionCreator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Question Creator")
        self.geometry("600x600")

        self.option_entries = []
        self.questions_file = "new_questions.txt"
        self.question_count = self.initialize_question_count()

        self.create_widgets()
        self.apply_styles()

    def apply_styles(self):
        style = ttk.Style()
        style.configure("TLabel", font=('Helvetica', 12))
        style.configure("TButton", font=('Helvetica', 12), background="blue", foreground="white")
        style.configure("TEntry", font=('Helvetica', 12))

    def create_widgets(self):
        self.lbl_question = ttk.Label(self, text="Enter Question:")
        self.lbl_question.pack(pady=(20, 10))

        self.txt_question = tk.Text(self, height=3, width=50)
        self.txt_question.pack()

        self.options_frame = ttk.Frame(self)
        self.options_frame.pack(pady=(10, 10))

        self.add_option()

        self.btn_add_option = ttk.Button(self, text="Add Option", command=self.add_option)
        self.btn_add_option.pack(pady=(10, 10))

        self.lbl_answer = ttk.Label(self, text="Enter the letter of the correct answer:")
        self.lbl_answer.pack(pady=(10, 10))

        self.txt_answer = ttk.Entry(self)
        self.txt_answer.pack()

        self.btn_save = ttk.Button(self, text="Save Question", command=self.save_question)
        self.btn_save.pack(pady=(20, 10))

    def add_option(self):
        option_letter = chr(65 + len(self.option_entries))
        lbl_option = ttk.Label(self.options_frame, text=f"{option_letter})")
        lbl_option.grid(row=len(self.option_entries), column=0)

        txt_option = ttk.Entry(self.options_frame, width=50)
        txt_option.grid(row=len(self.option_entries), column=1, padx=(5, 20))

        self.option_entries.append((option_letter, txt_option))

        if len(self.option_entries) >= 5:
            self.btn_add_option.pack_forget()

    def initialize_question_count(self):
        if os.path.exists(self.questions_file):
            with open(self.questions_file, "r") as file:
                return sum(1 for line in file if line.strip() and line.strip().isdigit())
        return 0

    def save_question(self):
        question = self.txt_question.get("1.0", "end-1c")
        answer = self.txt_answer.get().strip().upper()

        if not question or not answer:
            messagebox.showerror("Error", "Question and answer fields are required!")
            return

        options_text = ""
        for letter, entry in self.option_entries:
            option_text = entry.get().strip()
            if option_text:
                options_text += f"{letter}) {option_text}\n"

        if not options_text:
            messagebox.showerror("Error", "At least one option is required!")
            return

        self.question_count += 1
        formatted_question = f"{self.question_count}) {question}\n{options_text}Answer: {answer}\n\n"

        with open(self.questions_file, "a") as file:
            file.write(formatted_question)

        messagebox.showinfo("Success", f"Question {self.question_count} added successfully!")
        self.reset_fields()

    def reset_fields(self):
        self.txt_question.delete("1.0", "end")
        for _, entry in self.option_entries:
            entry.delete(0, 'end')
        self.txt_answer.delete(0, 'end')

def main():
    app = QuestionCreator()
    app.mainloop()

if __name__ == "__main__":
    main()