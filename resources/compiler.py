import datetime
import json
import os


class pysilon_Compiler:
    def __init__(self) -> None:
        os.chdir('resources')
        with open('source.py', 'r', encoding='utf-8') as f: self.source = f.readlines(); self.log('Loaded source.py', 0)
        with open('assets/compiler_configuration.json', 'r', encoding='utf-8') as f: self.compiler_configuration = json.load(f); self.log('Loaded compiler configuration', 0)
        self.dataframe = self.parse_source(self.source)
        print(self.dataframe)

    def parse_source(self, source_code) -> list:
        dataframe = {}
        for line_index, line in enumerate(source_code):
            line = line.strip()
            if line[:2] == '#!':
                dataframe[line[2:].split('.')[0]] = {'intendation': int(line.split('=')[1]), 'line': line_index}
                self.log(f'Found parameter "{line[2:].split(".")[0]}" at line {line_index}.', 0)
        if len(dataframe) == 0: self.log('No parameters found. This should not occur. Contact PySilon development staff for help or try to re-clone the repository.', 2)
        else: self.log(f'Successfully parsed source code. Found {len(dataframe)} parameters.', 0)
        return dataframe
    
    def log(self, message, type) -> None:
        if type == 0: prefix = 'INFO'
        elif type == 1: prefix = 'WARNING'
        elif type == 2: prefix = 'ERROR'
        print(f"[{prefix}][{datetime.datetime.now().strftime('%d.%m.%y-%H:%M:%S')}] {message}")
        if type == 2: exit()

pysilon_Compiler()

