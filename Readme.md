# Wallpaper Changer

Wallpaper Changer is a desktop application for Windows that automatically changes your desktop wallpaper at a set interval. You can select a folder of your favorite images, set the change frequency, and choose to have the images shuffle randomly. The application is built with Python using `CustomTkinter` for the GUI and `pystray` for system tray functionality.

> I wrote this because the slideshow feature on Windows keeps stopping randomly, and they haven't bothered to fix it. Unlike similar apps, this one is very lightweight and resource-friendly.

## Features

- **Automatic Wallpaper Cycling:** Automatically changes your desktop wallpaper from a selected folder. 
- **Customizable Interval:** Set the time interval for changing wallpapers in seconds, minutes, or hours.
- **Randomize Order:** Shuffle the order of the wallpapers for a new look every time. 
- **System Tray Integration:** Minimize the application to the system tray to run it in the background. 
- **Persistent Settings:** The application saves your settings (folder path, interval, and shuffle preference) so you don't have to configure them every time you launch it.
    

## Usage

If you just want to use it, download the `wallpaper_changer.exe` from the releases and run it.
- **Select a Folder:** Click the "Browse" button to choose the directory containing your wallpapers.
- **Set the Interval:** Enter the desired time and select the unit (Seconds, Minutes, or Hours).
- **Shuffle (Optional):** Check the "Shuffle the picture order" box to randomize the wallpaper sequence.
- **Start:** Click the "Start" button to begin changing your wallpapers. The application will start cycling through the images in the selected folder.
- **Stop:** Click the "Stop" button to halt the wallpaper changing process.
- **Minimize to Tray:** Click "Minimize" to send the application to your system tray. It will continue to run in the background.

Otherwise, if you want to run it with Python or build it yourself, follow the instructions below.

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

## Project Structure

- [`main.py`](http://main.py): Contains the core logic for setting the wallpaper and retrieving image files.
- [`gui.py`](http://gui.py): The main application file with the `CustomTkinter` GUI and threading logic.
- `wallpaper_changer.spec`: The PyInstaller spec file for building the executable.
- `assets/`: Folder for application icons and images used in the GUI.

## License

This project is licensed under the MIT License - see the LICENSE file for details.