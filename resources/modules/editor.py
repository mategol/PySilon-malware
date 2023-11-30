import tkinter as tk

root = tk.Tk()
root.geometry('400x500')
root.title('Configuration Editor')

frame = tk.Frame(root)
frame.place(x=0, y=0, width=400, height=500)

text = tk.Text(frame)
text.place(x=0, y=0, width=400, height=475)

text.insert('1.0', 'Hello, world!')

root.tk_setPalette(background='#0A0A10', foreground='white', activeBackground='#0A0A10', activeForeground='white')
root.mainloop()