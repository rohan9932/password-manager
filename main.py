from tkinter import *
from tkinter import messagebox
import json
import random
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # making list of random items
    password_letters = [random.choice(letters) for new_item in range(random.randint(5,7))]
    password_numbers = [random.choice(numbers) for new_item in range(random.randint(3,5))]
    password_symbols = [random.choice(symbols) for new_item in range(random.randint(4, 6))]
    password_list = password_letters + password_numbers + password_symbols

    # shuffles the password list to generate random password
    random.shuffle(password_list)

    password = "".join(password_list) # it joins all the items in a single string
    pyperclip.copy(password) # automatically copies the password on the clipboard
    password_input.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    website = website_input.get()
    username = username_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": username,
            "password": password,
        },
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title= "Warning", message= "Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(message= f"These are the details entered:\nWebsite: {website}\n"
                                                           f"Email: {username}\nPassword: {password}\nIs it ok to save?")
        if is_ok:
            try:
                with open(file= "data.json", mode= "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except (FileNotFoundError, json.JSONDecodeError):
                with open(file= "data.json", mode= "w") as data_file:
                    json.dump(new_data, data_file, indent= 4)
            else:
                # Updating old data with new data
                data.update(new_data)
                with open(file= "data.json", mode= "w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent= 4)

    # reset the input boxes
    website_input.delete(0, END)
    password_input.delete(0, END)


# -------------------------- SEARCH DATA ------------------------------ #
def search_data():
    try:
        website = website_input.get()
        with open(file="data.json", mode="r") as data_file:
            # Reading data
            data = json.load(data_file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showinfo(message= "Data file does not exist.")
    else:
        if website in data:
            messagebox.showinfo(title= data[website], message= f"Email: {data[website]['email']}\n"
                                                               f"Password: {data[website]['password']}")
        else:
            messagebox.showinfo(message= "Sorry! Data not found!")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx= 50, pady= 50)

# Canvas (Logo part)
canvas = Canvas(width= 200, height= 200)
logo_img = PhotoImage(file= "logo.png")
canvas.create_image(125, 100, image= logo_img)
canvas.grid(column= 1, row= 0)

# titles
website_title = Label(text= "Website:")
website_title.grid(column= 0, row= 1)

username_title = Label(text= "Username/Email:")
username_title.grid(column= 0, row= 2)

password_title = Label(text= "Password:")
password_title.grid(column= 0, row= 3)

# buttons and entries
website_input = Entry(width= 21)
website_input.grid(column= 1, row= 1)
website_input.focus()

username_input = Entry(width= 38)
username_input.grid(column=1 , row= 2, columnspan= 2)
username_input.insert(0, "rohanrahim04@gmail.com")

password_input = Entry(width= 21)
password_input.grid(column= 1, row= 3)

search_btn = Button(text= "Search", width= 12, command= search_data)
search_btn.grid(column= 2, row= 1)

generate_pass_btn = Button(text= "Generate Password", width= 12, command= password_generator)
generate_pass_btn.grid(column= 2, row= 3)

add_btn = Button(text= "Add", width= 36, command= save_data)
add_btn.grid(column= 1, row= 4, columnspan= 2)


window.mainloop()
