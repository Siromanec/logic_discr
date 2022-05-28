from tkinter import *
import customtkinter
from PIL import Image, ImageTk

#Just a setup for a theme
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


class App(customtkinter.CTk):

    WIDTH = 1400
    HEIGHT = 800
    def __init__(self):
        super().__init__()

        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.title("Logical Elements Constructor")
        self.iconbitmap("icon1.ico")
        
        #Setup for frame with logical gates
        self.frame_logical_gates = customtkinter.CTkFrame(master=self)
        self.frame_logical_gates.grid(row=0, column=0, sticky="nswe",  padx=20, pady=20)
        
        #Label for the framw
        self.label_logical_frame = customtkinter.CTkLabel(master=self.frame_logical_gates, text="Logic Gates", text_font = ("Roboto Medium", 13))
        self.label_logical_frame.grid(row = 0, column = 0)

        #Setup for buttons in a frames
        local_compound = "top"
        local_height = 40
        local_width = 100
        local_fg_color = ("gray75", "gray30")
        
        #Buffer button
        self.buffer_button = customtkinter.CTkButton(
            master=self.frame_logical_gates, text="Buffer", 
            compound= local_compound,
            height= local_height, 
            width = local_width, 
            fg_color=local_fg_color)
        
        img = ImageTk.PhotoImage(Image.open("buffer.png"))
        self.buffer_button.set_image(img)
        self.buffer_button.grid(row = 1, column = 0, padx=5, pady=5)

        #NOT button
        self.not_button = customtkinter.CTkButton(
            master=self.frame_logical_gates, text="NOT Gate",  
            compound= local_compound,
            height= local_height, 
            width = local_width, 
            fg_color=local_fg_color)
        
        img = ImageTk.PhotoImage(Image.open("not.png"))
        self.not_button.set_image(img)
        self.not_button.grid(row = 1, column = 1, padx=5, pady=5)

        #AND button
        self.and_button = customtkinter.CTkButton(
            master=self.frame_logical_gates, text="AND Gate",  
            compound= local_compound,
            height= local_height, 
            width = local_width, 
            fg_color=local_fg_color)
        
        img = ImageTk.PhotoImage(Image.open("and.png"))
        self.and_button.set_image(img)
        self.and_button.grid(row = 2, column = 0, padx=5, pady=5)

        #NAND button
        self.nand_button = customtkinter.CTkButton(
            master=self.frame_logical_gates, text="NAND Gate", 
            compound= local_compound, 
            height= local_height, 
            width = local_width, 
            fg_color=local_fg_color)
        
        img = ImageTk.PhotoImage(Image.open("nand.png"))
        self.nand_button.set_image(img)
        self.nand_button.grid(row = 2, column = 1, padx=5, pady=5)

        #OR button
        self.or_button = customtkinter.CTkButton(
            master=self.frame_logical_gates, text="OR Gate", 
            compound= local_compound, 
            height= local_height, 
            width = local_width, 
            fg_color=local_fg_color)
        
        img = ImageTk.PhotoImage(Image.open("or.png"))
        self.or_button.set_image(img)
        self.or_button.grid(row = 3, column = 0, padx=5, pady=5)

        #NOR button
        self.nor_button = customtkinter.CTkButton(
            master=self.frame_logical_gates, text="NOR Gate", 
            compound= local_compound, 
            height= local_height, 
            width = local_width, 
            fg_color=local_fg_color)
        
        img = ImageTk.PhotoImage(Image.open("nor.png"))
        self.nor_button.set_image(img)
        self.nor_button.grid(row = 3, column = 1, padx=5, pady=5)

        #XOR button
        self.xor_button = customtkinter.CTkButton(
            master=self.frame_logical_gates, text="XOR Gate", 
            compound= local_compound, 
            height= local_height, 
            width = local_width, 
            fg_color=local_fg_color)
        
        img = ImageTk.PhotoImage(Image.open("xor.png"))
        self.xor_button.set_image(img)
        self.xor_button.grid(row = 4, column = 0, padx=5, pady=5)

        #XNOR button
        self.xnor_button = customtkinter.CTkButton(
            master=self.frame_logical_gates, text="XNOR Gate", 
            compound= local_compound, 
            height= local_height, 
            width = local_width, 
            fg_color=local_fg_color)
        
        img = ImageTk.PhotoImage(Image.open("XNOR.png"))
        self.xnor_button.set_image(img)
        self.xnor_button.grid(row = 4, column = 1, padx=5, pady=5)


    def button_function():
        """Just shob bulo"""
        print("button pressed")
    
    def start(self):
        """Starts the whole thing"""
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
