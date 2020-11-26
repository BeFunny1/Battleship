from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow

from work_with_confg.config_handler import ConfigHandler


class ConfigurationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_reader = ConfigHandler()
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("central_widget")

        self.inscriptions: [QtWidgets.QLabel] = None
        self.continuation_button: QtWidgets.QPushButton = None
        self.check_box_for_3D_field: QtWidgets.QCheckBox = None
        self.radio_button_for_AI_difficult_level: [QtWidgets.QRadioButton] = None
        self.combo_box_for_choice_permission: QtWidgets.QComboBox = None

        self.customer = None

    def establish_communication(self, customer) -> None:
        self.customer = customer

    def setupUi(self) -> None:
        self.customize_window()

        self.inscriptions = self.create_inscriptions()
        self.continuation_button = self.create_continuation_button()
        self.check_box_for_3D_field = self.create_check_box_for_3D_field()
        self.radio_button_for_AI_difficult_level \
            = self.create_radio_button_for_AI_difficult_level()
        self.combo_box_for_choice_permission \
            = self.create_combo_box_for_choice_permission()

    def create_continuation_button(self) -> QtWidgets.QPushButton:
        push_button = QtWidgets.QPushButton(self.central_widget)
        push_button.setGeometry(QtCore.QRect(100, 290, 200, 30))
        push_button.setObjectName('pushButton')
        push_button.setText('Продолжить')
        push_button.clicked.connect(self.take_final_configuration)
        return push_button

    def create_inscriptions(self) -> [QtWidgets.QLabel]:
        labels = []
        inscriptions_and_geometric_data \
            = self.config_reader.read_config_file(
              'inscriptions_and_geometric_data_configuration_window')
        for inscription in inscriptions_and_geometric_data.keys():
            label = QtWidgets.QLabel(self.central_widget)
            x, y, width, height = inscriptions_and_geometric_data[inscription]
            label.setGeometry(QtCore.QRect(x, y, width, height))
            label.setObjectName("label")
            label.setText(inscription)
            labels.append(label)
        labels[0].setAlignment(QtCore.Qt.AlignCenter)
        return labels

    def customize_window(self) -> None:
        self.setObjectName('MainWindow')
        self.resize(400, 380)
        self.setMinimumSize(QtCore.QSize(400, 380))
        self.setMaximumSize(QtCore.QSize(400, 380))
        self.setWindowTitle('Конфигурация')
        self.setCentralWidget(self.central_widget)

    def create_check_box_for_3D_field(self) -> QtWidgets.QCheckBox:
        check_box = QtWidgets.QCheckBox(self.central_widget)
        check_box.setGeometry(QtCore.QRect(120, 110, 80, 20))
        check_box.setObjectName('checkBox')
        check_box.setText('3D поле')
        return check_box

    def create_radio_button_for_AI_difficult_level(self) \
            -> [QtWidgets.QRadioButton]:
        radio_buttons = []
        options = ['Easy', 'Normal', 'Hard']
        for x in range(3):
            radio_button = QtWidgets.QRadioButton(self.central_widget)
            radio_button.setGeometry(QtCore.QRect(50, 170 + 20 * x, 95, 20))
            radio_button.setObjectName('radioButton')
            radio_button.setText(options[x])
            radio_buttons.append(radio_button)
        radio_buttons[0].setChecked(True)
        return radio_buttons

    def create_combo_box_for_choice_permission(self) -> QtWidgets.QComboBox:
        combo_box = QtWidgets.QComboBox(self.central_widget)
        combo_box.setGeometry(QtCore.QRect(120, 80, 80, 20))
        combo_box.setObjectName('comboBox')
        items = self.config_reader.read_config_file(
                'field_size_configuration_window')
        for item in items:
            combo_box.addItem(item)
        return combo_box

    def take_final_configuration(self) -> None:
        three_dimensional_map = bool(self.check_box_for_3D_field.checkState())
        permission = self.combo_box_for_choice_permission.currentText()
        ai_level = 'easy'
        for option in self.radio_button_for_AI_difficult_level:
            if option.isChecked():
                ai_level = option.text().lower()
                break
        self.customer(permission, three_dimensional_map, ai_level)


if __name__ == '__main__':
    pass
