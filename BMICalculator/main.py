from customtkinter import *
from tkinter import ttk
from PIL import Image
from datetime import datetime
import sqlite3
import matplotlib.pyplot as plt

set_appearance_mode("dark")

window = CTk()
window.title("BMI Calculator")
window.geometry("760x500")
window.resizable(False, False)

db = sqlite3.connect("history.db")
cursor = sqlite3.Cursor(db)


def calculate_bmi():
    global bmi,height, weight, category

    category = ""
    chart_img = CTkImage(Image.open("BIM.jpg"), size=(800,800))

    try:
        height = float(height_entry.get())
        weight = float(weight_entry.get())

        if weight_unit_label.get() == "g":
            weight = weight/1000

        if height_unit_label.get() == "cm":
            height = height*0.01

        elif height_unit_label.get() == "in":
            height = height*0.02540

        elif height_unit_label.get() == "ft":
            height = height*0.30480

        bmi = round(weight / height**2, 3)

        if bmi < 18.5:
            category = "UnderWeight"
        elif 18.5 < bmi < 24.9:
            category = "Normal"
        elif 25 < bmi < 29.9:
            category = "OverWeight"
        else:
            category = "Obese"

        save_data()

        category_label.configure(text=f"You are in {category} Category")
        result_label.configure(text=f"Your Body Mass Index is: {bmi}kg/m2")

        if show_chart_btn.get() == 1:

            toplvl_win = CTkToplevel(window)
            toplvl_win.geometry("800x800")
            toplvl_win.title("Body Mass Index Chart")

            chart_img_label = CTkLabel(toplvl_win, text="", image=chart_img)
            chart_img_label.place(x=0,y=0)

    except ValueError:
        category_label.configure(text="Enter Valid Value!")


def save_data():
    cursor.execute("""CREATE TABLE IF NOT EXISTS USERS(
                   Date TEXT,
                   Time TEXT,
                   Height REAL,
                   Weight REAL,
                   BMI REAL,
                   Category TEXT);""")
    
    cursor.execute("INSERT INTO USERS (Date, Time, Height, Weight, BMI, Category) VALUES(?,?,?,?,?,?)", (datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H-%M-%S"), height, weight, bmi, category))
    db.commit()


def show_data():
        data = cursor.execute("""SELECT * FROM USERS""")
        data_list = data.fetchall()

        data_win = CTkToplevel(window)
        data_win.title("History")
        data_win.geometry("1200x500")
        data_win.resizable(False, False)

        tree = ttk.Treeview(data_win, column=("c1", "c2", "c3", "c4", "c5", "c6"), show='headings', height=len(data_list))
        tree.column("# 1", anchor=CENTER)
        tree.heading("# 1", text="Date")
        tree.column("# 2", anchor=CENTER)
        tree.heading("# 2", text="Time")
        tree.column("# 3", anchor=CENTER)
        tree.heading("# 3", text="Height")
        tree.column("# 4", anchor=CENTER)
        tree.heading("# 4", text="Weight")
        tree.column("# 5", anchor=CENTER)
        tree.heading("# 5", text="BMI")
        tree.column("# 6", anchor=CENTER)
        tree.heading("# 6", text="Category")

        for i in range(len(data_list)):
            tree.insert('', 'end', text="", values=data_list[i])

        tree.pack()


def plot_graph():
    data = cursor.execute("""SELECT * FROM USERS""")
    data_list = data.fetchall()

    date_list = []
    bmi_list = []

    for i in range(len(data_list)):

        date = data_list[i][0]
        date_list.append(date)

        bmi = data_list[i][4]
        bmi_list.append(bmi)

        plt.plot(date_list, bmi_list)

    plt.show()
  

head_label = CTkLabel(window, text="BMI Calculator", font=("Raleway", 20))
head_label.place(x=330, y=25)

height_label = CTkLabel(window, text="Enter Height", font=("Raleway", 20))
height_label.place(x=150, y=90)

height_unit_label = CTkOptionMenu(window, values=["m", "cm", "in", "ft"], font=("Raleway", 20), width=20, dropdown_font=("Raleway", 20))
height_unit_label.place(x=520, y=90)

height_entry = CTkEntry(window, font=("Raleway", 20), height=20, width=200)
height_entry.place(x=300, y=90)

weight_label = CTkLabel(window, text="Enter Weight", font=("Raleway", 20))
weight_label.place(x=150, y=160)

weight_unit_label = CTkOptionMenu(window, values=["kg", "g"], font=("Raleway", 20), width=20, dropdown_font=("Raleway", 20))
weight_unit_label.place(x=520, y=160)

weight_entry = CTkEntry(window, font=("Raleway", 20), height=20, width=200)
weight_entry.place(x=300, y=160)

history_btn = CTkButton(window, text="History", font=("Raleway", 20), height=30, width=200, command=lambda:show_data())
history_btn.place(x=60, y=260)

calculate_btn = CTkButton(window, text="Calculate", font=("Raleway", 20), height=30, width=200, command=lambda:calculate_bmi())
calculate_btn.place(x=280, y=260)

graph_btn = CTkButton(window, text="History Visual", font=("Raleway", 20), height=30, width=200, command=lambda:plot_graph())
graph_btn.place(x=500, y=260)

show_chart_btn = CTkCheckBox(window, text="Show BMI Chart", font=("Raleway", 20))
show_chart_btn.place(x=275, y=330)

result_label = CTkLabel(window, text="", font=("Raleway", 20))
result_label.place(x=180, y=380)

category_label = CTkLabel(window, text="", font=("Raleway", 20))
category_label.place(x=180, y=430)

window.mainloop()

cursor.close()
db.close()