from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
import json
from win32gui import *
from win32con import *
from win32api import *
from win32print import * 
import time
import os

def hex_to_rgb(hex):
    rgb = []
    hex = hex[1:]
    for i in (0, 2, 4):
        decimal = int(hex[i:i+2], 16)
        rgb.append(decimal)
    return tuple(rgb)

class drawling_studio:
    def __init__(self, saved_file):
        with open(f'saves/{saved_file}.drawdata', 'r', encoding='utf-8') as read_data:
            input_data = read_data.readlines()[0]
        settings, pixeldata = input_data.split('|')
        self.settings = json.loads(settings)
        self.pixeldata = pixeldata.split(',')
        self.saved_file = saved_file
        
        self.canvas_width, self.canvas_height = self.settings['resolution'][0], self.settings['resolution'][1]

        self.root = tk.Tk()
        self.root.title(f'DrawlingStudio -> {saved_file}.drawdata - {"BITMAP" if self.settings["mode"] == "bmp" else "IMAGE"} - {self.settings["resolution"][0]}x{self.settings["resolution"][1]}')
        self.root.configure(bg='#0A0A10')
        self.root.iconbitmap('assets/icon.ico')
        self.root.tk_setPalette(background='#0A0A10', foreground='white', activeBackground='#0A0A10', activeForeground='white')
        self.zoom = min(800 // self.canvas_width, 800 // self.canvas_height)

        self.canvas = tk.Canvas(self.root, width=self.canvas_width*self.zoom, height=self.canvas_height*self.zoom, bg='#000000', highlightbackground='#808080')
        self.canvas.grid(row=1, column=2, rowspan=self.canvas_height)

        self.foreground_preview_color = '#ffffff'
        self.background_preview_color = '#000000'
        self.current_color = '#ffffff'

        if self.settings['mode'] == 'bmp':
            self.pixels = [['#000000' for _ in range(self.canvas_height)] for _ in range(self.canvas_width)]
            if len(self.pixeldata) > 1:
                for pixel in self.pixeldata:
                    pixel = tuple(pixel.split('.'))
                    self.pixels[int(pixel[0])][int(pixel[1])] = '#ffffff'
                    self.canvas.create_rectangle(int(pixel[0]) * self.zoom, int(pixel[1]) * self.zoom, (int(pixel[0]) + 1) * self.zoom, (int(pixel[1]) + 1) * self.zoom, fill=self.current_color, outline='')

        self.drawing = False

        self.canvas.bind("<Button-1>", self.start_paint)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.stop_paint)

        save_button = tk.Button(self.root, text="Save", command=self.save_image)
        save_button.grid(row=self.canvas_height+1, column=2, sticky="sw")

        preview_button = tk.Button(self.root, text='Preview (2s)', command=lambda: self.preview_project(2))
        preview_button.grid(row=1, column=3)
        move_up_10_button = tk.Button(self.root, text='Move up\nby 10%', command=lambda: self.move_project('up', 10))
        move_up_10_button.grid(row=3, column=3)
        move_up_2_button = tk.Button(self.root, text='Move up\nby 2%', command=lambda: self.move_project('up', 2))
        move_up_2_button.grid(row=4, column=3)
        move_right_10_button = tk.Button(self.root, text='Move right\nby 10%', command=lambda: self.move_project('right', 10))
        move_right_10_button.grid(row=5, column=3)
        move_right_2_button = tk.Button(self.root, text='Move right\nby 2%', command=lambda: self.move_project('right', 2))
        move_right_2_button.grid(row=6, column=3)
        move_left_10_button = tk.Button(self.root, text='Move left\nby 10%', command=lambda: self.move_project('left', 10))
        move_left_10_button.grid(row=7, column=3)
        move_left_2_button = tk.Button(self.root, text='Move left\nby 2%', command=lambda: self.move_project('left', 2))
        move_left_2_button.grid(row=8, column=3)
        move_down_10_button = tk.Button(self.root, text='Move down\nby 10%', command=lambda: self.move_project('down', 10))
        move_down_10_button.grid(row=9, column=3)
        move_down_2_button = tk.Button(self.root, text='Move down\nby 2%', command=lambda: self.move_project('down', 2))
        move_down_2_button.grid(row=10, column=3)

        brush_button = tk.Button(self.root, text='Brush', command=self.switch_brush)
        brush_button.grid(row=1, column=1)
        eraser_button = tk.Button(self.root, text='Eraser', command=self.switch_eraser)
        eraser_button.grid(row=2, column=1)

        self.root.mainloop()

    def move_project(self, direction, amount):
        self.settings['position'][0 if direction in ['left', 'right'] else 1] += amount if direction in ['right', 'down'] else -amount
        self.preview_project(0.5)

    def preview_project(self, seconds):
        image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        draw = ImageDraw.Draw(image)
        for x in range(self.canvas_width):
            for y in range(self.canvas_height):
                draw.point((x, y), fill=self.pixels[x][y])
        image.save(f'saves/previews/{self.saved_file}_preview.png', "PNG")

        new_data = []
        data = self.fetch_data(f'saves/previews/{self.saved_file}_preview.png', self.settings['mode'])
        for pixel in data:
            if self.settings['mode'] == 'img':
                new_data.append(f'{pixel[0]}.{pixel[1]}:{pixel[2]}')
            elif self.settings['mode'] == 'bmp':
                new_data.append(f'{pixel[0]}.{pixel[1]}')

        with open(f'saves/{self.saved_file}_preview.drawdata', 'w', encoding='utf-8') as save_data:
            save_data.write(f'{json.dumps(self.settings).replace(" ", "")}|{",".join(new_data)}')

        with open(f'saves/{self.saved_file}_preview.drawdata', 'r', encoding='utf-8') as load_data:
            data = load_data.readlines()
        os.system(f'del saves\\{self.saved_file}_preview.drawdata')
        os.system(f'del saves\\previews\\{self.saved_file}_preview.png')

        frame, unfetched_pixels = data[0].split('|')
        frame = json.loads(frame)

        pixels = []
        for line in unfetched_pixels.split(','):
            x, y = line.split(':')[0].split('.')
            if frame['mode'] == 'img':
                color = line.split(':')[1]
            elif frame['mode'] == 'bmp':
                color = frame['color']
            pixels.append((int(x), int(y), hex_to_rgb(color)))

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
        
    def switch_brush(self):
        self.current_color = self.foreground_preview_color

    def switch_eraser(self):
        self.current_color = self.background_preview_color

    def start_paint(self, event):
        global drawing
        drawing = True
        self.paint(event)
            
    def update_canvas(self):
        self.canvas = tk.Canvas(self.root, width=self.canvas_width*self.zoom, height=self.canvas_height*self.zoom, bg=self.background_preview_color, highlightbackground='#808080')
        self.canvas.grid(row=1, column=2, rowspan=self.canvas_height)

        if self.settings['mode'] == 'bmp':
            self.pixels = [[self.background_preview_color for _ in range(self.canvas_height)] for _ in range(self.canvas_width)]
            if len(self.pixeldata) > 1:
                for pixel in self.pixeldata:
                    pixel = tuple(pixel.split('.'))
                    self.pixels[int(pixel[0])][int(pixel[1])] = self.foreground_preview_color
                    self.canvas.create_rectangle(int(pixel[0]) * self.zoom, int(pixel[1]) * self.zoom, (int(pixel[0]) + 1) * self.zoom, (int(pixel[1]) + 1) * self.zoom, fill=self.foreground_preview_color, outline='')

        self.drawing = False

    def paint(self, event):
        if drawing:
            x, y = event.x // self.zoom, event.y // self.zoom
            if 0 <= x < self.canvas_width and 0 <= y < self.canvas_height:
                self.pixels[x][y] = self.current_color
                self.canvas.create_rectangle(x * self.zoom, y * self.zoom, (x + 1) * self.zoom, (y + 1) * self.zoom, fill=self.current_color, outline='')

    def stop_paint(self, event):
        global drawing
        drawing = False

    def rgb_to_hex(self, r, g, b):
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    def fetch_data(self, path, mode):
        image = Image.open(path)
        pixels = list(image.getdata())
        width, height = image.size

        valid_pixels = []
        for y in range(height):
            for x in range(width):
                pixel = self.rgb_to_hex(pixels[y*width+x][0], pixels[y*width+x][1], pixels[y*width+x][2])
                if pixel == '#ffffff' and mode == 'bmp':
                    valid_pixels.append((x, y))
                elif mode == 'img':
                    valid_pixels.append((x, y, pixel))
        image.close()
        return valid_pixels
    
    def save_image(self):
        image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        draw = ImageDraw.Draw(image)
        for x in range(self.canvas_width):
            for y in range(self.canvas_height):
                draw.point((x, y), fill=self.pixels[x][y])
        image.save(f'saves/previews/{self.saved_file}.png', "PNG")

        new_data = []
        data = self.fetch_data(f'saves/previews/{self.saved_file}.png', self.settings['mode'])
        for pixel in data:
            if self.settings['mode'] == 'img':
                new_data.append(f'{pixel[0]}.{pixel[1]}:{pixel[2]}')
            elif self.settings['mode'] == 'bmp':
                new_data.append(f'{pixel[0]}.{pixel[1]}')

        with open(f'saves/{self.saved_file}.drawdata', 'w', encoding='utf-8') as save_data:
            save_data.write(f'{json.dumps(self.settings).replace(" ", "")}|{",".join(new_data)}')
