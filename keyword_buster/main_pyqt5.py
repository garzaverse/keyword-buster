import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt

# e.g., ?hin d?sk to?s ye? rel?cate co?bine

class GridApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Grid Navigation")
        self.setGeometry(100, 100, 400, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.grid_layout = QGridLayout()
        self.central_widget.setLayout(self.grid_layout)

        self.upper_grid_widget = QWidget()
        self.lower_grid_widget = QWidget()

        self.upper_grid_layout = QGridLayout()
        self.lower_grid_layout = QGridLayout()

        self.upper_grid_widget.setLayout(self.upper_grid_layout)
        self.lower_grid_widget.setLayout(self.lower_grid_layout)

        self.grid_layout.addWidget(self.upper_grid_widget, 0, 0, Qt.AlignCenter)
        self.grid_layout.addWidget(self.lower_grid_widget, 1, 0, Qt.AlignCenter)

        self.upper_grid = [[None for _ in range(8)] for _ in range(8)]
        self.lower_grid = [[None for _ in range(8)] for _ in range(8)]

        self.selected_grid = 1
        self.current_cell = [0, 0]
        self.create_grids()

        self.update_selection()

    def create_grids(self):
        """Create labels for both upper and lower grids."""
        for r in range(8):
            for c in range(8):
                self.upper_grid[r][c] = QLabel("", self)
                self.upper_grid[r][c].setFixedSize(40, 40)
                self.upper_grid[r][c].setFont(QFont('Arial', 16))
                self.upper_grid[r][c].setAlignment(Qt.AlignCenter)
                self.upper_grid[r][c].setAutoFillBackground(True)
                self.upper_grid_layout.addWidget(self.upper_grid[r][c], r, c)

                self.lower_grid[r][c] = QLabel("", self)
                self.lower_grid[r][c].setFixedSize(40, 40)
                self.lower_grid[r][c].setFont(QFont('Arial', 16))
                self.lower_grid[r][c].setAlignment(Qt.AlignCenter)
                self.lower_grid[r][c].setAutoFillBackground(True)
                self.lower_grid_layout.addWidget(self.lower_grid[r][c], r, c)

    def update_selection(self):
        """Update the background color of selected cell."""
        for r in range(8):
            for c in range(8):
                self.upper_grid[r][c].setStyleSheet("background-color: white;")
                self.lower_grid[r][c].setStyleSheet("background-color: white;")

        if self.selected_grid == 1:
            self.upper_grid[self.current_cell[0]][self.current_cell[1]].setStyleSheet("background-color: blue;")
        else:
            self.lower_grid[self.current_cell[0]][self.current_cell[1]].setStyleSheet("background-color: blue;")

    def keyPressEvent(self, event):
        """Handle key press events to navigate and quit."""
        if event.key() == Qt.Key_1:
            self.selected_grid = 1
        elif event.key() == Qt.Key_2:
            self.selected_grid = 2
        elif event.key() == Qt.Key_Q:
            self.close()  # Quit the program
        elif event.key() == Qt.Key_Left:
            self.current_cell[1] = (self.current_cell[1] - 1) % 8
        elif event.key() == Qt.Key_Right:
            self.current_cell[1] = (self.current_cell[1] + 1) % 8
        elif event.key() == Qt.Key_Up:
            self.current_cell[0] = (self.current_cell[0] - 1) % 8
        elif event.key() == Qt.Key_Down:
            self.current_cell[0] = (self.current_cell[0] + 1) % 8

        self.update_selection()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GridApp()
    window.show()
    sys.exit(app.exec_())
