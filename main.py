import os
import ctypes
from pathlib import Path

# from https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-systemparametersinfow
SPI_SETDESKWALLPAPER = 0x0014


def set_wallpaper(image_path: str) -> None:
    """Sets the desktop wallpaper on Windows."""
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)


def get_images_from_folder(folder: str, extensions: None | list[str] = None) -> list[str]:
    """Retrieves a list of image files from the given folder."""
    if extensions is None:
        extensions = [".jpg", ".jpeg", ".png", ".bmp", '.webp']

    folder_path = Path(folder)
    if not Path.is_dir(folder_path):
        raise IsADirectoryError(f"Folder does not exist: {folder_path}")
    return [str(p) for p in folder_path.iterdir() if p.suffix.lower() in extensions]
