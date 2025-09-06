# Wallpaper Changer

Wallpaper Changer is a desktop application for Windows that automatically changes your desktop wallpaper at a set interval. You can select a folder of your favorite images, set the change frequency, and choose to have the images shuffle randomly. The application is built with Python using `CustomTkinter` for the GUI and `pystray` for system tray functionality.

> I wrote this because the slideshow feature on Windows keeps stopping randomly, and they haven't bothered to fix it. Unlike similar apps, this one is very lightweight and resource-friendly.

## Usage

If you just want to use it, download the `wallpaper_changer.exe` from the releases and run it, otherwise, if you want to run it with Python or build it yourself, follow the instructions below.

## Prerequisites

-  Windows operating system 
Python 3.x 
- Required Python libraries:
    
    - `customtkinter`
    - `pystray`
    - `Pillow`
        

## Installation

1. Clone this repository or download the source code.
2. Install the required packages using pip:
    
    ```shell
    pip install customtkinter pystray Pillow
    ```

## Building an Executable

The `wallpaper_changer.spec` file is used with `PyInstaller` to create a standalone executable for Windows.

1. Install PyInstaller:
    
    ```shell
    pip install PyInstaller
    ```
2. Run PyInstaller from the project directory:
    ```shell
    pyinstaller wallpaper_changer.spec
    ```
3. The executable will be located in the `dist` folder.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
