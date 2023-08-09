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

def select_files():
    root = tk.Tk()
    root.withdraw()

    file_types = [
        ("Processable files", "*.jpg *.jpeg *.png *.gif *.bmp *.heic *.tif *.tiff"),
        ("JPEG files", "*.jpg *.jpeg"),
        ("PNG files", "*.png"),
        ("GIF files", "*.gif"),
        ("BMP files", "*.bmp"),
        ("HEIC files", "*.heic"),
        ("TIFF files", "*.tif *.tiff"),
        ("All files", "*.*")
    ]

    file_paths = filedialog.askopenfilenames(title="Select the files you want", filetypes=file_types)

    return file_paths

def get_exe_dir():
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))

def get_icon_path():
    return os.path.join(get_exe_dir(), 'opti-webp.ico')


class MaxDimensionSizeDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Max Dimension Size")
#        self.iconbitmap(get_icon_path())
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

# Given a filename, return a Webflow-friendly WEBP filename, no path
def generate_webp_filename(original_filename):
    base = os.path.basename(original_filename)
    base = os.path.splitext(original_filename)[0]
    if settings.webflow:
        # rename to Webflow asset-compatible names
        # https://university.webflow.com/lesson/assets-panel#how-to-name-assets
        sanitized_name = re.sub(r'[^a-zA-Z0-9_-]', '_', base)
        max_length = 94
        base = sanitized_name[:max_length]
    return base + ".webp"

def resize_and_convert(filenames, max_dimension_size):
    if not filenames:
        print("No optimizable images found.")
        return

    print(f"Processing {len(filenames)} images:")
    for filename in filenames: # os.listdir(directory):
        try:
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".heic", ".tiff", ".tif")):
                print(f"Processing image: {filename}")

                # Parse filename
                img = Image.open(filename)
                filename_base = os.path.splitext(os.path.basename(filename))[0]
                filename_path = os.path.dirname(filename)
                output_path = filename_path
                if settings.output_directory:
                    output_path = settings.output_directory

                # Resize to max_size (optional)
                if not max_dimension_size is None:
                    img.thumbnail((max_dimension_size, max_dimension_size))

                    # Save as PNG
                    new_filename = filename_base + "_resized.png"
                    img.save(os.path.join(output_path, new_filename), "PNG", optimize=True)
                    print(f"Saved resized image as: {new_filename}")

                # Convert to WebP
                webp_filename = generate_webp_filename(filename_base)
                img.save(os.path.join(output_path, webp_filename), "WEBP")
                print(f"Converted image to WebP: {webp_filename}")

                # Delete resized PNG file
                if not max_dimension_size is None:
                    os.remove(os.path.join(output_path, new_filename))
                    print(f"Deleted resized image: {new_filename}")

        except Exception as e:
            print(f"An error occurred while processing image {filename}: {e}")


def init_settings():

    # Parse arguments
    parser = argparse.ArgumentParser(description=f'These are the command line arguments for Opti-WebP {VERSION}.')

    # Add arguments
    parser.add_argument('filenames', metavar='F', type=str, nargs='*', help='a list of filenames to process (in auto mode)')
    parser.add_argument('-d', '--dir', dest='directory', type=str, help="process all compatible files in this input directory (in auto mode)")
    parser.add_argument('-a', '--auto', action='store_true', help="run in automatic mode")
    parser.add_argument('-w', '--webflow', action='store_true', help="rename the files for Webflow asset compatability")
    parser.add_argument('-o', '--out', type=str, dest="output_directory", default=None, help="output to the specified directory, instead of the source file's directory")
    parser.add_argument('-m', '--maxsize', type=int, default=None, dest='max_size', help="resize to fit in maximum dimensions, preserving aspect ratio")

    # Parse the arguments
    args = parser.parse_args()

    print("INITIAL SETTINGS:")
    print("Files", args.filenames)
    print("Input Directory:", args.directory)
    print("Output Directory:", args.output_directory)
    print("Rename for Webflow?", args.webflow)
    print("Max Dimensions Size:", args.max_size)
    print("\n")

    if not args.directory:
        args.interactive = True

    return args




def add_directory_files(directory):
    print(f"Processing images in directory: {directory}")
    for filename in os.listdir(directory):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".heic", ".tiff", ".tif")):
            settings.filenames.append(os.path.join(directory, filename))  # Append the full path of the file




def run_main():

    # Manual mode
    if not settings.auto:
        # Get list of filenames to process
        settings.filenames = select_files()

    # Auto mode
    if settings.auto:
        # Filenames have been automatically added by params
        # Process a directory and add those files, if one is specified
        if settings.directory:
            add_directory_files(settings.directory)


    # Validate settings
    if not settings.filenames:
        print("Error: At least one file or directory is required.")
        sys.exit(1)

    # Get the max width (optional)
    max_dimension_size = settings.max_size
    if not settings.auto:
        max_dimension_size = get_max_dimension_size()
    resize_and_convert(settings.filenames, max_dimension_size)




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
