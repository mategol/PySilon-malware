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
        self.issued_command = input('.')
        match self.issued_command.split()[0]:
            case 'set':
                possible_settings = []
                for argument in self.issued_command.split()[1:]:
                    if argument.count('-') == 2 and argument.count('=') == 1 and argument.count('"') == 2:
                        possible_settings.append(argument)
                    else:
                        self.error('Syntax', 'set')
                        possible_settings = []
                        self.get_command()
                for setting in possible_settings:
                    setting = setting.split('=')
                    self.command_set(setting[0][2:], setting[1][1:-1])

    def command_set(self, setting, value):
        print(setting, value)

    def error(self, type, help):
        print('Error')
                
                


CLI_Builder()