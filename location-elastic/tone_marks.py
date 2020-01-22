# TODO: Reconstruct data structure, plan B: encode to byte
import pickle

DOUBLE_TM = [
    'ằ', 'ắ', 'ẳ', 'ẵ', 'ặ',
    'Ằ', 'Ắ', 'Ẳ', 'Ẵ', 'Ặ',
    'ầ', 'ấ', 'ẩ', 'ẫ', 'ậ',
    'Ầ', 'Ấ', 'Ẩ', 'Ẫ', 'Ậ',
    'ề', 'ế', 'ể', 'ễ', 'ệ',
    'Ề', 'Ế', 'Ể', 'Ễ', 'Ệ',
    'ồ', 'ố', 'ổ', 'ỗ', 'ộ',
    'Ồ', 'Ố', 'Ổ', 'Ỗ', 'Ộ',
    'ờ', 'ớ', 'ở', 'ỡ', 'ợ',
    'Ờ', 'Ớ', 'Ở', 'Ỡ', 'Ợ',
    'ừ', 'ứ', 'ử', 'ữ', 'ự',
    'Ừ', 'Ứ', 'Ử', 'Ữ', 'Ự',
]

SINGLE_TM = [
    'ă', 'Ă', 'â', 'Â', 'ê', 'Ê', 'ô', 'Ô', 'ơ', 'Ơ', 'ư', 'Ư', 'đ', 'Đ',
    'à', 'á', 'ả', 'ã', 'ạ', 'À', 'Á', 'Ả', 'Ã', 'Ạ',
    'è', 'é', 'ẻ', 'ẽ', 'ẹ', 'È', 'É', 'Ẻ', 'Ẽ', 'Ẹ',
    'ò', 'ó', 'ỏ', 'õ', 'ọ', 'Ò', 'Ó', 'Ỏ', 'Õ', 'Ọ',
    'ù', 'ú', 'ủ', 'ũ', 'ụ', 'Ù', 'Ú', 'Ủ', 'Ũ', 'Ụ',
    'ì', 'í', 'ỉ', 'ĩ', 'ị', 'Ì', 'Í', 'Ỉ', 'Ĩ', 'Ị',
    'ỳ', 'ý', 'ỷ', 'ỹ', 'ỵ', 'Ỳ', 'Ý', 'Ỷ', 'Ỹ', 'Ỵ'
]

TM = DOUBLE_TM + SINGLE_TM

NON_TM = [
    'a', 'A', 'a', 'A', 'e', 'E', 'o', 'O', 'o', 'O', 'u', 'U', 'd', 'D', 'i', 'I', 'y', 'Y'
]

# ă, â, ơ, đ, à, á, ả, ã, ạ
ENCODE_CHARACTER = [
    '@', '^', '*', '_','&', '$', '?', '~', '!'
]

REMOVED_TM = pickle.load(open('non_tm.p', 'rb'))
ENCODED_TM = pickle.load(open('encode_tm.p', 'rb'))
DECODED_TM = dict((v,k) for k,v in ENCODED_TM.items())


def __remove_tm_character(character: str):
    if character not in TM:
        return character
    idx = TM.index(character)
    if idx < 60: # DOUBLE_TM
        return NON_TM[idx // 5]
    if idx < 74: # SINGLE_TM ROW 1
        return NON_TM[idx - 60]
    if idx < 84: # SINGLE_TM ROW 2
        return NON_TM[(idx - 74) // 5]
    if idx < 94: # SINGLE_TM ROW 3
        return NON_TM[(idx - 84) // 5 + 4]
    if idx < 104: # SINGLE_TM ROW 4
        return NON_TM[(idx - 94) // 5 + 6]
    if idx < 114: # SINGLE_TM ROW 5
        return NON_TM[(idx - 104) // 5 + 10]
    return NON_TM[(idx - 114) // 5 + 14 ] # SINGLE_TM ROW 5


def __encode_tm_character(character: str):
    if character not in TM:
        return character
    idx = TM.index(character)
    if idx < 20:
        return __remove_tm_character(character) + ENCODE_CHARACTER[idx // 10] + ENCODE_CHARACTER[idx % 5 + 4]
    if idx < 60:
        return __remove_tm_character(character) + ENCODE_CHARACTER[(idx - 20) // 20 + 1] + ENCODE_CHARACTER[idx % 5 + 4]
    if idx < 62:
        return __remove_tm_character(character) + ENCODE_CHARACTER[0]
    if idx < 68:
        return __remove_tm_character(character) + ENCODE_CHARACTER[1]
    if idx < 72:
        return __remove_tm_character(character) + ENCODE_CHARACTER[2]
    if idx < 74:
        return __remove_tm_character(character) + ENCODE_CHARACTER[3]
    return __remove_tm_character(character) + ENCODE_CHARACTER[(idx - 74) % 5 + 4]


def remove_tm_character(character:str):
    if character not in REMOVED_TM:
        return character
    return REMOVED_TM[character]


def encode_tm_character(character:str):
    if character not in ENCODED_TM:
        return character
    return ENCODED_TM[character]


def decode_tm_character(character:str):
    if character not in DECODED_TM:
        return character
    return DECODED_TM[character]


def remove_tm_string(string:str):
    for character in string:
        string = string.replace(character, remove_tm_character(character))
    return string


def encode_tm_string(string:str):
    for character in ENCODE_CHARACTER:
        string = string.replace(character, '')
    for character in string:
        string = string.replace(character, encode_tm_character(character))
    return string


def decode_tm_string(string:str):
    for character in DECODED_TM.keys():
        string = string.replace(character, decode_tm_character(character))
    return string


if __name__ == '__main__':
    string = 'Phnôm Pênh'
    print(remove_tm_string(string))
    print(encode_tm_string(string))
    print(decode_tm_string(encode_tm_string(string)))
    print()
