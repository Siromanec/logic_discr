from tkinter import *
import customtkinter
from PIL import Image, ImageTk
from Simple_board_elements import *
from Fundamentals import *


class Line:
    last_pins_to_connect = []

    def __init__(self, color="black", canvas: Canvas = None, connected_pins=(None, None)) -> None:
        self.color = color
        self.width = 3
        self.canvas = canvas
        self.connected_pins = connected_pins

    def set_connected_pins(self, pins: tuple[Pin]):
        self.connected_pins = pins

    def get_connected_pins(self):
        return self.connected_pins

    @classmethod
    def clear_last_pins(cls):
        """
        Clear list with last pair of pins to connect.
        """
        cls.last_pins_to_connect.clear()

    @ classmethod
    def valide_click(cls, x_coord, y_coord):
        """
        Check if user clicked on the free pin.
        If yes: return True and add that pin to list, no: return False
        """
        for pin in board.get_all_pins():
            if pin.check_dot(x_coord, y_coord) and not pin.is_connected():
                cls.last_pins_to_connect.append(pin)
                return True
        return False

    def draw_line(self):
        """Connect two pins with a line"""
        pin1 = self.get_connected_pins()[0].get_reaction_area()
        center1 = ((pin1[0]+pin1[2])/2, (pin1[1]+pin1[3])/2)
        pin2 = self.get_connected_pins()[1].get_reaction_area()
        center2 = ((pin2[0]+pin2[2])/2, (pin2[1]+pin2[3])/2)
        print("draw a line")
        self.canvas.create_line(
            center1[0], center1[1], center2[0], center2[1], width=self.width, fill=self.color)


def connect(event):
    print("clicked at", event.x, event.y)

    if not Line.valide_click(event.x, event.y):
        print("invalid click")
        Line.clear_last_pins()

    elif len(Line.last_pins_to_connect) == 2:
        last_pins = Line.last_pins_to_connect
        if isinstance(last_pins[0], OutputPin) and isinstance(last_pins[1], InputPin):
            board.connect_pins(last_pins[0], last_pins[1])
            line = Line(canvas=canvas, connected_pins=last_pins)
            line.draw_line()
        elif isinstance(last_pins[0], InputPin) and isinstance(last_pins[1], OutputPin):
            board.connect_pins(last_pins[1], last_pins[0])
            line = Line(canvas=canvas, connected_pins=last_pins)
            line.draw_line()
        Line.clear_last_pins()


def curr_com_connect():
    Line.clear_last_pins()
    canvas.bind("<Button-1>", connect)


def put_bulb(event):
    """Puts image bulb on the canvas"""
    print("clicked at", event.x, event.y)
    new_lamp = board.create_element(Lamp)
    new_lamp.update_reaction_areas(event.x, event.y)
    # print(new_lamp._input_pins[0].get_reaction_area())
    img = ImageTk.PhotoImage(Image.open(new_lamp.img_path).resize((50, 100)))
    board.add_to_img_list(img)
    canvas.create_image(event.x, event.y, image=img)


def curr_com_put_bulb():
    """Defines command"""
    canvas.bind("<Button-1>", put_bulb)


def put_buffer():
    pass


def put_not(event):
    """Puts image of gate NOT on the canvas"""
    print("clicked at", event.x, event.y)
    new_not = board.create_element(NOT_Gate)
    new_not.update_reaction_areas(event.x, event.y)
    # print(new_not._input_pins[0].get_reaction_area())
    # print(new_not._output_pins[0].get_reaction_area())
    img = ImageTk.PhotoImage(Image.open(new_not.img_path).resize((100, 50)))
    board.add_to_img_list(img)
    canvas.create_image(event.x, event.y, image=img)


def curr_com_put_not():
    """Defines command"""
    canvas.bind("<Button-1>", put_not)


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

    img = ImageTk.PhotoImage(Image.open("visuals/buffer.png").resize((80, 40)))
    buffer_button.set_image(img)
    buffer_button.grid(row=1, column=0, padx=5, pady=5)

    # NOT button
    not_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="NOT Gate",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color,
        command=curr_com_put_not)

    img = ImageTk.PhotoImage(Image.open("visuals/not.png").resize((80, 40)))
    not_button.set_image(img)
    not_button.grid(row=1, column=1, padx=5, pady=5)

    # AND button
    and_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="AND Gate",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open("visuals/and.png").resize((80, 40)))
    and_button.set_image(img)
    and_button.grid(row=2, column=0, padx=5, pady=5)

    # NAND button
    nand_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="NAND Gate",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open("visuals/nand.png").resize((80, 40)))
    nand_button.set_image(img)
    nand_button.grid(row=2, column=1, padx=5, pady=5)

    # OR button
    or_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="OR Gate",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open("visuals/or.png").resize((80, 40)))
    or_button.set_image(img)
    or_button.grid(row=3, column=0, padx=5, pady=5)

    # NOR button
    nor_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="NOR Gate",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open("visuals/nor.png").resize((80, 40)))
    nor_button.set_image(img)
    nor_button.grid(row=3, column=1, padx=5, pady=5)

    # XOR button
    xor_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="XOR Gate",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open("visuals/xor.png").resize((80, 40)))
    xor_button.set_image(img)
    xor_button.grid(row=4, column=0, padx=5, pady=5)

    # XNOR button
    xnor_button = customtkinter.CTkButton(
        master=frame_logical_gates, text="XNOR Gate",
        compound=local_compound,
        height=local_height,
        width=local_width,
        fg_color=local_fg_color)

    img = ImageTk.PhotoImage(Image.open("visuals/xnor.png").resize((80, 40)))
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
        "visuals/high_constant.png").resize((80, 40)))
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
        "visuals/low_constant.png").resize((80, 40)))
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

    img = ImageTk.PhotoImage(Image.open(
        "visuals/light_bulb.png").resize((40, 80)))
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
    global canvas  # please don't use globals
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
