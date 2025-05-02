from .buttom_appbar import ButtomAppBar
import flet as ft
from flet.core.types import MainAxisAlignment, CrossAxisAlignment
from random import choices
import re
import os
import time
from settings import *



cl = ColorSetting()
ws = WindowSetting()
cg = ConfigGenerator()

class GeneratorView:
    def __init__(self, page, user_id):
        self.page = page
        self.cl = ColorSetting()
        self.appbar = ButtomAppBar(page, user_id)

        self.path = self.appbar.settings_load(user_id)['path'] + r'\logpass.txt'
        self.path_with_email = self.appbar.settings_load(user_id)['path'] + r'\logpass_with_email.txt'

        self.generate = ft.ElevatedButton(text='Generate', disabled=True,
                                          tooltip='Enter login',
                                          color=cl.secFontColor,
                                          bgcolor=cl.buttonColor,
                                          width=300, height=40,
                                          on_click=lambda e: self.generate_info(e))
        self.name = ft.TextField(value='', hint_text="Enter your login",
                                 color=cl.secFontColor,
                                 bgcolor=cl.buttonColor,
                                 border_radius=18,
                                 border_color=cl.secBgColor, text_size=25,
                                 text_align=ft.TextAlign.CENTER,
                                 on_change=lambda e: self.check_textfield_login(e))
        self.slider_counter = ft.Slider(min=0, max=100, divisions=20, width=300,
                                        active_color=cl.secFontColor, thumb_color=cl.buttonColor,
                                        label="{value}", value=10,
                                        on_change=lambda e: self.change_value(e))
        self.result_text = ft.Text(f'account value: {int(self.slider_counter.value)}', size=20, color=cl.secFontColor,
                                   weight=ft.FontWeight.W_600)

        self.generator_page = ft.Column(
            controls=[
                ft.Column(
                    expand=True,
                    controls=[
                        ft.Row(controls=[ft.Icon(name=ft.Icons.VERIFIED_USER_OUTLINED, size=30, color=cl.secFontColor),
                                         ft.Text(value='GENERATE INFO', font_family='Cuprum', size=30,
                                                 color=cl.secFontColor,
                                                 weight=ft.FontWeight.W_600)], alignment=MainAxisAlignment.CENTER),
                        ft.Row(controls=[self.name], alignment=MainAxisAlignment.CENTER),
                        ft.Row(controls=[self.generate], alignment=MainAxisAlignment.CENTER),
                        ft.Row(controls=[
                            ft.ElevatedButton(text='Open', bgcolor=cl.buttonColor, color=cl.secFontColor, width=145,
                                              height=40,
                                              on_click=lambda e: self.open_txt_files(e)),
                            ft.ElevatedButton(text='Clear', bgcolor=cl.buttonColor, color=cl.secFontColor, width=145,
                                              height=40,
                                              on_click=lambda e: self.clear_txt(e))],
                            alignment=MainAxisAlignment.CENTER),
                        ft.Row(
                            controls=[self.result_text], alignment=MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            controls=[self.slider_counter], alignment=MainAxisAlignment.CENTER
                        ),
                    ]
                )
            ]
        )

    # FUNC CHANGE result_text
    def change_value(self, e):
        self.result_text.value = f'account value: {int(self.slider_counter.value)}'
        self.page.update()

    # FUNC GENERATION AND WRITE INFO
    def generate_info(self, e):
        self.result_text.value = "User info created."
        for i in range(int(self.slider_counter.value)):
            # GENERATE INFO ACCOUNT
            password = ''.join(choices(cg.chars, k=16))
            login = self.name.value + ''.join(choices(cg.digits, k=6))
            mail = login + '@outlook.com'
            # WRITE LOGIN PASSWORD EMAIL
            with open(self.path_with_email, 'a+', encoding="utf-8") as file:
                line_count = sum(1 for line in open(self.path_with_email))
                file.write(
                    'LOGIN = ' + login + ' | ' + 'PASSWORD = ' + password + ' | ' + 'MAIL = ' + mail + ' | ' +
                    str(1 + line_count) + '\n')
            # WRITE LOGIN PASSWORD
            with open(self.path, 'a+', encoding="utf-8") as file:
                file.write(f"{login}:{password}\n")

        self.page.update()
        time.sleep(2)
        self.result_text.value = f'account value: {int(self.slider_counter.value)}'
        self.page.update()

    # TEXTFIELD DISABLE
    def check_textfield_login(self, e):
        if len(self.name.value) > 2:
            if re.search(r'[а-яА-ЯёЁ]', self.name.value):
                self.generate.disabled = True
            else:
                self.generate.disabled = False
        else:
            self.generate.disabled = True

        self.page.update()
    # OPEN FILES
    def open_txt_files(self, e):
        try:
            os.startfile(self.path)
            os.startfile(self.path_with_email)
        except:
            self.result_text.value = "Fail not created."
            self.page.update()
            time.sleep(2)
            self.result_text.value = f'account value: {int(self.slider_counter.value)}'
            self.page.update()

    def clear_txt(self, e):
        try:
            os.remove(self.path)
            os.remove(self.path_with_email)

            self.result_text.value = "Files deleted."
            self.page.update()

        except FileNotFoundError:
            self.result_text.value = "Files not found."
        except Exception as ex:
            self.result_text.value = f"Failed to delete files: {str(ex)}"

        self.page.update()

        time.sleep(2)

        self.result_text.value = f'Account value: {int(self.slider_counter.value)}'
        self.page.update()
