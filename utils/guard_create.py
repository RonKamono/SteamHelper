import hmac, base64, hashlib
from re import search

import ntplib
import time
import json, os
from urllib.parse import urlparse, parse_qs

class SteamGuard:
    def __init__(self):
        self.dir_mafile = rf'C:\SteamHelper\mafiles'
        self.acc_id = []
        self.account_names = []
        self.secret_keys = []
        self.login_secret = []
        self.secret = ''
        self.code = ''
        self.remaining_time = 0

    def get_ntp_time(self):
        try:
            client = ntplib.NTPClient()
            response = client.request('pool.ntp.org')
            print(int(response.tx_time))
            return int(response.tx_time)
        except:
            return int(time.time())

    def generate_steam_code(self, login):
        """Генерация 5-значного Steam Guard кода"""
        try:
            time_buffer = int(time.time()) // 30
            def decode_steam_secret(secret):
                secret += '=' * ((8 - len(secret) % 8) % 8)
                return base64.b32decode(secret, casefold=True)
            self.get_secret_key(login)
            key = decode_steam_secret(self.secret)
            time_bytes = time_buffer.to_bytes(8, 'big')
            hmac_hash = hmac.new(key, time_bytes, hashlib.sha1).digest()
            offset = hmac_hash[-1] & 0xF
            code_bytes = hmac_hash[offset:offset + 4]
            full_code = int.from_bytes(code_bytes, 'big') & 0x7FFFFFFF
            steam_chars = '23456789BCDFGHJKMNPQRTVWXY'
            self.code = ''

            for _ in range(5):
                self.code += steam_chars[full_code % len(steam_chars)]
                full_code //= len(steam_chars)

            current_time = int(time.time())
            seconds_since_epoch = current_time % 30
            self.timer = 30 - seconds_since_epoch

            return self.code



        except Exception as e:
            print(f"Fail generate guard: {e}")
            return "00000"

    def get_secret_key(self, login):
        for i in range(len(self.login_secret)):
            if self.login_secret[i][0] == login:
                self.secret = self.login_secret[i][1]
        return self.secret

    def load_secret_keys(self):
        for filename in os.listdir(self.dir_mafile):
            file_path = os.path.join(self.dir_mafile, filename)
            acc_id = filename.replace('.maFile', "")  # Изменил переменную id на acc_id
            self.acc_id.append(acc_id)

            if os.path.isfile(file_path):
                try:
                    # Открываем файл и читаем данные
                    with open(file_path, 'r') as file:
                        content = file.read()
                        data = json.loads(content)

                        account_name = data.get('account_name')
                        otp_auth_url = data.get('uri')
                        parsed_url = urlparse(otp_auth_url)
                        query_params = parse_qs(parsed_url.query)
                        secret_key = query_params.get('secret', [None])[0]
                        self.account_names.append(account_name)
                        # Добавляем имя аккаунта и секретный ключ в список login_secret
                        if account_name and secret_key:
                            self.login_secret.append(
                                (account_name, secret_key))  # Кортеж (имя аккаунта, секретный ключ)
                except Exception as e:
                    print(f'An error occurred while processing file: {filename}. Error: {e}')
