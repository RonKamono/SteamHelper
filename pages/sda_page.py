import pyperclip

from .bottom_appbar import BottomAppBar
import flet as ft
from flet import MainAxisAlignment, CrossAxisAlignment
from flet import ControlState
from settings import *
import time
import threading
from utils import *
cl = ColorSetting()
sg = SteamGuard()

class SdaView:

    def __init__(self, page, user_id):
        sg.load_secret_keys()
        self.page = page
        self.cl = ColorSetting()
        self.appbar = BottomAppBar(page, user_id, on_go_generator=None, on_go_sda=None)
        self.guard = ft.Text(value=sg.secret, selectable=True, size=20)

        self.logins_acc = ft.Container(
            content=ft.Column(
                controls=[], spacing=5
            )
        )

        def guard_generate(login, e, acc_index):
            self.logins_acc.content.controls[acc_index].content.style.text_style[ControlState.DEFAULT].size = 25
            self.logins_acc.content.controls[acc_index].content.style.color = cl.defFontColor
            self.logins_acc.content.controls[acc_index].content.style.text_style[ControlState.DEFAULT].weight = ft.FontWeight.W_600
            for _ in range(len(self.logins_acc.content.controls)):
                if _ != acc_index:
                    self.logins_acc.content.controls[_].content.style.text_style[ControlState.DEFAULT].size = 20
                    self.logins_acc.content.controls[_].content.style.color = cl.secFontColor
                    self.logins_acc.content.controls[_].content.style.text_style[
                        ControlState.DEFAULT].weight = ft.FontWeight.W_400
            sg.generate_steam_code(login)
            self.guard.value = sg.code
            self.page.update()
            print(f'{login}, {sg.code}, {sg.timer}')


        for _ in range(len(sg.account_names)):
            account_name = sg.account_names[_]
            if _ == 0:
                self.guard.value = sg.generate_steam_code(login=account_name)

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
                    on_click=lambda e, acc_index=_,login=account_name: guard_generate(login, e, acc_index)
                )
            )
            if __ != "":
                self.logins_acc.content.controls.append(__)

        self.sda_page = ft.Column(
            controls=[
                # MAIN COLUMN
                ft.Column(
                    expand=True,
                    controls=[
                        ###NAME
                        ft.Row(controls=[
                            ft.Text(value='STEAM DESKTOP AUTHENTICATOR', font_family='Cuprum', size=20,
                                    color=cl.secFontColor,
                                    weight=ft.FontWeight.W_600)
                        ], alignment=MainAxisAlignment.CENTER),
                        #GUARD AREA
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

                        #LOGIN AREA
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
                                    ft.Container(
                                        content=ft.ElevatedButton(text='Copy', color=cl.secFontColor,
                                                                  bgcolor=cl.appBarColor, height=40,
                                                                  width=400,
                                                                  on_click=lambda e: self.copy_guard(e)))
                                ]
                            )
                        ], alignment=MainAxisAlignment.CENTER),
                    ]
                )
            ]
        )

    def copy_guard(self, e):
        pyperclip.copy(self.guard.value)