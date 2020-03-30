import re

white_space_patt = re.compile('\s{2,}')
def __pre_regex(text: str):
    removed_character = ['-', '/', '\\', ',']
    for rc in removed_character:
        text = text.replace(rc, ' ')
    text = re.sub(white_space_patt, ' ', text)
    return text

test = [
    '12/13/1967',
    'jan, 12 - 1487'
]
for t in test:
    print(__pre_regex(t))