from PyQt6 import QtWidgets as qw  # type: ignore
from PyQt6.QtCore import QDate  # type: ignore

from calcs import brl_to_float, float_to_brl
from data import Investments


class InvestmentApp(qw.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Investment Tracker')

        # Layouts
        main_layout = qw.QVBoxLayout()
        form_layout = qw.QHBoxLayout()
        button_layout = qw.QHBoxLayout()
        table_layout = qw.QVBoxLayout()

        # Labels and Entry widgets for input
        self.amount_label = qw.QLabel('Valor do Depósito:')
        self.amount_entry = qw.QLineEdit()
        self.amount_entry.setText('R$ 0,00')
        self.amount_entry.textChanged.connect(self.format_amount)
        form_layout.addWidget(self.amount_label)
        form_layout.addWidget(self.amount_entry)

        self.deposit_date_label = qw.QLabel('Data do Depósito:')
        self.deposit_date_entry = qw.QDateEdit()
        self.deposit_date_entry.setDisplayFormat('dd/MM/yyyy')
        self.deposit_date_entry.setDate(QDate.currentDate())
        self.deposit_date_entry.setCalendarPopup(True)
        form_layout.addWidget(self.deposit_date_label)
        form_layout.addWidget(self.deposit_date_entry)

        self.withdrawal_date_label = qw.QLabel('Data de Retirada:')
        self.withdrawal_date_entry = qw.QDateEdit(QDate.currentDate())
        self.withdrawal_date_entry.setDisplayFormat('dd/MM/yyyy')
        self.withdrawal_date_entry.setDate(QDate.currentDate())
        self.withdrawal_date_entry.setCalendarPopup(True)
        form_layout.addWidget(self.withdrawal_date_label)
        form_layout.addWidget(self.withdrawal_date_entry)

        # Button to add investment
        self.add_button = qw.QPushButton('Adicionar Investimento')
        self.add_button.clicked.connect(self.add_investment)
        button_layout.addWidget(self.add_button)

        # Table to display investments
        self.table = qw.QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(
            ['Valor', 'Data do Depósito', 'Data de Retirada']
        )
        table_layout.addWidget(self.table)

        # Add layouts to main layout
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(table_layout)

        self.setLayout(main_layout)

        self.investments = Investments()
        self.load_initial_data()

    def load_initial_data(self) -> None:
        for index, row in self.investments.data.iterrows():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for i, item in enumerate(row):
                self.table.setItem(row_position, i, qw.QTableWidgetItem(str(item)))

    def format_amount(self) -> None:
        try:
            num: float = brl_to_float(self.amount_entry.text())
            text: str = float_to_brl(num)
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
            qw.QMessageBox.critical(
                self, 'Erro', 'Por favor, preencha todos os campos obrigatórios.'
            )
            return

        new_data = {
            'Valor': amount,
            'Data do Depósito': deposit_date,
            'Data da Retirada': withdrawal_date,
        }

        self.investments.add_row(**new_data)
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        for i, item in enumerate(new_data.values()):
            self.table.setItem(row_position, i, qw.QTableWidgetItem(str(item)))

        # Clear the entry fields
        self.amount_entry.clear()
        self.deposit_date_entry.setDate(QDate.currentDate())
        self.withdrawal_date_entry.setDate(QDate.currentDate())
