from .bottom_appbar import BottomAppBar
import flet as ft

from settings import *

class SdaView:
    def __init__(self, page, user_id):
        self.page = page
        self.cl = ColorSetting()
        self.appbar = BottomAppBar(page, user_id, on_go_generator=None, on_go_sda=None)

        self.sda_page = ft.Column(
            controls=[
                ft.Column(
                    expand=True,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text('STEAM AUTH')
                            ]
                        )
                    ]
                )
            ]
        )
