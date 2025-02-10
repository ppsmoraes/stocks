from pandas import DataFrame, concat
from PyQt6 import QtWidgets  # type: ignore
from PyQt6.QtCore import QDate  # type: ignore
from PyQt6.QtWidgets import QDateEdit  # type: ignore
from PyQt6.QtWidgets import QHBoxLayout  # type: ignore
from PyQt6.QtWidgets import QLabel  # type: ignore
from PyQt6.QtWidgets import QLineEdit  # type: ignore
from PyQt6.QtWidgets import QMessageBox  # type: ignore
from PyQt6.QtWidgets import QPushButton  # type: ignore
from PyQt6.QtWidgets import QTableWidget  # type: ignore
from PyQt6.QtWidgets import QTableWidgetItem  # type: ignore
from PyQt6.QtWidgets import QVBoxLayout  # type: ignore

import cache
import calcs
import data


class InvestmentApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Investment Tracker')

        # Layouts
        main_layout = QVBoxLayout()
        form_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        table_layout = QVBoxLayout()

        # Labels and Entry widgets for input
        self.amount_label = QLabel('Valor do Depósito:')
        self.amount_entry = QLineEdit()
        self.amount_entry.setText('R$ 0,00')
        self.amount_entry.textChanged.connect(self.format_amount)
        form_layout.addWidget(self.amount_label)
        form_layout.addWidget(self.amount_entry)

        self.deposit_date_label = QLabel('Data do Depósito:')
        self.deposit_date_entry = QDateEdit()
        self.deposit_date_entry.setDisplayFormat('dd/MM/yyyy')
        self.deposit_date_entry.setDate(QDate.currentDate())
        self.deposit_date_entry.setCalendarPopup(True)
        form_layout.addWidget(self.deposit_date_label)
        form_layout.addWidget(self.deposit_date_entry)

        self.withdrawal_date_label = QLabel('Data de Retirada:')
        self.withdrawal_date_entry = QDateEdit(QDate.currentDate())
        self.withdrawal_date_entry.setDisplayFormat('dd/MM/yyyy')
        self.withdrawal_date_entry.setDate(QDate.currentDate())
        self.withdrawal_date_entry.setCalendarPopup(True)
        form_layout.addWidget(self.withdrawal_date_label)
        form_layout.addWidget(self.withdrawal_date_entry)

        # Button to add investment
        self.add_button = QPushButton('Adicionar Investimento')
        self.add_button.clicked.connect(self.add_investment)
        button_layout.addWidget(self.add_button)

        # Table to display investments
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(
            ['Valor', 'Data do Depósito', 'Data de Retirada']
        )
        table_layout.addWidget(self.table)

        # Add layouts to main layout
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(table_layout)

        self.setLayout(main_layout)

        # In-memory storage for investment data
        self.investments = data.get_investiments()

    def format_amount(self) -> None:
        try:
            num: float = calcs.brl_to_float(self.amount_entry.text())
            text: str = calcs.float_to_brl(num)
        except ValueError:
            text = self.amount_entry.text()[:-1]

        self.amount_entry.blockSignals(True)
        self.amount_entry.setText(text)
        self.amount_entry.blockSignals(False)

    def add_investment(self) -> None:
        amount = self.amount_entry.text()
        deposit_date = self.deposit_date_entry.text()
        withdrawal_date = self.withdrawal_date_entry.text()

        if not amount or not deposit_date:
            QMessageBox.critical(
                self, 'Erro', 'Por favor, preencha todos os campos obrigatórios.'
            )
            return

        new_data = {
            'Valor': amount,
            'Data do Depósito': deposit_date,
            'Data de Retirada': withdrawal_date,
        }

        self.investments = data.add_row('investimento', **new_data)
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        for i, item in enumerate(new_data.values()):
            self.table.setItem(row_position, i, QTableWidgetItem(str(item)))

        # Clear the entry fields
        self.amount_entry.clear()
        self.deposit_date_entry.setDate(QDate.currentDate())
        self.withdrawal_date_entry.setDate(QDate.currentDate())


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = InvestmentApp()
    window.show()
    app.exec()
