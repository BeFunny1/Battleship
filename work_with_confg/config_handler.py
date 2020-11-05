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
            'direction_arrows_button': {
                "up": {
                    "↑": {
                        "arrange": [215, 530, 90, 70],
                        "game": [340, 530, 90, 70]
                    }
                },
                "down": {
                    "↓": {
                        "arrange": [215, 610, 90, 70],
                        "game": [340, 610, 90, 70]
                    }
                },
                "left": {
                    "←": {
                        "arrange": [110, 570, 90, 70],
                        "game": [240, 570, 90, 70]
                    }
                },
                "right": {
                    "→": {
                        "arrange": [320, 570, 90, 70],
                        "game": [440, 570, 90, 70]
                    }
                }
            },
            'field_size_configuration_window': [
                "10x10", "16x16", "32x32",
                "64x64", "128x128", "256x256",
                "512x512", "1024x1024", "2048x2048"
            ],
            'inscriptions_and_geometric_data_arrange_the_ships_window': {
                "general_labels": {
                    "Разместите корабли:": [40, 10, 140, 20],
                    "Нажмите на эту кнопку,"
                    " чтобы перейти в режим"
                    " удаления кораблей.": [200, -10, 221, 81],
                    "Сейчас режим:": [200, 60, 90, 20]
                },
                "ships": {
                    "Линкоры:": [30, 30, 60, 20],
                    "Крейсеры:": [30, 50, 60, 20],
                    "Эсминцы:": [30, 70, 60, 20],
                    "Катера:": [30, 90, 60, 20]
                  },
                "submarine": {
                    "Атомная подлодка:": [30, 30, 140, 20],
                    "Большая подлодка:": [30, 50, 140, 20],
                    "Средняя подлодка:": [30, 70, 140, 20],
                    "Сверхмалая подлодка:": [30, 90, 140, 20]
                  }
            },
            'inscriptions_and_geometric_data_configuration_window': {
                "Задайте нужные конфигурации.": [10, 0, 380, 40],
                "Уровень AI противника:": [30, 150, 160, 15],
                "Выберите конфигурацию поля:": [30, 50, 260, 15],
                "Размер:": [50, 80, 60, 20],
                "Свойство:": [50, 110, 60, 20]
            },
            'inscriptions_and_geometric_data_game_window': {
                "general_labels": {
                    "Уничтожьте корабли:": [40, 10, 140, 20]
                },
                "ships": {
                    "Линкоры:": [30, 30, 60, 20],
                    "Крейсеры:": [30, 50, 60, 20],
                    "Эсминцы:": [30, 70, 60, 20],
                    "Катера:": [30, 90, 60, 20]
                },
                "submarine": {
                    "Атомная подлодка:": [30, 30, 140, 20],
                    "Большая подлодка:": [30, 50, 140, 20],
                    "Средняя подлодка:": [30, 70, 140, 20],
                    "Сверхмалая подлодка:": [30, 90, 140, 20]
                },
                "end_game": {
                    "player": {
                      "Игра закончена. Вы победили.": [0, 140, 520, 20]
                    },
                    "enemy": {
                      "Игра закончена. Вы проиграли.": [0, 140, 520, 20]
                    }
                }
            },
            'label_field_arrange_the_ships_window': {
                "ships": {
                    "battleship": [150, 30, 60, 20],
                    "cruiser": [150, 50, 60, 20],
                    "destroyer": [150, 70, 60, 20],
                    "boat": [150, 90, 60, 20]
                },
                "submarine": {
                    "nuclear submarine": [150, 30, 60, 20],
                    "large submarine": [150, 50, 60, 20],
                    "medium submarine": [150, 70, 60, 20],
                    "ultra-small submarine": [150, 90, 60, 20]
                },
                "interval": {
                    "x_start": [100, 134, 55, 16],
                    "x_end": [364, 134, 55, 16],
                    "y_start": [45, 152, 55, 16],
                    "y_end": [45, 452, 55, 16]
                },
                "sub_level_activate": [300, 60, 90, 20]
            },
            'label_field_game_window': {
                "ships": {
                    "battleship": [150, 30, 60, 20],
                    "cruiser": [150, 50, 60, 20],
                    "destroyer": [150, 70, 60, 20],
                    "boat": [150, 90, 60, 20]
                },
                "submarine": {
                    "nuclear submarine": [150, 30, 60, 20],
                    "large submarine": [150, 50, 60, 20],
                    "medium submarine": [150, 70, 60, 20],
                    "ultra-small submarine": [150, 90, 60, 20]
                },
                "interval": {
                    "x_start_player": [40, 160, 55, 16],
                    "x_end_player": [302, 160, 55, 16],
                    "y_start_player": [-19, 180, 55, 16],
                    "y_end_player": [-19, 480, 55, 16],
                    "x_start_enemy": [410, 160, 55, 16],
                    "x_end_enemy": [672, 160, 55, 16],
                    "y_start_enemy": [351, 180, 55, 16],
                    "y_end_enemy": [351, 480, 55, 16]
                }
            },
            'styles_for_element': {
                "button": "min-width: 19px;min-height: 19px;"
            }
        }
        with open(link, 'w') as file:
            config_content = config_default_backup[filename]
            text = json.dumps(config_content)
            file.write(text)
