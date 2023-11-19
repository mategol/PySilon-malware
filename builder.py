features = {
     "screenshot": "screenshot.py"
}

with open("source.py", 'r') as file:
        for line_num, line in enumerate(file):
            if '# [pysilon] commands' in line:
                line_num

for feature, feature_path in features.items():
    with open(feature_path, "r") as sc:
        screenshot_contents = sc.read()
     
with open("source_prepared.py", "w") as write_source:
    with open("source.py", "r") as source_file:
        for current_line_num, current_line in enumerate(source_file):
            write_source.write(current_line)
            if current_line_num == line_num:
                write_source.write('\n' + screenshot_contents + '\n')
        write_source.write("\nclient.run(bot_token)")