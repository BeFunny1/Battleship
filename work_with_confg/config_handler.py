import json


class ConfigHandler:
    def __init__(self):
        self.path_to_dir_with_config = './configs/'

    def read_config_file(self, file: str) -> dict:
        with open(self.path_to_dir_with_config + file,
                  'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
