import os
import requests
import time
data_file = '../data/png.m3u8'
output_folder = '../../Temp'


def handle_png(png_link, file_index, is_png=True):
    # Download png
    retry = 5
    while retry > 0:
        try:
            print('Download: {}'.format(png_link))
            data = requests.get(png_link, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 OPR/86.0.4363.59',
                'Accept-Language': 'en-US,en;q=0.9',
            })
            if not data.status_code == 200:
                raise Exception
            if is_png:
                content = data.content[8:]
            else:
                content = data.content
            file = open('{}/{}.html'.format(output_folder, file_index), 'wb')
            file.write(content)
            return
        except Exception as e:
            print(e)
            retry -= 1
            time.sleep(2)
    print('Invalid download' + png_link)


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
        handle_png(line.strip(), file_index, False)
        lines[i] = './{}.html\n'.format(file_index)
        output_cmd.append('file {}\n'.format(lines[i]))
        file_index += 1
        # time.sleep(2)
print('ffmpeg -f concat -safe 0 -i ../Temp/out.txt -c copy ../output.mp4')
file = open('{}/out.txt'.format(output_folder), 'w')
file.writelines(output_cmd)
if __name__ == '__main__':
    print('Hello')
