import flet as ft
import getpass
import os
from pages import *
from pages.sda_page import SdaView
from settings import *
from utils.config_utils import load_cfg



cl = ColorSetting()
ws = WindowSetting()


class PanelPage:
    def __init__(self, ):
        self.page = ft.Page

    def main(self, page):

        user_id = getpass.getuser()
        load_cfg(user_id)
        icon_path = os.path.abspath('assets/icons/icon.ico')
        page.window.icon = icon_path
        page.title = "SteamHelper"
        page.bgcolor = cl.defBgColor
        page.window.width = ws.defaultWidth
        page.window.height = ws.defaultHeight
        page.window.resizable = False
        page.window.full_screen = False
        # page.window.center()
        page.padding = 0
        page.window.frameless = True

        self.generator = GeneratorView(page, user_id)
        self.sda = SdaView(page, user_id)
        self.bottom_bar = BottomAppBar(
            page,
            user_id,
            on_go_sda=lambda e: self.show_sda(),
            on_go_generator=lambda e: self.show_generator()
        )
        self.top_bar = TopAppBar(
            page,
            close_app =lambda e: close_app(e)
        )

        page.bottom_appbar = self.bottom_bar.bottom_appbar

        # Главный контейнер для страниц
        self.main_container = ft.Column(expand=True, controls=[
            ft.Column(expand=1, controls=[self.top_bar.top_appbar]),
            ft.Column(expand=3, controls=[self.sda.sda_page])
        ])

        page.add(self.main_container)

        def close_app(e):
            page.window.close()

    def show_generator(self):
        """SHOW PAGE GENERATOR"""
        self.main_container.controls[1].controls = [self.generator.generator_page]
        self.main_container.update()

    def show_sda(self):
        """SHOW PAGE SDA"""

        self.main_container.controls[1].controls = [self.sda.sda_page]
        self.main_container.update()


panel_page_instance = PanelPage()
ft.app(panel_page_instance.main)