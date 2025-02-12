from PyQt6.QtWidgets import QApplication  # type: ignore

from front import InvestmentApp


def main() -> None:
    app = QApplication([])
    window = InvestmentApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
