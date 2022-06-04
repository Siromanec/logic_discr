from __future__ import annotations

import time
from tkinter import Canvas
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from board_elements.SimpleBoardElements import *
from board_elements.Fundamentals import *


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
            center1[0], center1[1], center2[0], center2[1], width=self.width, fill=self.color, tag=self.tag)
        for pin in self.get_connected_pins():
            pin.set_connected_line_tag(self.tag)


def connect(event):
    print("clicked at", event.x, event.y)

    if not Line.valide_click(event.x, event.y):
        print("invalid click")
        Line.clear_last_pins()

    elif len(Line.last_pins_to_connect) == 2:
        last_pins = Line.last_pins_to_connect
        if isinstance(last_pins[0], OutputPin) and isinstance(last_pins[1], InputPin):
            board.connect_pins(last_pins[0], last_pins[1])
            for element in board.get_circuits_list():
                img = ImageTk.PhotoImage(
                    Image.open(element.img)).resize((50, 100))
                canvas.itemconfig(element.img_object, image=img)
                board.add_to_img_list(img)
            line = Line(canvas=canvas, connected_pins=last_pins)
            line.draw_line()
        elif isinstance(last_pins[0], InputPin) and isinstance(last_pins[1], OutputPin):
            board.connect_pins(last_pins[1], last_pins[0])
            for element in board.get_circuits_list():
                img = ImageTk.PhotoImage(
                    Image.open(element.img)).resize((50, 100))
                canvas.itemconfig(element.img_object, image=img)
                board.add_to_img_list(img)
            line = Line(canvas=canvas, connected_pins=last_pins)
            line.draw_line()
        Line.clear_last_pins()


def delete(event):
    """Delete element from canvas"""
    for element in board.get_circuits_list():
        # remove if lamp!!!!!!!!!!!!!!
        if isinstance(element, Lamp) and element.check_dot_in_img(event.x, event.y):
            canvas.delete(element.tag)
            for input_pin in element.get_inputs():
                # delete line from canvas
                line_to_delete = input_pin.get_connected_line_tag()
                canvas.delete(line_to_delete)
                # remove line tag from parent pin
                parent = input_pin.get_parent()
                if parent:
                    parent.remove_connected_line_tag()
            for output_pin in element.get_outputs():
                # delete line from canvas
                line_to_delete = output_pin.get_connected_line_tag()
                canvas.delete(line_to_delete)
                # remove line tag from children pins
                children = output_pin.get_children()
                for child in children:
                    if child:
                        child.remove_connected_line_tag()

            board.remove_element(element)


def put(element_type, event):
    """Puts image of gate NOT on the canvas"""
    print("clicked at", event.x, event.y)
    new_not = board.create_element(element_type)
    new_not.update_reaction_areas(event.x, event.y)
    # print(new_not._input_pins[0].get_reaction_area())
    # print(new_not._output_pins[0].get_reaction_area())
    img = ImageTk.PhotoImage(Image.open(new_not.img_path).resize((100, 50)))
    board.add_to_img_list(img)
    canvas.create_image(event.x, event.y, image=img)


def put_bulb(event):
    """Puts image bulb on the canvas"""
    print("clicked at", event.x, event.y)
    new_lamp = board.create_element(Lamp)
    new_lamp.update_reaction_areas(event.x, event.y)
    new_lamp.set_img_coords(event.x, event.y)
    # print(new_lamp._input_pins[0].get_reaction_area())
    img = ImageTk.PhotoImage(Image.open(
        new_lamp.img_path_off).resize((50, 100)))
    board.add_to_img_list(img)
    canvas.create_image(event.x, event.y, image=img, tag=new_lamp.tag)
    # m = canvas.create_image(event.x, event.y, image=img)


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


def put_and(event):
    """Puts image of gate AND on the canvas"""
    print("clicked at", event.x, event.y)
    new_and = board.create_element(AND_Gate)
    new_and.update_reaction_areas(event.x, event.y)
    print(new_and._input_pins[0].get_reaction_area())
    img = ImageTk.PhotoImage(Image.open(new_and.img_path).resize((100, 50)))
    board.add_to_img_list(img)
    canvas.create_image(event.x, event.y, image=img)


def put_nand(event):
    """Puts image of gate NAND on the canvas"""
    print("clicked at", event.x, event.y)
    new_nand = board.create_element(NAND_Gate)
    new_nand.update_reaction_areas(event.x, event.y)
    img = ImageTk.PhotoImage(Image.open(new_nand.img_path).resize((100, 50)))
    board.add_to_img_list(img)
    canvas.create_image(event.x, event.y, image=img)


def put_or(event):
    """Puts image of gate OR on the canvas"""
    print("clicked at", event.x, event.y)
    new_or = board.create_element(OR_Gate)
    new_or.update_reaction_areas(event.x, event.y)
    img = ImageTk.PhotoImage(Image.open(new_or.img_path).resize((100, 50)))
    board.add_to_img_list(img)
    new_or.img_object = canvas.create_image(event.x, event.y, image=img)


def put_nor(event):
    """Puts image of gate NOR on the canvas"""
    print("clicked at", event.x, event.y)
    new_nor = board.create_element(NOR_Gate)
    new_nor.update_reaction_areas(event.x, event.y)
    img = ImageTk.PhotoImage(Image.open(new_nor.img_path).resize((100, 50)))
    board.add_to_img_list(img)
    canvas.create_image(event.x, event.y, image=img)


def put_xor(event):
    """Puts image of gate XOR on the canvas"""
    print("clicked at", event.x, event.y)
    new_xor = board.create_element(XOR_Gate)
    new_xor.update_reaction_areas(event.x, event.y)
    img = ImageTk.PhotoImage(Image.open(new_xor.img_path).resize((100, 50)))
    board.add_to_img_list(img)
    canvas.create_image(event.x, event.y, image=img)


def put_xnor(event):
    """Puts image of gate XNOR on the canvas"""
    print("clicked at", event.x, event.y)
    new_xnor = board.create_element(XNOR_Gate)
    new_xnor.update_reaction_areas(event.x, event.y)
    img = ImageTk.PhotoImage(Image.open(new_xnor.img_path).resize((100, 50)))
    board.add_to_img_list(img)
    canvas.create_image(event.x, event.y, image=img)


def put_high_const(event):
    """Puts image of ONE generator on the canvas"""
    print("clicked at", event.x, event.y)
    new_high_const = board.create_element(ONE_Generator)
    new_high_const.update_reaction_areas(event.x, event.y)
    img = ImageTk.PhotoImage(Image.open(
        new_high_const.img_path).resize((100, 50)))
    board.add_to_img_list(img)
    canvas.create_image(event.x, event.y, image=img)


def put_low_const(event):
    """Puts image of ZERO generator on the canvas"""
    print("clicked at", event.x, event.y)
    new_low_const = board.create_element(ZERO_Generator)
    new_low_const.update_reaction_areas(event.x, event.y)
    img = ImageTk.PhotoImage(Image.open(
        new_low_const.img_path).resize((100, 50)))
    board.add_to_img_list(img)
    canvas.create_image(event.x, event.y, image=img)


def dec(element):
    def curr_com(element):
        canvas.bind("<Button-1>", element)
    return curr_com


def curr_com_connect():
    Line.clear_last_pins()
    canvas.bind("<Button-1>", connect)


def curr_com_delete():
    """Defines command"""
    canvas.bind("<Button-1>", delete)


def curr_com_put_bulb():
    """Defines command"""
    canvas.bind("<Button-1>", put_bulb)


def curr_com_put_not():
    """Defines command"""
    canvas.bind("<Button-1>", put_not)


def curr_com_put_and():
    """Defines command"""
    canvas.bind("<Button-1>", put_and)


def curr_com_put_nand():
    """Defines command"""
    canvas.bind("<Button-1>", put_nand)


def curr_com_put_or(el_type):
    """Defines command"""
    canvas.bind("<Button-1>", put_or)


def curr_com_put_nor():
    """Defines command"""
    canvas.bind("<Button-1>", put_nor)


def curr_com_put_xor():
    """Defines command"""
    canvas.bind("<Button-1>", put_xor)


def curr_com_put_xnor():
    """Defines command"""
    canvas.bind("<Button-1>", put_xnor)


def curr_com_put_high_const():
    """Defines command"""
    canvas.bind("<Button-1>", put_high_const)


def curr_com_put_low_const():
    """Defines command"""
    canvas.bind("<Button-1>", put_low_const)


def start(app: ctk.CTk):
    """Starts the whole thing"""
    app.mainloop()


def main():
    # Just a setup for a theme
    # Modes: system (default), light, dark
    ctk.set_appearance_mode("dark")
    # Themes: blue (default), dark-blue, green
    ctk.set_default_color_theme("blue")

    WIDTH = 1400
    HEIGHT = 900

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

    # Buffer button
    buffer_button = ctk.CTkButton(
        master=frame_logical_gates, text="Buffer",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color)

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/buffer.png").resize((80, 40)))
    buffer_button.set_image(img)
    buffer_button.grid(row=1, column=0, padx=5, pady=5)

    # NOT button
    not_button = ctk.CTkButton(
        master=frame_logical_gates, text="NOT Gate",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=dec())

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/not.png").resize((80, 40)))
    not_button.set_image(img)
    not_button.grid(row=1, column=1, padx=5, pady=5)

    # AND button
    and_button = ctk.CTkButton(
        master=frame_logical_gates, text="AND Gate",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=curr_com_put_and)

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/and.png").resize((80, 40)))
    and_button.set_image(img)
    and_button.grid(row=2, column=0, padx=5, pady=5)

    # NAND button
    nand_button = ctk.CTkButton(
        master=frame_logical_gates, text="NAND Gate",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=curr_com_put_nand)

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/nand.png").resize((80, 40)))
    nand_button.set_image(img)
    nand_button.grid(row=2, column=1, padx=5, pady=5)

    # OR button
    or_button = ctk.CTkButton(
        master=frame_logical_gates, text="OR Gate",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=curr_com_put_or)

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/or.png").resize((80, 40)))
    or_button.set_image(img)
    or_button.grid(row=3, column=0, padx=5, pady=5)

    # NOR button
    nor_button = ctk.CTkButton(
        master=frame_logical_gates, text="NOR Gate",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=curr_com_put_nor)

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/nor.png").resize((80, 40)))
    nor_button.set_image(img)
    nor_button.grid(row=3, column=1, padx=5, pady=5)

    # XOR button
    xor_button = ctk.CTkButton(
        master=frame_logical_gates, text="XOR Gate",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=curr_com_put_xor)

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/xor.png").resize((80, 40)))
    xor_button.set_image(img)
    xor_button.grid(row=4, column=0, padx=5, pady=5)

    # XNOR button
    xnor_button = ctk.CTkButton(
        master=frame_logical_gates, text="XNOR Gate",
        compound=cmpd,
        height=hght,
        width=wdth,
        fg_color=fg_color,
        command=curr_com_put_xnor)

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/xnor.png").resize((80, 40)))
    xnor_button.set_image(img)
    xnor_button.grid(row=4, column=1, padx=5, pady=5)

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
        command=curr_com_put_high_const)

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
        command=curr_com_put_low_const)

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/low_constant.png").resize((80, 40)))
    low_constant_button.set_image(img)
    low_constant_button.grid(row=1, column=1, padx=5, pady=5)

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
        command=curr_com_put_bulb
    )

    img = ImageTk.PhotoImage(Image.open(
        "app_code/visuals/textures/light_bulb.png").resize((40, 80)))
    light_bulb_button.set_image(img)
    light_bulb_button.grid(row=1, column=0, padx=5, pady=5)

    # Connect button
    connect_button = ctk.CTkButton(
        master=output_controls, text="Connect", text_font=("Roboto Medium", 14),
        compound=cmpd,
        height=hght,
        width=wdth,
        command=curr_com_connect)
    connect_button.grid(row=1, column=1, padx=5, pady=5)

    # Delete button
    delete_button = ctk.CTkButton(
        master=output_controls, text="Delete", text_font=("Roboto Medium", 14),
        compound=cmpd,
        height=hght,
        width=wdth,
        command=curr_com_delete)
    delete_button.grid(row=2, column=0, padx=5, pady=5)

    # Setting up the canvas
    global canvas  # please don't use globals
    canvas = Canvas(master=app, height=700,
                    width=1000, bg="light grey")
    canvas.grid(row=0, column=2, rowspan=3)

    # Setting up the board
    global board
    board = Board()

    # start a main loop
    start(app)


if __name__ == "__main__":
    main()
