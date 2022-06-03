from tkinter import *
import customtkinter
from PIL import Image, ImageTk
from Simple_board_elements import Lamp
from Fundamentals import Board


def put_bulb(event):
    """Puts image bulb on the canvas"""
    print("clicked at", event.x, event.y)
    # coords.append(event.x)
    # coords.append(event.y)
    # global one
    # one = ImageTk.PhotoImage(Image.open(
    #     "light_bulb.png").resize((50, 100)))
    one = Lamp(board).img
    canvas.create_image(event.x, event.y, image=one)
    # coords.clear()


def curr_com_put_bulb():
    """Defines command"""
    # coords.clear()
    canvas.bind("<Button-1>", put_bulb)

def connect(event):
    print("current function: connect")
    print ("clicked at", event.x, event.y)
    coords.append(event.x)
    coords.append(event.y)

def curr_com_connect():
    coords.clear()
    canvas.bind("<Button-1>", connect)


def put_buffer():
    pass


def put_not():
    pass


def put_and():
    pass


def put_nand():
    pass


def put_or():
    pass


def put_nor():
    pass


def put_xor():
    pass


def put_xnor():
    pass


def button_function():
    """Just shob bulo"""
    print("button pressed")


def start():
    """Starts the whole thing"""
    mainloop()


def main():
    # Just a setup for a theme
    # Modes: system (default), light, dark
    customtkinter.set_appearance_mode("dark")
    # Themes: blue (default), dark-blue, green
    customtkinter.set_default_color_theme("blue")

    WIDTH = 1400
    HEIGHT = 800
    global coords
    coords = []

    app = customtkinter.CTk()

    app.geometry(f"{WIDTH}x{HEIGHT}")
    app.title("Logical Elements Constructor")
    # iconbitmap("icon1.ico")

    # Setup for frame with logical gates
    frame_logical_gates = customtkinter.CTkFrame(master=app)
    frame_logical_gates.grid(
        row=0, column=0, sticky="nswe",  padx=20, pady=20)

    # Label for the framw
    label_logical_frame = customtkinter.CTkLabel(
        master=frame_logical_gates, text="Logic Gates", text_font=("Roboto Medium", 13))
    label_logical_frame.grid(row=0, column=0)

    # Setup for buttons in a frames
    local_compound = "top"
    local_height = 80
    local_width = 150
    local_fg_color = ("gray75", "gray30")

    # Buffer button
    buffer_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="Buffer",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open("buffer.png").resize((80, 40)))
    buffer_button.set_image(img)
    buffer_button.grid(row=1, column=0, padx=5, pady=5)

    # NOT button
    not_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="NOT Gate",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open("not.png").resize((80, 40)))
    not_button.set_image(img)
    not_button.grid(row=1, column=1, padx=5, pady=5)

    # AND button
    and_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="AND Gate",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open("and.png").resize((80, 40)))
    and_button.set_image(img)
    and_button.grid(row=2, column=0, padx=5, pady=5)

    # NAND button
    nand_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="NAND Gate",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open("nand.png").resize((80, 40)))
    nand_button.set_image(img)
    nand_button.grid(row=2, column=1, padx=5, pady=5)

    # OR button
    or_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="OR Gate",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open("or.png").resize((80, 40)))
    or_button.set_image(img)
    or_button.grid(row=3, column=0, padx=5, pady=5)

    # NOR button
    nor_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="NOR Gate",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open("nor.png").resize((80, 40)))
    nor_button.set_image(img)
    nor_button.grid(row=3, column=1, padx=5, pady=5)

    # XOR button
    xor_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="XOR Gate",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open("xor.png").resize((80, 40)))
    xor_button.set_image(img)
    xor_button.grid(row=4, column=0, padx=5, pady=5)

    # XNOR button
    xnor_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="XNOR Gate",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open("xnor.png").resize((80, 40)))
    xnor_button.set_image(img)
    xnor_button.grid(row=4, column=1, padx=5, pady=5)

    # Setup for frame with input controls
    input_controls = customtkinter.CTkFrame(master=app)
    input_controls.grid(
        row=1, column=0, sticky="nswe",  padx=20, pady=20)

    # Label for the framw
    label_input_controls = customtkinter.CTkLabel(
        master=input_controls, text="Input Controls", text_font=("Roboto Medium", 13))
    label_input_controls.grid(row=0, column=0)

    # High Constant button
    high_constant_button = customtkinter.CTkButton(
        master=input_controls, text="High Constant",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open(
        "high_constant.png").resize((80, 40)))
    high_constant_button.set_image(img)
    high_constant_button.grid(row=1, column=0, padx=5, pady=5)

    # Low Constant button
    low_constant_button = customtkinter.CTkButton(
        master=input_controls, text="Low Constant",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open(
        "low_constant.png").resize((80, 40)))
    low_constant_button.set_image(img)
    low_constant_button.grid(row=1, column=1, padx=5, pady=5)

    # Setup for frame with output controls
    output_controls = customtkinter.CTkFrame(master=app)
    output_controls.grid(
        row=2, column=0, sticky="nswe",  padx=20, pady=20)

    # Label for the framw
    label_output_controls = customtkinter.CTkLabel(
        master=output_controls, text="Output Controls", text_font=("Roboto Medium", 13))
    label_output_controls.grid(row=0, column=0)

    # Light Bulb button
    light_bulb_button = customtkinter.CTkButton(
        master=output_controls,
        text="Light Bulb",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color,
        command=curr_com_put_bulb
    )

    img = ImageTk.PhotoImage(Image.open("light_bulb.png").resize((40, 80)))
    light_bulb_button.set_image(img)
    light_bulb_button.grid(row=1, column=0, padx=5, pady=5)


    # Connect button
    connect_button = customtkinter.CTkButton(
        master=output_controls, text="Connect",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color,
        command=curr_com_connect)
    connect_button.grid(row=1, column=1, padx=5, pady=5)

    # Setting up the canvas
    global canvas
    canvas = Canvas(master=app, height=700,
                    width=1000, bg="light grey")
    canvas.grid(row=0, column=2, rowspan=3)

    # Setting up the board
    global board
    board = Board()

    # start a main loop
    start()


if __name__ == "__main__":
    main()
