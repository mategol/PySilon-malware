import os

os.chdir('../.')
print(f'Listing all the files from {os.getcwd()}')

tree = []
def list_files(path):
    global tree
    for element in os.listdir(path):
        if element not in ['.git', '.github', '.gitignore', 'Windows-10', 'Windows-11']:
            if os.path.isdir(f'{path}/{element}'): list_files(f'{path}/{element}')
            else: tree.append(f'{path[path.find("PySilon-malware"):].replace("PySilon-malware", ".", 1)}/{element}')

list_files(os.getcwd())



for i in tree:
    print(f'{i}')











input()