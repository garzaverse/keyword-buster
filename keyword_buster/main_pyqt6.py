import sys
import argparse
import logging
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt

# Initialize logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

FG_COLOUR = "#000000"  # Foreground color (black text)
BG_COLOUR = "#FFFFFF"  # Background color (white background)


class GridApp(QMainWindow):
    def __init__(self, dict_words, arg_words):
        super().__init__()
        self.dict_words = dict_words
        self.arg_words = [word.upper() for word in arg_words]

        # Align the words vertically within the constructor
        self.arg_words_aligned = self._align_words(self.arg_words)

        # Generate the column-major order aligned array
        self.cli_args_aligned_array = self._create_cli_args_aligned_array(self.arg_words_aligned)

        # Determine the dimensions of the aligned array
        self.cli_args_longest = len(self.cli_args_aligned_array)
        self.cli_args_count = len(self.cli_args_aligned_array[0]) if self.cli_args_aligned_array else 0

        self.setWindowTitle("Grid Navigation")
        self.setGeometry(100, 100, 800, 600)

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

        self.grid_layout.addWidget(self.upper_grid_widget, 0, 0, Qt.AlignmentFlag.AlignCenter)
        self.grid_layout.addWidget(self.lower_grid_widget, 1, 0, Qt.AlignmentFlag.AlignCenter)

        self.upper_grid = [[None for _ in range(self.cli_args_count)] for _ in range(self.cli_args_longest)]
        self.lower_grid = [[None for _ in range(self.cli_args_count)] for _ in range(8)]

        self.selected_grid = 1
        self.current_cell = [0, 0]
        self.create_grids()

        self.update_selection()

    def _align_words(self, arg_words):
        """Align words vertically such that all '?' align in the same row."""
        if not arg_words:
            return []

        max_index = max(word.index('?') for word in arg_words if '?' in word)
        max_length = max(map(len, arg_words))

        aligned_words = []

        for word in arg_words:
            before_question = word[:word.index('?')]
            after_question = word[word.index('?') + 1:]

            # Create aligned string maintaining the same length
            padded_word = ' ' * (max_index - len(before_question)) + word + ' ' * (
                    max_length - len(after_question) - len(word[:word.index('?') + 1]))
            aligned_words.append(padded_word)

        for word in aligned_words:
            logger.debug(f"Aligned word: {word}")

        return aligned_words

    def _create_cli_args_aligned_array(self, arg_words_aligned):
        """Create a column-major order array from the aligned CLI arguments."""
        cli_args_longest = max(map(len, arg_words_aligned), default=0)
        cli_args_count = len(arg_words_aligned)

        # Initialize empty 2D array
        cli_args_aligned_array = [[" " for _ in range(cli_args_count)] for _ in range(cli_args_longest)]

        # Populate the array in column-major order
        for c in range(cli_args_count):
            word = arg_words_aligned[c]
            for r in range(cli_args_longest):
                if r < len(word):
                    cli_args_aligned_array[r][c] = word[r]
                else:
                    cli_args_aligned_array[r][c] = " "

        # Log the array for debugging purposes
        logger.debug("CLI Arguments Aligned Array (Column-Major Order):")
        for row in cli_args_aligned_array:
            logger.debug("".join(row))

        return cli_args_aligned_array

    def create_grids(self):
        """Create and populate labels for both upper and lower grids."""
        for c in range(self.cli_args_count):
            for r in range(self.cli_args_longest):
                self.upper_grid[r][c] = QLabel("", self)
                self.upper_grid[r][c].setFixedSize(40, 40)
                self.upper_grid[r][c].setFont(QFont('Arial', 16))
                self.upper_grid[r][c].setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.upper_grid[r][c].setAutoFillBackground(True)
                palette = self.upper_grid[r][c].palette()
                palette.setColor(QPalette.ColorRole.WindowText, QColor(FG_COLOUR))
                palette.setColor(QPalette.ColorRole.Window, QColor(BG_COLOUR))
                self.upper_grid[r][c].setPalette(palette)
                self.upper_grid[r][c].setText(self.cli_args_aligned_array[r][c])
                self.upper_grid[r][c].setStyleSheet(f"background-color: {BG_COLOUR}; color: {FG_COLOUR};")
                self.upper_grid_layout.addWidget(self.upper_grid[r][c], r, c)

        for r in range(8):
            for c in range(self.cli_args_count):
                self.lower_grid[r][c] = QLabel("", self)
                word = self.arg_words[c] if r == 0 and c < len(self.arg_words) else ""
                self.lower_grid[r][c].setText(word)
                # Calculate the required width dynamically for each word
                required_width = 10 * len(word) + 20
                self.lower_grid[r][c].setFixedSize(required_width, 40)  # Make the cell wide enough for the word
                self.lower_grid[r][c].setFont(QFont('Arial', 16))
                self.lower_grid[r][c].setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.lower_grid[r][c].setAutoFillBackground(True)
                palette = self.lower_grid[r][c].palette()
                palette.setColor(QPalette.ColorRole.WindowText, QColor(FG_COLOUR))
                palette.setColor(QPalette.ColorRole.Window, QColor(BG_COLOUR))
                self.lower_grid[r][c].setPalette(palette)
                self.lower_grid[r][c].setStyleSheet(f"background-color: {BG_COLOUR}; color: {FG_COLOUR};")
                self.lower_grid_layout.addWidget(self.lower_grid[r][c], r, c)

    def update_selection(self):
        """Update the background color of the selected cell."""
        for c in range(self.cli_args_count):
            for r in range(self.cli_args_longest):
                self.upper_grid[r][c].setStyleSheet(f"background-color: {BG_COLOUR}; color: {FG_COLOUR};")

        for r in range(8):
            for c in range(self.cli_args_count):
                self.lower_grid[r][c].setStyleSheet(f"background-color: {BG_COLOUR}; color: {FG_COLOUR};")

        if self.selected_grid == 1 and self.cli_args_count > 0 and self.cli_args_longest > 0:
            self.upper_grid[self.current_cell[0]][self.current_cell[1]].setStyleSheet(
                "background-color: blue; color: white;")
        else:
            self.lower_grid[self.current_cell[0]][self.current_cell[1]].setStyleSheet(
                "background-color: blue; color: white;")

    def keyPressEvent(self, event):
        """Handle key press events to navigate and quit."""
        if event.key() == Qt.Key.Key_1:
            self.selected_grid = 1
        elif event.key() == Qt.Key.Key_2:
            self.selected_grid = 2
        elif event.key() == Qt.Key.Key_Q:
            self.close()  # Quit the program
        elif event.key() == Qt.Key.Key_Left:
            self.current_cell[1] = (self.current_cell[1] - 1) % self.cli_args_count
        elif event.key() == Qt.Key.Key_Right:
            self.current_cell[1] = (self.current_cell[1] + 1) % self.cli_args_count
        elif event.key() == Qt.Key.Key_Up:
            self.current_cell[0] = (self.current_cell[0] - 1) % (
                self.cli_args_longest if self.selected_grid == 1 else 8)
        elif event.key() == Qt.Key.Key_Down:
            self.current_cell[0] = (self.current_cell[0] + 1) % (
                self.cli_args_longest if self.selected_grid == 1 else 8)

        self.update_selection()

        # Log the word in the current column when navigating left or right
        if self.selected_grid == 1 and self.cli_args_count > 0 and self.cli_args_longest > 0:
            current_column = self.current_cell[1]
            current_word = self.arg_words[current_column] if current_column < len(self.arg_words) else ""
            logger.debug(f"Current word in column {current_column}: {current_word}")


def read_words_from_file(file_path):
    """Reads words from a file and returns them as a list."""
    with open(file_path, 'r') as file:
        words = file.read().splitlines()
    words = [word.upper() for word in words]
    return words


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Grid Navigation Program')
    parser.add_argument('words', nargs='*', help='Words to be added to the list')
    args = parser.parse_args()

    # Read words from the file
    dict_words = read_words_from_file('/srv/dict/words_alpha.txt')

    # Create and run the application
    app = QApplication(sys.argv)
    window = GridApp(dict_words, args.words)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
