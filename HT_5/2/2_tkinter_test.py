import time
from tkinter import *

root = Tk()
root.title("Traffic Lights")

c = Canvas(root, width=255, height=300, bg="black")
c.pack()

t_sec_1 = c.create_oval(20, 20, 100, 100, fill="red")
t_sec_2 = c.create_oval(20, 110, 100, 190, fill="gray34")
t_sec_3 = c.create_oval(20, 200, 100, 280, fill="gray34")

p_sec_1 = c.create_oval(150, 65, 230, 145, fill="gray34")
p_sec_2 = c.create_oval(150, 155, 230, 235, fill="green")

c.update()

while True:
    time.sleep(3)
    c.itemconfig(t_sec_1, fill="red")
    c.itemconfig(t_sec_2, fill="yellow")
    c.itemconfig(t_sec_3, fill="gray34")
    c.itemconfig(p_sec_1, fill="red")
    c.itemconfig(p_sec_2, fill="gray34")
    c.update()
    time.sleep(1)
    c.itemconfig(t_sec_1, fill="gray34")
    c.itemconfig(t_sec_2, fill="gray34")
    c.itemconfig(t_sec_3, fill="green")
    c.itemconfig(p_sec_1, fill="red")
    c.itemconfig(p_sec_2, fill="gray34")
    c.update()
    time.sleep(3)
    c.itemconfig(t_sec_1, fill="gray")
    c.itemconfig(t_sec_2, fill="yellow")
    c.itemconfig(t_sec_3, fill="gray34")
    c.itemconfig(p_sec_1, fill="red")
    c.itemconfig(p_sec_2, fill="gray34")
    c.update()
    time.sleep(1)
    c.itemconfig(t_sec_1, fill="red")
    c.itemconfig(t_sec_2, fill="gray34")
    c.itemconfig(t_sec_3, fill="gray34")
    c.itemconfig(p_sec_1, fill="gray34")
    c.itemconfig(p_sec_2, fill="green")
    c.update()
