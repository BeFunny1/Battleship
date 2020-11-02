import json
import os
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class ConfigHandler:
    path_to_dir_with_config: ClassVar[str] = './configs/'

    def read_config_file(self, filename: str) -> dict:
        link = self.path_to_dir_with_config + filename
        if not os.path.exists(link):
            self.create_config_file(link, filename)
        with open(link, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config

    @staticmethod
    def create_config_file(link: str, filename: str) -> None:
        config_default_backup = {
            'field_size_configuration_window': [
                "10x10", "16x16", "32x32",
                "64x64", "128x128", "256x256",
                "512x512", "1024x1024", "2048x2048"
            ],
            'inscriptions_and_geometric_data_arrange_the_ships_window': {
                "Разместите корабли:": [40, 10, 140, 20],
                "Линкоры:": [30, 30, 60, 20],
                "Крейсеры:": [30, 50, 60, 20],
                "Эсминцы:": [30, 70, 60, 20],
                "Катера:": [30, 90, 60, 20],
                "Нажмите на эту кнопку, чтобы "
                "перейти в режим удаления кораблей.": [200, -10, 221, 81],
                "Сейчас режим:": [200, 60, 90, 20]
            },
            'inscriptions_and_geometric_data_configuration_window': {
                "Задайте нужные конфигурации.": [10, 0, 380, 40],
                "Уровень AI противника:": [30, 150, 160, 15],
                "Выберите конфигурацию поля:": [30, 50, 260, 15],
                "Размер:": [50, 80, 60, 20],
                "Свойство:": [50, 110, 60, 20]
            },
            'inscriptions_and_geometric_data_game_window': {
                "Уничтожьте корабли:": [40, 10, 140, 20],
                "Линкоры:": [30, 30, 60, 20],
                "Крейсеры:": [30, 50, 60, 20],
                "Эсминцы:": [30, 70, 60, 20],
                "Катера:": [30, 90, 60, 20]
            },
            'label_field_arrange_the_ships_window': {
                "ships": {
                    "battleship": [120, 30, 60, 20],
                    "cruiser": [120, 50, 60, 20],
                    "destroyer": [120, 70, 60, 20],
                    "boat": [120, 90, 60, 20]
                },
                "sub_level_activate": [300, 60, 90, 20]
            },
            'label_field_game_window': {
                "battleship": [120, 30, 60, 20],
                "cruiser": [120, 50, 60, 20],
                "destroyer": [120, 70, 60, 20],
                "boat": [120, 90, 60, 20]
            }
        }
        with open(link, 'w') as file:
            config_content = config_default_backup[filename]
            text = json.dumps(config_content)
            file.write(text)
