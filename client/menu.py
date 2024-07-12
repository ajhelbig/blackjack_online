import pygame
import pygame_menu

class Menu: #eventually move menu code here

    def __init__(self, window):

        self.window = window
        self.window_size = window.get_size()
        self.menu_x_scale_factor = 0.5
        self.menu_y_scale_factor = 0.5

        self.menus = {}

    def create_start_menu(self):
        self.menus['start menu'] = pygame_menu.Menu('What Should We Call You?',
                                        self.window_size[0] * self.menu_x_scale_factor, 
                                        self.window_size[1] * self.menu_y_scale_factor,
                                        theme=pygame_menu.themes.THEME_DARK)

    def create_main_menu(self):
        pass

    def create_join_menu(self):
        pass

    def switch_to_menu(self, menu_name):
        if menu_name in self.menus:
            self.menus[menu_name].enable()

    