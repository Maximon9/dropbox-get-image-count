from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout


def on_button_click():
    print("Button clicked!")


# Create the application object
app = QApplication([])

# Create the main window
window = QWidget()
window.setWindowTitle("PyQt Example")
window.setGeometry(100, 100, 300, 200)

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
app.exec_()
