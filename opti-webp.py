import ctypes
import sys
import os
import re
import tkinter as tk
import argparse
from tkinter import filedialog, simpledialog
from PIL import Image

# Constants
VERSION = "1.1"

# Params
# directory
# output dir 
# resize max
# keep resized pngs
# webflow filenames 


def set_console_title():
    ctypes.windll.kernel32.SetConsoleTitleW(f"Opti-WebP {VERSION}")

def display_initial_message():
    print(f"Opti-WebP {VERSION} - Image Optimization Tool")
    print("Opti-WebP will bulk resize, compress and convert non WebP images to an optimized WebP final version.")
    print("It will also rename the result to a Webflow asset-compatible filename.")
    print("Created by John Large aka bloom")
    print("Website: https://studiobloom.xyz")
    print("If this tool helps you, please consider donating:\n$studiobloomxyz on cash app, paypal.me/studiobloomxyz\nBTC @ 33bhGfzcKekYh8oB31Jzv5FYUkdahyC3eA\nETH @ 0xD974b9ab6e897d1128F2aFe98Aa172dE8180D27E")
    print("\n")

def display_instructions():    
    print("Choose the directory of the image(s) to be optimized.\nProceed through the following window prompts.")

def select_directory():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory()
    return directory

def get_icon_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'opti-webp.ico')
    else:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'opti-webp.ico')

class MaxDimensionSizeDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Max Dimension Size")
        self.iconbitmap(get_icon_path())
        self.geometry("300x250")
        self.resizable(False, False)

        self.max_dimension_size = None
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Limit max width/height of image(s).\nAspect Ratio will remain locked.\n(between 500px-4000px is suggested)\nEnter the maximum dimension size:")
        label.pack(pady=10)

        self.entry = tk.Entry(self)
        if settings.max_size:
            self.entry.insert(0, settings.max_size) # set a default
        self.entry.pack()

        button = tk.Button(self, text="OK", command=self.set_max_dimension_size)
        button.pack(pady=10)
        
    def set_max_dimension_size(self):
        try:
            self.max_dimension_size = int(self.entry.get())
        except ValueError:
            pass
        self.destroy()
        
def get_max_dimension_size():
    root = tk.Tk()
    root.withdraw()
    dialog = MaxDimensionSizeDialog(root)
    root.wait_window(dialog)
    return dialog.max_dimension_size

def count_images(directory):
    image_count = sum([filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".heic", ".tiff", ".tif")) for filename in os.listdir(directory)])
    print(f"Optimizable Images found in directory: {image_count}")
    return image_count

def generate_webp_filename(original_filename):
    base = os.path.splitext(original_filename)[0]
    if settings.webflow:
        # rename to Webflow asset-compatible names
        # https://university.webflow.com/lesson/assets-panel#how-to-name-assets
        sanitized_name = re.sub(r'[^a-zA-Z0-9_-]', '_', base)
        max_length = 94
        base = sanitized_name[:max_length]
    return base + ".webp"

def resize_and_convert(directory, max_dimension_size):
    image_count = count_images(directory)
    if image_count == 0:
        print("No optimizable images found.")
        return

    print(f"Processing images in directory: {directory}")
    for filename in os.listdir(directory):
        try:
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".heic", ".tiff", ".tif")):
                print(f"Processing image: {filename}")

                img = Image.open(os.path.join(directory, filename))

                # Resize to max_size (optional)
                if not max_dimension_size is None:
                    img.thumbnail((max_dimension_size, max_dimension_size))

                    # Save as PNG
                    # Make this a configurable option, or cmdline param 
                    new_filename = os.path.splitext(filename)[0] + "_resized.png"
                    img.save(os.path.join(settings.output_directory, new_filename), "PNG", optimize=True)
                    print(f"Saved resized image as: {new_filename}")

                # Convert to WebP
                webp_filename = generate_webp_filename(os.path.splitext(filename)[0])
#                webp_filename = os.path.splitext(filename)[0] + ".webp"
                img.save(os.path.join(settings.output_directory, webp_filename), "WEBP")
                print(f"Converted image to WebP: {webp_filename}")

                # Delete resized PNG file
                if not max_dimension_size is None:
                    os.remove(os.path.join(directory, new_filename))
                    print(f"Deleted resized image: {new_filename}")

        except Exception as e:
            print(f"An error occurred while processing image {filename}: {e}")


def init_settings():

    # Parse arguments
    parser = argparse.ArgumentParser(description=f'These are the command line arguments for Opti-WebP {VERSION}.')

    # Add arguments
    parser.add_argument('directory', type=str, nargs='?', help="input directory")
    parser.add_argument('-a', '--auto', action='store_true', help="run in automatic mode")
    parser.add_argument('-w', '--webflow', action='store_true', help="rename the files for Webflow asset compatability")
    parser.add_argument('-o', '--out', type=str, dest="output_directory", help="output to the specified directory, instead of the source file's directory")
    parser.add_argument('-m', '--maxsize', type=int, default=None, dest='max_size', help="resize to fit in maximum dimensions, preserving aspect ratio")

    # Parse the arguments
    args = parser.parse_args()

    # Set outputDirectory to directory value if not specified
    if not args.output_directory:
        args.output_directory = args.directory

    print("Input Directory:", args.directory)
    print("Output Directory:", args.output_directory)
    print("Rename for Webflow?", args.webflow)
    print("Max Dimensions Size:", args.max_size)
    print("Max Dimensions Size:", args.max_size)
    print("\n")

    if not args.directory:
        args.interactive = True

    return args



def run_main():

    # Get the input directory
    directory = settings.directory # sys.argv[1]
    if not directory:
        directory = select_directory()
    if not directory:
        print("Error: A directory is required.")
        sys.exit(1)

    # Get the max width
    max_dimension_size = settings.max_size
    if not settings.auto:
        max_dimension_size = get_max_dimension_size()
    resize_and_convert(directory, max_dimension_size)



if __name__ == "__main__":

    set_console_title()
    display_initial_message()
    settings = init_settings()
    display_instructions()

    run_main()
 
    # Keep the command window open and prompt the user to restart
    if not settings.auto:
        while True:
            user_input = input("Your conversion is now complete, thank you for using Opti-WebP:)\nType 'r' to run the script again, or press enter to exit:")
            if user_input.lower() == "r":
                set_console_title()
                run_main()
            else:
                break
