import tkinter as tk
from PIL import Image, ImageTk


#inf ordeR: F T J P S

def InitWindow(root, title, geometry="400x500"):
    """Init a new window, left or """
    window = tk.Toplevel(root)
    window.title(title)
    window.geometry(geometry)
    return window


root = tk.Tk()


# Configure control window
root.title("Control")
root.resizable(width=tk.FALSE, height=tk.FALSE)



#leftWindow = InitWindow(root, "Left")
#rightWindow = InitWindow(root, "Right")
tk.Label(root, text="Player 1 Decks").grid(row=0, column=0)
tk.Label(root, text="F").grid(row=0, column=1)
tk.Label(root, text="T").grid(row=0, column=2)
tk.Label(root, text="J").grid(row=0, column=3)
tk.Label(root, text="P").grid(row=0, column=4)
tk.Label(root, text="S").grid(row=0, column=5)
tk.Label(root, text="ELEM").grid(row=0, column=6)
tk.Label(root, text="BAN").grid(row=0, column=7)


tk.Label(root, text="Player 2 Decks").grid(row=0, column=10)
tk.Label(root, text="F").grid(row=0, column=11)
tk.Label(root, text="T").grid(row=0, column=12)
tk.Label(root, text="J").grid(row=0, column=13)
tk.Label(root, text="P").grid(row=0, column=14)
tk.Label(root, text="S").grid(row=0, column=15)
tk.Label(root, text="ELEM").grid(row=0, column=16)
tk.Label(root, text="BAN").grid(row=0, column=17)

p1_decks = [(tk.StringVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()) for r in range(1, 5)]
p2_decks = [(tk.StringVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()) for r in range(1, 5)]

#Player 1 entry
for x in range(0, 4):
    tk.Entry(root, textvariable=p1_decks[x][0]).grid(row=x+1, column=0)
    for y in range(0, 7):
        tk.Checkbutton(root, variable=p1_decks[x][y+1]).grid(row=x+1, column=y+1)

# Player 2 entry
for x in range(0, 4):
    tk.Entry(root, textvariable=p2_decks[x][0]).grid(row=x+1, column=10)
    for y in range(0, 7):
        tk.Checkbutton(root, variable=p2_decks[x][y+1]).grid(row=x+1, column=y+11)

window = InitWindow(root, "test")


symbols = [tk.Canvas(window, width=380, height=100) for x in range(0, 4)]
for i, can in enumerate(symbols):
    can.grid(row=i, column=2)

label1 = tk.Label(window, textvariable=p1_decks[0][0], font="Helvetica 40 bold")
label1.grid(row=0, column=0, sticky=tk.E)


window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)
window.rowconfigure(3, weight=1)
window.columnconfigure(0, weight=4)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=0)

fire = Image.open("Assets/fire.png")
time = Image.open("Assets/time.png")
justice = Image.open("Assets/justice.png")
primal = Image.open("Assets/primal.png")
shadow = Image.open("Assets/shadow.png")
ph_fire = ImageTk.PhotoImage(fire)
ph_time = ImageTk.PhotoImage(time)
ph_justice = ImageTk.PhotoImage(justice)
ph_shadow = ImageTk.PhotoImage(shadow)
ph_primal = ImageTk.PhotoImage(primal)

symbols[0].create_image(0, 0, anchor=tk.NW, image=ph_fire)
symbols[0].create_image(63, 0, anchor=tk.NW, image=ph_time)


symbols[0].create_image(126, 0, anchor=tk.NW, image=ph_shadow)
symbols[0].create_image(189, 0, anchor=tk.NW, image=ph_justice)
symbols[0].create_image(252, 0, anchor=tk.NW, image=ph_primal)
symbols[1].create_image(0, 0, anchor=tk.NW, image=ph_shadow)
symbols[1].create_image(63, 0, anchor=tk.NW, image=ph_time)
symbols[2].create_image(0, 0, anchor=tk.NW, image=ph_fire)
symbols[2].create_image(63, 0, anchor=tk.NW, image=ph_justice)
symbols[3].create_image(0, 0, anchor=tk.NW, image=ph_shadow)
symbols[3].create_image(63, 0, anchor=tk.NW, image=ph_primal)


root.mainloop()
