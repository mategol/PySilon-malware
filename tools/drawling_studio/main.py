import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk
import json

class drawling_studio:
    def __init__(self, saved_file):
        with open(f'saves/{saved_file}.drawdata', 'r', encoding='utf-8') as read_data:
            input_data = read_data.readlines()[0]
        settings, pixeldata = input_data.split('|')
        self.settings = json.loads(settings)
        pixeldata = pixeldata.split(',')
        self.saved_file = saved_file
        
        self.canvas_width, self.canvas_height = self.settings['resolution'][0], self.settings['resolution'][1]

        root = tk.Tk()
        root.title(f'{saved_file} - {"BITMAP" if self.settings["mode"] == "bmp" else "IMAGE"} - {self.settings["resolution"][0]}x{self.settings["resolution"][1]}')

        self.zoom = min(800 // self.canvas_width, 800 // self.canvas_height)

        self.canvas = tk.Canvas(root, width=self.canvas_width*self.zoom, height=self.canvas_height*self.zoom, bg='white')
        self.canvas.grid(row=1, column=2, rowspan=self.canvas_height)

        self.current_color = '#000000'

        if self.settings['mode'] == 'bmp':
            self.pixels = [['#ffffff' for _ in range(self.canvas_height)] for _ in range(self.canvas_width)]
            for pixel in pixeldata:
                pixel = tuple(pixel.split('.'))
                self.pixels[int(pixel[0])][int(pixel[1])] = '#000000'
                self.canvas.create_rectangle(int(pixel[0]) * self.zoom, int(pixel[1]) * self.zoom, (int(pixel[0]) + 1) * self.zoom, (int(pixel[1]) + 1) * self.zoom, fill=self.current_color, outline='')

        self.drawing = False

        self.canvas.bind("<Button-1>", self.start_paint)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.stop_paint)

        save_button = tk.Button(root, text="Save", command=self.save_image)
        save_button.grid(row=self.canvas_height+1, column=2, sticky="sw")

        right_button1 = tk.Button(root, text='Test')
        right_button1.grid(row=1, column=3)

        brush_button = tk.Button(root, text='Brush', command=self.switch_brush)
        brush_button.grid(row=1, column=1)
        eraser_button = tk.Button(root, text='Eraser', command=self.switch_eraser)
        eraser_button.grid(row=2, column=1)

        root.mainloop()

    def switch_brush(self):
        self.current_color = '#000000'

    def switch_eraser(self):
        self.current_color = '#ffffff'

    def start_paint(self, event):
        global drawing
        drawing = True
        self.paint(event)

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
                if pixel == '#000000' and mode == 'bmp':
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

        with open(f'saves/{self.saved_file}.drawdata', 'rb') as read_bytes:
            temp = read_bytes.read(10000)
        print(bytes(temp)[::-1])

drawling_studio(input('Project name: '))
