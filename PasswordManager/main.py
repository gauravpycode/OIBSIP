from customtkinter import *
import sqlite3
import random
from PIL import Image
from email.message import EmailMessage
import smtplib
import ssl
from tkinter import ttk

set_appearance_mode("Dark")

window = CTk()
window.title("Password Manager")
window.geometry("700x500")
window.resizable(False, False)

def create_databases():
    global cursor, users_db
    users_db = sqlite3.connect("UsersData/users.db")
    cursor = sqlite3.Cursor(users_db)

    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                   Username TEXT,
                   Password TEXT,
                   Email TEXT);""")
    
    users_db.commit()


def login():
    global user_cursor, user_db, login_username
    login_username = login_username_entry.get()
    login_password = login_password_entry.get()

    try:
        if login_username != "" and login_password != "":
            cursor.execute("SELECT Password FROM users WHERE Username = ?;", [login_username])
            user_pass = cursor.fetchone()

            if (user_pass[0] == login_password):
                    user_db = sqlite3.connect(f"UsersData/{login_username}.db")
                    user_cursor = sqlite3.Cursor(user_db)
                    login_frame.forget()
                    main_window()
            else:
                text_label.configure(text="Invlaid Username or Password!")
    except TypeError:
        text_label.configure("Invlaid Username or Password!")


def signup():
    global user_db, user_cursor, sign_username
    sign_username = sign_username_entry.get()
    sign_password = sign_password_entry.get()
    confirm_password = sign_confirm_password_entry.get()

    if sign_password == confirm_password:
        if sign_username != "" and sign_password != "":
            cursor.execute("INSERT INTO users (Username, Password) VALUES (?,?)", (sign_username, sign_password))
            user_db = sqlite3.connect(f"UsersData/{sign_username}.db")
        else:
            print("Username or Password is Invalid!")
    else:
        print("Password does not match!")
    
    users_db.commit()
    sign_frame.forget()
    login_window()


def save_user_passwords():
    global user_db, saved_appname, saved_password, saved_username, user_cursor

    saved_appname = app_name_entry.get()
    saved_username = pass_username_entry.get()
    saved_password = pass_password_entry.get()

    user_cursor.execute("""CREATE TABLE IF NOT EXISTS passwords(
                        AppName TEXT,
                        Username TEXT,
                        Password Text);""")
    
    user_cursor.execute("INSERT INTO passwords (AppName, Username, Password) VALUES(?,?,?)", (saved_appname, saved_username, saved_password))

    user_cursor.execute("SELECT * FROM passwords")

    user_db.commit()


def update_slider_label(value):
    global capitals, smalls, numbers, symbols
    capitals = Capital_letters_number_label.configure(text=f"{int(Capital_letters_slider.get())}")
    smalls = small_letters_number_label.configure(text=f"{int(small_letters_slider.get())}")
    numbers = numbers_update_label.configure(text=f"{int(numbers_slider.get())}")
    symbols = symbols_update_label.configure(text=f"{int(symbols_slider.get())}")


def fill_password():
    password = show_password_label.cget("text")
    pass_password_entry.insert(1, password)
    toplvl_pass_window.destroy()


def generate_random_password():
    global show_password_label
    UPPERCASE = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q," "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    LOWERCASE = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    NUMBERS = ["1","2","3","4","5","6","7","8","9","0"]
    SYMBOLS = ["!", "`", "~", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-", "+", "=", "[", "]", "{", "}", "\\", "|", ";", ":", "\"", "'", ",", "<", ".", ">", "/", "?"]

    PASSWORD = []

    for i in range(0,int(Capital_letters_slider.get())):
        rndm = random.choice(UPPERCASE)
        PASSWORD.append(rndm)
    
    for j in range(0,int(numbers_slider.get())):
        rndm = random.choice(NUMBERS)
        PASSWORD.append(rndm)
    
    for k in range(0,int(symbols_slider.get())):
        rndm = random.choice(SYMBOLS)
        PASSWORD.append(rndm)

    for l in range(0,int(small_letters_slider.get())):
        rndm = random.choice(LOWERCASE)
        PASSWORD.append(rndm)

    random.shuffle(PASSWORD)
    PASSWORD = "".join(PASSWORD)

    show_password_label = CTkLabel(toplvl_frame, font=("Raleway", 20))
    show_password_label.place(x=50, y=420)

    fill_btn = CTkButton(toplvl_frame, text="Fill", font=("Raleway", 20), command=lambda: fill_password())
    fill_btn.place(x=500, y=400)

    show_password_label.configure(text=f"{PASSWORD}")


def show_passwords():
    global user_cursor

    pass_win = CTk()
    pass_win.title("Saved Passwords")
    pass_win.geometry("590x500")
    pass_win.resizable(False, False)

    user_cursor.execute("SELECT * FROM passwords")

    fetched_username = user_cursor.fetchall()

    tree = ttk.Treeview(pass_win, column=("c1", "c2", "c3"), show='headings', height=len(fetched_username))
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="App Name")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Username")
    tree.column("# 3", anchor=CENTER)
    tree.heading("# 3", text="Password")

    for i in range(len(fetched_username)):
        tree.insert('', 'end', text="", values=fetched_username[i])

    tree.pack()

    pass_win.mainloop()


def send_email():
    global otp

    otp = random.randint(100000, 999999)
    email_sender = "" # I have removed my email address due to security issue.
    email_password = ""
    email_receiver = email_entry.get()
    email_subject = "OTP Verification (Password Recovery)"
    email_body = f"""Your One-Time-Password for password recovery is {otp}.\nDo not share this code with anyone.\nThis code is valid only for 15 minutes."""

    print(email_receiver)

    if "@" in email_receiver and email_subject != "":
        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = email_receiver
        em["subject"] = email_subject
        em.set_content(email_body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
            msg_label.configure(text="OTP send successfully.")
            otp_entry.configure(state="normal")
    elif email_subject == "":
        msg_label.configure(text="Please fill the subject field.")
    elif "@" not in email_receiver:
        msg_label.configure(text="Invalid email format!")
    else:
        msg_label.configure(text="Some error occured please ensure that you fill all details correctly.")


def verify_otp():

    entered_otp = int(otp_entry.get())

    if entered_otp == otp:
        msg_label.configure(text="OTP Verified!")
        password_recovery_window()
    else:
        msg_label.configure(text="Invalid OTP")


def update_password():

    new_password = confirm_pass_entry.get()
    username = recovery_username_entry.get()

    cursor.execute("UPDATE users SET password = ? WHERE USERNAME = ?", (new_password, username))

    users_db.commit()

    recovery_msg_label.configure(text="Password Reset Successfully. Please Login Again!")

    print(cursor.fetchall())
    print(login_username)


def signup_window():
    global sign_frame, sign_password_entry, sign_confirm_password_entry, sign_username_entry

    sign_frame = CTkFrame(window, width=660, height=460)
    sign_frame.place(x=20, y=20)

    head_label = CTkLabel(sign_frame, text="Sign Up", font=("Raleway", 30))
    head_label.place(x=265, y=20)

    username_label = CTkLabel(sign_frame, text="Username", font=("Raleway", 20))
    username_label.place(x=170, y=100)

    sign_username_entry = CTkEntry(sign_frame, font=("Raleway", 20), width=250)
    sign_username_entry.place(x=300, y=100)

    password_label = CTkLabel(sign_frame, text="Password", font=("Raleway", 20))
    password_label.place(x=170, y=160)

    sign_password_entry = CTkEntry(sign_frame, font=("Raleway", 20), width=250)
    sign_password_entry.place(x=300, y=160)

    confirm_password_label = CTkLabel(sign_frame, text="Confirm Password", font=("Raleway", 20))
    confirm_password_label.place(x=90, y=220)

    sign_confirm_password_entry = CTkEntry(sign_frame, font=("Raleway", 20), width=250)
    sign_confirm_password_entry.place(x=300, y=220)

    signup_btn = CTkButton(sign_frame, font=("Raleway", 20), width=250, text="Sign Up", command=lambda: signup())
    signup_btn.place(x=190, y=300)

    login_label = CTkLabel(sign_frame, text="Already have an account ?", font=("Raleway", 20))
    login_label.place(x=135, y=400)

    login_btn = CTkButton(sign_frame, text="Login Here", font=("Raleway", 20), fg_color="#2a2a2b", text_color="#1f6aa5", hover_color="#2a2a2b", width=100, command=lambda: login_window())
    login_btn.place(x=385, y=400)


def login_window():
    global login_frame, login_password_entry, login_username_entry, text_label

    login_frame = CTkFrame(window, width=660, height=460)
    login_frame.place(x=20, y=20)

    head_label = CTkLabel(login_frame, text="Login", font=("Raleway", 30))
    head_label.place(x=310, y=20)

    username_label = CTkLabel(login_frame, text="Username", font=("Raleway", 20))
    username_label.place(x=170, y=120)

    login_username_entry = CTkEntry(login_frame, font=("Raleway", 20), width=250)
    login_username_entry.place(x=300, y=120)

    password_label = CTkLabel(login_frame, text="Password", font=("Raleway", 20))
    password_label.place(x=170, y=180)

    login_password_entry = CTkEntry(login_frame, font=("Raleway", 20), width=250)
    login_password_entry.place(x=300, y=180)

    login_btn = CTkButton(login_frame, font=("Raleway", 20), width=250, text="Login", command=lambda: login())
    login_btn.place(x=220, y=260)

    text_label = CTkLabel(login_frame, text="", font=("Raleway", 20))
    text_label.place(x=200, y=315)

    forget_password_btn = CTkButton(login_frame, text="Forget Password ?", font=("Raleway", 20), fg_color="#2a2a2b", text_color="#1f6aa5", hover_color="#2a2a2b", command=lambda: email_window())
    forget_password_btn.place(x=250, y=360)

    sign_label = CTkLabel(login_frame, text="Don't have an account ?", font=("Raleway", 20))
    sign_label.place(x=165, y=400)

    sign_btn = CTkButton(login_frame, text="Create One", font=("Raleway", 20), fg_color="#2a2a2b", text_color="#1f6aa5", hover_color="#2a2a2b", width=100, command=lambda: signup_window())
    sign_btn.place(x=390, y=400)


def main_window():
    global main_frame, pass_username_entry, pass_password_entry, app_name_entry

    main_frame = CTkFrame(window, width=660, height=460)
    main_frame.place(x=20, y=20)

    head_label = CTkLabel(main_frame, text="Password Manager", font=("Raleway", 30))
    head_label.place(x=210, y=20)

    app_name_label = CTkLabel(main_frame, text="App Name", font=("Raleway", 20))
    app_name_label.place(x=170, y=100)

    app_name_entry = CTkEntry(main_frame, font=("Raleway", 20), width=250)
    app_name_entry.place(x=300, y=100)

    username_label = CTkLabel(main_frame, text="Username", font=("Raleway", 20))
    username_label.place(x=170, y=160)

    pass_username_entry = CTkEntry(main_frame, font=("Raleway", 20), width=250)
    pass_username_entry.place(x=300, y=160)

    password_label = CTkLabel(main_frame, text="Password", font=("Raleway", 20))
    password_label.place(x=170, y=220)

    pass_password_entry = CTkEntry(main_frame, font=("Raleway", 20), width=250)
    pass_password_entry.place(x=300, y=220)

    create_rndm_pass_btn = CTkButton(main_frame, font=("Raleway", 20), width=250, text="Create Random Password", fg_color="#2a2a2b", text_color="#1f6aa5", hover_color="#2a2a2b", command = lambda: random_pass_window())
    create_rndm_pass_btn.place(x=190, y=300) 

    create_btn = CTkButton(main_frame, font=("Raleway", 20), width=250, text="Save Password", command=lambda: save_user_passwords())
    create_btn.place(x=190, y=360)

    show_btn = CTkButton(main_frame, font=("Raleway", 20), width=250, text="Show Passwords", command=lambda: show_passwords())
    show_btn.place(x=190, y=410)


def random_pass_window():
    global random_pass_frame, Capital_letters_number_label, small_letters_number_label, numbers_update_label, symbols_update_label, Capital_letters_slider, small_letters_slider, symbols_slider, numbers_slider, toplvl_frame, toplvl_pass_window

    toplvl_pass_window = CTkToplevel(window)
    toplvl_pass_window.title("Generate Random Password")
    toplvl_pass_window.geometry("700x500")
    toplvl_pass_window.resizable(False, False)

    toplvl_frame = CTkFrame(toplvl_pass_window, width=660, height=460)
    toplvl_frame.place(x=20, y=20)

    head_label = CTkLabel(toplvl_frame, text="Generate Random Password", font=("Raleway", 30))
    head_label.place(x=125, y=20)

    Capital_letters_label = CTkLabel(toplvl_frame, text="Capital Letters", font=("Raleway", 20))
    Capital_letters_label.place(x=110, y=100)

    Capital_letters_slider = CTkSlider(toplvl_frame, width=250, from_=0, to=100, number_of_steps=100, command=update_slider_label)
    Capital_letters_slider.place(x=260, y=105)

    Capital_letters_number_label = CTkLabel(toplvl_frame, text=0, font=("Raleway", 20))
    Capital_letters_number_label.place(x=530, y=100)

    small_letters_label = CTkLabel(toplvl_frame, text="Small Letters", font=("Raleway", 20))
    small_letters_label.place(x=110, y=160)

    small_letters_slider = CTkSlider(toplvl_frame, width=250, from_=0, to=100, number_of_steps=100, command=update_slider_label)
    small_letters_slider.place(x=260, y=165)

    small_letters_number_label = CTkLabel(toplvl_frame, text=0, font=("Raleway", 20))
    small_letters_number_label.place(x=530, y=160)

    numbers_label = CTkLabel(toplvl_frame, text="Numbers", font=("Raleway", 20))
    numbers_label.place(x=110, y=220)

    numbers_slider = CTkSlider(toplvl_frame, width=250, from_=0, to=100, number_of_steps=100, command=update_slider_label)
    numbers_slider.place(x=260, y=225)

    numbers_update_label = CTkLabel(toplvl_frame, text=0, font=("Raleway", 20))
    numbers_update_label.place(x=530, y=220)

    symbols_label = CTkLabel(toplvl_frame, text="Symbols", font=("Raleway", 20))
    symbols_label.place(x=110, y=280)

    symbols_slider = CTkSlider(toplvl_frame, width=250, from_=0, to=100, number_of_steps=100, command=update_slider_label)
    symbols_slider.place(x=260, y=285)

    symbols_update_label = CTkLabel(toplvl_frame, text=0, font=("Raleway", 20))
    symbols_update_label.place(x=530, y=280)

    create_btn = CTkButton(toplvl_frame, font=("Raleway", 20), width=250, text="Generate Password", command=lambda: generate_random_password())
    create_btn.place(x=190, y=360)

    toplvl_pass_window.mainloop()


def email_window():
    global email_entry, msg_label, otp_entry, otp_disabled, toplvl_email_window

    toplvl_email_window = CTkToplevel(window)
    toplvl_email_window.title("Email Verfication")
    toplvl_email_window.geometry("700x500")
    toplvl_email_window.resizable(False, False)

    email_frame = CTkFrame(toplvl_email_window, width=660, height=460)
    email_frame.place(x=20, y=20)

    head_label = CTkLabel(email_frame, text="Verify It's You", font=("Raleway", 20))
    head_label.place(x=270, y=20)

    email_label = CTkLabel(email_frame, text="Enter Email", font=("Raleway", 20))
    email_label.place(x=130, y=80)

    email_entry = CTkEntry(email_frame, font=("Raleway", 20), width=350)
    email_entry.place(x=250, y=80)

    email_btn = CTkButton(email_frame, font=("Raleway", 20), text="Send OTP", command=lambda: send_email())
    email_btn.place(x=260, y=160)

    email_label = CTkLabel(email_frame, text="Enter OTP", font=("Raleway", 20))
    email_label.place(x=130, y=240)

    otp_entry = CTkEntry(email_frame, font=("Raleway", 20), width=350, state="disabled")
    otp_entry.place(x=260, y=240)

    otp_btn = CTkButton(email_frame, font=("Raleway", 20), text="Verify OTP", command=lambda: verify_otp())
    otp_btn.place(x=260, y=320)

    msg_label = CTkLabel(email_frame, text="", font=("Raleway", 20))
    msg_label.place(x=235, y=420)

    toplvl_email_window.mainloop()


def password_recovery_window():
    global confirm_pass_entry, recovery_username_entry, recovery_msg_label

    pass_recovery_frame = CTkFrame(toplvl_email_window, width=660, height=460)
    pass_recovery_frame.place(x=20, y=20)

    head_label = CTkLabel(pass_recovery_frame, text="Reset Password", font=("Raleway", 20))
    head_label.place(x=270, y=20)

    recovery_username_label = CTkLabel(pass_recovery_frame, text="Username", font=("Raleway", 20))
    recovery_username_label.place(x=80, y=80)

    recovery_username_entry = CTkEntry(pass_recovery_frame, font=("Raleway", 20), width=350)
    recovery_username_entry.place(x=270, y=80)

    new_pass_label = CTkLabel(pass_recovery_frame, text="New Password", font=("Raleway", 20))
    new_pass_label.place(x=80, y=160)

    new_pass_entry = CTkEntry(pass_recovery_frame, font=("Raleway", 20), width=350)
    new_pass_entry.place(x=270, y=160)

    confirm_pass_label = CTkLabel(pass_recovery_frame, text="Confirm Password", font=("Raleway", 20))
    confirm_pass_label.place(x=80, y=240)

    confirm_pass_entry = CTkEntry(pass_recovery_frame, font=("Raleway", 20), width=350)
    confirm_pass_entry.place(x=270, y=240)

    reset_btn = CTkButton(pass_recovery_frame, font=("Raleway", 20), text="Reset Password", command=lambda: update_password())
    reset_btn.place(x=260, y=320)

    recovery_msg_label = CTkLabel(pass_recovery_frame, text="", font=("Raleway", 20))
    recovery_msg_label.place(x=80, y=400)

    toplvl_email_window.mainloop()

login_window()
create_databases()

window.mainloop()