import tkinter as tk
from PIL import Image, ImageTk


#inf ordeR: F T J P S

root = tk.Tk()


class Deck:
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    icon_offset = 63
    fire = Image.open("Assets/fire.png").convert("LA").convert("RGBA")


    icon_image = [
        Image.open("Assets/fire.png"),
        Image.open("Assets/time.png"),
        Image.open("Assets/justice.png"),
        Image.open("Assets/primal.png"),
        Image.open("Assets/shadow.png"),
    ]

    ban_image = [
        ImageTk.PhotoImage(Image.open("Assets/x1.png")),
        ImageTk.PhotoImage(Image.open("Assets/x1.png")),
        ImageTk.PhotoImage(Image.open("Assets/x2.png")),
        ImageTk.PhotoImage(Image.open("Assets/x3.png")),
        ImageTk.PhotoImage(Image.open("Assets/x4.png")),
        ImageTk.PhotoImage(Image.open("Assets/x5.png"))
    ]

    icon_image_color = [ImageTk.PhotoImage(img) for img in icon_image]
    icon_image_gray = [ImageTk.PhotoImage(img.convert("LA").convert("RGBA")) for img in icon_image]

    def __init__(self, _window, _icon_alignment):
        self.name = tk.StringVar()
        self.fire = tk.BooleanVar()

        self.time = tk.BooleanVar()
        self.justice = tk.BooleanVar()
        self.primal = tk.BooleanVar()
        self.shadow = tk.BooleanVar()
        self.influence = [self.fire, self.time, self.justice, self.primal, self.shadow]
        self.banned = tk.BooleanVar()
        self.eliminated = tk.BooleanVar()
        self.icon = tk.Canvas(_window, width=380, height=100)
        self.icon_alignment = _icon_alignment

    def update_icon(self):

        self.icon.delete("all")
        positions = range(0, self.icon_offset * len(self.influence), self.icon_offset)

        if self.icon_alignment == self.LEFT:
            keys = range(0, len(self.influence))
        else:
            keys = range(len(self.influence) - 1, -1, -1)

        current_position = iter(list(keys))
        influence_count = 0
        for key in keys:
            if self.influence[key].get():
                influence_count += 1
                self.icon.create_image(
                    positions[next(current_position)],
                    0,
                    anchor=tk.NW,
                    image=(self.icon_image_gray[key] if self.eliminated.get() else self.icon_image_color[key]))

        if self.banned.get():
            self.icon.create_image(0, 0, anchor=tk.NW,image=self.ban_image[influence_count])


    def add_controls(self, _window, _row, _column_multiplier):
        column_count = 8
        column_offset = column_count * _column_multiplier

        tk.Entry(_window, textvariable=self.name)          .grid(row=_row, column=0+column_offset)
        tk.Checkbutton(_window, variable=self.fire,         command=self.update_icon).grid(row=_row, column=1+column_offset)
        tk.Checkbutton(_window, variable=self.time,         command=self.update_icon).grid(row=_row, column=2+column_offset)
        tk.Checkbutton(_window, variable=self.justice,      command=self.update_icon).grid(row=_row, column=3+column_offset)
        tk.Checkbutton(_window, variable=self.primal,       command=self.update_icon).grid(row=_row, column=4+column_offset)
        tk.Checkbutton(_window, variable=self.shadow,       command=self.update_icon).grid(row=_row, column=5+column_offset)
        tk.Checkbutton(_window, variable=self.banned,       command=self.update_icon).grid(row=_row, column=6+column_offset)
        tk.Checkbutton(_window, variable=self.eliminated,   command=self.update_icon).grid(row=_row, column=7+column_offset)

    def add_display(self, _window, _row, _column_multiplier):
        column_count = 2
        column_offset = column_count * _column_multiplier

        icon_column = 0
        text_column = 0
        if self.icon_alignment == self.RIGHT:
            text_column = 0+column_offset
            icon_column = 1+column_offset
        else:
            text_column = 1+column_offset
            icon_column = 0+column_offset


        tk.Label(_window, textvariable=self.name, font="Helvetica 40 bold").grid(row=_row, column=text_column, sticky=tk.E)
        self.icon.grid(row=_row, column=icon_column)


def InitWindow(root, title, geometry="1000x500"):
    """Init a new window, left or """
    window = tk.Toplevel(root)
    window.title(title)
    window.geometry(geometry)
    return window


# Initialize and configure windows
root.title("Control")
root.resizable(width=tk.FALSE, height=tk.FALSE)

# Control window header labels
tk.Label(root, text="Player 1 Decks")   .grid(row=0, column=0)
tk.Label(root, text="F")                .grid(row=0, column=1)
tk.Label(root, text="T")                .grid(row=0, column=2)
tk.Label(root, text="J")                .grid(row=0, column=3)
tk.Label(root, text="P")                .grid(row=0, column=4)
tk.Label(root, text="S")                .grid(row=0, column=5)
tk.Label(root, text="BAN")              .grid(row=0, column=6)
tk.Label(root, text="ELIM")             .grid(row=0, column=7)
tk.Label(root, text="Player 2 Decks")   .grid(row=0, column=8)
tk.Label(root, text="F")                .grid(row=0, column=9)
tk.Label(root, text="T")                .grid(row=0, column=10)
tk.Label(root, text="J")                .grid(row=0, column=11)
tk.Label(root, text="P")                .grid(row=0, column=12)
tk.Label(root, text="S")                .grid(row=0, column=13)
tk.Label(root, text="BAN")              .grid(row=0, column=14)
tk.Label(root, text="ELIM")             .grid(row=0, column=15)

# display window layout
window = InitWindow(root, "test")
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)
window.rowconfigure(3, weight=1)
window.columnconfigure(0, weight=4)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=0)

# Init deck objects
p1_decks = [Deck(window, Deck.RIGHT) for r in range(1, 5)]
p2_decks = [Deck(window, Deck.LEFT) for r in range(1, 5)]

# Add decks to control window
for i, decks in enumerate(zip(p1_decks, p2_decks)):
    decks[0].add_controls(root, i+1, 0)
    decks[1].add_controls(root, i+1, 1)

# Add decks to display window
for i, decks in enumerate(zip(p1_decks, p2_decks)):
    decks[0].add_display(window, i, 0)
    decks[1].add_display(window, i, 1)


root.mainloop()
