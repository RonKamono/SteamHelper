from .buttom_appbar import ButtomAppBar
import flet as ft

from settings import *

class SdaView:
    def __init__(self, page, user_id):
        self.page = page
        self.cl = ColorSetting()
        self.appbar = ButtomAppBar(page, user_id)