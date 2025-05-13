import os
from pathlib import Path
from datetime import datetime

WORK_DIR = Path('E:\\Games\\Wuthering Waves ModsLaunchers\\XXMI Launcher\\WWMI\\Mods\\Character Skins')
BASE_CHARACTER_LIST = []


class Character:
    name = ''
    hash_codes = []

    def __init__(self, name, hash_code):
        self.name = name
        self.hash_codes = [hash_code]


def create_character_bases():
    BASE_CHARACTER_LIST.append(Character('Aalto', '93bbbdc0'))
    BASE_CHARACTER_LIST.append(Character('Baizhi', '3cb91e7f'))
    BASE_CHARACTER_LIST.append(Character('Brant', '5943f99a'))
    BASE_CHARACTER_LIST.append(Character('Calcharo', '1408f42b'))
    BASE_CHARACTER_LIST.append(Character('Camellya', '7748c1d8'))
    BASE_CHARACTER_LIST.append(Character('Cantarella', '5432f939'))
    BASE_CHARACTER_LIST.append(Character('Carlotta', '4ba716ae'))
    BASE_CHARACTER_LIST.append(Character('Changli', 'd14bed8b'))
    BASE_CHARACTER_LIST.append(Character('Chixia', '1606ae41'))
    BASE_CHARACTER_LIST.append(Character('Danjin', '6aefd9b3'))
    BASE_CHARACTER_LIST.append(Character('Encore', '592add5c'))
    BASE_CHARACTER_LIST.append(Character('Jianxin', '9b60ec42'))
    BASE_CHARACTER_LIST.append(Character('Jinhsi', '243b7e59'))
    BASE_CHARACTER_LIST.append(Character('Jiyan', '31b50c1d'))
    BASE_CHARACTER_LIST.append(Character('Lingyang', '9925d10e'))
    BASE_CHARACTER_LIST.append(Character('Lumi', 'b441b9f6'))
    BASE_CHARACTER_LIST.append(Character('Mortefi', '7b29fedf'))
    BASE_CHARACTER_LIST.append(Character('Phoebe', '026f7616'))
    BASE_CHARACTER_LIST.append(Character('Roccia', '8d97c1bd'))
    BASE_CHARACTER_LIST.append(Character('Rover_Female', '3533a957'))
    BASE_CHARACTER_LIST.append(Character('Rover_Male', 'b22dacf9'))
    BASE_CHARACTER_LIST.append(Character('Sanhua', '33e4890f'))
    BASE_CHARACTER_LIST.append(Character('Shorekeeper', '0266ab77'))
    BASE_CHARACTER_LIST.append(Character('Taoqi', 'e2685889'))
    BASE_CHARACTER_LIST.append(Character('Verina', '82aa82e1'))
    BASE_CHARACTER_LIST.append(Character('Xiangli_Yao', 'ed536543'))
    BASE_CHARACTER_LIST.append(Character('Yangyang', 'bb5dfeaf'))
    BASE_CHARACTER_LIST.append(Character('Yinlin', '42702199'))
    BASE_CHARACTER_LIST.append(Character('Youhu', '03eea2d0'))
    BASE_CHARACTER_LIST.append(Character('Yuanwu', '540c83c5'))
    BASE_CHARACTER_LIST.append(Character('Zani', '07352718'))
    BASE_CHARACTER_LIST.append(Character('Zhezhi', 'b4525ff8'))


## Вспомогательные функции

# Логическая операция И (пересечение)
def intersection(arr1, arr2):
    return list(set(arr1) & set(arr2)) or None


# Логическая операция ИЛИ (объединение)
def union(arr1, arr2):
    return list(set(arr1) | set(arr2))


# Найти персонажа по имени
def character_by_name(name):
    return next((character for character in BASE_CHARACTER_LIST if character.name == name), None)


# Все папки в директории
def directory_list(listen_directory):
    return [d.name for d in Path(listen_directory).iterdir() if d.is_dir()]


## Основной функционал

# Получение всех хэш кодов из .ini файла
def get_character_hashes(path_to_ini_file):
    with open(path_to_ini_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    hashes = []
    for index in range(len(lines)):
        if lines[index].strip().startswith('[TextureOverrideComponent'):
            hashes.append(lines[index + 1].split('=')[1].strip())

        index += 1
    return hashes


# Поиск персонажа по совпаднению большинства хэшей в .ini файле
def find_character(hash_codes):
    matched_index = -1
    matched_count = 0

    for index in range(len(BASE_CHARACTER_LIST)):
        duplicates = intersection(BASE_CHARACTER_LIST[index].hash_codes, hash_codes)
        if duplicates and matched_count < len(duplicates):
            matched_count = len(duplicates)
            matched_index = index
        index += 1

    if matched_index != -1:
        updated_hashes = union(BASE_CHARACTER_LIST[matched_index].hash_codes, hash_codes)
        BASE_CHARACTER_LIST[matched_index].hash_codes = updated_hashes
        return BASE_CHARACTER_LIST[matched_index]

    return None


# Распределение модов по папкам персонажей
def mod_distribution_by_character():
    print('----------[ Distribution ]----------')
    for files in WORK_DIR.rglob('*.ini'):
        if os.path.basename(files) != 'SkinSwapFile.ini':
            current_character_hash_codes = get_character_hashes(files)
            current_character = find_character(current_character_hash_codes)

            if current_character:
                temp_path = files

                while WORK_DIR != temp_path.parent:
                    if temp_path.parent.name == current_character.name:
                        break
                    temp_path = temp_path.parent

                destination = WORK_DIR / current_character.name / temp_path.name
                if destination == temp_path:
                    print(f'{temp_path.name} --> Nothing to change')
                else:
                    os.renames(temp_path, destination)
                    print(f'Moving\nFrom\t{temp_path} \nTo\t\t{destination}')


# Добавление папкам со скином ID в названии
def mod_mapper():
    print('------------[ Remapping ]------------')
    for character in os.listdir(WORK_DIR):
        if character.endswith('.ini'):
            break

        character_mods = directory_list(WORK_DIR / character)

        if character_by_name(character):
            print(f'Character: {character}')
            for index in range(len(character_mods)):
                tmp_name = character_mods[index]
                if character_mods[index].strip().startswith('ID='):
                    tmp_name = character_mods[index].split('_')[1].strip()

                if character_mods[index] != f'ID={index + 1}_{tmp_name}':
                    os.rename(WORK_DIR / character / character_mods[index],
                              WORK_DIR / character / f'ID={index + 1}_{tmp_name}')
                    print(f'{character_mods[index]} --> ID={index + 1}_{tmp_name}')
                else:
                    print(f'{character_mods[index]} --> Nothing to change')
                index += 1


# Создание SwapFile для каждого персонажа
def mod_swap_ini():
    print('--------[ Create Swap Files ]--------')
    for character in os.listdir(WORK_DIR):
        if character.endswith('.ini'):
            break

        current_character = character_by_name(character)
        if current_character:
            with open('SkinSwapTempFile', 'r', encoding='utf-8') as file:
                content = file.read()

            print(f'Create/Change SwapFile for: {current_character.name}')
            mod_count = len(directory_list(WORK_DIR / current_character.name))

            character_name = current_character.name
            character_hash = '\n'.join(f'hash = {i}' for i in current_character.hash_codes)
            skins_swap_var = ', '.join(f'{i}' for i in range(mod_count + 1))

            content = content.replace('#{character_name}', character_name)
            content = content.replace('#{character_hash}', character_hash)
            content = content.replace('#{skins_count}', skins_swap_var)

            with open(WORK_DIR / character / 'SkinSwapFile.ini', 'w', encoding='utf-8') as file:
                file.write(content)


# Основная логика изменения mod.ini
def change_logic(lines, character, number):
    out = []
    tab_flag = False
    hash_flag = False

    index = 0
    while index < len(lines):
        if lines[index].strip().startswith('hash'):
            out.append(lines[index])
            hash_flag = True
            index += 1

            if lines[index].strip().startswith('match_priority'):
                index += 1
            out.append('match_priority = 1\n')

            tab_flag = True
            if lines[index].strip().startswith(f'if $\\{character.name}\\'):
                tab_flag = False
                index += 1
            out.append(f'if $\\{character.name}\\SkinSwapVar\\SkinSwapVar=={number}\n')

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

    return out


# Изменение файлов .ini
def mod_ini_change():
    print('--------[ Changing ini files ]-------')
    for character_name in os.listdir(WORK_DIR):
        if character_name.endswith('.ini'):
            break

        mod_list = directory_list(WORK_DIR / character_name)
        if character_by_name(character_name):
            print(f'Character: {character_name}')
            number = 0
            for mod in mod_list:
                number += 1
                print(f'Change ini files for mod {mod}')

                directory = WORK_DIR / character_name / mod
                for ini_file in directory.rglob('*.ini'):
                    with open(directory / ini_file, 'r', encoding='utf-8') as file:
                        lines = file.readlines()

                    with open(f'{directory / ini_file} {datetime.now().strftime('%d-%m-%Y %H-%M-%S')}_backup', 'w',
                              encoding='utf-8') as file:
                        file.writelines(lines)

                    out = change_logic(lines, character_by_name(character_name), number)

                    with open(directory / ini_file, 'w', encoding='utf-8') as file:
                        file.writelines(out)


### ВЫЗОВ ФУНКЦИЙ
create_character_bases()
mod_distribution_by_character()
mod_mapper()
mod_swap_ini()
mod_ini_change()
