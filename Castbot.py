import tkinter as tk
import tkinter.font as tkFont
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk


#inf ordeR: F T J P S

root = tk.Tk()


class Deck:
    """
    Track a single deck and it's display
    """

    # Alignments for display
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    icon_offset = 63

    # Assets for Icon
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

    def __init__(self, win, alignment):
        """
        A single deck
        :param win: The window that will display the influence icon
        :param alignment: Display alignment, Deck.LEFT or Deck.RIGHT
        """
        self.name = tk.StringVar()
        self.fire = tk.BooleanVar()
        self.time = tk.BooleanVar()
        self.justice = tk.BooleanVar()
        self.primal = tk.BooleanVar()
        self.shadow = tk.BooleanVar()
        self.banned = tk.BooleanVar()
        self.eliminated = tk.BooleanVar()
        self.font = tk.StringVar()
        self.font_size = tk.IntVar()

        self.alignment = alignment
        self.icon = tk.Canvas(win, width=380, height=100)
        self.label = tk.Label(win, textvariable=self.name)

    def update_icon(self):
        """
        Update the icon canvas.  Mostly used as a callback
        :return:
        """

        # Clear the canvas
        self.icon.delete("all")

        # Setup variables for operation
        influence = [self.fire, self.time, self.justice, self.primal, self.shadow]
        positions = range(0, self.icon_offset * len(influence), self.icon_offset)
        keys = range(0, len(influence)) if self.alignment == self.LEFT else range(len(influence) - 1, -1, -1)
        current_position = iter(list(keys))
        influence_count = 0

        # Add relevant influence icons to canvas
        for key in keys:
            if influence[key].get():
                influence_count += 1
                self.icon.create_image(
                    positions[next(current_position)],
                    0,
                    anchor=tk.NW,
                    image=(self.icon_image_gray[key] if self.eliminated.get() else self.icon_image_color[key]))

        # Add ban X if relevant
        if influence_count != 0 and self.banned.get():
            if self.alignment == self.LEFT:
                self.icon.create_image(-(len(self.icon_image) - influence_count) * self.icon_offset, 0, anchor=tk.NW, image=self.ban_image[influence_count])
            else:
                self.icon.create_image(0, 0, anchor=tk.NW, image=self.ban_image[influence_count])

    def add_controls(self, win, row, column):
        """
        Add deck controls to control window
        :param win: control window to which controls will be added
        :param row: row of grid to add
        :param column: starting column
        :return: The entry field, so we can set tab order
        """

        # Add deck name entry field
        deck_label_entry = tk.Entry(win, textvariable=self.name)
        deck_label_entry.grid(row=row, column=0+column)

        # Add configuration checkbuttons
        tk.Checkbutton(win, variable=self.fire,         command=self.update_icon).grid(row=row, column=1+column)
        tk.Checkbutton(win, variable=self.time,         command=self.update_icon).grid(row=row, column=2+column)
        tk.Checkbutton(win, variable=self.justice,      command=self.update_icon).grid(row=row, column=3+column)
        tk.Checkbutton(win, variable=self.primal,       command=self.update_icon).grid(row=row, column=4+column)
        tk.Checkbutton(win, variable=self.shadow,       command=self.update_icon).grid(row=row, column=5+column)
        tk.Checkbutton(win, variable=self.banned,       command=self.update_icon).grid(row=row, column=6+column)
        tk.Checkbutton(win, variable=self.eliminated,   command=self.update_icon).grid(row=row, column=7+column)

        return deck_label_entry

    def add_display(self, win, row, column=0):
        """
        Add display name and Influence icon
        :param win: display window to use
        :param row: Row to apply
        :param column: Leftmost column
        :return:
        """

        # Order name and icon
        if self.alignment == self.RIGHT:
            text_column = 0+column
            icon_column = 2+column
        else:
            text_column = 2+column
            icon_column = 0+column

        # Add label and icon to grid
        self.label.grid(row=row, column=text_column, sticky=(tk.E if self.alignment == self.RIGHT else tk.W))
        self.icon.grid(row=row, column=icon_column, sticky=tk.E if self.alignment == self.LEFT else tk.W)

class Settings:
    """
    Track display settings and handle loading/saving of settings
    """

    class Weights:
        """
        Data holder for column and ro weights
        """
        name_spacer_column = tk.IntVar()
        center_spacer_column = tk.IntVar()
        header_row = tk.IntVar()
        deck_row = tk.IntVar()

    deck_font = tk.StringVar()
    deck_font_size = tk.IntVar()
    player_font = tk.StringVar()
    player_font_size = tk.IntVar()


    weights = Weights()

    def __init__(self, display_window):
        """
        The settings
        :param display_window: display window that will be configured with these settings
        """

        self.window = display_window

        # Add update_weights callbacks to relevant variables
        self.weights.name_spacer_column.trace(mode="w", callback=self.update_weights)
        self.weights.center_spacer_column.trace(mode="w", callback=self.update_weights)
        self.weights.header_row.trace(mode="w", callback=self.update_weights)
        self.weights.deck_row.trace(mode="w", callback=self.update_weights)

        # set default fonts
        self.deck_font.set("Courier")
        self.player_font.set("Courier")

    def pick_color(self):
        """
        Callback for color pickerz
        :return:
        """

        color = askcolor()
        print(color)

    def add_display(self, win, row):
        """
        Add display for settings
        :param win: to this window
        :param row: at and below this row
        :return:
        """

        def add_combo_slider(win, row, text, var, from_=0, to=20, default=1):
            """
            Add label, entry, and slider display bound to the same variable
            :param win: to this window
            :param row: on this row
            :param text: Entry text
            :param var: control this variable
            :param from_: lower bound of slider
            :param to: upper bound of slider
            :param default: set variable to this value after init
            :return:
            """
            tk.Label(win, text=text).grid(row=row, column=0, sticky=tk.E)
            tk.Entry(win, textvariable=var, width=3).grid(row=row, column=1)
            scale = tk.Scale(win,
                             from_=from_,
                             to=to,
                             variable=var,
                             showvalue=tk.FALSE,
                             orient=tk.HORIZONTAL)
            scale.grid(row=row, column=2, columnspan=4)
            scale.set(default)

        # Layout lable
        tk.Label(win, text="Layout").grid(row=row, column=0)

        # Column weighting combo sliders
        add_combo_slider(
            win=win,
            row=row+1,
            text="Deck text Column:",
            var=self.weights.name_spacer_column
        )
        add_combo_slider(
            win=win,
            row=row+3,
            text="Center Spacer Column:",
            var=self.weights.center_spacer_column
        )
        add_combo_slider(
            win=win,
            row=row+4,
            text="Header Row",
            var=self.weights.header_row
        )
        add_combo_slider(
            win=win,
            row=row+5,
            text="Deck Row",
            var=self.weights.deck_row
        )

        # Font size combo sliders
        add_combo_slider(
            win=win,
            row=row+6,
            text="Name Font",
            var=self.player_font_size,
            from_=1,
            to=60,
            default=12
        )
        add_combo_slider(
            win=win,
            row=row + 7,
            text="Deck Font",
            var=self.deck_font_size,
            from_=1,
            to=60,
            default=20
        )

        # Add font selectors
        tk.OptionMenu(win, self.player_font, *tkFont.families()).grid(row=row+6, column=6, columnspan=3)
        tk.OptionMenu(win, self.deck_font, *tkFont.families()).grid(row=row+7, column=6, columnspan=3)

        # Add window size controls
        tk.Label(win, text="Window Size").grid(row=row+8, column=0, sticky=tk.E)
        tk.Entry(win, width=3).grid(row=row+8, column=1)

        # Add background color selector
        tk.Button(win, text="Background Color", command=self.pick_color).grid(row=row+9, column=0)

    def update_weights(self, a, b, c):
        """Set column and row weights for display
        Arguments: a, b, c are all required for callback use, dunno what they do though."""

        # Name column weights
        window.columnconfigure(0, weight=10)
        window.columnconfigure(6, weight=10)

        # Deck name spacer columns
        window.columnconfigure(1, weight=self.weights.name_spacer_column.get())
        window.columnconfigure(5, weight=self.weights.name_spacer_column.get())

        # Center spacer column
        window.columnconfigure(3, weight=self.weights.center_spacer_column.get())

        # Header player name row
        window.rowconfigure(0, weight=self.weights.header_row.get())

        # Deck rows
        for row in range(1, 5):
            window.rowconfigure(row, weight=self.weights.deck_row.get())


def init_window(root, title, geometry="1000x500"):
    """Init a new window"""

    window = tk.Toplevel(root)
    window.title(title)
    window.geometry(geometry)
    return window


def select_text_on_click(entry):
    def entry_callback(event):
        entry.selection_range(0, tk.END)
    entry.bind("<FocusIn>", entry_callback)


def bind_label_font(font, font_size, label):
    """
    Bind a font and font size of a tkinter label to the settings object with a callback
    :param font: canonical font that will cause updates
    :param font_size: canonical font size that will cause updates
    :param label: to be updated on font or size change
    """
    def update_font(name=None, ops=None, commandPrefix=None):
        """
        Callback for font/size updates
        """
        label.config(font=(font.get(), font_size.get()))

    font.trace(mode="w", callback=update_font)
    font_size.trace(mode="w", callback=update_font)
    update_font()

tab_order = []

player1_name, player2_name = tk.StringVar(), tk.StringVar()
name_weight, icon_weight = tk.IntVar(), tk.IntVar()


# Initialize and configure windows
root.title("Control")
root.resizable(width=tk.FALSE, height=tk.FALSE)

window = init_window(root, "test")

# Setup player name fields
p1_entry = tk.Entry(root, textvariable=player1_name)
p1_entry.grid(row=0, column=0)
p1_entry.insert(0, "Player 1 Name")
tab_order.append(p1_entry)

p2_entry = tk.Entry(root, textvariable=player2_name)
p2_entry.grid(row=1, column=0)
p2_entry.insert(0, "Player 2 Name")
tab_order.append(p2_entry)

#  Select whole text on entry window click
select_text_on_click(p1_entry)
select_text_on_click(p2_entry)

# Control window header labels
headerrow = 2
tk.Label(root, textvariable=player1_name)   .grid(row=headerrow, column=0)
tk.Label(root, text="F")                    .grid(row=headerrow, column=1)
tk.Label(root, text="T")                    .grid(row=headerrow, column=2)
tk.Label(root, text="J")                    .grid(row=headerrow, column=3)
tk.Label(root, text="P")                    .grid(row=headerrow, column=4)
tk.Label(root, text="S")                    .grid(row=headerrow, column=5)
tk.Label(root, text="BAN")                  .grid(row=headerrow, column=6)
tk.Label(root, text="ELIM")                 .grid(row=headerrow, column=7)
tk.Label(root, textvariable=player2_name)   .grid(row=headerrow, column=8)
tk.Label(root, text="F")                    .grid(row=headerrow, column=9)
tk.Label(root, text="T")                    .grid(row=headerrow, column=10)
tk.Label(root, text="J")                    .grid(row=headerrow, column=11)
tk.Label(root, text="P")                    .grid(row=headerrow, column=12)
tk.Label(root, text="S")                    .grid(row=headerrow, column=13)
tk.Label(root, text="BAN")                  .grid(row=headerrow, column=14)
tk.Label(root, text="ELIM")                 .grid(row=headerrow, column=15)



# Init deck objects
p1_decks = [Deck(window, Deck.RIGHT) for r in range(1, 5)]
p2_decks = [Deck(window, Deck.LEFT) for r in range(1, 5)]

# Add decks to control window
for i, deck in enumerate(p1_decks):
    tab_order.append(deck.add_controls(root, i+3, 0))
for i, deck in enumerate(p2_decks):
    tab_order.append(deck.add_controls(root, i+3, 8))

# Add player labels to display window
player1_name_label = tk.Label(window, textvariable=player1_name)
player1_name_label.grid(row=0, column=0, columnspan=2)
player2_name_label = tk.Label(window, textvariable=player2_name)
player2_name_label.grid(row=0, column=3, columnspan=2)

# Add decks to display window
for i, decks in enumerate(zip(p1_decks, p2_decks)):
    decks[0].add_display(window, row=i+1, column=0)
    decks[1].add_display(window, row=i+1, column=4)

# Setup settings
settings = Settings(window)
settings.add_display(win=root, row=6)


# Configure decks
for deck in p1_decks + p2_decks:
    bind_label_font(settings.deck_font, settings.deck_font_size, deck.label)

# Configure player labels
    bind_label_font(settings.player_font, settings.player_font_size, player1_name_label)
    bind_label_font(settings.player_font, settings.player_font_size, player2_name_label)


# rebuild tab order
for element in tab_order:
    element.lift()


root.mainloop()
