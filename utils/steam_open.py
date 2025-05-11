import json
import ctypes
import pyautogui
import pygetwindow as gw
import py_win_keyboard_layout
import subprocess
import os
import time
import pyperclip
import keyboard
from .config_utils import settings_load
from .guard_code import SteamGuard
class Steam:
    def __init__(self):
        self.steam_path = settings_load()['steam_path']
        self.login_attempts = 0
        self.windows_list = []
        self.title_name = ['Sign in to Steam',
                           'Войти в Steam']

    def open_steam_account(self, login, password, guard_code):
        steam_path = self.steam_path + '/steam.exe'
        config_path = self.steam_path + '/config'
        try:
            os.remove(os.path.join(config_path, "loginusers.vdf"))
            os.remove(os.path.join(config_path, "config.vdf"))
            try:
                subprocess.run(["taskkill", "/f", "/im", "steam.exe"], check=True)
                subprocess.run(["taskkill", "/f", "/im", "steamwebhelper.exe"], check=True)
            except:
                pass
        except FileNotFoundError:
            pass
        time.sleep(2)
        subprocess.Popen([steam_path, '-login', '', ''])
        self.wait_steam()
        self.auto_login(login, password, guard_code)

    def wait_steam(self):
        while True:
            for __ in self.title_name:
                windows = gw.getWindowsWithTitle(__)
                if windows:
                    title_name = __
                    print(windows)
                    for window in windows:
                        try:
                            self.windows_list.append(windows)
                            if pyautogui.getActiveWindowTitle() not in title_name:
                                hwnd = user32.FindWindowW(None, title_name)
                                if hwnd:
                                    user32.ShowWindow(hwnd, 2)
                                    user32.SetForegroundWindow(hwnd)
                            return window
                        except Exception as e:
                            print(f"Ошибка при активации окна: {e}")
                time.sleep(1)

    def auto_login(self, login, password, guard_code):
        py_win_keyboard_layout.change_foreground_window_keyboard_layout(0x04090409)
        while True:
            for __ in self.title_name:
                windows = gw.getWindowsWithTitle(__)
                if windows:
                    title_name = __
                    print(windows)
                    for window in windows:
                        try:
                            print(self.windows_list)
                            window = self.windows_list[0]
                            print(f'[WINDOW] {window}: [WINDOWS] {windows}')
                            pyperclip.copy(login)
                            clipboard_content = pyperclip.paste()
                            print(clipboard_content)
                            if clipboard_content == login:
                                keyboard.press_and_release('ctrl+v')
                                time.sleep(0.05)
                                keyboard.press_and_release('tab')
                                time.sleep(0.05)
                                pyperclip.copy(password)
                                time.sleep(0.05)
                                keyboard.press_and_release('ctrl+v')
                                time.sleep(0.05)
                                keyboard.press_and_release('tab')
                                time.sleep(0.05)
                                keyboard.press_and_release('tab')
                                time.sleep(0.05)
                                keyboard.press_and_release('enter')
                                while True:
                                    if windows == window:
                                        pyperclip.copy(guard_code)
                                        time.sleep(0.05)
                                        print(guard_code)
                                        time.sleep(0.05)
                                        keyboard.press_and_release('ctrl+v')
                                        time.sleep(0.05)
                                        keyboard.press_and_release('enter')
                                        time.sleep(3)
                                        windows = gw.getWindowsWithTitle(title_name)
                                        if windows != window:
                                            print('Success')
                                            self.login_attempts = 0
                                            self.windows_list.clear()
                                            break
                            return True
                        except:
                            return False