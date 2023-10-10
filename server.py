import random
import tkinter as tk
from PIL import Image, ImageTk
import socket
import threading
import os

root = tk.Tk()
root.title('Server')
width, height = 900, 700
width_center, height_center = (root.winfo_screenwidth() / 2) - (width / 2), (root.winfo_screenheight() / 2) - (
        height / 2)
root.geometry(f"{width}x{height}+{int(width_center)}+{int(height_center)}")
root.resizable(False, False)
root.config(bg='gray')
photos_directory = os.path.join(os.getcwd(), "photos")
image_files = os.listdir(photos_directory)
count_photos = len(image_files) - 1
image_paths = [file for file in image_files if file.lower().endswith((".jpg", ".png", ".gif"))]
image_objects = []
for file in image_files:
    file_path = os.path.join(photos_directory, file)
    image = Image.open(file_path)
    image_tk = ImageTk.PhotoImage(image)
    image_objects.append(image_tk)
num_photo = 1
photo = tk.Label(root, image=image_objects[num_photo])
label = tk.Label(root, text="The client is not connected",
                 bg='gray',
                 fg='white',
                 font=('Berlin Sans FB', 20, 'bold')
                 )


def change_background_color(received_integer):
    label.config(text="The client was connected!")
    photo.config(image=image_objects[received_integer])
    photo.place(relx=0.5, rely=0.5, anchor='center')


def server_thread():
    global server
    global num_photo
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.237.10', 1000))
    server.listen(1)
    client_socket, client_address = server.accept()
    while True:
        data_received = client_socket.recv(1024).decode()
        if not data_received:
            root.destroy()
        received_integer = int(data_received)
        while received_integer == num_photo:
            received_integer = random.randint(0, count_photos)
        num_photo = received_integer
        change_background_color(received_integer)


label.pack(anchor='nw')
server_thread = threading.Thread(target=server_thread)
server_thread.daemon = True
server_thread.start()
root.mainloop()