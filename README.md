# Opti-WebP

Opti-WebP is an image optimization tool that enables bulk resizing, compression, and conversion of non-WebP 
images to an optimized WebP format. It helps reduce image file sizes while maintaining visual quality, making 
it suitable for web development and optimization tasks.

## Installation

-You can download the latest release: [Latest Release](https://github.com/studiobloom/opti-webp/releases/latest)

-OR you can download this repo and run the .exe, or simply run the opti-webp.py program yourself although you 
are likely to require downloading some additional libraries and you should remove the icon function.

## Features

- Bulk resize, compress, and convert non-WebP images to WebP format.
- Limit the maximum width/height of images while preserving aspect ratio.
- Supports various image formats, including PNG, JPEG, GIF, BMP, HEIC, TIFF, and TIF.
- Optimized images are saved as WebP format, providing smaller file sizes.
- Easy-to-use GUI for selecting the target directory and configuring the max dimension size.
- Specify multiple files, or an entire directory to process
- Name your WEBP's using Webflow asset-compliant names, for easier upload
- Runs in interactive mode, or auto mode for batch-file use

## Usage

1. Download the latest release from the [Releases](https://github.com/studiobloom/opti-webp/releases) page.
2. Extract the contents of the release package.
3. Run the `opti-webp.exe` executable.
4. Choose the directory containing the images you want to optimize.
5. Set the maximum dimension size (width/height) for the images. (500px-4000px is suggested)
6. Click the "OK" button to start the optimization process.
7. Opti-WebP will resize, compress, and convert the images to WebP format.
8. The optimized images will be saved in the same directory with "_resized.png" and ".webp" extensions.
9. Once the optimization process is complete, you can find the optimized images in the target directory.

## Command Line Options

- `-h` or `--help` for Help to list these options
- `<filename> ...` to specify one or more filenames on the command line
- `-d <directory>` or `--dir <directory>` to specify a full directory to process
- `-m <number>` or `--maxsize <number>` to specify maximum bounding box dimensions, in pixels
- `-w` or `--webflow` to generate your WEBP's with Webflow asset-compatible filenames
- `-o <directory>` or `--out <directory>` to specify a different output directory
- `-a` or `--auto` for auto mode, which will run with no prompting

## Credits

Opti-WebP is created by John Large (aka bloom) and is available at [GitHub](https://github.com/studiobloom/opti-webp). 
Visit the [website](https://studiobloom.xyz) for more information and updates.

Automation enhancements by Michael Wells (aka memetican).

## License

This project is licensed under the [MIT License](LICENSE).
