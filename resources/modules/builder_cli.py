import json

class CLI_Builder:
    def __init__(self):
        print(
f'''
PySilon Malware Builder
Version: 4.0

Type "help" for list of commands.
''')
        self.get_command()

    def get_command(self):
        self.issued_command = input('.').split()
        match self.issued_command[0]:
            case 'set':
                self.issued_command[1] = self.issued_command[1].split('"')
                print(f'    Command: {self.issued_command[0]}\n    Setting: {self.issued_command[1]}\n')


CLI_Builder()