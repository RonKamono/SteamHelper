import flet as ft
from flet.core.types import MainAxisAlignment, CrossAxisAlignment
import json
from settings import *
from utils.config_utils import settings_load
cl = ColorSetting()
ws = WindowSetting()
cg = ConfigGenerator()

class BottomAppBar:
    def __init__(self, page, on_go_sda, on_go_generator):
        self.page = page
        self.on_go_sda = on_go_sda  # Функция для перехода в SDA
        self.on_go_generator = on_go_generator  # Функция для перехода в Generator

        self.path_textfield = ft.TextField(
            label='Path to files',
            width=250,
            height=50,
            border_radius=18,
            value=settings_load()['path'],
            bgcolor=cl.appBarColor,
            color=cl.secFontColor,
            border_color=cl.secBgColor,
            label_style=ft.TextStyle(color=cl.secFontColor)
        )

        self.steam_textfield = ft.TextField(
            label='Steam folder',
            width=250,
            height=50,
            border_radius=18,
            value=settings_load()['steam_path'],
            bgcolor=cl.appBarColor,
            color=cl.secFontColor,
            border_color=cl.secBgColor,
            label_style=ft.TextStyle(color=cl.secFontColor)
        )

        self.settings_alert = ft.AlertDialog(
            alignment=ft.alignment.center,
            title_padding=ft.padding.all(25),
            content=ft.Column(
                height=220,
                width=250,
                controls=[
                    ft.Text(value='SETTINGS', size=30, weight=ft.FontWeight.W_600, color=cl.secFontColor),
                    self.path_textfield,
                    self.steam_textfield,
                    ft.ElevatedButton(
                        text='Confirm',
                        width=250,
                        height=40,
                        bgcolor=cl.appBarColor,
                        color=cl.secFontColor,
                        on_click=lambda e: self.save_setting(e)
                    ),
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER
            ),
        )

        self.bottom_appbar = ft.BottomAppBar(
            bgcolor=cl.appBarColor,
            height=70,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.SUPERVISOR_ACCOUNT,
                        tooltip='Steam Desktop Authenticator',
                        on_click=self.on_go_sda,
                        icon_color=cl.secFontColor
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CREATE_ROUNDED,
                        tooltip='Account Info Generate',
                        on_click=self.on_go_generator,
                        icon_color=cl.secFontColor
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.SETTINGS,
                        tooltip='Settings',
                        icon_color=cl.secFontColor,
                        icon_size=30,
                        on_click=lambda e: self.open_setting(e)
                    ),
                ]
            ),
        )

    def open_setting(self, e):
        self.page.open(self.settings_alert)


    def save_setting(self, e):
        settings = {
            "path": self.path_textfield.value,
            "steam_path": self.steam_textfield.value
        }
        with open(rf'C:\Program Files\SteamHelper\settings.json', 'w', encoding='utf-8') as json_file:
            json.dump(settings, json_file, ensure_ascii=False, indent=4)
        self.page.close(self.settings_alert)
        settings_load()

