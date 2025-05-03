import json
import os

def load_cfg(user_id):
    config_dir = rf'C:\Users\{user_id}\AppData\Local\SteamHelper'
    settings_path = os.path.join(config_dir, r"settings.json")
    default_data = {"path": "C:\\SteamHelper"}
    data_dir = rf'C:\SteamHelper'
    os.makedirs(config_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(f'{data_dir}\mafiles', exist_ok=True)

    if not os.path.exists(settings_path):
        try:
            with open(fr'{settings_path}', 'w', encoding='utf-8') as f:
                json.dump(default_data, f, indent=4)
        except Exception as e:
            print(f"Error create file: {str(e)}")
