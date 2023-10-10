import tkinter as tk
from socket import *
import random
import os

connected = False
client = socket(AF_INET, SOCK_STREAM)
root = tk.Tk()
root.title('Client')
width, height = 900, 700
width_center, height_center = (root.winfo_screenwidth() / 2) - (width / 2), (root.winfo_screenheight() / 2) - (
        height / 2)
root.geometry(f"{width}x{height}+{int(width_center)}+{int(height_center)}")
root.resizable(False, False)
root.config(bg='gray')
label = tk.Label(root, text="Disconnected",
                 bg='gray',
                 fg='white',
                 font=('Berlin Sans FB', 20, 'bold'))
button = tk.Button(root, text="connect", font=('Berlin Sans FB', 20, 'bold'))
photos_directory = os.path.join(os.getcwd(), "photos")
image_files = os.listdir(photos_directory)
count_photos = len(image_files) - 1


def connecting():
    global connected
    button.config(state='disabled', bg='gray')
    label.config(text="Connecting...")
    root.update()

    try:
        client.connect(('192.168.237.10', 1000))
        label.config(font=('Berlin Sans FB', 20, 'bold'), text="Connected!")
        connected = True
        button.config(text="Tap To Switch", command=switch_png)
        num_photo = random.randint(0, count_photos)
        client.send(str(num_photo).encode())
    except Exception as e:
        connected = False
        button.config(command=connecting)
        label.config(font=('Berlin Sans FB', 10, 'bold'), text="Error: " + str(e))
    button.config(state='normal', bg='SystemButtonFace')


def switch_png():
    button.config(state='disabled', bg='gray')
    label.config(text="Switching...")
    try:
        num_photo = random.randint(0, count_photos)
        client.send(str(num_photo).encode())
        label.config(text="Switched")
    except:
        label.config(font=('Berlin Sans FB', 20, 'bold'), text="Error: It didn't switch")
    button.config(state='normal', bg='SystemButtonFace')


def update_connection():
    if connected == False:
        button.config(command=connecting)
    else:
        button.config(command=switch_png)


update_connection()
label.grid()
button.place(relx=0.5, rely=0.5, anchor='center')
root.mainloop()