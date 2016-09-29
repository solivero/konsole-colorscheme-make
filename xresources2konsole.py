from sys import argv
import re


hex_part = '#(\w{6})'
color_num_patt = re.compile(r'[a-z]+([0-9]+): ' + hex_part)

konsole_file = open(argv[2], 'r')
konsole_file_data = konsole_file.read()
konsole_file.close()
xterm_file = open(argv[1], 'r')
xterm_file_data = xterm_file.read()
xterm_file.close()

def main():
        background_match = re.search(r'background: ' + hex_part, xterm_file_data)
        background_rgb = hex_to_rgb(background_match.group(1))
        foreground_match = re.search(r'foreground: ' + hex_part, xterm_file_data)
        foreground_rgb = hex_to_rgb(foreground_match.group(1))
        k_background_section = "Background"
        k_foreground_section = "Foreground"
        replace(k_background_section, background_rgb)
        replace(k_background_section + "Intense", background_rgb)
        replace(k_foreground_section, foreground_rgb)
        replace(k_foreground_section + "Intense", foreground_rgb)
        x_color_matches = re.findall(color_num_patt, xterm_file_data)

        #for line in konsole_file.readlines():
        #    if line.startswith("[Background"):
        #        is_background = True
        #        continue
        #    if line.startswith("[Foreground"):
        #        is_foreground = True
        #        continue
        for x_color_match in x_color_matches:
            print x_color_match
            color_num = int(x_color_match[0])
            x_rgb = hex_to_rgb(x_color_match[1])
            section_name = ""
            if color_num < 8:
                section_name = str(color_num)
            else:
                section_name = str(color_num - 8) + "Intense"
            replace(section_name, x_rgb)
        new_file = open(argv[2], 'w')
        new_file.write(konsole_file_data)
        new_file.close()

def replace(section_name, new_color):
    global konsole_file_data
    pattern = section_name + r"\]\nColor=(\d+,\d+,\d+)"
    match = re.search(pattern, konsole_file_data)
    found_text = match.group(0)
    old_rgb = match.group(1)
    konsole_file_data = re.sub(
        pattern,
        found_text.replace(old_rgb, new_color),
        konsole_file_data,
    )

def hex_to_rgb(hex_str):
    base_ten = []
    for i in range(len(hex_str)/2):
        two_digits = hex_str[i*2:(i+1)*2]
        base_ten.append(str(int(two_digits, base=16)))
    return ",".join(base_ten)





if __name__ == '__main__':
    main()
