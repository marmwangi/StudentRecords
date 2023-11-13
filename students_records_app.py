from tkinter import Tk, Label, Entry, Button, Text, END, NORMAL, DISABLED, font
import sqlite3
from tkinter.messagebox import showinfo
from datetime import datetime
import csv

# Creating student_records database
  # PantherID, Name, Email as columns
conn = sqlite3.connect('student_records.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS student_records
(pantherID INTEGER Primary Key, name TEXT, email TEXT)''')
conn.commit()

# Creating main application window 
app = Tk()
app.title("Student Records")
app.geometry("500x500")

# Labels for PantherID, Name, and Email in app
pantherid_label = Label(app, text="Panther ID")
pantherid_label.grid(row=0, column=0, sticky='W', pady=2)
name_label = Label(app, text="Name")
name_label.grid(row=1, column=0, sticky='W', pady=2)
email_label = Label(app, text="Email")
email_label.grid(row=2, column=0, sticky='W', pady=2)

# Entries for PantherID, Name, and Email for user input
pantherid_entry = Entry(app)
pantherid_entry.grid(row = 0, column = 1, sticky='W')
name_entry = Entry(app)
name_entry.grid(row=1, column=1, sticky='W')
email_entry = Entry(app)
email_entry.grid(row=2, column=1, sticky='W')

# Display for records
record_display = Text(app, height=10, width=50)
record_display.grid(row=5, column=0, columnspan=2, pady=5)

# Function that will clear entries for PantherID, Name, and Email 
#   when 'Add Student' button is clicked
def clear_entries():
    pantherid_entry.delete(0, END)
    name_entry.delete(0, END)
    email_entry.delete(0, END)

# Function that will check whether student record exists in student_record database 
def is_Student(panId):

    # counts if pantherid exists in database
        # will be 0 or 1
    cursor.execute('SELECT COUNT(1) from Students WHERE pantherid = ' + panId)
    records = cursor.fetchone()
    if records[0] == 0: # When record is not found
        showinfo(message=f'No record was found for {panId}')
        return False
    return True

# Function that will add student to student_records database 
#   when 'Add Student' button is clicked
def add_Students():
  try:
    pantherId = pantherid_entry.get()
    name = name_entry.get()
    email = email_entry.get()
    param = (pantherId, name, email)
    query = 'INSERT INTO student_records VALUES (?,?,?)'
    cursor.execute(query, param)
    conn.commit()
    showinfo(title="Student added!", message="Student added successfully")
    pantherid_entry.delete(0, END)
    name_entry.delete(0, END)
    email_entry.delete(0, END)
  except sqlite3.IntegrityError:
    showinfo("Entry already added")

# Function that will list students in student_record database 
#   when 'List Student' button is clicked
def list_Students():
  cursor.execute('''SELECT* FROM student_records''')
  records = cursor.fetchall() #displays all rows
  record_display.config(state=NORMAL)
  record_display.delete(1.0, END)
  timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  record_display.insert(END, f'Student List as of {timestamp}\n')
  for record in records:
    record_display.insert(END, f"PantherID: {record[0]}\nName: {record[1]}\nEmail:{record[2]}\n\n")

# Function that will search for student record in student_record database 
#   when 'Search Record' button is clicked
def search_record():
    try:
        pantherid = pantherid_entry.get()
        if is_Student(pantherid): # Checks that student record exists

            # Selects database entries that matches the pantherid
            cursor.execute('SELECT * from Students WHERE PantherID = ' + pantherid)
            records = cursor.fetchall()

            # Prints the record or records that match
            for record in records:
                record_display.insert(END, f"PantherID: {record[0]}   Name: {record[1]}   Email: {record[2]}\n")
            clear_entries()

    except sqlite3.OperationalError: # Exception for when pantherid is not entered
        showinfo(message='Please enter a PantherID to search for a record')

# Function that will update student record in student_record database 
#   when 'Update Record' button is clicked
def update_record():
    try:
        pantherid = pantherid_entry.get()
        name = name_entry.get()
        email = email_entry.get()
        if is_Student(pantherid): # Checks that student record exists

            # Updates record using pantherid
            cmd = 'UPDATE Students SET Name = ?, Email = ? WHERE PantherID = ?'
            cursor.execute(cmd, (name, email, pantherid))

    except sqlite3.OperationalError: # Exception for when pantherid is not entered
        showinfo(message='Please enter a PantherID, Name, and Email to update a record')

# Function that will delete student record in student_record database 
#   when 'Delete Record' button is clicked
def delete_record():
    try:
        pantherid = pantherid_entry.get()
        if is_Student(pantherid): # Checks that student record exists
            
            # Deletes record using pantherid
            cmd = 'DELETE from Students WHERE PantherID = ?'
            cursor.execute(cmd, (pantherid))
            showinfo(message='Record has been deleted')

    except sqlite3.OperationalError: # Exception for when pantherid is not entered
        showinfo(message='Please enter a PantherID to delete a record')

# Function that will export student_record database to 'student_records_csv' file
#   when 'Export to CSV' button is clicked
def export_to_csv():
    try:
        infile = open('students.csv', 'w') # Creates or opens existing 'students' csv
        writer = csv.writer(infile) # Creates a writer for csv

        # Selects the the Students database and puts it in a list of tuples
        cursor.execute('SELECT * from Students')
        records = cursor.fetchall()

        # Writes in rows in csv from database
        for record in records:
            writer.writerow(record)
        infile.close()

    except FileNotFoundError: # Exception for when file doesn't exist and won't create new file
        infile = open('students.csv', 'x')
        infile.close()
        showinfo('Please press the Export to CSV button again')

# Buttons for adding students to student_records database
add_Button = Button(app, text="Add Student", command=add_Students)
add_Button.grid(row=3, column=0, columnspan=2)

# Button for listing students in student_records database
list_Button = Button(app, text="List Students", command=list_Students)
list_Button.grid(row=4, column=0, columnspan=2)

# Button for searching for student record
search_button = Button(master=app, text='Search Record', command=search_record)
search_button.grid(row=3, column=1)

# Button for updating a student record
update_button = Button(master=app, text='Update Record', command=update_record)
update_button.grid(row=3, column=2)

# Button for deleting a student record
delete_button = Button(master=app, text='Delete Record', command=delete_record)
delete_button.grid(row=4, column=1)

# Button for exporting student_records database 
# to 'student_records_csv' csv file
export_csv_button = Button(master=app, text='Export to CSV', command=export_to_csv)
export_csv_button.grid(row=4, column=2)

app.mainloop()