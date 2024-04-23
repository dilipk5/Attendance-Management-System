from tkinter import *
from tkinter import messagebox, filedialog, ttk
import csv
import firebase_admin
from firebase_admin import db, credentials
from tkinter import simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {'databaseURL': "https://attendance-management-sy-967d3-default-rtdb.asia-southeast1.firebasedatabase.app/"})
ref = db.reference('/')


# Global variables
subjects = []
data = {}


# User accounts
student_accounts = {
    "student1": "password1",
    "student2": "password2",
    "2":'2'
}

teacher_accounts = {
    "teacher1": "password3",
    "teacher2": "password4",
    "1": '1'
}

BG_COLOR = "#D2B48C"
FRAME_COLOR = "#ADD8E6"
ACCENT_COLOR = "#8B0000"
FONT = ("roboto", 12)

def clearasdf():
    for widget in asdf.winfo_children():
        widget.destroy()
def student_login():
    global usertype
    usertype = "Student"
    clearasdf()
    global studentdatafromdb, totalclass, attendedclass
    totalclass = 0
    attendedclass = 0
    student_id = simpledialog.askstring("Student Login", "Enter your Student ID:")
    if student_id:
        try:
            studentdatafromdb = ref.get().get(student_id)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        subject_titles = ["Phy", "M-2", "BXE", "Mech", "graphics"]
        for i in range(5):
            totalclass = totalclass + int(studentdatafromdb.get('subjects').get(subject_titles[i]).get('totalclass'))
            attendedclass = attendedclass + int(studentdatafromdb.get('subjects').get(subject_titles[i]).get('attended'))
        print(studentdatafromdb.get('subjects').get(subject_titles[i]).get('totalclass'))
        print(totalclass)
        frame1()
        frame2()
        frame3()



def teacher_login():
    global usertype
    clearasdf()
    usertype = "Teacher"
    global username, password, loginframev
    loginframev = Frame(root)
    loginframev.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
    Label(loginframev, text="Enter username").grid()
    username = Entry(loginframev)
    username.grid()
    Label(loginframev, text="Password").grid()
    password = Entry(loginframev)
    password.grid()
    Button(loginframev, text="Login" ,command=teacherlogincheck).grid()

def teacherlogincheck():
    global fg
    fg = username.get()
    print(username.get(), password.get())
    if username.get() in teacher_accounts and teacher_accounts[username.get()] == password.get():
        clearloginframe()
        frame1()
        frame2()
        frame3()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")
    
def clearloginframe():
    for widget in loginframev.winfo_children():
        widget.destroy()

def current_attendance(totalclass, attendedclass):
    if totalclass == 0 or attendedclass == 0:
        return 0
    else:
        return (attendedclass / totalclass) * 100

def frame1():
    global tc, ac, ca
    if usertype == "Student":
        topframe = LabelFrame(root, text=f"Student Info", bg=BG_COLOR, fg=FRAME_COLOR, bd=2)
        topframe.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        f1namelabel = Label(topframe, text=f'Welcome, {studentdatafromdb['name']}', bg="#D2B48C", fg="black")
        f1namelabel.grid(row=0, column=0, padx=5, pady=5)
        tc = Label(topframe, text=f'Total classes: {totalclass}', bg="#D2B48C", fg="black")
        tc.grid(row=0, column=1, padx=5, pady=5)
        ac = Label(topframe, text=f'Attended classes: {attendedclass}', bg="#D2B48C", fg="black")
        ac.grid(row=0, column=2, padx=5, pady=5)
        ca = Label(topframe, text=f'Current attendance: {current_attendance(totalclass, attendedclass)}%', bg="#D2B48C", fg="black")
        ca.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
    
    elif usertype == "Teacher":
        topframe = LabelFrame(root, text=f"Teacher Panel", bg="#D2B48C", fg="black", bd=2)
        topframe.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        f1namelabel = Label(topframe, text=f'Welcome {fg}', bg="#D2B48C", fg="black")
        f1namelabel.grid(row=0, column=0, padx=5, pady=5)

    

def frame2():
    leftframe = LabelFrame(root, text="Actions", height=700, width=200, bg="#ADD8E6", fg="black", bd=2)
    leftframe.grid(row=1, column=0, padx=10, pady=10)

    if usertype == "Student":
        btn0 = Button(leftframe, text="All subject attendance", command=show_student_sub_data, bg="#ADD8E6", fg="black")
        btn0.grid(row=0, column=0, padx=5, pady=5)
        btn1 = Button(leftframe, text="Graph and statistics", command=graphandstat, bg="#ADD8E6", fg="black")
        btn1.grid(row=1, column=0, padx=5, pady=5)
        btn3 = Button(leftframe, text="Leave calculator", command=Leavecalculator, bg="#ADD8E6", fg="black")
        btn3.grid(row=2, column=0, padx=5, pady=5)
        btn4 = Button(leftframe, text="Attendance improver", command=attendanceimprover, bg="#ADD8E6", fg="black")
        btn4.grid(row=3, column=0, padx=5, pady=5)
        btn5 = Button(leftframe, text="Leaderboard", command=Leaderboard, bg="#ADD8E6", fg="black")
        btn5.grid(row=4, column=0, padx=5, pady=5)
        btn9 = Button(leftframe, text="Quit app", command=rootquit, bg="#ADD8E6", fg="black")
        btn9.grid(row=5, column=0, padx=5, pady=5)

    elif usertype == "Teacher":
        btn2 = Button(leftframe, text="Mark Student attendance", command=markattendance, bg="#ADD8E6", fg="black")
        btn2.grid(row=0, column=0, padx=5, pady=5)
        btn7 = Button(leftframe, text="Add CSV file", command=add_csv_file, bg="#ADD8E6", fg="black")
        btn7.grid(row=1, column=0, padx=5, pady=5)
        btn8 = Button(leftframe, text="All student data", command=allstudentdata, bg="#ADD8E6", fg="black")
        btn8.grid(row=2, column=0, padx=5, pady=5)
        btn6 = Button(leftframe, text="Attendance Forecasting", command=ps, bg="#ADD8E6", fg="black")
        btn6.grid(row=3, column=0, padx=5, pady=5)
        btn9 = Button(leftframe, text="Quit app", command=rootquit, bg="#ADD8E6", fg="black")
        btn9.grid(row=4, column=0, padx=5, pady=5)

def frame3():
    global rightframe
    rightframe = Frame(root, bg="#FFF0F5", height=700, width=1000, bd=2)
    rightframe.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
    if usertype == "Teacher":
        clearrightframe()
        markattendance()
    elif usertype == "Student":
        clearrightframe()
        show_student_sub_data()

def ps():
    clearrightframe()
    Label(rightframe, text="This feature will come soon")

def show_student_sub_data():
    clearrightframe()
    student_data_tree = ttk.Treeview(rightframe, columns=("Subject", "Attended", "Total"), show="headings")

# Define column headings
    student_data_tree.heading("Subject", text="Subject")
    student_data_tree.heading("Attended", text="Attended")
    student_data_tree.heading("Total", text="Total Classes")

    student_subs = studentdatafromdb.get('subjects')

    for subjects, values in student_subs.items():
        attended = values["attended"]
        total_classes = values["totalclass"]
        student_data_tree.insert("", "end", values=(subjects, attended, total_classes))
    
    student_data_tree.grid(row=0, column=0, padx=5, pady=5)

def markattendance():
    clearrightframe()
    global markattendanceframe, heading, student_data_button
    markattendanceframe = Frame(rightframe)
    markattendanceframe.grid()
    heading = Label(markattendanceframe, text="Daily attendance", font=("Arial", 16), bg="#FFF0F5", fg="#8B0000")
    heading.grid(row=0, column=0, padx=5, pady=5)

    student_data_button = Button(markattendanceframe, text="Add Student Attendance", command=student_data, bg="#8B0000", fg="#FFF0F5")
    student_data_button.grid(row=1, column=0, padx=5, pady=5)
def student_data():
    clearrightframe()
    global student_data_frame, student_name_entry, student_id_entry, subject_tc_entries, subject_ac_entries, subject_data_table, subject_titles
    student_data_frame = Frame(rightframe)
    student_data_frame.grid()
    heading = Label(student_data_frame, text="Student Data", font=("Arial", 16), bg="#FFF0F5", fg="#8B0000")
    heading.grid(row=0, column=0, padx=5, pady=5)

    student_name_label = Label(student_data_frame, text="Student Name", bg="#FFF0F5", fg="#8B0000")
    student_name_label.grid(row=1, column=0, padx=5, pady=5)
    student_name_entry = Entry(student_data_frame, bg="#FFF0F5", fg="#8B0000")
    student_name_entry.grid(row=2, column=0, padx=5, pady=5)

    student_id_label = Label(student_data_frame, text="Student ID", bg="#FFF0F5", fg="#8B0000")
    student_id_label.grid(row=1, column=1, padx=5, pady=5)
    student_id_entry = Entry(student_data_frame, bg="#FFF0F5", fg="#8B0000")
    student_id_entry.grid(row=2, column=1, padx=5, pady=5)

    subject_titles = ["Phy", "M-2", "BXE", "Mech", "graphics"]
    subject_tc_entries = []
    subject_ac_entries = []

    for i in range(5):
        subject_tc_label = Label(student_data_frame, text=f"{subject_titles[i]} Total Classes", bg="#FFF0F5", fg="#8B0000")
        subject_tc_label.grid(row=3, column=i, padx=5, pady=5)
        subject_tc_entry = Entry(student_data_frame, bg="#FFF0F5", fg="#8B0000")
        subject_tc_entry.grid(row=4, column=i, padx=5, pady=5)
        subject_tc_entries.append(subject_tc_entry)

        subject_ac_label = Label(student_data_frame, text=f"{subject_titles[i]} Attended Classes", bg="#FFF0F5", fg="#8B0000")
        subject_ac_label.grid(row=5, column=i, padx=5, pady=5)
        subject_ac_entry = Entry(student_data_frame, bg="#FFF0F5", fg="#8B0000")
        subject_ac_entry.grid(row=6, column=i, padx=5, pady=5)
        subject_ac_entries.append(subject_ac_entry)

    add_data_button = Button(student_data_frame, text="Add Data", command=add_student_data, bg="#8B0000", fg="#FFF0F5")
    add_data_button.grid(row=7, column=0, columnspan=5, padx=5, pady=5)

    subject_data_table = Frame(rightframe)
    subject_data_table.grid(row=8, column=0, columnspan=5, padx=5, pady=5)

    # return subject_tc_entries, subject_ac_entries

def add_student_data():
    global subject_tc_entries_cook, subject_ac_entries_cook, student_name, student_id, subject_titles
    student_name = student_name_entry.get()
    student_id = student_id_entry.get()
    subject_ac_entries_cook = []
    subject_tc_entries_cook = []
    subject_titles = ["Phy", "M-2", "BXE", "Mech", "graphics"]
    # subject_titles = ["Phy", "M-2"]

    for i in range(5):
        subject_tc_entries_cook.append(int(subject_tc_entries[i].get()))
        subject_ac_entries_cook.append(int(subject_ac_entries[i].get()))

    print(subject_ac_entries_cook, "subject_ac_entries_cook")
    print(subject_tc_entries_cook, "subject_tc_entries_cook")

    try:
            if subject_ac_entries_cook[i] > subject_tc_entries_cook[i]:
                raise ValueError("Error", "Total classes cannot be greater than attended classes")
            else:
                display_student_data(student_name, student_id, subject_titles)
    except ValueError as e:
            messagebox.showerror("Error", str(e))
def display_student_data(student_name, student_id, subject_titles):
    clearrightframe()
    global subject_data_table
    subject_data_table = Frame(rightframe)
    subject_data_table.grid(row=0, column=0, padx=10, pady=10)

    # Display student name and ID
    student_info_label = Label(subject_data_table, text=f"Student Name: {student_name}, Student ID: {student_id}", font=("Arial", 14), bg="#FFF0F5", fg="#8B0000")
    student_info_label.grid(row=0, column=0, columnspan=5, padx=5, pady=5)

    print(student_name, student_id, subject_titles, subject_tc_entries_cook, subject_ac_entries_cook)
    # Display subject data
    for i in range(5):
        subject_title_label = Label(subject_data_table, text=subject_titles[i], font=("Arial", 12), bg="#FFF0F5", fg="#8B0000")
        subject_title_label.grid(row=1, column=i, padx=5, pady=5)

        subject_tc_label = Label(subject_data_table, text=f"Total Classes: {subject_tc_entries_cook[i]}", font=("Arial", 12), bg="#FFF0F5", fg="#8B0000")
        subject_tc_label.grid(row=2, column=i, padx=5, pady=5)

        subject_ac_label = Label(subject_data_table, text=f"Attended Classes: {subject_ac_entries_cook[i]}", font=("Arial", 12), bg="#FFF0F5", fg="#8B0000")
        subject_ac_label.grid(row=3, column=i, padx=5, pady=5)

    btn = Button(rightframe, text="Add to database", command=addtodb)
    btn.grid()

def addtodb():
    data[student_id] = {
                            "name": student_name,
                            "student id": student_id,
                            "subjects": {
                                subject_titles[0]: {
                                    "totalclass": subject_tc_entries_cook[0],
                                    "attended": subject_ac_entries_cook[0]
                                },
                                subject_titles[1]: {
                                    "totalclass": subject_tc_entries_cook[1],
                                    "attended": subject_ac_entries_cook[1]
                                },
                                subject_titles[2]: {
                                    "totalclass": subject_tc_entries_cook[2],
                                    "attended": subject_ac_entries_cook[2]
                                },
                                subject_titles[3]: {
                                    "totalclass": subject_tc_entries_cook[3],
                                    "attended": subject_ac_entries_cook[3]
                                },
                                subject_titles[4]: {
                                    "totalclass": subject_tc_entries_cook[4],
                                    "attended": subject_ac_entries_cook[4]
                                },
                            }
                        }
        
    try:
        ref.update(data)
        messagebox.showinfo("Success", "Data added to database")
    except:
        messagebox.showerror("Error", "Error adding data to database")
    clearrightframe()
    frame1()
    frame2()
    frame3()

def add_csv_file():
    clearrightframe()
    global csvdataframe
    csvdataframe = Frame(rightframe)
    csvdataframe.grid()
    # Open a file dialog to select the CSV file
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])


    if file_path:
        # Read the CSV file
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                student_name = row["name"]
                student_id = row["student_id"]
                subjects = {
                    "M-2": {
                        "totalclass": int(row["m2_total_classes"]),
                        "attended": int(row["m2_classes_attended"])
                    },
                    "Phy": {
                        "totalclass": int(row["phy_total_classes"]),
                        "attended": int(row["phy_classes_attended"])
                    },
                    "BXE": {
                        "totalclass": int(row["bxe_total_classes"]),
                        "attended": int(row["bxe_classes_attended"])
                    },
                    "Mech": {
                        "totalclass": int(row["mech_classes_total"]),
                        "attended": int(row["mech_classes_attended"])
                    },
                    "graphics": {
                        "totalclass": int(row["graphics_total_class"]),
                        "attended": int(row["graphics_classes_attended"])
                    }
                }
                data[student_id] = {
                    "name": student_name,
                    "student id": student_id,
                    "subjects": subjects
                }
        print(data)

        csv_tree = ttk.Treeview(rightframe, columns=("Name", "Student ID", "Subject", "Attended", "Total"), show="headings")
        csv_tree.heading("Name", text="Name")
        csv_tree.heading("Student ID", text="Student ID")
        csv_tree.heading("Subject", text="Subject")
        csv_tree.heading("Attended", text="Attended")
        csv_tree.heading("Total", text="Total Classes")

        for student_id, student_data in data.items():
            name = student_data["name"]
            student_id = student_data["student id"]
            subjects = student_data["subjects"]

            for subject, values in subjects.items():
                attended = values["attended"]
                total_classes = values["totalclass"]
                csv_tree.insert("", "end", values=(name, student_id, subject, attended, total_classes))

        csv_tree.grid()
        
        Button(rightframe, text="add to database", command=csvdatatodb).grid()
        
def csvdatatodb():
    try:
        ref.update(data)
        messagebox.showinfo("Success", "Data added to database")
        clearrightframe()
        markattendance()
    except:
        messagebox.showerror("Error", "Error adding data to database")

def graphandstat():
    clearrightframe()
    graphandstatframe = Frame(rightframe)
    graphandstatframe.grid()
    heading = Label(graphandstatframe, text="Graph and Statistics")
    heading.grid(row=0, column=0, padx=5, pady=5)
    
    graphdata = studentdatafromdb.get('subjects')

    subjects = list(graphdata.keys())
    attended = [graphdata[subject]["attended"] for subject in subjects]
    totalclass = [graphdata[subject]["totalclass"] for subject in subjects]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    canvas = FigureCanvasTkAgg(fig, master=rightframe)
    canvas_widget = canvas.get_tk_widget()
    
    ax1.clear()
    ax1.bar(subjects, attended, color='skyblue', label='Attended')
    ax1.bar(subjects, [totalclass[i]-attended[i] for i in range(len(subjects))], bottom=attended, color='orange', label='Missed')
    ax1.set_xlabel('Subjects')
    ax1.set_ylabel('Number of Classes')
    ax1.set_title('Attendance Comparison')
    ax1.legend()

    ax2.clear()
    ax2.pie(attended, labels=subjects, autopct='%1.1f%%', startangle=140)
    ax2.set_title('Attendance Percentage')

    canvas.draw()
    canvas_widget.grid(row=0, column=0)

def Leavecalculator():
    clearrightframe()
    heading = Label(rightframe, text="Leave calculator")
    heading.grid(row=0, column=0, padx=5, pady=5)
    leaves = 0
    a = totalclass
    b = attendedclass
    target_attendance = 75

    if current_attendance(a,b) > target_attendance:
        while True:
                leaves = leaves + 1
                a = a + leaves
                b = b
                if (b/a) * 100 < target_attendance:
                    print(leaves - 1)
                    break
        Label(rightframe, text=f'You can bunk the upcoming {leaves - 1} lectures and after missing {leaves - 1} lectures your attendance will be 75%').grid()
    else:
        Label(rightframe, text="you cant take more leaves you have to imporve your attendance").grid()

def attendanceimprover():
    a = totalclass
    b = attendedclass
    clearrightframe()
    heading = Label(rightframe, text="Attendance Improver")
    heading.grid(row=0, column=0, padx=5, pady=5)

    currentclasses = 0
    target_attendance = 75
    c = 0

    if current_attendance(a,b) > target_attendance:
        Label(rightframe, text=f'You have already cleared the target attendance').grid()
    else:
        while True:
                currentclasses = currentclasses + 1
                a = a + currentclasses
                b = b + currentclasses
                if (b/a)*100 > target_attendance:
                    print(currentclasses)
                    break
                    
        Label(rightframe, text=f'You have to attend upcoming {currentclasses} leactures to clear your target attendance').grid(row=1, column=0, padx=5, pady=5)

def Leaderboard():
    clearrightframe()
    heading = Label(rightframe, text="Leaderboard").grid(row=0, column=0, padx=5, pady=5)

    student_data_fb = ref.get()
    ratios = {}

    for student_id, student in student_data_fb.items():
        total_attended = sum(subject['attended'] for subject in student['subjects'].values())
        total_classes = sum(subject['totalclass'] for subject in student['subjects'].values())
        if total_classes > 0:
            ratio = total_attended / total_classes
            ratios[student_id] = (student['name'], ratio)

    leaderboard_tree = ttk.Treeview(rightframe, columns=("Name", "Ratio"), show="headings")
    leaderboard_tree.heading("Name", text="Name")
    leaderboard_tree.heading("Ratio", text="Attendance Ratio")

    sorted_ratios = sorted(ratios.items(), key=lambda x: x[1][1], reverse=True)
    for i, (student_id, (name, ratio)) in enumerate(sorted_ratios, start=1):
        leaderboard_tree.insert("", "end", values=(name, f"{ratio:.2f}"))

    leaderboard_tree.grid(row=0, column=0, padx=5, pady=5)

def allstudentdata():
    clearrightframe()
    allstudentsdata = ref.get()
    print(allstudentsdata)

    allstudentdata_tree = ttk.Treeview(rightframe, columns=("Student Name", "Student ID", "Subject", "Attended", "Total"))

    # Define column headings
    allstudentdata_tree.heading("Student Name", text="Student Name")
    allstudentdata_tree.heading("Student ID", text="Student ID")
    allstudentdata_tree.heading("Subject", text="Subject")
    allstudentdata_tree.heading("Attended", text="Attended")
    allstudentdata_tree.heading("Total", text="Total Classes")

    # Insert data into the allstudentdata_treeview
    for student_id, allstudentsdata in allstudentsdata.items():
        name = allstudentsdata["name"]
        student_id = allstudentsdata["student id"]
        subjects = allstudentsdata["subjects"]

        for subject, values in subjects.items():
            attended = values["attended"]
            total_classes = values["totalclass"]
            allstudentdata_tree.insert("", "end", values=(name, student_id, subject, attended, total_classes))

    # Pack the allstudentdata_treeview widget
    allstudentdata_tree.grid(row=0, column=0, padx=5, pady=5)

def rootquit():
    root(quit())

def clearrightframe():
    for widget in rightframe.winfo_children():
        widget.destroy()

def loginframe():
    global asdf
    asdf = Frame(root)
    asdf.grid()
    label = Label(asdf, text="Select login type:")
    label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    student_button = Button(asdf, text="Student Login", command=student_login)
    student_button.grid(row=1, column=0, padx=10, pady=10)

    teacher_button = Button(asdf, text="Teacher Login", command=teacher_login)
    teacher_button.grid(row=1, column=1, padx=10, pady=10)

root = Tk()
root.geometry("1200x720")
loginframe()
root.mainloop()