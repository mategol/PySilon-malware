import os
from filesplit.merge import Merge
from tkinter import Tk, filedialog

def get_manual_path():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    open_dir = filedialog.askdirectory()
    root.destroy()
    return open_dir

input_dir = get_manual_path()
for i in os.listdir(input_dir):
    if i != 'manifest':
        os.rename(input_dir + '/' + i, input_dir + '/' + i[:-8])

with open(input_dir + '/manifest', 'r') as manifest:
    filename = manifest.readlines()[1]
filename = ','.join(filename[::-1].split(',')[2:]).replace('1_', '', 1)[::-1]

Merge(input_dir, '.', filename).merge(cleanup=True)
print('Done')
