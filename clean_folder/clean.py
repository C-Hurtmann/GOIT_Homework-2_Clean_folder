import sys
from normalize import normalize
from pathlib import Path
from shutil import move, rmtree, unpack_archive
from os import rename, makedirs, listdir, remove
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

suffix_navigator = {'изображения':('JPEG', 'PNG', 'JPG', 'SVG')
                    , 'видео файлы':('AVI', 'MP4', 'MOV', 'MKV')
                    , 'документы':('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
                    , 'музыка':('MP3', 'OGG', 'WAV', 'AMR')
                    , 'архивы':('ZIP', 'GZ', 'TAR')}


def file_checking(file):
    '''
    Recieve file name. 
    Searching file suffix in suffix_navigator dict values. 
    Return key corresponding to the value. If haven't matched - return 'Unknown extentions'.
    '''
    file_suffix = (Path(file).suffix)[1:].upper()
    for key, values in suffix_navigator.items():
        if file_suffix in values:
            return key
    return 'неизвестные расширения'


def main():
    try:
        folder_name = sys.argv[1]
    except IndexError:
        folder_name = input('Введите имя папки: ')
    path = Path(folder_name)
    revision_list = []
    
    # revision
    
    def revision(folder):
        '''
        Recieve folder name. 
        Collects file path and file name of all files in any depth. 
        Also run file_checking func for file name. 
        Writes file path, file_checking func value and file name to the revision list.
        '''
        for item in folder.iterdir():
            if item.is_file():
                file_name = item.name
                directory = file_checking(file_name)
                revision_list.append((item, directory, file_name))
            else:
                revision(item)
                
    revision(path)
    
    # sorting
    
    for old_path, directory, file_name in revision_list:
        makedirs(f'{path}\{directory}', exist_ok=True)
        move(old_path, f'{path}\{directory}\{file_name}') 
        rename(f'{path}\{directory}\{file_name}', f'{path}\{directory}\{normalize(file_name)}')
    for item in path.iterdir():
        if len(listdir(item)) == 0:
            rmtree(item)
            
    # archive unpacking
    
    try:
        archive_folder = Path(f'{folder_name}\архивы')
        for archive in archive_folder.iterdir():
            makedirs(f'{archive.parent}\{archive.stem}')
            unpacked_archive_folder = Path(f'{archive.parent}\{archive.stem}')
            unpack_archive(archive, unpacked_archive_folder)
            remove(archive)
            for file in unpacked_archive_folder.iterdir():
                rename(file, f'{file.parent}\{normalize(file.name)}')
                
                
    # completion report                
                
    except FileNotFoundError:    
        print('Сортировка папки успешно завершена :-)\n', '-' * 50)
    else:
        print('Сортировка папки успешно завершена :-)\n', '-' * 50)
    finally:
        what_in_the_folder_report = {'изображения':[]
                    , 'видео файлы':[]
                    , 'документы':[]
                    , 'музыка':[]
                    , 'архивы':[]
                    , 'неизвестные расширения':[]}
        all_suffixes_in_folder_report = set()
        unknown_suffixes_if_folder_report = set()
        for old_path, directory, file_name in revision_list:
            what_in_the_folder_report.get(directory).append(file_name)
            if directory == 'неизвестные расширения':
                unknown_suffixes_if_folder_report.add(Path(file_name).suffix)
            else:
                all_suffixes_in_folder_report.add(Path(file_name).suffix)
    # print first report
    print('Таблица с содержимым новосозданных папок:\n', '|{:^25}|{:^24}|\n'.format('Папка', 'Файл'), '-' * 50)
    for k, v in what_in_the_folder_report.items():
        for item in v:
            print(f'{k:25}|{str(item):<20}\n', '-' * 50)
    # print second report
    print('Перечень всех известных скрипту расширений, которые встречаются в целевой папке:\n', all_suffixes_in_folder_report)
    # print third report
    print('Перечень всех расширений, которые скрипту неизвестны:\n', unknown_suffixes_if_folder_report)

            
if __name__ == '__main__':
    main()