"""
Text Editor
Notepad style application that can open, edit, and save text documents. 
Optional: Add syntax highlighting and other features.
"""

from tkinter import Tk, Frame, Scrollbar,  Text, Menu, filedialog, RIGHT, END, Y


class TextEditor(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title('Practice Text Editor')
        self.geometry('900x460')
        self.current_file_name = False
        self.frame = Frame(self)
        self.frame.pack(pady=5)

    def set_text_box(self):
        text_scroll = Scrollbar(self.frame)
        text_scroll.pack(side=RIGHT, fill=Y)
        self.text_box = Text(self.frame, width=97, height=25, font=(
            "Helvetica", 16), selectbackground="white", selectforeground='black', undo=True, yscrollcommand=text_scroll.set)
        self.text_box.pack()
        text_scroll.config(command=self.text_box.yview)

    def set_menu(self):
        self.menu = Menu(self, tearoff=False)
        self.config(menu=self.menu)

        file_menu = [
            {'label': 'New', 'command': self.new_file, 'separate': False},
            {'label': 'Open', 'command': self.open_file, 'separate': False},
            {'label': 'Save as', 'command': self.save_as_file, 'separate': False},
            {'label': 'Save', 'command': self.save_file, 'separate': False},
            {'label': 'Exit', 'command': self.quit, 'separate': True}
        ]
        self.set_submenu('File', file_menu)

    def set_submenu(self, label: str, commands: list[tuple]):
        menu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label=label, menu=menu)
        for command in commands:
            if command['separate']:
                menu.add_separator()
            menu.add_command(
                label=command['label'], command=command['command'])

    def new_file(self):
        self.text_box.delete('1.0', END)
        self.title('New File - Denic Text Editor')

    def open_file(self):
        file_name = filedialog.askopenfilename(
            title='Open File', filetypes=([("Text Files", '.txt')]))

        if not file_name:
            return

        self.current_file_name = file_name
        self.text_box.delete('1.0', END)
        with open(file_name, 'r') as file:
            self.text_box.insert(END, file.read())

        name = file_name.split('/')[-1]
        self.title(f'{name} - Denic Text Editor')

    def save_as_file(self):
        file_name = filedialog.asksaveasfilename(
            defaultextension='.txt', title='Save file', filetypes=[('Text Files', '.txt')])

        if not file_name:
            return

        self.current_file_name = file_name
        with open(file_name, 'w') as file:
            file.write(self.text_box.get('1.0', END))

        name = file_name.split('/')[-1]
        self.title(f'{name} - Denic Text Editor')

    def save_file(self):
        if not self.current_file_name:
            return self.save_as_file()

        with open(self.current_file_name, 'w') as file:
            file.write(self.text_box.get('1.0', END))

    def start(self):
        self.set_text_box()
        self.set_menu()
        self.mainloop()


text_editor = TextEditor()
text_editor.start()
