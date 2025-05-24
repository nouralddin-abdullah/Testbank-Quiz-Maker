import tkinter as tk
from tkinter import ttk
import os

class NotesViewer(tk.Tk):
    def __init__(self, notes_directory=None):
        super().__init__()
        self.title('Quiz Notes Viewer')
        self.notes_directory = notes_directory if notes_directory else "C:\\notes"
        if not os.path.exists(self.notes_directory):
            os.makedirs(self.notes_directory)
        self.create_widgets()
        self.populate_treeview()
        self.state('zoomed') 

    def create_widgets(self):

        tree_frame = tk.Frame(self)
        tree_frame.pack(fill='both', expand=True)


        self.tree = ttk.Treeview(tree_frame, columns=('Question', 'Note'), show='headings')
        self.tree.pack(side='left', fill='both', expand=True)


        self.tree.heading('Question', text='Question')
        self.tree.heading('Note', text='Note')


        self.tree.column('Question', width=900, anchor='w')
        self.tree.column('Note', width=900, anchor='w')


        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')


        self.tree.configure(yscrollcommand=scrollbar.set)

    def populate_treeview(self):

        for i in self.tree.get_children():
            self.tree.delete(i)


        for filename in os.listdir(self.notes_directory):
            if filename.endswith('.txt'):
                file_path = os.path.join(self.notes_directory, filename)
                try:
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                        for i in range(0, len(lines), 2):
                            question = lines[i].strip().replace('Question: ', '')
                            note = lines[i+1].strip().replace('Note: ', '')

                            self.tree.insert('', 'end', values=(question, note))
                except Exception as e:
                    print(f"Error reading file {filename}: {e}")