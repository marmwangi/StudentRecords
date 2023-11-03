from tkinter import Tk, Label, Entry, Button, Text, END, NORMAL, DISABLED, font
import sqlite3
from tkinter.messagebox import showinfo
from datetime import datetime

#making database
conn = sqlite3.connect('student_records.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS student_records
(pantherID INTEGER Primary Key, name TEXT, email TEXT)''')
conn.commit() #permantly saves changes, can't undo

app = Tk()
app.title("Student Records")
app.geometry("500x500")

#making labels
pantherid_label = Label(app, text="Panther ID")
pantherid_label.grid(row=0, column=0, sticky='W', pady=2)
name_label = Label(app, text="Name")
name_label.grid(row=1, column=0, sticky='W', pady=2)
email_label = Label(app, text="Email")
email_label.grid(row=2, column=0, sticky='W', pady=2)

#creating entries for user input
pantherid_entry = Entry(app)
pantherid_entry.grid(row = 0, column = 1, sticky='W')
name_entry = Entry(app)
name_entry.grid(row=1, column=1, sticky='W')
email_entry = Entry(app)
email_entry.grid(row=2, column=1, sticky='W')

#display for records
record_display = Text(app, height=10, width=50)
record_display.grid(row=5, column=0, columnspan=2, pady=5)

#functions
def add_Students():
  try:
    pantherId = pantherid_entry.get()
    name = name_entry.get()
    email = email_entry.get()
    param = (pantherId, name, email)
    query = '''INSERT INTO student_records VALUES (?,?,?)'''
    cursor.execute(query, param)
    conn.commit()
    showinfo(title="Student added!", message="Student added successfully")
    pantherid_entry.delete(0, END)
    name_entry.delete(0, END)
    email_entry.delete(0, END)
  except sqlite3.IntegrityError:
    showinfo                                    ("Entry already added")

def list_Students():
  cursor.execute('''SELECT* FROM student_records''')
  records = cursor.fetchall() #displays all rows
  record_display.config(state=NORMAL)
  record_display.delete(1.0, END)
  timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  record_display.insert(END, f'Student List as of {timestamp}\n')
  for record in records:
    record_display.insert(END, f"PantherID: {record[0]}\nName: {record[1]}\nEmail:{record[2]}\n\n")

#making buttons
add_Button = Button(app, text="Add Student", command=add_Students)
add_Button.grid(row=3, column=0, columnspan=2)

list_Button = Button(app, text="List Students", command=list_Students)
list_Button.grid(row=4, column=0, columnspan=2)

add_Button.config(command=add_Students)
list_Button.config(command=list_Students)

app.mainloop()