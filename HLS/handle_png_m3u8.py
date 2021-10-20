import os
import requests
data_file = '../data/png.m3u8'
output_folder = '../data/out'


def handle_png(png_link, file_index):
    # Download png
    print('Download: {}'.format(png_link))
    data = requests.get(png_link, timeout=10)
    content = data.content[8:]
    file = open('{}/{}.html'.format(output_folder, file_index), 'wb')
    file.write(content)


try:
    os.mkdir(output_folder)
except OSError as error:
    print(error)

file = open(data_file, 'r')
lines = file.readlines()
file_index = 0
output_cmd = []
for i, line in enumerate(lines):
    if line.startswith('http'):
        # handle_png(line.strip(), file_index)
        lines[i] = './{}.html\n'.format(file_index)
        output_cmd.append('file {}\n'.format(lines[i]))
        file_index += 1
print('ffmpeg -f concat -safe 0 -i out.txt -c copy output.mp4')
# file = open('{}/out.m3u8'.format(output_folder), 'w')
# file.writelines
file = open('{}/out.txt'.format(output_folder), 'w')
file.writelines(output_cmd)
if __name__ == '__main__':
    print('Hello')
