from tkinter import *
import customtkinter
from PIL import Image, ImageTk
import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from board_elements.SimpleBoardElements import Lamp
from board_elements.Fundamentals import Board, OutputPin


class Line:
    last_coords = []

    def __init__(self, color="black", canvas=None, coords=[]) -> None:
        self.color = color
        self.canvas = canvas
        self.coords = coords
        self.connected_pins = [None, None]

    @classmethod
    def clear(cls):
        """
        Clear list with last coordinates.
        """
        cls.last_coords.clear()

    def valide_click(self, x_coord, y_coord):
        """
        Check if user clicked on the free pin.
        """
        for pin in board.get_all_pins():
            if pin.check_dot(x_coord, y_coord) and not pin.is_connected():
                if isinstance(pin, OutputPin):
                    self.connected_pins[0] = pin
                else:
                    self.connected_pins[1] = pin
                return True
        return False


def put_bulb(event):
    """Puts image bulb on the canvas"""
    print("clicked at", event.x, event.y)
    # coords.append(event.x)
    # coords.append(event.y)
    new_lamp = Lamp(board)
    new_lamp.update_reaction_areas(event.x, event.y)
    Lamp.all_lamp_images.append(new_lamp.img)
    canvas.create_image(event.x, event.y, image=Lamp.all_lamp_images[-1])
    # coords.clear()


def curr_com_put_bulb():
    """Defines command"""
    # coords.clear()
    canvas.bind("<Button-1>", put_bulb)


def connect(event):
    print("current function: connect")
    print("clicked at", event.x, event.y)
    Line.last_coords.append(event.x)
    Line.last_coords.append(event.y)


def curr_com_connect():
    Line.last_coords.clear()
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

    img = ImageTk.PhotoImage(Image.open("app_code/visuals/textures/buffer.png").resize((80, 40)))
    buffer_button.set_image(img)
    buffer_button.grid(row=1, column=0, padx=5, pady=5)

    # NOT button
    not_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="NOT Gate",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open("app_code/visuals/textures/not.png").resize((80, 40)))
    not_button.set_image(img)
    not_button.grid(row=1, column=1, padx=5, pady=5)

    # AND button
    and_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="AND Gate",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open("app_code/visuals/textures/and.png").resize((80, 40)))
    and_button.set_image(img)
    and_button.grid(row=2, column=0, padx=5, pady=5)

    # NAND button
    nand_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="NAND Gate",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open("app_code/visuals/textures/nand.png").resize((80, 40)))
    nand_button.set_image(img)
    nand_button.grid(row=2, column=1, padx=5, pady=5)

    # OR button
    or_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="OR Gate",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open("app_code/visuals/textures/or.png").resize((80, 40)))
    or_button.set_image(img)
    or_button.grid(row=3, column=0, padx=5, pady=5)

    # NOR button
    nor_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="NOR Gate",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open("app_code/visuals/textures/nor.png").resize((80, 40)))
    nor_button.set_image(img)
    nor_button.grid(row=3, column=1, padx=5, pady=5)

    # XOR button
    xor_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="XOR Gate",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open("app_code/visuals/textures/xor.png").resize((80, 40)))
    xor_button.set_image(img)
    xor_button.grid(row=4, column=0, padx=5, pady=5)

    # XNOR button
    xnor_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="XNOR Gate",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open("app_code/visuals/textures/xnor.png").resize((80, 40)))
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
        "app_code/visuals/textures/high_constant.png").resize((80, 40)))
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
        "app_code/visuals/textures/low_constant.png").resize((80, 40)))
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

    img = ImageTk.PhotoImage(Image.open("app_code/visuals/textures/light_bulb.png").resize((40, 80)))
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
    global canvas # please don't use globals
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
