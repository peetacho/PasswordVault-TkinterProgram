from tkinter import *
from Entries import Entries
import binascii
import json


def rgb2hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def enc(s):
    return bin(int.from_bytes(s.encode(), 'big'))


def dec(s):
    n = int(s, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()


window_bg = rgb2hex(230, 230, 230)

root = Tk()
root.title('Password Vault')
root.configure(bg=window_bg)
# 842x480+425+250
root.geometry(newGeometry="842x480+425+250")
root.resizable(False, False)

####################### ENTRY ##########################

ENTRIES = []

# json_string = json.dumps([ob.__dict__ for ob in ENTRIES])
# print(json_string)

f_1 = open("/Users/peter/Desktop/Programming/Python/PasswordVault/.pass.txt", "r")
not_available = '[{"account": "new  ", "username": "  ", "email": "  ", "password": "  ", "description": "  "}]'
try:
    t_1 = f_1.readlines()[1]
    if t_1 == "[]":
        t_1 = not_available
except:
    t_1 = not_available

json_string = t_1
f_1.close()


# ENTRIES =
# print(json.loads(json_string)[1]["account"])

for var in json.loads(dec(json_string)):
    # print(var)
    temp = Entries(var["account"], var["username"],
                   var["email"], var["password"], var["description"])
    # for key, value in var.items():
    #     temp = [key, value]
    ENTRIES.append(temp)

# print(ENTRIES)
# listbox
scrollbar = Scrollbar(root)
mylist = Listbox(root, yscrollcommand=scrollbar.set)


def selectedIndex():
    index = 0
    try:
        index = mylist.curselection()[0]
    except:
        index = 0

    # print(index)
    return index


# Entry Item
frame = LabelFrame(root)

for entry in ENTRIES:
    mylist.insert(END, entry)

scrollbar.config(command=mylist)


def getClipBoard(mode):
    root.clipboard_clear()
    text = ""

    if mode == "acc":
        text = accText.get("1.0", "end").strip()
    elif mode == "user":
        text = userText.get("1.0", "end").strip()
    elif mode == "email":
        text = emailText.get("1.0", "end").strip()
    elif mode == "pass":
        text = passText.get("1.0", "end").strip()
    elif mode == "desc":
        text = descText.get("1.0", "end").strip()

    root.clipboard_append(text)


# account
accCopy = Button(frame, text="Account:", borderwidth=0,
                 command=lambda: getClipBoard('acc'))
accCopy.pack(anchor="w")
accText = Text(frame, height=2)
accText.insert(END, ENTRIES[0].account)
accText.pack(anchor="w", padx=10)

# username
userLabel = Button(frame, text="Username:", borderwidth=0,
                   command=lambda: getClipBoard('user'))
userLabel.pack(anchor="w")
userText = Text(frame, height=2)
userText.insert(END, ENTRIES[0].username)
userText.pack(anchor="w", padx=10)

# email
emailLabel = Button(frame, text="Email:", borderwidth=0,
                    command=lambda: getClipBoard('email'))
emailLabel.pack(anchor="w")
emailText = Text(frame, height=2)
emailText.insert(END, ENTRIES[0].email)
emailText.pack(anchor="w", padx=10)

# password
passLabel = Button(frame, text="Password:", borderwidth=0,
                   command=lambda: getClipBoard('pass'))
passLabel.pack(anchor="w")
passText = Text(frame, height=2)
passText.insert(END, ENTRIES[0].password)
passText.pack(anchor="w", padx=10)

# description
descLabel = Button(frame, text="Description:", borderwidth=0,
                   command=lambda: getClipBoard('desc'))
descLabel.pack(anchor="w")
descText = Text(frame, height=2)
descText.insert(END, ENTRIES[0].description)
descText.pack(anchor="w", padx=10)


def changeInFile():

    # convert ENTRIES to JSON string
    json_string = json.dumps([ob.__dict__ for ob in ENTRIES])
    # print(json_string)

    # opens pass.txt read mode
    f_1 = open(
        "/Users/peter/Desktop/Programming/Python/PasswordVault/.pass.txt", "r")

    list_lines = f_1.readlines()

    # listlines 1 = encoded json string
    list_lines[1] = enc(json_string)

    # opens pass.txt write mode
    f_1 = open(
        "/Users/peter/Desktop/Programming/Python/PasswordVault/.pass.txt", "w")

    # writes to all lines
    f_1.writelines(list_lines)
    f_1.close()


def addEntry():
    temp = Entries("new", "", "", "", "")
    mylist.insert(END, temp)
    ENTRIES.append(temp)
    changeInFile()


def deleteEntry():
    index = selectedIndex()
    mylist.delete(index)
    ENTRIES.pop(index)
    changeInFile()
    # print(ENTRIES)


def editEntry():
    index = selectedIndex()
    at = accText.get("1.0", "end").strip()
    ut = userText.get("1.0", "end").strip()
    et = emailText.get("1.0", "end").strip()
    pt = passText.get("1.0", "end").strip()
    dt = descText.get("1.0", "end").strip()

    temp = Entries(at, ut, et, pt, dt)

    ENTRIES[index] = temp
    changeInFile()


    # entry info
search = Entry(root, borderwidth=0, width=25)
buttonFrame = LabelFrame(root, borderwidth=0)
add = Button(buttonFrame, text="+", height=2,
             width=4, highlightbackground="green", command=addEntry)
delete = Button(buttonFrame, text="-", height=2,
                width=4, highlightbackground="red", command=deleteEntry)
edit = Button(buttonFrame, text="Enter Changes", height=2,
              width=10, highlightbackground="yellow", command=editEntry)


def enterPass(event):
    f_0 = open(
        "/Users/peter/Desktop/Programming/Python/PasswordVault/.pass.txt", "r")
    t_0 = f_0.readlines()[0]
    enterPass = dec(t_0)
    f_0.close()
    # print(enterPass)
    if enter.get() == enterPass:  # enterPass:
        enter.pack_forget()
        enterLabel.pack_forget()
        root.unbind('<Return>')

        # pack search bar and add/- button
        # search.pack()
        buttonFrame.pack(anchor=E, padx=10)
        add.grid(row=0, column=0)
        delete.grid(row=0, column=1)
        edit.grid(row=0, column=2)

        # pack listbox
        scrollbar.pack(side=LEFT, fill=Y)
        mylist.pack(side=LEFT, fill=Y)
        # pack frame
        frame.pack(expand=True, fill=BOTH, padx=25, pady=25)

    else:
        print('wrong password')


def CursorSelect(evt):
    index = selectedIndex()
    accText.delete(0.0, END)
    accText.insert(END, ENTRIES[index].account)

    userText.delete(0.0, END)
    userText.insert(END, ENTRIES[index].username)

    emailText.delete(0.0, END)
    emailText.insert(END, ENTRIES[index].email)

    passText.delete(0.0, END)
    passText.insert(END, ENTRIES[index].password)

    descText.delete(0.0, END)
    descText.insert(END, ENTRIES[index].description)


mylist.bind('<<ListboxSelect>>', CursorSelect)


enterLabel = Label(root, text="Enter Password: ", bg=window_bg)
root.bind('<Return>', enterPass)
enterLabel.pack(pady=10)

enter = Entry(root, borderwidth=0, width=25)
enter.pack()

####################### Home Page ##########################


root.mainloop()
