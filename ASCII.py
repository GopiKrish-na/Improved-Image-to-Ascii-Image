from PIL import Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QTextEdit, QFileDialog
from PyQt5.QtGui import QPixmap

# Define the ASCII characters to use
ascii_chars = ['@', '%', '#', '*', '+', '=', '-', ':', '.', ' ']

# Define the function to convert an image to ASCII art and display it in the GUI
def convert_to_ascii():
    # Open the selected image file
    file_path, _ = QFileDialog.getOpenFileName()
    if file_path:
        image = Image.open(file_path)

        # Resize the image to a smaller size
        width, height = image.size
        aspect_ratio = height/width
        new_width = 200
        new_height = int(aspect_ratio * new_width * 0.5)
        resized_image = image.resize((new_width, new_height))

        # Convert the image to grayscale
        grayscale_image = resized_image.convert('L')

        # Compute the step size based on the full range of brightness values
        min_brightness = 0
        max_brightness = 255
        num_steps = len(ascii_chars)
        step_size = (max_brightness - min_brightness) / num_steps
        # Handle edge cases where step size is zero or out of range
        if step_size == 0:
            step_size = 1
        elif step_size > (max_brightness - min_brightness):
            step_size = (max_brightness - min_brightness) / len(ascii_chars)


        # Convert each pixel to an ASCII character based on its brightness
        ascii_art = ""
        for y in range(new_height):
            for x in range(new_width):
                pixel_brightness = grayscale_image.getpixel((x, y))
                ascii_index = int((pixel_brightness - min_brightness) / step_size)
                
                # Handle edge cases where ASCII index is out of range
                if ascii_index >= len(ascii_chars):
                    ascii_index = len(ascii_chars) - 1
                ascii_art += ascii_chars[ascii_index]
            ascii_art += "\n"

        # Display the ASCII art in the GUI
        ascii_text.clear()
        ascii_text.insertPlainText(ascii_art)


# Create the GUI
app = QApplication([])
window = QMainWindow()
window.setWindowTitle("Image to ASCII Art Converter")

# Add a label to display the selected image
image_label = QLabel(window)
image_label.setGeometry(10, 10, 200, 200)

# Add a button to select an image file
select_button = QPushButton("Select Image File", window)
select_button.setGeometry(10, 220, 150, 30)
select_button.clicked.connect(convert_to_ascii)

# Add a text widget to display the ASCII art
ascii_text = QTextEdit(window)
ascii_text.setGeometry(220, 10, 600, 600)

# Maximize the window
window.showMaximized()

# Start the GUI event loop
app.exec_()

