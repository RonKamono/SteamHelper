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
    async def main(self, page: ft.Page):
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
        page.window.maximizable = False
        page.window.center()
        generator = GeneratorView(page, user_id)
        buttom_bar = ButtomAppBar(page, user_id)
        sda = SdaView(page, user_id)
        # VIEW APPBAR
        page.bottom_appbar = buttom_bar.buttom_appbar
        # VIEW GENERATOR
        page.add(
            ft.Column(expand=True,
                      controls=[
                          ft.Column(expand=1),
                          ft.Column(
                              expand=3,
                              controls=[
                                  generator.generator_page
                              ]),
                      ])
        )



panel_page_instance = PanelPage()
ft.app(panel_page_instance.main)
