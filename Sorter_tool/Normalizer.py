from re import sub
from pathlib import Path
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()    

def normalize(string: str):
    '''
    Recieve string. If string is a file name - remove the suffix.
    Split string to list. 
    For each char of list applies the following processing:
    if chat is a cyrillic symbol - transliterate it to latinic symbol \ 's
    if char is a digit - skips it
    if char is any else - replace it by _
    Return reprocessed string. If string is a file name - add the unprocessed suffix
    '''
    suffix = Path(string).suffix
    if not suffix:
        string_list = list(string)
    else:
       string_list = list(string[:string.rfind(suffix)])
    for ch, num in zip(string_list, range(len(string_list))):
        if ch in CYRILLIC_SYMBOLS or ch in CYRILLIC_SYMBOLS.upper():
            string_list[num] = ch.translate(TRANS)
        elif ch.isdigit():
            continue
        elif ch.isalpha():
            if not ('a' <= ch <= 'z' or 'A' <= ch <= "Z"):
                string_list[num] = ch.casefold()
        else:
            string_list[num] = '_'  
                
    return ''.join(string_list) + suffix
    

def normalize_testing(result):
    '''Testing for normalize func'''
    try:
        for ch in result:
            if ch in CYRILLIC_SYMBOLS:
                return 'Test failed'
        else:
            return 'Test passed!'
    except TypeError:
        return 'Test failed'
            
if __name__ == '__main__':
    test_cases = ('Привет Мир!', 'HE;;llo', '.', '123', 'Schloß', '123))###!@(llo', 'Hello.org', 'heel.re')
    for testing in test_cases:
        print(f'{testing=}')
        result = normalize(testing)
        print(f'{result=}\n{normalize_testing(result)}\n' + '-'*20)