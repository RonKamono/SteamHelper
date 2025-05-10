import json
import ctypes
import pyautogui
import pygetwindow as gw
import py_win_keyboard_layout
import subprocess
import os
import time
import pyperclip
from .config_utils import settings_load
from .guard_code import SteamGuard
class Steam:
    def __init__(self):
        self.steam_path = settings_load()['steam_path']
        self.login_attempts = 0
        self.windows_list = []

    def open_steam_account(self, login, password, guard_code):
        steam_path = self.steam_path + '/steam.exe'
        config_path = self.steam_path + '/config'
        try:
            os.remove(os.path.join(config_path, "loginusers.vdf"))
            os.remove(os.path.join(config_path, "config.vdf"))
            subprocess.run(["taskkill", "/f", "/im", "steam.exe"], check=True)
            subprocess.run(["taskkill", "/f", "/im", "steamwebhelper.exe"], check=True)
        except FileNotFoundError:
            pass
        time.sleep(2)
        subprocess.Popen([steam_path, '-login', '', ''])
        self.wait_steam()
        self.auto_login(login, password, guard_code)

    def wait_steam(self):
        title_name = f'Sign in to Steam'
        print(f"Ожидание открытия окна с заголовком: '{title_name}'...")
        user32 = ctypes.windll.user32
        while True:
            windows = gw.getWindowsWithTitle(title_name)
            if windows:
                for window in windows:
                    try:
                        self.windows_list.append(windows)
                        if pyautogui.getActiveWindowTitle() != title_name:
                            hwnd = user32.FindWindowW(None, title_name)

                            if hwnd:
                                user32.ShowWindow(hwnd, 2)
                                user32.SetForegroundWindow(hwnd)

                        return window
                    except Exception as e:
                        print(f"Ошибка при активации окна: {e}")
            time.sleep(3)

    def auto_login(self, login, password, guard_code):
        sg = SteamGuard()
        py_win_keyboard_layout.change_foreground_window_keyboard_layout(0x04090409)
        title_name = f'Sign in to Steam'
        windows = gw.getWindowsWithTitle(title_name)
        if self.login_attempts >= 1:
            return
        self.login_attempts += 1
        time.sleep(1)
        pyperclip.copy(login)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('tab')
        pyperclip.copy(password)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('enter')
        print(self.windows_list)
        window = self.windows_list[0]
        print(f'[WINDOW] {window}: [WINDOWS] {windows}')
        while True:
            if windows == window:
                pyperclip.copy(guard_code)
                print(guard_code)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.press('enter')
                time.sleep(3)
                windows = gw.getWindowsWithTitle(title_name)
                if windows != window:
                    print('Success')
                    self.login_attempts = 0
                    self.windows_list.clear()
                    break