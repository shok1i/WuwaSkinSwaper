import os

WORK_DIR = 'C:\\Users\\shilo\\Downloads\\Проектирование информационных систем'


def directory_list(listen_directory):
    return [directory.name for directory in os.scandir(listen_directory) if directory.is_dir()]


def mod_mapper():
    character_mod_list = directory_list(WORK_DIR)

    index = 0
    for character_mod in character_mod_list:
        index += 1
        if str(character_mod).strip().startswith('ID='):
            character_mod = str(character_mod).split('_')[1]

        os.renames(os.path.join(WORK_DIR, character_mod_list[index - 1]),
                   os.path.join(WORK_DIR, f'ID={index}_{character_mod}'))


def mod_swap_ini():
    mod_count = len(directory_list(WORK_DIR))

    character_name = 'CharacterName'
    character_hash = '00000000'
    skins_swap_var = ', '.join(f'{i}' for i in range(mod_count + 1))


def get_all_character_hashes():
    with open('mod.ini', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    hashes = []
    for line in lines:
        if line.strip().startswith('hash'):
            hash = line.split('=')[1].strip()
            if hash not in hashes and hash != 'f02baf77':
                hashes.append(hash)

    return hashes


def duplicates_from_two_arr(arr1, arr2):
    duplicates = set(arr1) & set(arr2)
    if len(duplicates):
        return duplicates
    return None


def mod_ini_change():
    with open('mod.ini', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    out = []
    index = 0
    tab_flag = False
    hash_flag = False
    while index < len(lines):
        if lines[index].strip().startswith('hash'):
            out.append(lines[index])
            index += 1
            hash_flag = True

            if lines[index].strip().startswith('match_priority'):
                index += 1
            out.append('match_priority = 1\n')

            tab_flag = True
            if lines[index].strip().startswith('if $SkinSwapVar'):
                tab_flag = False
                index += 1
            out.append('if $SkinSwapVar/CharacterName == 1\n')

        if lines[index] != '\n' and not lines[index].strip().startswith(';'):
            if tab_flag:
                out.append('\t' + lines[index])
            else:
                out.append(lines[index])

        index += 1
        if index < len(lines) and lines[index].strip().startswith('['):
            if hash_flag and tab_flag:
                out.append('endif\n')
                hash_flag = False
            tab_flag = False
            out.append('\n')

    with open('mod_test.ini', 'w', encoding='utf-8') as file:
        file.writelines(out)


mod_ini_change()
