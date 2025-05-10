import json
import os

def load_cfg():
    config_dir = rf'C:\Program Files\SteamHelper'
    settings_path = os.path.join(config_dir, r"settings.json")
    default_data = {"path": "C:\\SteamHelper",
                    "steam_path": "C:\\Program Files (x86)\\Steam"}
    data_dir = rf'C:\SteamHelper' # переделать путь / что-бы папка могла генерироваться в другом месте
    os.makedirs(config_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(rf'{data_dir}\mafiles', exist_ok=True)
    if not os.path.exists(settings_path):
        try:
            with open(fr'{settings_path}', 'w', encoding='utf-8') as f:
                json.dump(default_data, f, indent=4)

        except Exception as e:
            print(f"Error create file: {str(e)}")

    if not os.path.exists(settings_load()['path'] + '\\accounts.txt'):
        path_accounts = settings_load()['path'] + '\\accounts.txt'
        print(path_accounts)
        with open(path_accounts, 'w', encoding="utf-8") as file:
            file.write('login:password')

def settings_load():
    with open(rf'C:\Program Files\SteamHelper\settings.json', 'r', encoding='utf-8') as json_file:
        settings_load = json.load(json_file)
    return settings_load

def load_account():
    path_accounts = settings_load()['path'] + '\\accounts.txt'
    print(path_accounts)
    accounts = []
    try:
        with open(path_accounts, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        login = parts[0].strip()
                        password = parts[1].strip()
                        accounts.append((login, password))
            return accounts
    except Exception as e:
        print(f"Ошибка загрузки аккаунтов: {str(e)}")

