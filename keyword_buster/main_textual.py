import sys
import argparse
import logging
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Static

# Initialize logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

FG_COLOUR = "#000000"  # Foreground color (black text)
BG_COLOUR = "#FFFFFF"  # Background color (white background)
SELECTED_COLOUR = "#0000FF"  # Selected cell background color (blue)
SELECTED_TEXT_COLOUR = "#FFFFFF"  # Selected cell text color (white)


class GridApp(App):
    CSS_PATH = "grid.css"

    def __init__(self, dict_words, arg_words):
        super().__init__()
        self.dict_words = dict_words
        self.arg_words = [word.upper() for word in arg_words]

        # Align the words vertically within the constructor
        self.arg_words_aligned = self._align_words(self.arg_words)

        # Generate the column-major order aligned array
        self.cli_args_aligned_array = self._create_cli_args_aligned_array(self.arg_words_aligned)

        # Determine the dimensions of the aligned array
        self.cli_args_longest = len(self.cli_args_aligned_array) if self.cli_args_aligned_array else 0
        self.cli_args_count = len(self.cli_args_aligned_array[0]) if self.cli_args_longest > 0 else 0

        self.selected_grid = 1
        self.current_cell = [0, 0]

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
                    cli_args_aligned_array[r][c] = ' '

        # Log the array for debugging purposes
        logger.debug("CLI Arguments Aligned Array (Column-Major Order):")
        for row in cli_args_aligned_array:
            logger.debug("".join(row))

        return cli_args_aligned_array

    def compose(self) -> ComposeResult:
        """Create and populate labels for both upper and lower grids."""
        upper_grid_container = Vertical(id="upper-grid")
        lower_grid_container = Vertical(id="lower-grid")

        # Yield containers first to ensure they are mounted before adding children
        yield upper_grid_container
        yield lower_grid_container

        self.upper_grid = [[None for _ in range(self.cli_args_count)] for _ in range(self.cli_args_longest)]
        self.lower_grid = [[None for _ in range(self.cli_args_count)] for _ in range(8)]

        upper_grid_container.mount(self._create_grid(self.upper_grid, self.cli_args_longest, self.cli_args_count,
                                                     self.cli_args_aligned_array))

        lower_grid_container.mount(self._create_grid(self.lower_grid, 8, self.cli_args_count, self.arg_words))

        self.update_selection()

    def _create_grid(self, grid, row_count, column_count, content):
        """Create a grid with specified rows, columns, and content."""
        container = Vertical()
        for r in range(row_count):
            row = Horizontal()
            container.mount(row)
            for c in range(column_count):
                cell_content = content[r][c] if isinstance(content[0], list) else (content[c] if r == 0 else "")
                grid[r][c] = Static(cell_content, classes="grid-cell")
                row.mount(grid[r][c])
        return container

    def update_selection(self):
        """Update the background color of the selected cell."""
        for r in range(self.cli_args_longest):
            for c in range(self.cli_args_count):
                self.upper_grid[r][c].remove_class("selected")

        for r in range(8):
            for c in range(self.cli_args_count):
                self.lower_grid[r][c].remove_class("selected")

        if self.selected_grid == 1 and self.cli_args_count > 0 and self.cli_args_longest > 0:
            self.upper_grid[self.current_cell[0]][self.current_cell[1]].add_class("selected")
        else:
            self.lower_grid[self.current_cell[0]][self.current_cell[1]].add_class("selected")

    def on_key(self, event):
        """Handle key press events to navigate and quit."""
        match event.key:
            case "1":
                self.selected_grid = 1
            case "2":
                self.selected_grid = 2
            case "q":
                self.exit()  # Quit the program
            case "left":
                self.current_cell[1] = (self.current_cell[1] - 1) % self.cli_args_count
            case "right":
                self.current_cell[1] = (self.current_cell[1] + 1) % self.cli_args_count
            case "up":
                self.current_cell[0] = (self.current_cell[0] - 1) % (
                    self.cli_args_longest if self.selected_grid == 1 else 8)
            case "down":
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
    app = GridApp(dict_words, args.words)
    app.run()


if __name__ == "__main__":
    main()
