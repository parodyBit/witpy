from pathlib import Path
import re



def loads(path):
    file_path = Path(path)

    raw_toml = open(file_path, "r+")
    lines = raw_toml.read().splitlines()
    toml = {}
    current_section = None
    current_item = None
    tmp_list = None
    begin_list, end_list = False, False
    for line in lines:
        if current_section is None:
            pass
        else:
            pass
        if begin_list:
            if line.strip() is ']':
                end_list = True
            else:
                if line.strip().startswith('"'):
                    tmp_list.append(re.findall('"([^"]*)"', line.rstrip())[0])
                else:
                    tmp_list.append(line.strip())

            if end_list:
                begin_list = False
                end_list = False
                toml[current_section][current_item] = tmp_list
                tmp_list = None

        # Check to see if we have a new section
        if line.startswith('#'):
            pass
        elif line.startswith('['):
            current_section = line[1:].rstrip(']')
            toml[current_section] = {}
            #print(line)
        elif '=' in line:

            current_item = line.split('=')[0].strip()
            current_value = line.split('=')[1].strip()
            toml[current_section][current_item] = current_value
            # if the value is a list; make a list and push
            if current_value.startswith('['):
                begin_list = True
                tmp_list = []
                toml[current_section][current_item] = []
            else:
                if current_value.startswith('"'):
                    current_value = re.findall('"([^"]*)"', current_value)[0]
                toml[current_section][current_item] = current_value
    return toml