import datetime
import os
import random
import subprocess
import sys
from tkinter import messagebox, simpledialog, ttk, filedialog
import tkinter as tk
from log_viewer import LogViewer
from question_query import QuestionCreator
from notes_viewer import NotesViewer

class Quiz:
    def __init__(self, master):
        self.master = master
        self.score = 0
        self.incorrect_answers = []
        self.questions = []
        self.current_question_index = 0
        self.total_questions = 0
        self.font_size = 15
        self.setup_quiz()
        self.display_question()
        self.notes = []
        self.notes_directory = "C:\\notes" 

    def increase_font_size(self):
        self.font_size += 1
        self.display_question()

    def decrease_font_size(self):
        if self.font_size > 1:
            self.font_size -= 1
        self.display_question()
    
    def open_notes_viewer(self):
        notes_viewer = NotesViewer(notes_directory=self.notes_directory)
        notes_viewer.populate_treeview()  
        notes_viewer.mainloop()

    def add_note(self):
        note = simpledialog.askstring("Add Note", "Enter your note:")
        if note:
            question_text = self.questions[self.current_question_index]['question']
            self.notes.append((question_text, note))
            filename = f"{self.notes_directory}\\note_{len(self.notes)}.txt" 
            with open(filename, 'a') as file:  
                file.write(f"Question: {question_text}\nNote: {note}\n")  

    def setup_quiz(self):
        load_choice = messagebox.askyesno("Quiz Setup", "Do you want to load questions from a file?")
        if load_choice:
            filename = filedialog.askopenfilename(title="Select Question File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if filename:
                self.questions = self.load_questions(filename)
            else:
                messagebox.showinfo("No File Selected", "No file was selected, opening question creator.")
                self.create_questions()
        else:
            self.create_questions()

        self.total_questions = len(self.questions)
        
        shuffle_questions = messagebox.askyesno("Quiz Setup", "Do you want to shuffle the questions?")
        if shuffle_questions:
            random.shuffle(self.questions)
            
        shuffle_options = messagebox.askyesno("Quiz Setup", "Do you want to shuffle the answer options? (True/False questions will not be shuffled)")
        if shuffle_options:
            for question in self.questions:
                self.shuffle_options(question)

    def create_questions(self):
        
        directory = os.path.dirname(os.path.abspath(__file__))
        question_file_path = os.path.join(directory, 'new_questions.txt')
        if os.path.exists(question_file_path):
            self.open_question_creator()

    def open_question_creator(self):
        creator = QuestionCreator()  
        creator.mainloop()  

    def load_questions(self, filename='Chapter11.txt'):
        questions = []
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError("No valid question file found")

        with open(file_path, 'r') as file:
            content = file.read()

        blocks = content.split('\n\n')
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) < 2:
                continue

            question_text = lines[0]
            choices = lines[1:-1]
            answer_line = lines[-1]
            answer = answer_line.split(': ')[1].strip()

            
            is_tf = len(choices) == 2 and all(choice.strip().endswith(('True', 'False')) for choice in choices)
            formatted_choices = [f"{chr(65+i)}) {choice.strip()}" for i, choice in enumerate(choices)]

            questions.append({
                "question": question_text,
                "choices": formatted_choices,
                "answer": answer,
                "is_tf": is_tf
            })

        return questions

    def shuffle_options(self, question):
        if not question['is_tf']:  
            answer_letter = question['answer']
            
            choices_with_letters = question['choices']
            correct_choice = next(c for c in choices_with_letters if c.startswith(f"{answer_letter})"))
            
            choice_contents = []
            for choice in choices_with_letters:
                content = choice.split(') ', 1)[1].strip()
                if content.startswith(tuple('ABCD')):
                    content = content.split(')', 1)[1].strip()
                choice_contents.append(content)
                
            random.shuffle(choice_contents)
            
            new_choices = [f"{chr(65+i)}) {text}" for i, text in enumerate(choice_contents)]
            
            correct_content = correct_choice.split(') ', 1)[1].strip()
            if correct_content.startswith(tuple('ABCD')):
                correct_content = correct_content.split(')', 1)[1].strip()
            new_position = choice_contents.index(correct_content)
            question['answer'] = chr(65 + new_position)
            
            question['choices'] = new_choices
            
    def save_incorrect_answers(self):
        logs_dir = r"C:\logs"
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.join(logs_dir, f'incorrect_answers_{date_str}.txt')

        with open(file_path, 'w') as file:
            for question, wrong_choice, correct_choice in self.incorrect_answers:
                file.write(f"Question: {question}\n")
                file.write(f"Your Choice: {wrong_choice}\n")
                file.write(f"Correct Answer: {correct_choice}\n\n")

    def display_question(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        if self.current_question_index < self.total_questions:
            question = self.questions[self.current_question_index]

            increase_font_button = tk.Button(self.master, text="+", command=self.increase_font_size)
            increase_font_button.pack(side=tk.TOP, anchor=tk.E)
            decrease_font_button = tk.Button(self.master, text="-", command=self.decrease_font_size)
            decrease_font_button.pack(side=tk.TOP, anchor=tk.E)


            self.detailed_results_button = tk.Button(self.master, text="View Detailed Results", state=tk.DISABLED, command=self.open_log_viewer, font=("Arial", self.font_size)) 
            self.detailed_results_button.pack(side=tk.TOP, anchor=tk.W)

            self.question_label = tk.Label(self.master, text=f"Question {self.current_question_index + 1}/{self.total_questions}\n{question['question']}", font=("Arial", self.font_size), wraplength=700)  
            self.question_label.pack()


            choices_frame = tk.Frame(self.master)
            choices_frame.pack()
            self.notes_button = tk.Button(self.master, text="Notes", command=self.open_notes_viewer, font=("Arial", self.font_size))  
            self.notes_button.pack(side=tk.TOP, anchor=tk.CENTER)
            self.add_note_button = tk.Button(self.master, text="Add note here", command=self.add_note, font=("Arial", self.font_size))  
            self.add_note_button.pack(side=tk.TOP, anchor=tk.CENTER)

            for i, choice in enumerate(question["choices"]):
                row = i // 2
                column = i % 2
                tk.Button(choices_frame, text=choice, command=lambda c=choice: self.check_answer(c, question["answer"]), height=2, width=50, font=("Arial", self.font_size), wraplength=350, padx=30, pady=50).grid(row=row, column=column, pady=7)
    def check_answer(self, choice, correct_answer):
        choice_letter = choice.split(')')[0].strip()
        
        correct_choice = next(c for c in self.questions[self.current_question_index]['choices'] 
                            if c.startswith(f"{correct_answer})"))

        if choice_letter == correct_answer.strip():
            self.score += 1
            messagebox.showinfo("Result", "You are correct! +1 point")
        else:
            question_text = self.questions[self.current_question_index]['question']
            self.incorrect_answers.append((question_text, choice, correct_choice))
            messagebox.showinfo("Result", f"You are wrong! The correct answer was: {correct_choice}")

        self.current_question_index += 1
        if self.current_question_index < self.total_questions:
            self.display_question()
        else:
            self.display_summary()

        if self.current_question_index >= self.total_questions:
            self.detailed_results_button.config(state=tk.NORMAL)
    def open_log_viewer(self):
        log_viewer = LogViewer(log_directory=r"C:\logs")
        log_viewer.mainloop()

    def display_summary(self):
        summary_window = tk.Toplevel(self.master)
        summary_window.title("Quiz Summary")

        canvas = tk.Canvas(summary_window)
        scrollbar = tk.Scrollbar(summary_window, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollbar.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)
        self.save_incorrect_answers()
        tk.Label(scrollable_frame, text="Quiz Completed! Here's your summary:").pack()
        tk.Label(scrollable_frame, text=f"Your score: {self.score}/{self.total_questions}").pack()

        if self.incorrect_answers:
            tk.Label(scrollable_frame, text="Incorrect Questions:").pack()
            for question, your_choice, correct_answer in self.incorrect_answers:
                tk.Label(scrollable_frame, text=f"Q: {question}").pack()
                tk.Label(scrollable_frame, text=f"Your Choice: {your_choice} | Correct Answer: {correct_answer}").pack()

root = tk.Tk()
root.title("Quiz App")

app = Quiz(root)

root.mainloop()