from PIL import Image, ImageDraw, ImageTk
import math
import tkinter as tk
import functools
import studio
import json
import os

class drawling_menu:
    def __init__(self, root):
        self.root = root
        self.root.geometry('390x500')

        header = tk.Label(self.root, text='Choose a project to begin:', font=('consolas', 14))
        header.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky='nw')

        project_position = [1, -1]
        for project_name in os.listdir('saves'):
            if os.path.isfile(f'saves/{project_name}'):
                project_name = project_name.replace('.drawdata', '')
                resolution = Image.open(f'saves/previews/{project_name}.png').size
                aspect_ratio = resolution[0 if resolution[0] > resolution[1] else 1]/resolution[0 if resolution[0] < resolution[1] else 1]
                exec(f'''self.photo_{project_name} = ImageTk.PhotoImage((Image.open(f'saves/previews/{project_name}.png')).resize(((100 if resolution[0] > resolution[1] else int(100/aspect_ratio)), (100 if resolution[1] > resolution[0] else int(100/aspect_ratio)))))''')
                exec(f'self.photo = self.photo_{project_name}')
                
                if project_position[1] == 2:
                    project_position[0] += 1
                    project_position[1] = -1
                project_position[1] += 1

                action_with_arg = functools.partial(self.open_project, project_name)
                tk.Button(self.root, text=project_name, bd=3, image=self.photo, command=action_with_arg, compound=tk.TOP, height=110).grid(row=project_position[0], column=project_position[1], padx=10, pady=10)
        self.new_project = ImageTk.PhotoImage((Image.open('assets/create_new.png')))
        
        if project_position[1] == 2:
            project_position[0] += 1
            project_position[1] = -1
        project_position[1] += 1

        action_with_arg = functools.partial(self.open_project, True)
        tk.Button(self.root, text='', bd=3, image=self.new_project, command=action_with_arg, compound=tk.TOP).grid(row=project_position[0], column=project_position[1], padx=10, pady=10)

        self.root.geometry(f'390x{34+math.ceil(len(os.listdir("saves"))/3)*135+20}')
        self.root.mainloop()

    def open_project(self, project_name):
        if project_name != True:
            studio.drawling_studio(project_name)
            self.root.destroy()
        else:
            for widget in self.root.winfo_children():
                widget.destroy()
            self.root.geometry('290x420')
            header = tk.Label(self.root, text='Create new project.', font=('consolas', 14))
            header.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky='nw')

            tk.Label(self.root, text='Name:', justify=tk.RIGHT, anchor=tk.E).grid(row=1, column=0, pady=(30, 2), sticky=tk.E)
            tk.Label(self.root, text='Type:', justify=tk.RIGHT, anchor=tk.E).grid(row=2, column=0, pady=(10, 2), sticky=tk.E)
            tk.Label(self.root, text='Resolution X:', justify=tk.RIGHT, anchor=tk.E).grid(row=3, column=0, pady=(10, 2), sticky=tk.E)
            tk.Label(self.root, text='Resolution Y:', justify=tk.RIGHT, anchor=tk.E).grid(row=4, column=0, pady=(10, 2), sticky=tk.E)
            tk.Label(self.root, text='Multiplied size*:', justify=tk.RIGHT, anchor=tk.E).grid(row=5, column=0, pady=(10, 2), sticky=tk.E)
            tk.Label(self.root, text='Display position*:', justify=tk.RIGHT, anchor=tk.E).grid(row=6, column=0, pady=(10, 2), sticky=tk.E)
            tk.Label(self.root, text='Display position*:', justify=tk.RIGHT, anchor=tk.E).grid(row=7, column=0, pady=(10, 2), sticky=tk.E)
            tk.Label(self.root, text='* these settings can be easily changed later.\nYou need to set the default values', justify=tk.RIGHT, anchor=tk.E).grid(row=10, column=0, columnspan=3, pady=(30, 2), sticky=tk.E)

            var_project_name = tk.StringVar()
            project_name = tk.Entry(self.root, textvariable=var_project_name)
            project_name.grid(row=1, column=1, pady=(30, 2), sticky=tk.W)

            var_mode = tk.StringVar()

            options = ['Bitmap', 'More maybe coming soon...']

            def set_selected_option(selected):
                var_mode.set(selected)

            option_menu = tk.OptionMenu(self.root, var_mode, *options, command=set_selected_option)
            option_menu.grid(row=2, column=1, pady=(10, 2), sticky=tk.W)

            var_mode.set(options[0])

            resolution_increment = 16
            var_resolution_x = tk.StringVar()
            resolution_x = tk.Spinbox(self.root, from_=16, to=512, textvariable=var_resolution_x, increment=resolution_increment, width=4)
            resolution_x.grid(row=3, column=1, pady=(10, 2), stick=tk.W)
            var_resolution_x.set(64)
            var_resolution_y = tk.StringVar()
            resolution_y = tk.Spinbox(self.root, from_=16, to=512, textvariable=var_resolution_y, increment=resolution_increment, width=4)
            resolution_y.grid(row=4, column=1, pady=(10, 2), stick=tk.W)
            var_resolution_y.set(64)

            size_increment = 1
            var_size = tk.StringVar()
            size = tk.Spinbox(self.root, from_=1, to=50, textvariable=var_size, increment=size_increment, width=4)
            size.grid(row=5, column=1, pady=(10, 2), stick=tk.W)
            var_size.set(5)

            position_increment = 5
            var_position_x = tk.StringVar()
            position_x = tk.Spinbox(self.root, from_=0, to=100, textvariable=var_position_x, increment=position_increment, width=4)
            position_x.grid(row=6, column=1, pady=(10, 2), stick=tk.W)
            var_position_x.set(0)
            var_position_y = tk.StringVar()
            position_y = tk.Spinbox(self.root, from_=0, to=100, textvariable=var_position_y, increment=position_increment, width=4)
            position_y.grid(row=7, column=1, pady=(10, 2), stick=tk.W)
            var_position_y.set(0)

            tk.Button(self.root, text='Create', bd=3, command=lambda: self.create_new_project((var_project_name.get(), var_resolution_x.get(), var_resolution_y.get(), ('bmp' if var_mode.get() == 'Bitmap' else 'bmp'), var_size.get(), var_position_x.get(), var_position_y.get()))).grid(row=15, column=3, sticky=tk.SE)
            
            self.root.mainloop()

    def create_new_project(self, settings):
        frame = {
            'resolution': [int(settings[1]), int(settings[2])],
            'mode': settings[3],
            'color': '#ffffff',
            'size': int(settings[4]),
            'position': [int(settings[5]), int(settings[6])]
        }
        with open(f'saves/{settings[0]}.drawdata', 'w', encoding='utf-8') as save_file:
            save_file.write(f'{json.dumps(frame).replace(" ", "")}|')

        image = Image.new("RGB", (frame['resolution'][0], frame['resolution'][1]), "black")
        image.save(f'saves/previews/{settings[0]}.png', "PNG")

        for widget in self.root.winfo_children():
            widget.destroy()
        drawling_menu(self.root)

root = tk.Tk()
root.title(f'DrawlingStudio - choose file to edit')
root.configure(bg='#0A0A10')
root.iconbitmap('assets/icon.ico')
root.tk_setPalette(background='#0A0A10', foreground='white', activeBackground='#0A0A10', activeForeground='white')
drawling_menu(root)
