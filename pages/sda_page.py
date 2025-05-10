import pyperclip
from .bottom_appbar import BottomAppBar
import flet as ft
from flet import MainAxisAlignment, CrossAxisAlignment
from flet import ControlState
import threading
from settings import *
from utils import *
import time
import os

cl = ColorSetting()
sg = SteamGuard()

class SdaView:
    def __init__(self, page):
        sg.load_secret_keys()
        self.page = page
        self.varibale_login = False
        self.cl = ColorSetting()
        self.appbar = BottomAppBar(page, on_go_generator=None, on_go_sda=None)
        self.guard = ft.Text(value=sg.secret, selectable=True, size=20)
        self.timer_text = ft.Text(value="", size=16, color=cl.secFontColor, weight=ft.FontWeight.W_600)
        self.last_login = ''
        self.timer_thread = threading.Thread(target=self.update_timer, daemon=True)
        self.steam = Steam()
        # CONTAINER WITH LOGINS
        self.logins_acc = ft.Container(
            content=ft.Column(
                controls=[], spacing=5
            )
        )

        self.error_alert = ft.AlertDialog(
        title=ft.Text("Login/Password missing",
                        size=20,
                        color=cl.secFontColor,
                        text_align=ft.TextAlign.CENTER
                        ),
            alignment=ft.alignment.center,
        bgcolor=cl.defBgColor,
    )

        def guard_generate(login, e, acc_index):
            self.logins_acc.content.controls[acc_index].content.style.text_style[ControlState.DEFAULT].size = 25
            self.logins_acc.content.controls[acc_index].content.style.color = cl.defFontColor
            self.logins_acc.content.controls[acc_index].content.style.text_style[
                ControlState.DEFAULT].weight = ft.FontWeight.W_600
            self.last_login = login
            for _ in range(len(self.logins_acc.content.controls)):
                if _ != acc_index:
                    self.logins_acc.content.controls[_].content.style.text_style[ControlState.DEFAULT].size = 20
                    self.logins_acc.content.controls[_].content.style.color = cl.secFontColor
                    self.logins_acc.content.controls[_].content.style.text_style[
                        ControlState.DEFAULT].weight = ft.FontWeight.W_400

            sg.generate_steam_code(login)
            self.guard.value = sg.code
            self.page.update()

        for _ in range(len(sg.account_names)):
            account_sort = sorted(sg.account_names)
            account_name = account_sort[_]
            __ = ft.Container(
                content=ft.TextButton(
                    text=account_name,
                    width=400,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(
                            size=20,
                            weight=ft.FontWeight.W_400
                        ),
                        color=cl.secFontColor,
                        shape=ft.RoundedRectangleBorder(radius=16),
                    ),
                    on_click=lambda e, acc_index=_, login=account_name: guard_generate(login, e, acc_index)
                )
            )
            if __ != "":
                self.logins_acc.content.controls.append(__)

        # GENERATE GUARD INDEX 0
        try:
            guard_generate(login=sorted(sg.account_names)[0], acc_index=0, e=None)
            # START TIMER
            timer_thread = threading.Thread(target=self.update_timer, daemon=True)
            timer_thread.start()
        except:
            self.guard.value = 'Add mafiles path in settings'

        self.sda_page = ft.Column(
            controls=[
                # MAIN COLUMN
                ft.Column(
                    expand=True,
                    controls=[
                        # NAME
                        ft.Row(controls=[
                            ft.Text(value='STEAM DESKTOP AUTHENTICATOR', font_family='Cuprum', size=20,
                                    color=cl.secFontColor,
                                    weight=ft.FontWeight.W_600)
                        ], alignment=MainAxisAlignment.CENTER),
                        # Timer
                        ft.Row(controls=[
                            ft.Container(
                                content=self.timer_text,
                                alignment=ft.alignment.center
                            )
                        ], alignment=MainAxisAlignment.CENTER),
                        # GUARD AREA
                        ft.Row(controls=[
                            ft.Container(
                                shadow=ft.BoxShadow(
                                    spread_radius=0,
                                    blur_radius=1,
                                    color=cl.hoverBgColor,
                                    offset=ft.Offset(0, 1),
                                    blur_style=ft.ShadowBlurStyle.OUTER,
                                ),
                                width=400, height=50,
                                padding=10, bgcolor=cl.appBarColor,
                                border_radius=18,
                                content=ft.Row(
                                    controls=[
                                        self.guard
                                    ], alignment=MainAxisAlignment.CENTER
                                )
                            )
                        ], alignment=MainAxisAlignment.CENTER),
                        # LOGIN AREA
                        ft.Row(controls=[
                            ft.Container(
                                shadow=ft.BoxShadow(
                                    spread_radius=0,
                                    blur_radius=1,
                                    color=cl.hoverBgColor,
                                    offset=ft.Offset(0, 1),
                                    blur_style=ft.ShadowBlurStyle.SOLID,
                                ),
                                border_radius=18,
                                width=400, height=250,
                                padding=10,
                                bgcolor=cl.appBarColor,
                                content=ft.Column(
                                    scroll=ft.ScrollMode.AUTO,
                                    controls=[
                                        self.logins_acc
                                    ]
                                )
                            )
                        ], alignment=MainAxisAlignment.CENTER
                        ),
                        ft.Row(controls=[
                            ft.Column(
                                controls=[
                                    ft.Row(controls=[
                                        ft.Container(
                                            content=ft.ElevatedButton(text='Copy', color=cl.secFontColor,
                                                                      bgcolor=cl.appBarColor, height=40,
                                                                      width=95,
                                                                      on_click=lambda e: self.copy_guard(e))),
                                        ft.Row(
                                            controls=[
                                                ft.Container(
                                                    content=ft.ElevatedButton(text='Add account', color=cl.secFontColor,
                                                                              bgcolor=cl.appBarColor, height=40,
                                                                              width=190,
                                                                              on_click=lambda e: self.add_account(e))),
                                                ft.Container(
                                                    content=ft.ElevatedButton(text='Folder', color=cl.secFontColor,
                                                                              bgcolor=cl.appBarColor, height=40,
                                                                              width=95,
                                                                              on_click=lambda e: self.open_folder(e))),
                                            ]
                                        )
                                    ]),
                                    ft.Container(
                                        content=ft.ElevatedButton(text='Open Steam', color=cl.secFontColor,
                                                                  bgcolor=cl.appBarColor, height=40,
                                                                  width=400,
                                                                  on_click=lambda e: self.steam_open(e)))
                                ]
                            )
                        ], alignment=MainAxisAlignment.CENTER),
                    ]
                )
            ]
        )

    def guard_generate(self, login, e, acc_index):
        self.logins_acc.content.controls[acc_index].content.style.text_style[ControlState.DEFAULT].size = 25
        self.logins_acc.content.controls[acc_index].content.style.color = cl.defFontColor
        self.logins_acc.content.controls[acc_index].content.style.text_style[
            ControlState.DEFAULT].weight = ft.FontWeight.W_600
        self.last_login = login
        for _ in range(len(self.logins_acc.content.controls)):
            if _ != acc_index:
                self.logins_acc.content.controls[_].content.style.text_style[ControlState.DEFAULT].size = 20
                self.logins_acc.content.controls[_].content.style.color = cl.secFontColor
                self.logins_acc.content.controls[_].content.style.text_style[
                    ControlState.DEFAULT].weight = ft.FontWeight.W_400

        sg.generate_steam_code(login)
        self.guard.value = sg.code
        self.page.update()

    def update_timer(self):
            correct_time = sg.timer
            while True:
                remaining_time =  max(0, correct_time)
                self.timer_text.value = f"Timer update: {remaining_time} sec"
                correct_time -= 1
                time_on = True
                self.page.update()
                if remaining_time == 0:
                    sg.generate_steam_code(self.last_login)
                    correct_time = sg.timer
                    self.guard.value = sg.code
                    self.page.update()
                    time_on = False
                if time_on:
                    time.sleep(1)

    def add_account(self, e):
        self.logins_acc.content.clean()
        sg.account_names.clear()
        sg.load_secret_keys()
        for _ in range(len(sg.account_names)):
            account_sort = sorted(sg.account_names)
            account_name = account_sort[_]
            #SAVE LAST LOGIN FIELD
            if account_name == self.last_login:
                __ = ft.Container(
                    content=ft.TextButton(
                        text=account_name,
                        width=400,
                        style=ft.ButtonStyle(
                            text_style=ft.TextStyle(
                                size=25,
                                weight=ft.FontWeight.W_600
                            ),
                            color=cl.defFontColor,
                            shape=ft.RoundedRectangleBorder(radius=16),
                        ),
                        on_click=lambda e, acc_index=_, login=account_name: self.guard_generate(login, e, acc_index)
                    )
                )
                if __ != "":
                    self.logins_acc.content.controls.append(__)
            #ELSE LOGINS
            else:
                __ = ft.Container(
                    content=ft.TextButton(
                        text=account_name,
                        width=400,
                        style=ft.ButtonStyle(
                            text_style=ft.TextStyle(
                                size=20,
                                weight=ft.FontWeight.W_400
                            ),
                            color=cl.secFontColor,
                            shape=ft.RoundedRectangleBorder(radius=16),
                        ),
                        on_click=lambda e, acc_index=_, login=account_name: self.guard_generate(login, e, acc_index)
                    )
                )
                if __ != "":
                    self.logins_acc.content.controls.append(__)

        for acc_index in range(len(sg.account_names)):
            if self.last_login in self.logins_acc.content.controls[acc_index].content.text:
                self.varibale_login = True
                index = acc_index

        try:
            if self.varibale_login:
                self.guard_generate(login=self.last_login, acc_index=index, e=None)
                try:
                    self.timer_thread.start()
                except:
                    pass
            else:
                self.guard.value = 'add mifile in folder'
                self.guard.update()
        except:
            pass
        self.logins_acc.update()


    def open_folder(self, e):
        os.startfile(settings_load()['path'])

    def copy_guard(self, e):
        pyperclip.copy(self.guard.value)
        self.guard.value = 'Copied'
        self.guard.update()
        time.sleep(1.5)
        self.guard.value = sg.code
        self.guard.update()

    def get_password(self, login):
        accounts = load_account()
        for account in accounts:
            if login == account[0]:
                return account[1]

    def check_valid_account(self, login):
        accounts = load_account()
        for account in accounts:
            if login == account[0]:
                return True

    def steam_open(self, e):
        login = self.last_login
        if self.check_valid_account(login):
            password = self.get_password(login)
            guard_code = sg.code
            self.steam.open_steam_account(login, password, guard_code)
        else:
            self.page.open(self.error_alert)
