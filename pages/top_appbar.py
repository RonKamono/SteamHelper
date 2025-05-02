import flet as ft
from flet import MainAxisAlignment
from settings import *

cl = ColorSetting()
ws = WindowSetting()
cg = ConfigGenerator()


class TopAppBar:
    def __init__(self, page, close_app):
        self.page = page
        self.close_app = close_app
        self.top_appbar = ft.Row(
            [
                ft.WindowDragArea(

                    ft.Container(
                        bgcolor=cl.appBarColor,
                        width=ws.defaultWidth,
                        height=40,
                        padding=ft.padding.symmetric(0, 10),
                        content=ft.Row(
                            expand=True,
                            controls=[
                                ft.Row(controls=[ft.Container(ft.Icon(ft.Icons.ALL_INBOX, color=cl.secFontColor)),
                                                 ft.Container(ft.Text('STEAM HELPER', weight=ft.FontWeight.W_600, size=16, color=cl.secFontColor))], expand=1),

                                ft.Row(controls=[ft.Container(ft.IconButton(icon=ft.Icons.CLOSE,
                                                                            icon_size=16,
                                                                            hover_color=cl.appBarColor,
                                                                            icon_color=cl.secFontColor,
                                                                            on_click=lambda e:close_app(e)))],
                                       expand=1, alignment=MainAxisAlignment.END)
                            ], alignment=MainAxisAlignment.CENTER
                        )
                    ),
                    expand=True,
                    maximizable=False,
                ),

            ]
        )






