from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
)
from PyQt6.QtGui import QScreen


def on_button_click():
    print("Button clicked!")


# Create the application object
app = QApplication([])

# Create the main window
window = QWidget()
window.setWindowTitle("Getting Count of DropBox Files")

# Get the screen dimensions
screen = app.primaryScreen()  # Get the primary screen (main monitor)
screen_geometry = (
    screen.availableGeometry()
)  # Get the screen's geometry (x, y, width, height)
screen_width = screen_geometry.width()
screen_height = screen_geometry.height()

width = 1280
height = 720
x = (screen_width - width) // 2
y = (screen_height - height) // 2
window.setGeometry(x, y, width, height)

# Create a button and connect it to a function
button = QPushButton("Click Me")
button.clicked.connect(on_button_click)

# Create a layout and add the button
layout = QVBoxLayout()
layout.addWidget(button)

# Set the layout for the window
window.setLayout(layout)

# Show the window
window.show()

# Run the application event loop
app.exec()
