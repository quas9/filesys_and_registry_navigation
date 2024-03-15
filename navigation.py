import argparse
import os
import shutil
import winreg
#file sys

def create_file(file):
    if os.path.exists(file) == False:
        with open(file, "x") as f:
            print(f"Файл {file} создан")
    else:
        print("Файл с таким названием уже существует.")

#create_file("C:\Users\79312\Desktop\асвт\28.txt")
def delete_file(file):
    if os.path.exists(file):
        os.remove(file)
        print(f'Файл {file} успешно удален')
    else:
        print("Файл с таким названием не существует.")  

#delete_file('test.txt')
def write_file(file, string):
    if os.path.exists(file):
        with open(file, "w") as f:
            f.write(string)
            print("Запись добавлена")
    else:
        print('Такого файла не существует.')

#write_file('e2.txt', 'magamag222am')
def read_file(file): 
    if os.path.exists(file):
        with open(file, "r") as f:
            print(f"Текст из {file} : ", f.read())
    else:
        print('Такого файла не существует.')

def copy_file(file, directory):
    if os.path.exists(file):
        with open(file, "r") as f:
            shutil.copy2(file, directory)
            print('Файл был скопирован в : ', directory)
    else:
        print('Такого файла не существует.')

def rename_file(file, new_file):
    if os.path.exists(file):
        os.rename(file, new_file)
        print('Файл был переименован, новое название : ',new_file )
    else:
        print('Такого файла не существует.')

def create_registry_key(root_key_str, key_path):
    root_keys = {
        'winreg.HKEY_CLASSES_ROOT': winreg.HKEY_CLASSES_ROOT,
        'winreg.HKEY_CURRENT_USER': winreg.HKEY_CURRENT_USER,
        'winreg.HKEY_LOCAL_MACHINE': winreg.HKEY_LOCAL_MACHINE,
        'winreg.HKEY_USERS': winreg.HKEY_USERS,
        'winreg.HKEY_CURRENT_CONFIG': winreg.HKEY_CURRENT_CONFIG
    }

    if root_key_str in root_keys:
        root_key = root_keys[root_key_str]
        try:
            winreg.CreateKey(root_key, key_path)
            print (f"Ключ по адресу {key_path} был создан")
            return True
        except Exception as e:
            print(f"Ошибка при создании ключа: {e}")
            return False
    else:
        print("Недопустимый корневой ключ реестра.")
        return False

def delete_registry_key(root_key_str, key_path):
    root_keys = {
        'winreg.HKEY_CLASSES_ROOT': winreg.HKEY_CLASSES_ROOT,
        'winreg.HKEY_CURRENT_USER': winreg.HKEY_CURRENT_USER,
        'winreg.HKEY_LOCAL_MACHINE': winreg.HKEY_LOCAL_MACHINE,
        'winreg.HKEY_USERS': winreg.HKEY_USERS,
        'winreg.HKEY_CURRENT_CONFIG': winreg.HKEY_CURRENT_CONFIG
    }

    if root_key_str in root_keys:
        root_key = root_keys[root_key_str]
        try:
            winreg.DeleteKey(root_key, key_path)
            print(f"Ключ по адресу {key_path} был успешно удален")
            return True
        except Exception as e:
            print(f"Ошибка при удалении ключа: {e}")
            return False
    else:
        print("Недопустимый корневой ключ реестра.")
        return False
    
import winreg
import winreg

def write_registry_value(root_key_str, key_path, key_name, key_value):
    root_keys = {
        'winreg.HKEY_CLASSES_ROOT': winreg.HKEY_CLASSES_ROOT,
        'winreg.HKEY_CURRENT_USER': winreg.HKEY_CURRENT_USER,
        'winreg.HKEY_LOCAL_MACHINE': winreg.HKEY_LOCAL_MACHINE,
        'winreg.HKEY_USERS': winreg.HKEY_USERS,
        'winreg.HKEY_CURRENT_CONFIG': winreg.HKEY_CURRENT_CONFIG
    }

    if root_key_str in root_keys:
        root_key = root_keys[root_key_str]
        try:
            key = winreg.OpenKey(root_key, key_path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, key_value)   
            print(f"Запись {key_value} была добавлена {'в ключ ' + key_path if key_path else 'в корневой ключ реестра'} под именем {key_name}")
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Ошибка при записи значения в {'ключ ' + key_path if key_path else 'корневой ключ реестра'}: {e}")
            return False
    else:
        print("Недопустимый корневой ключ реестра.")
        return False



def menu():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(usage=argparse.SUPPRESS)

     #file sys
    parser.add_argument('-cr', '--create', metavar='',
                        help='Создание файла (название файла)')
    parser.add_argument('-del', '--delete', metavar='',
                        help='Удаление файла (название файла)')
    parser.add_argument('-w', '--write', metavar='',nargs = 2,
                        help='Запись в файл (название файла, передаваемое значение)')
    parser.add_argument('-r', '--read', metavar='',
                         help='Чтение файла (название файла)')
    parser.add_argument('-cp', '--copy', metavar='', nargs = 2,
                        help='Копирование файла в другую директорию (название файла, директория)')
    parser.add_argument('-rn', '--rename', metavar='', nargs = 2,
                        help='Изменение имена файла (название файла, новое название файла)')

    #registry
    
    parser.add_argument('-kc', '--key_create', metavar='', nargs = 2,
                        help='Создание ключа (название реестра (winreg.*), путь к ключу)')
    parser.add_argument('-kd', '--key_delete', metavar='', nargs = 2,
                        help='Удаление ключа (название реестра (winreg.*), путь к ключу)')
    parser.add_argument('-kv', '--key_value', metavar='', nargs = 4,
                        help='Добавление значения ключу (название реестра(winreg.*), путь название ключа, значение ключа)')

    get_args = parser.parse_args()

    if get_args.create:
        create_file(get_args.create)
    elif get_args.delete:
        delete_file(get_args.delete)
    elif get_args.write:
        write_file(get_args.write[0], get_args.write[1])
    elif get_args.read:
        read_file(get_args.read)
    elif get_args.copy:
        copy_file(get_args.copy[0], get_args.copy[1])
    elif get_args.rename:
        rename_file(get_args.rename[0], get_args.rename[1])
    elif get_args.key_create:
        create_registry_key(get_args.key_create[0], get_args.key_create[1])
    elif get_args.key_delete:
        delete_registry_key(get_args.key_delete[0], get_args.key_delete[1])
    elif get_args.key_value:
        write_registry_value(get_args.key_value[0], get_args.key_value[1], 
                            get_args.key_value[2], get_args.key_value[3])
    else:
        print("Вы сделали ошибку. Введите -h и ознакомьтесь с инструкцией")

if __name__ == "__main__":
    menu()