# This is simple text Editor with basic features like
# Creating, editing, and viewing of a file.

from tkinter import *
from tkinter import filedialog
from tkinter import font
import win32api

root = Tk()
root.title('IGNOU - Textedit!')
# root.iconbitmap('C:/Users/shashank.arya/Desktop/mcs044 mini project - Text Editor/gui/icon.ico')
root.geometry('800x500')

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Set variable for open file name
global already_open_filename
already_open_filename = FALSE

global selected
selected = FALSE


# create new file function

def new_file():
    # Delete Previous text
    my_text.delete("1.0", END)
    # update Status with New File
    root.title('New File - Text Pad!')
    status_bar.config(text="New File    ")

    global already_open_filename
    already_open_filename = FALSE


# create open file function
def open_file():
    my_text.delete("1.0", END)
    # Grab file name
    text_file = filedialog.askopenfilename(initialdir="C:/gui/", title="Open File", filetypes=(
        ("text files", "*.txt"), ("html files", "*.html"), ("Python Files", "*.py"), ("All File", "*.*")))

    if text_file:
        # make file name global so we can access it later
        global already_open_filename
        already_open_filename = text_file

    # update Status bars
    name = text_file
    status_bar.config(text=f'{name}')
    name.replace("C:/gui/", "")
    root.title(f'{name} - TextPad!')
    # open the file
    text_file = open(text_file, 'r')
    content = text_file.read()
    # Insert character in textbox
    my_text.insert(END, content)
    # close the opened file
    text_file.close()


# save an existing file
def save_file():
    global already_open_filename
    if already_open_filename:
        # save the file
        text_file = open(already_open_filename, 'w')
        text_file.write(my_text.get("1.0", END))
        # close the file
        text_file.close()
        status_bar.config(text=f' Saved: {already_open_filename}')
    else:
        save_as_file()


# save as file
def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:/gui/", title="Save File", filetypes=(
        (("text files", "*.txt"), ("html files", "*.html"), ("Python Files", "*.py"), ("All File", "*.*"))))
    if text_file:
        # update status bars
        name = text_file
        status_bar.config(text=f'{name}')
        name = name.replace("C:/gui/", "")
        root.title(f'{name} - Textpad!')

        # save the file
        text_file = open(text_file, 'w')
        text_file.write(my_text.get("1.0", END))
        text_file.close()


# Cut Text

def cut_text(e):
    global selected
    # check to see if keyboard shortcut is used
    if e:
        selected = root.clipboard_get()

    if my_text.selection_get():
        # grab selected text from text box
        selected = my_text.selection_get()
        # delete the selected text
        my_text.delete("sel.first", "sel.last")
        # clear the clipboard and append
        root.clipboard_clear()
        root.clipboard_append(selected)


# Copy Text

def copy_text(e):
    global selected
    # check to see if we used keyboard shortcuts
    if e:
        selected = root.clipboard_get()

    if my_text.selection_get():
        selected = my_text.selection_get()
        # clear the clipboard and append
        root.clipboard_clear()
        root.clipboard_append(selected)


# Paste Text

def paste_text(e):
    global selected
    # check to see if keyboard shortcut is used
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.insert(position, selected)


# bold text
def bold_it():
    bold_font = font.Font(my_text, my_text.cget("font"))
    bold_font.configure(weight="bold")

    # current tags
    current_tags = my_text.tag_names("sel.first")

    # configure a tag
    my_text.tag_configure("bold", font=bold_font)

    # if statement
    if "bold" in current_tags:
        my_text.tag_remove("bold", "sel.first", "sel.last")
    else:
        my_text.tag_add("bold", "sel.first", "sel.last")


# Italic text
def italic_it():
    italics_font = font.Font(my_text, my_text.cget("font"))
    italics_font.configure(slant="italic")
    # configure a tag
    my_text.tag_configure("italic", font=italics_font)

    # current tags
    current_tags = my_text.tag_names("sel.first")

    # if statement
    if "italic" in current_tags:
        my_text.tag_remove("italic", "sel.first", "sel.last")
    else:
        my_text.tag_add("italic", "sel.first", "sel.last")


# underline text
def underline_it():
    underline_font = font.Font(my_text, my_text.cget("font"))
    underline_font.configure(underline=1)

    my_text.tag_configure("underline", font=underline_font)

    current_tags = my_text.tag_names("sel.first")
    if "underline" in current_tags:
        my_text.tag_remove("underline", "sel.first", "sel.last")
    else:
        my_text.tag_add("underline", "sel.first", "sel.last")


# Find a char or string in the file
def find_text():
    search_toplevel = Toplevel(root)
    search_toplevel.title('Find Text')
    search_toplevel.transient(root)
    search_toplevel.resizable(False, False)
    Label(search_toplevel, text="Find All:").grid(row=0, column=0, sticky='e')
    search_entry_widget = Entry(search_toplevel, width=25)
    search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value = IntVar()
    Checkbutton(search_toplevel, text='Ignore Case', variable=ignore_case_value).grid(row=1, column=1, sticky='e',
                                                                                      padx=2, pady=2)
    Button(search_toplevel, text="Find All", underline=0,
           command=lambda: search_output(
               search_entry_widget.get(), ignore_case_value.get(),
               my_text, search_toplevel, search_entry_widget)
           ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

    def close_search_window():
        my_text.tag_remove('match', '1.0', END)
        search_toplevel.destroy()

    search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
    return "break"


def search_output(needle, if_ignore_case, my_text, search_toplevel, search_box):
    my_text.tag_remove('match', '1.0', END)
    matches_found = 0
    if needle:
        start_pos = '1.0'
        while True:
            start_pos = my_text.search(needle, start_pos, nocase=if_ignore_case, stopindex=END)
            if not start_pos:
                break
            end_pos = '{} + {}c'.format(start_pos, len(needle))
            my_text.tag_add('match', start_pos, end_pos)
            matches_found += 1
            start_pos = end_pos
        my_text.tag_config('match', background='yellow', foreground='blue')
    search_box.focus_set()
    search_toplevel.title('{} matches found'.format(matches_found))


# print a file

def print():
    # print_name = win32print.GetDefaultPrint()
    # status_bar.config(text=print_name)
    file_to_print = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:/gui/", title="Save File",
                                                 filetypes=((("text files", "*.txt"), ("html files", "*.html"),
                                                             ("Python Files", "*.py"), ("All File", "*.*"))))

    if file_to_print:
        win32api.ShellExecute(0, "print", file_to_print, None, ".", 0)


def delete():
    global selected
    my_text.delete.index(selected)


# create a toolbar frame
toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X)

# Create Main Frame
my_frame = Frame(root)
my_frame.pack(pady=5)

# Create Scrollbar for Text Editor
ver_scroll = Scrollbar(my_frame)
ver_scroll.pack(side=RIGHT, fill=Y)

# horizontal Scrollbar
hor_scroll = Scrollbar(my_frame, orient=HORIZONTAL)
hor_scroll.pack(side=BOTTOM, fill=X)

# Create Text Box
my_text = Text(my_frame, width=800, height=500, font=("calibri", 16), selectbackground="yellow",
               selectforeground="black", undo=True, yscrollcommand=ver_scroll.set, wrap="none",
               xscrollcommand=hor_scroll)
my_text.pack(fill=Y, expand=1)

# Configure Scrollbar
ver_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Create File menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_command(label="Print", command=print)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Create Edit Menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=my_text.edit_undo, accelerator="Ctrl+z")
edit_menu.add_command(label="Cut", command=lambda: cut_text(FALSE), accelerator="Ctrl+x")
edit_menu.add_command(label="Copy", command=lambda: copy_text(FALSE), accelerator="Ctrl+c")
edit_menu.add_command(label="Paste", command=lambda: paste_text(FALSE), accelerator="Ctrl+v")
edit_menu.add_command(label="Redo", command=my_text.edit_redo, accelerator="Ctrl+y")
edit_menu.add_command(label="Delete", command=delete)

# Status bar at the bottom
status_bar = Label(root, text='Ready', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=15)

# edit Bindings
root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)

# create button

bold_button = Button(toolbar_frame, text="Bold", command=bold_it)
bold_button.grid(row=0, column=0, sticky=W, padx=5)

italics_button = Button(toolbar_frame, text="Italics", command=italic_it)
italics_button.grid(row=0, column=1, sticky=W, padx=5)

underline_button = Button(toolbar_frame, text="Underline", command=underline_it)
underline_button.grid(row=0, column=2, sticky=W, padx=5)

find_button = Button(toolbar_frame, text="Find", command=find_text)
find_button.grid(row=0, column=3, sticky=W, padx=5)

root.mainloop()
