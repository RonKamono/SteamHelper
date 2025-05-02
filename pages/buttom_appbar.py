import os
import flet as ft
from flet.core.types import MainAxisAlignment, CrossAxisAlignment
import json
from settings import *

cl = ColorSetting()
ws = WindowSetting()
cg = ConfigGenerator()

class ButtomAppBar:
    def __init__(self, page, user_id):
        self.page = page
        self.path_textfield = ft.TextField(label='Path to save files', width=250, height=50, border_radius=18,
                                           value=self.settings_load(user_id)['path'],
                                           bgcolor=cl.buttonColor, color=cl.secFontColor, border_color=cl.secBgColor,
                                           label_style=ft.TextStyle(color=cl.secFontColor))

        self.settings_alert = ft.AlertDialog(
            alignment=ft.alignment.center,
            title_padding=ft.padding.all(25),
            content=ft.Column(
                height=140,
                width=250,
                controls=[
                    ft.Text(value='SETTINGS', size=30, weight=ft.FontWeight.W_600, color=cl.secFontColor),
                    self.path_textfield,
                    ft.ElevatedButton(text='Confirm', width=250, height=40, bgcolor=cl.secBgColor,
                                      color=cl.secFontColor, on_click=lambda e: self.save_setting(e)),
                ], horizontal_alignment=CrossAxisAlignment.CENTER
            ),
        )

        self.buttom_appbar = ft.BottomAppBar(
            bgcolor=cl.appBarColor,
            height=70,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=ft.Row(
                controls=[
                    ft.IconButton(icon=ft.Icons.LOGIN_ROUNDED,
                                  icon_color=cl.secFontColor),
                    ft.IconButton(icon=ft.Icons.SUPERVISOR_ACCOUNT,
                                  icon_color=cl.secFontColor),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.SETTINGS,
                                  icon_color=cl.secFontColor,
                                  icon_size=30,
                                  on_click=lambda e: self.open_setting(e)),
                ]
            ),
        )

    def save_setting(self, e, user_id):
        settings = {
            "path": self.path_textfield.value,
        }
        with open(rf'C:\Users\{user_id}\AppData\Local\SteamHelper\settings.json', 'w', encoding='utf-8') as json_file:
            json.dump(settings, json_file, ensure_ascii=False, indent=4)
        self.page.close(self.settings_alert)

    def open_setting(self, e):
        self.page.open(self.settings_alert)

    def settings_load(self, user_id):
        with open(rf'C:\Users\{user_id}\AppData\Local\SteamHelper\settings.json', 'r', encoding='utf-8') as json_file:
            settings_load = json.load(json_file)
        return settings_load
