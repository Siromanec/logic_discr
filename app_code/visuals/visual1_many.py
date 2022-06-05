from __future__ import annotations
from tkinter import Canvas
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from board_elements.SimpleBoardElements import *
from board_elements.Fundamentals import *
from board_elements.AdvancedBoardElements import *


class Line:
    last_pins_to_connect = []
    count = 0

    def __init__(self, color="black", canvas: Canvas = None, connected_pins=(None, None)) -> None:
        self.color = color
        self.width = 3
        self.canvas = canvas
        self.connected_pins = connected_pins
        self.id = Line.count
        Line.count += 1
        self.tag = 'line'+str(self.id)

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

    @classmethod
    def valide_click(cls, x_coord, y_coord):
        """
        Check if user clicked on the free pin.
        If yes: return True and add that pin to list, no: return False
        """
        for pin in board.get_all_pins():
            if pin.check_dot(x_coord, y_coord) and not pin.is_connected():
                if isinstance(pin, InputPin) and not pin.is_connected(): # check
                    cls.last_pins_to_connect.append(pin)
                    return True
                elif isinstance(pin, OutputPin):
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
        self.tag = self.canvas.create_line(
            center1[0], center1[1], center2[0], center2[1], width=self.width, fill=self.color)
        for pin in self.get_connected_pins():
            pin.append_connected_line_tag(self.tag)


def connect(event):
    print("clicked at", event.x, event.y)

    if not Line.valide_click(event.x, event.y):
        print("invalid click")
        Line.clear_last_pins()

    elif len(Line.last_pins_to_connect) == 2:
        last_pins = Line.last_pins_to_connect
        valide = True

        try:
            if isinstance(last_pins[0], OutputPin) and isinstance(last_pins[1], InputPin):
                output_pin, input_pin = last_pins[0], last_pins[1]
            elif isinstance(last_pins[0], InputPin) and isinstance(last_pins[1], OutputPin):
                output_pin, input_pin = last_pins[1], last_pins[0]
            else:
                valide = False

            if valide:
                board.connect_pins(output_pin, input_pin)
                line = Line(canvas=canvas, connected_pins=last_pins)
                line.draw_line()
        except ParentAlreadyExistsError:
            print("Failed 'connect' action!")
        Line.clear_last_pins()
        board.update_board()


def delete(event):
    """Delete element from canvas"""
    for element in board.get_circuits_list():
        if element.check_dot_in_img(event.x, event.y):
            canvas.delete(element.img_object)

            for input_pin in element.get_inputs():
                # delete line from canvas
                for line_to_delete in input_pin.get_connected_line_tags():
                    canvas.delete(line_to_delete)
                    # remove line tag from parent pin
                    parent = input_pin.get_parent()
                    if parent:
                        parent.remove_connected_line_tag(line_to_delete)
            for output_pin in element.get_outputs():
                # delete line from canvas
                for line_to_delete in output_pin.get_connected_line_tags():
                    canvas.delete(line_to_delete)
                    # remove line tag from children pins
                    children = output_pin.get_children()
                    for child in children:
                        if child:
                            child.remove_connected_line_tag(line_to_delete)

            board.remove_element(element)


def curr_com_put(element_type):
    """Defines command that puts element images and creates objects"""
    canvas.bind("<Button-1>", lambda event: put(element_type, event))
    canvas.bind("<Button-3>", switch_click)


def put(element_type, event):
    """Puts image of element on the canvas and crates an appropriate object"""
    print("clicked at", event.x, event.y)
    new_element = board.create_element(element_type)
    new_element.update_reaction_areas(event.x, event.y)
    new_element.set_img_coords(event.x, event.y)
    img = ImageTk.PhotoImage(Image.open(new_element.img_path)\
                             .resize((new_element.get_img_width(), new_element.get_img_height())))
    board.add_to_img_list(img)

    new_element.img_object = canvas.create_image(event.x, event.y, image=img)


def switch_click(event):
    print("clicked at", event.x, event.y)
    for element in board.get_circuits_list():
        if isinstance(element, Switch) and element.check_dot_in_img(event.x, event.y):
            element.switch()


def curr_com_connect():
    """Binds left click to the connect function"""
    Line.clear_last_pins()
    canvas.bind("<Button-1>", connect)


def curr_com_delete():
    """Binds left click to the delete function"""
    canvas.bind("<Button-1>", delete)


def start(app: ctk.CTk):
    """Starts the whole thing"""
    app.mainloop()


def main():
    # Just a setup for a theme
    # Modes: system (default), light, dark
    ctk.set_appearance_mode("dark")
    # Themes: blue (default), dark-blue, green
    ctk.set_default_color_theme("blue")

    WIDTH = 1800
    HEIGHT = 850

    app = ctk.CTk()

    app.geometry(f"{WIDTH}x{HEIGHT}")
    app.title("Logical Elements Constructor")
    # iconbitmap("icon1.ico")

    # Setup for frame with logical gates
    frame_logical_gates = ctk.CTkFrame(master=app)
    frame_logical_gates.grid(
        row=0, column=0, sticky="nswe",  padx=20, pady=20)

    # Label for the framw
    label_logical_frame = ctk.CTkLabel(
        master=frame_logical_gates, text="Logic Gates", text_font=("Roboto Medium", 13))
    label_logical_frame.grid(row=0, column=0)

    # Setup for buttons in a frames
    cmpd = "top"
    hght = 80
    wdth = 150
    fg_color = ("gray75", "gray30")

    # NOT button
    not_button = ctk.CTkButton(
        master=frame_logical_gates, text="NOT Gate",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        # command=dec(NOT_Gate))
        command=lambda: curr_com_put(NOT_Gate))

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/not.png").resize((80, 40)))
    not_button.set_image(img)
    not_button.grid(row=1, column=0, padx=5, pady=5)

    # AND button
    and_button = ctk.CTkButton(
        master=frame_logical_gates, text="AND Gate",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=lambda: curr_com_put(AND_Gate))

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/and.png").resize((80, 40)))
    and_button.set_image(img)
    and_button.grid(row=1, column=1, padx=5, pady=5)

    # NAND button
    nand_button = ctk.CTkButton(
        master=frame_logical_gates, text="NAND Gate",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=lambda: curr_com_put(NAND_Gate))

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/nand.png").resize((80, 40)))
    nand_button.set_image(img)
    nand_button.grid(row=2, column=0, padx=5, pady=5)

    # OR button
    or_button = ctk.CTkButton(
        master=frame_logical_gates, text="OR Gate",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=lambda: curr_com_put(OR_Gate))

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/or.png").resize((80, 40)))
    or_button.set_image(img)
    or_button.grid(row=2, column=1, padx=5, pady=5)

    # NOR button
    nor_button = ctk.CTkButton(
        master=frame_logical_gates, text="NOR Gate",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=lambda: curr_com_put(NOR_Gate))

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/nor.png").resize((80, 40)))
    nor_button.set_image(img)
    nor_button.grid(row=3, column=0, padx=5, pady=5)

    # XOR button
    xor_button = ctk.CTkButton(
        master=frame_logical_gates, text="XOR Gate",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=lambda: curr_com_put(XOR_Gate))

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/xor.png").resize((80, 40)))
    xor_button.set_image(img)
    xor_button.grid(row=3, column=1, padx=5, pady=5)

    # XNOR button
    xnor_button = ctk.CTkButton(
        master=frame_logical_gates, text="XNOR Gate",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=lambda: curr_com_put(XNOR_Gate))

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/xnor.png").resize((80, 40)))
    xnor_button.set_image(img)
    xnor_button.grid(row=4, column=0, padx=5, pady=5)

    # Setup for frame with input controls
    input_controls = ctk.CTkFrame(master=app)
    input_controls.grid(
        row=1, column=0, sticky="nswe",  padx=20, pady=20)

    # Label for the framw
    label_input_controls = ctk.CTkLabel(
        master=input_controls, text="Input Controls", text_font=("Roboto Medium", 13))
    label_input_controls.grid(row=0, column=0)

    # High Constant button
    high_constant_button = ctk.CTkButton(
        master=input_controls, text="High Constant",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=lambda: curr_com_put(ONE_Generator))

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/high_constant.png").resize((80, 40)))
    high_constant_button.set_image(img)
    high_constant_button.grid(row=1, column=0, padx=5, pady=5)

    # Low Constant button
    low_constant_button = ctk.CTkButton(
        master=input_controls, text="Low Constant",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=lambda: curr_com_put(ZERO_Generator))

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/low_constant.png").resize((80, 40)))
    low_constant_button.set_image(img)
    low_constant_button.grid(row=1, column=1, padx=5, pady=5)

    # Switch button
    switch_button = ctk.CTkButton(
        master=input_controls, text="Switch",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=lambda: curr_com_put(Switch))

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/switch_off.png").resize((80, 40)))
    switch_button.set_image(img)
    switch_button.grid(row=2, column=0, padx=5, pady=5)

    # Clock button
    clock_button = ctk.CTkButton(
        master=input_controls, text="Clock",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=lambda: curr_com_put(ClockGenerator))

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/clock_off.png").resize((80, 40)))
    clock_button.set_image(img)
    clock_button.grid(row=2, column=1, padx=5, pady=5)

    # Setup for frame with output controls
    output_controls = ctk.CTkFrame(master=app)
    output_controls.grid(
        row=2, column=0, sticky="nswe",  padx=20, pady=20)

    # Label for the frame
    label_output_controls = ctk.CTkLabel(
        master=output_controls, text="Output Controls", text_font=("Roboto Medium", 13))
    label_output_controls.grid(row=0, column=0)

    # Light Bulb button
    light_bulb_button = ctk.CTkButton(
        master=output_controls,
        text="Light Bulb",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=lambda: curr_com_put(Lamp)
    )

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/light_bulb.png").resize((40, 80)))
    light_bulb_button.set_image(img)
    light_bulb_button.grid(row=1, column=0, padx=5, pady=5)

    # Setup for frame with advanced elements
    frame_advanced_elements = ctk.CTkFrame(master=app)
    frame_advanced_elements.grid(
        row=0, column=3, rowspan=2, sticky="nswe", padx=20, pady=20)

    # Label for the frame
    label_advanced_elements = ctk.CTkLabel(
        master=frame_advanced_elements, text="Advanced elements", text_font=("Roboto Medium", 13))
    label_advanced_elements.grid(row=0, column=0)

    # Half Adder button
    half_adder_button = ctk.CTkButton(
        master=frame_advanced_elements, text="Half Adder",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=lambda: curr_com_put(HalfAdder))

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/half_adder.png").resize((80, 40)))
    half_adder_button.set_image(img)
    half_adder_button.grid(row=1, column=0, padx=5, pady=5)

    # Adder button
    adder_button = ctk.CTkButton(
        master=frame_advanced_elements, text="Adder",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=lambda: curr_com_put(Adder))

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/adder.png").resize((80, 40)))
    adder_button.set_image(img)
    adder_button.grid(row=1, column=1, padx=5, pady=5)

    # Decoder button
    decoder_button = ctk.CTkButton(
        master=frame_advanced_elements, text="Decoder",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=lambda: curr_com_put(Decoder))

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/decoder.png").resize((70, 80)))
    decoder_button.set_image(img)
    decoder_button.grid(row=2, column=0, padx=5, pady=5)

    # Encoder 8 to 3 button
    encoder_8_to_3_button = ctk.CTkButton(
        master=frame_advanced_elements, text="Encoder 8 to 3",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=lambda: curr_com_put(Encoder_8_to_3))

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/encoder_8_to_3.png").resize((70, 80)))
    encoder_8_to_3_button.set_image(img)
    encoder_8_to_3_button.grid(row=2, column=1, padx=5, pady=5)

    # Half Substractor button
    half_substractor_button = ctk.CTkButton(
        master=frame_advanced_elements, text="Half Substractor",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=lambda: curr_com_put(HalfSubstractor))

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/half_substractor.png").resize((80, 40)))
    half_substractor_button.set_image(img)
    half_substractor_button.grid(row=3, column=0, padx=5, pady=5)

    # Substractor button
    substractor_button = ctk.CTkButton(
        master=frame_advanced_elements, text="Substractor",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=lambda: curr_com_put(Substractor))

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/substractor.png").resize((80, 40)))
    substractor_button.set_image(img)
    substractor_button.grid(row=3, column=1, padx=5, pady=5)

    # Left Shift button
    left_shift_button = ctk.CTkButton(
        master=frame_advanced_elements, text="Left Shift",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=lambda: curr_com_put(ShiftLeft))

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/left_shift.png").resize((100, 60)))
    left_shift_button.set_image(img)
    left_shift_button.grid(row=4, column=0, padx=5, pady=5)

    # Right Shift button
    right_shift_button = ctk.CTkButton(
        master=frame_advanced_elements, text="Right Shift",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=lambda: curr_com_put(ShiftRight))

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/right_shift.png").resize((100, 60)))
    right_shift_button.set_image(img)
    right_shift_button.grid(row=4, column=1, padx=5, pady=5)

    # Encoder 4 to 2 button
    encoder_4_to_2_button = ctk.CTkButton(
        master=frame_advanced_elements, text="Encoder 4 to 2",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=lambda: curr_com_put(Encoder_4_to_2))

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/encoder_4_to_2.png").resize((80, 40)))
    encoder_4_to_2_button.set_image(img)
    encoder_4_to_2_button.grid(row=5, column=0, padx=5, pady=5)

    # Setup for frame with action buttons
    action_buttons_frame = ctk.CTkFrame(master=app)
    action_buttons_frame.grid(
        row=2, column=3, sticky="nswe", padx=20, pady=20)

    # Connect button
    connect_button = ctk.CTkButton(
        master=action_buttons_frame, text="Connect", text_font=("Roboto Medium", 14),
        compound=cmpd,
        height=hght,
        width=wdth,
        command=curr_com_connect)
    connect_button.grid(row=0, column=0, padx=5, pady=5)

    # Delete button
    delete_button = ctk.CTkButton(
        master=action_buttons_frame, text="Delete", text_font=("Roboto Medium", 14),
        compound=cmpd,
        height=hght,
        width=wdth,
        command=curr_com_delete)
    delete_button.grid(row=0, column=1, padx=5, pady=5)

    # Setting up the canvas
    global canvas  # please don't use globals
    canvas = Canvas(master=app, height=700,
                    width=1000, bg="light grey", )
    canvas.grid(row=0, column=1, rowspan=3)

    # Setting up the board
    global board
    board = Board(canvas)

    # start a main loop
    start(app)


if __name__ == "__main__":
    main()
