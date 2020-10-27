from windows.configuration_window import ConfigurationWindow


class Application:
    def __init__(self):
        self.config_window = None

    def create_config_window(self):
        self.config_window = ConfigurationWindow()
        self.config_window.setupUi()
        self.config_window.show()
        self.config_window.establish_communication(self.check)

    def check(self, permission, three_dimensional_map, ai_level):
        self.config_window.hide()
        print(permission, three_dimensional_map, ai_level)


if __name__ == '__main__':
    pass
