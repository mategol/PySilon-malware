import json
import os

os.chdir('resources')
with open('source.py', 'r', encoding='utf-8') as f: source = f.readlines()
with open('assets/compiler_configuration.json', 'r', encoding='utf-8') as f: compiler_configuration = json.load(f)
print(compiler_configuration)

