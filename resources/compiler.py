import datetime
import json
import os

class pysilon_Compiler:
    def __init__(self) -> None:
        with open('resources/source.py', 'r', encoding='utf-8') as f: self.source = f.readlines(); self.log('Loaded source.py', 0)
        with open('resources/assets/compiler_configuration.json', 'r', encoding='utf-8') as f: self.compiler_configuration = json.load(f); self.log('Loaded compiler configuration', 0)
        self.dataframe = self.parse_source(self.source)
        self.parse_parameters()
        self.clean_imports()
        self.assemble_source()
        
    def parse_source(self, source_code) -> list:
        dataframe = {'imports': {'intendation': 0, 'line': 0, 'code': []}}
        for line_index, line in enumerate(source_code):
            line = line.strip()
            if line[:2] == '#!':
                dataframe[line[2:].split('.')[0]] = {'intendation': int(line.split('=')[1]), 'line': line_index, 'code': []}
                self.log(f'Found parameter "{line[2:].split(".")[0]}" at line {line_index}.', 0)
        if len(dataframe) == 1: self.log('No parameters found. This should not occur. Contact PySilon development staff for help or try to re-clone the repository.', 2)
        else: self.log(f'Successfully parsed source code. Found {len(dataframe)} parameters.', 0)
        return dataframe
    
    def parse_parameters(self) -> None:
        for parameter in self.dataframe.keys():
            for entry in self.compiler_configuration[parameter]:
                attention = False
                with open(entry[0], 'r', encoding='utf-8') as f:
                    parameter_source = f.readlines()
                for line in parameter_source:
                    if attention and line[:3] != '#</': self.dataframe[parameter]['code'].append(line)
                    if line.replace('\n', '') == f'#<{entry[1]}>': attention = True; self.log(f'Parsed entry "{entry[1]}" from "{entry[0]}".', 0)
                    elif line.replace('\n', '') == f'#</{entry[1]}>': break
            self.log(f'Parsed parameter "{parameter}"', 0)

    def clean_imports(self) -> None:
        raw_imports, imports = self.dataframe['imports']['code'], []
        for line in raw_imports:
            if line not in imports: imports.append(line)
        self.dataframe['imports']['code'] = sorted(imports, key=len)[::-1]
        self.log('Removed duplicated imports', 0)

    def assemble_source(self) -> None:
        pass

    def log(self, message, type) -> None:
        if type == 0: prefix = 'INFO'
        elif type == 1: prefix = 'WARNING'
        elif type == 2: prefix = 'ERROR'
        print(f"[{prefix}][{datetime.datetime.now().strftime('%d.%m.%y-%H:%M:%S')}] {message}")
        if type == 2: exit()

os.chdir('.')
pysilon_Compiler()

