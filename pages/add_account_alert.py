import flet as ft

from settings import *

cl = ColorSetting()

class AddAccountAlert:
    login = ft.TextField(value='', hint_text="Enter your login",
                            color=cl.secFontColor,
                            bgcolor=cl.appBarColor,
                            width=250,
                            height=50,
                            border_radius=18,
                            border_color=cl.appBarColor, text_size=16,
                            text_align=ft.TextAlign.CENTER)

    password = ft.TextField(value='', hint_text="Enter your password",
                            color=cl.secFontColor,
                            bgcolor=cl.appBarColor,
                            width=250,
                            height=50,
                            border_radius=18,
                            password=True,
                            border_color=cl.appBarColor, text_size=16,
                            text_align=ft.TextAlign.CENTER)

    account_alert = ft.AlertDialog(
        content=ft.Container(
            content=ft.Column(
                height=200,
                width=250,
                controls=[
                    ft.Text(
                        value='Pair steam account',
                        size=25,
                        weight=ft.FontWeight.W_600,
                        color=cl.secFontColor
                    ),
                    login,
                    password,
                    ft.ElevatedButton(
                        text='Confirm',
                        width=250,
                        height=40,
                        color=cl.secFontColor,
                        bgcolor=cl.appBarColor
                    )
                ], alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
    )

