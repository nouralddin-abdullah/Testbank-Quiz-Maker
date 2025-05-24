import sys
import tkinter as tk
from tkinter import ttk
import os
import datetime

def write_debug_info(message):
    """Helper function to write debug information to a file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('debug_log.txt', 'a') as debug_file:
        debug_file.write(f"{timestamp} - {message}\n")

class LogViewer(tk.Tk):
    def __init__(self, log_directory):
        super().__init__()
        self.title('Quiz Log Viewer')
        self.log_directory = log_directory
        self.create_widgets()
        self.populate_treeview()
        self.state('zoomed') 

    def create_widgets(self):

        tree_frame = tk.Frame(self)
        tree_frame.pack(fill='both', expand=True)


        self.tree = ttk.Treeview(tree_frame, columns=('Question', 'Choice', 'Correct Answer'), show='headings')
        self.tree.pack(side='left', fill='both', expand=True)


        self.tree.heading('Question', text='Question')
        self.tree.heading('Choice', text='Choice')
        self.tree.heading('Correct Answer', text='Correct Answer')


        self.tree.column('Question', width=900, anchor='w')
        self.tree.column('Choice', width=20, anchor='center')
        self.tree.column('Correct Answer', width=150, anchor='center')


        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')


        self.tree.configure(yscrollcommand=scrollbar.set)

    def populate_treeview(self):
        write_debug_info(f"Looking for logs in: {self.log_directory}")


        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for filename in os.listdir(self.log_directory):
            if filename.startswith('incorrect_answers_') and filename.endswith('.txt'):
                file_path = os.path.join(self.log_directory, filename)
                write_debug_info(f"Found log file: {file_path}")
                try:
                    with open(file_path, 'r') as file:
                        current_question = None
                        current_choice = None
                        correct_answer = None
                        
                        for line in file:
                            line = line.strip()
                            if line.startswith('Question: '):

                                if current_question and current_choice and correct_answer:
                                    self.tree.insert('', 'end', values=(current_question, 
                                                                    current_choice, 
                                                                    correct_answer))
                                current_question = line[len('Question: '):]
                            elif line.startswith('Your Choice: '):
                                current_choice = line[len('Your Choice: '):]
                            elif line.startswith('Correct Answer: '):
                                correct_answer = line[len('Correct Answer: '):]
                        

                        if current_question and current_choice and correct_answer:
                            self.tree.insert('', 'end', values=(current_question, 
                                                            current_choice, 
                                                            correct_answer))

                except Exception as e:
                    write_debug_info(f"Error reading file {filename}: {str(e)}")

if __name__ == "__main__":
    log_viewer = LogViewer(log_directory=r"C:\logs")
    log_viewer.mainloop()


