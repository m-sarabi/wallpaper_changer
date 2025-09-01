import json
import os
import random
import sys
import threading
import webbrowser
from tkinter import filedialog, messagebox

import customtkinter as ctk
import pystray
from PIL import Image
from customtkinter import CTkImage

from main import get_images_from_folder, set_wallpaper


def resource_path(relative_path: str) -> str:
    """Get the absolute path to the resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath("assets")
    return os.path.join(base_path, relative_path)


class WallpaperChangerGUI(ctk.CTk):
    """CustomTkinter GUI for the wallpaper changer."""

    def __init__(self):
        super().__init__()

        # App settings
        ctk.set_appearance_mode("dark")  # "light", "dark", or "system"
        ctk.set_default_color_theme("dark-blue")  # "blue", "green", "dark-blue"
        self.base_title = "Wallpaper Changer"
        self.title(self.base_title)
        self.geometry("800x500")
        self.resizable(False, False)
        self.iconbitmap(resource_path('icon.ico'))

        self.stop_event = threading.Event()
        self.stop_event.set()
        self.wallpaper_thread = None

        self.previous_image = None
        self.icon = None

        # Settings storage
        app_data_path = os.path.join(os.path.expanduser("~"), 'AppData', 'Roaming')
        self.settings_dir = os.path.join(app_data_path, 'WallpaperChanger')
        self.settings_file = os.path.join(self.settings_dir, 'settings.json')
        os.makedirs(self.settings_dir, exist_ok=True)

        # Variables
        self.folder_path = ctk.StringVar()
        self.time_unit = ctk.StringVar(value="Minutes")
        self.randomize_var = ctk.BooleanVar(value=True)

        # Layout
        self._create_widgets()
        self._load_settings()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _create_widgets(self):
        """Create the GUI elements."""
        main_font = ctk.CTkFont(size=16)
        header_font = ctk.CTkFont(size=20)
        radius = 1
        label_width = 250
        button_size = (120, 35)

        # Main frame
        main_frame = ctk.CTkFrame(self, corner_radius=radius,
                                  fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        main_frame.pack(fill="both", expand=True, padx=4, pady=4)

        # Settings:
        (ctk.CTkLabel(main_frame, text="Settings:", font=header_font, width=label_width, anchor='w')
         .pack(pady=(6, 3), padx=(15, 5), fill='both', expand=True))

        # Folder selection
        folder_frame = ctk.CTkFrame(main_frame, corner_radius=radius)
        folder_frame.pack(fill="both", expand=True, padx=0, pady=(0, 2))
        (ctk.CTkLabel(folder_frame, text="Choose a picture directory:", font=main_font, width=label_width, anchor='w')
         .pack(side='left', pady=5, padx=(15, 5)))
        folder_entry = ctk.CTkEntry(folder_frame, textvariable=self.folder_path, width=250, state="readonly",
                                    font=main_font)
        folder_entry.pack(side='left', pady=10, padx=5)
        ctk.CTkButton(folder_frame, text="Browse", command=self.select_folder, font=main_font,
                      corner_radius=100).pack(
            side='right', pady=10, padx=(5, 15))

        # Interval
        interval_frame = ctk.CTkFrame(main_frame, corner_radius=radius)
        interval_frame.pack(fill="both", expand=True, padx=0, pady=2)
        (ctk.CTkLabel(interval_frame, text="Change pictures every: ", font=main_font, width=label_width, anchor='w')
         .pack(side='left', pady=10, padx=(15, 5)))
        self.interval_entry = ctk.CTkEntry(interval_frame, width=80, font=main_font, corner_radius=0)
        self.interval_entry.insert(0, "60")
        self.interval_entry.pack(side='left', pady=10, padx=(5, 0))

        ## Time unit
        time_unit_menu = ctk.CTkOptionMenu(interval_frame, variable=self.time_unit,
                                           values=["Seconds", "Minutes", "Hours"], font=main_font, corner_radius=0)
        time_unit_menu.pack(side='left', pady=10, padx=(0, 15))

        # Randomize
        random_frame = ctk.CTkFrame(main_frame, corner_radius=radius)
        (ctk.CTkLabel(random_frame, text="Shuffle the picture order:", font=main_font, width=label_width, anchor='w')
         .pack(side='left', pady=10, padx=(15, 5)))
        random_frame.pack(fill="both", expand=True, padx=0, pady=2)
        randomize_check = ctk.CTkCheckBox(random_frame, text="", variable=self.randomize_var,
                                          font=main_font)
        randomize_check.pack(pady=10, side='left', padx=15)

        # Controls:
        (ctk.CTkLabel(main_frame, text="Controls:", font=header_font, width=label_width, anchor='w')
         .pack(pady=(6, 3), padx=(15, 5), fill='both', expand=True))

        ## Buttons
        buttons_frame = ctk.CTkFrame(main_frame, corner_radius=radius)
        buttons_frame.pack(fill="both", expand=True, padx=0, pady=(2, 0))
        self.start_image = CTkImage(Image.open(resource_path('start.png')), size=(20, 20))
        self.start_image_disabled = CTkImage(Image.open(resource_path('start_disabled.png')), size=(20, 20))
        self.start_button = ctk.CTkButton(buttons_frame, font=main_font,
                                          text="Start", image=self.start_image, compound='left',
                                          fg_color="#4CAF50", hover_color="#45A049", command=self.start_changer,
                                          corner_radius=100,
                                          width=button_size[0], height=button_size[1])
        self.start_button.pack(side='left', pady=10, padx=(15, 5))

        self.stop_image = CTkImage(Image.open(resource_path('stop.png')), size=(20, 20))
        self.stop_image_disabled = CTkImage(Image.open(resource_path('stop_disabled.png')), size=(20, 20))
        self.stop_button = ctk.CTkButton(buttons_frame, font=main_font,
                                         text="Stop", image=self.stop_image_disabled, compound='left',
                                         fg_color="#E53935", hover_color="#D32F2F", command=self.stop_changer,
                                         state="disabled", corner_radius=100,
                                         width=button_size[0], height=button_size[1])
        self.stop_button.pack(side='left', pady=10, padx=5)

        (ctk.CTkButton(buttons_frame, text="Minimize", command=self.minimize_to_tray, corner_radius=100, font=main_font,
                       width=button_size[0] // 2, height=button_size[1],
                       image=CTkImage(Image.open(resource_path('tray.png')), size=(20, 20)), compound='left')
        .pack(
            side='right', pady=10, padx=5))

        # Footer
        ## Status bar
        status_frame = ctk.CTkFrame(self, corner_radius=5, border_width=2, border_color='#555555')
        status_frame.pack(padx=0, pady=(5, 0), side='left')
        self.status_label = ctk.CTkLabel(status_frame, text="Status: Ready", anchor="center",
                                         font=ctk.CTkFont(size=14))
        self.status_label.pack(side="bottom", pady=6, padx=10)

        ## Repository
        self.status_label = ctk.CTkLabel(self, text="by m_sarabi", anchor="center", text_color="#888888",
                                         cursor='hand2', font=ctk.CTkFont(size=12))
        self.status_label.bind("<Button-1>",
                               lambda e: webbrowser.open_new("https://github.com/m-sarabi/wallpaper_changer"))
        self.status_label.pack(side="right", pady=6, padx=10)

    def select_folder(self):
        """Open the folder selection dialog and get the folder path"""
        folder_selected = filedialog.askdirectory(title="Select a folder with wallpapers")
        if folder_selected:
            self.folder_path.set(folder_selected)

    def _get_interval_in_seconds(self) -> int:
        """Convert the intervals to seconds"""
        try:
            interval_val = int(self.interval_entry.get())
            if interval_val <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Interval must be a positive integer.")
            return -1

        unit = self.time_unit.get()
        return interval_val * (60 if unit == "Minutes" else 3600 if unit == "Hours" else 1)

    def start_changer(self):
        """Start button handler to change the wallpaper on a new thread"""
        self.stop_changer(wait=True)

        if not self.folder_path.get():
            messagebox.showerror("Error", "Please select a folder.")
            return

        if self._get_interval_in_seconds() == -1:
            return

        self.stop_event.clear()
        self.start_button.configure(state="disabled", image=self.start_image_disabled)
        self.stop_button.configure(state="normal", image=self.stop_image)
        self.status_label.configure(text="Status: Running...")

        self.wallpaper_thread = threading.Thread(
            target=self._run_changer,
            args=(self.folder_path.get(),),
            daemon=True
        )
        self.wallpaper_thread.start()

    def stop_changer(self, wait: bool = False):
        """Stop button handler that stops the changer thread"""
        self.stop_event.set()
        if wait and self.wallpaper_thread and self.wallpaper_thread.is_alive():
            self.wallpaper_thread.join(timeout=1)

        self.start_button.configure(state="normal", image=self.start_image)
        self.stop_button.configure(state="disabled", image=self.stop_image_disabled)
        self.status_label.configure(text="Status: Stopped")

    def _run_changer(self, folder: str):
        """Run the changer thread to change the wallpaper"""
        try:
            images = get_images_from_folder(folder)
            if not images:
                self.after(0, messagebox.showerror, "Error", "No images found in the selected folder.")
                self.after(0, self.stop_changer, False)
                return

            if self.previous_image and self.previous_image in images:
                index = images.index(self.previous_image)
            else:
                index = 0
            while not self.stop_event.is_set():
                if self.randomize_var.get():
                    if len(images) > 1:
                        while True:
                            image = random.choice(images)
                            if image != self.previous_image:
                                break
                    else:
                        image = random.choice(images)
                    index = (images.index(image) + 1) % len(images)
                else:
                    image = images[index % len(images)]
                    index = (index + 1) % len(images)

                print(f"Setting wallpaper: {image}")
                set_wallpaper(image)
                self.title(f'{self.base_title} | {os.path.basename(image)}')
                if self.stop_event.wait(self._get_interval_in_seconds()):
                    break

        except Exception as e:
            self.after(0, messagebox.showerror, "Error", f"An error occurred:\n\n{e}")
            self.after(0, self.stop_changer, False)

    def minimize_to_tray(self):
        """System tray functionality using pystray"""
        self.withdraw()
        image = Image.open(resource_path("icon.ico"))
        menu = (pystray.MenuItem("Show", self._restore_window),
                pystray.MenuItem("Quit", self.on_quit))
        self.icon = pystray.Icon("name", image, "Wallpaper Changer", menu)
        threading.Thread(target=self.icon.run, daemon=True).start()

    def _restore_window(self):
        self.deiconify()
        self.icon.stop()

    def on_quit(self):
        self.icon.stop()
        self.stop_changer(wait=True)
        self.quit()

    def on_close(self):
        self._save_settings()
        if not self.stop_event.is_set():
            self.minimize_to_tray()
        else:
            self.stop_changer(wait=True)
            self.destroy()

    def _save_settings(self):
        """Save the settings to a file on close"""
        settings = {
            "folder_path": self.folder_path.get(),
            "interval_value": self.interval_entry.get(),
            "time_unit": self.time_unit.get(),
            "randomize": self.randomize_var.get()
        }
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f)

    def _load_settings(self):
        """Load the previously set settings from a file if it exists"""
        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                self.folder_path.set(settings.get("folder_path", ""))
                self.interval_entry.delete(0, "end")
                self.interval_entry.insert(0, settings.get("interval_value", "60"))
                self.time_unit.set(settings.get("time_unit", "Minutes"))
                self.randomize_var.set(settings.get("randomize", True))
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    app = WallpaperChangerGUI()
    app.mainloop()
