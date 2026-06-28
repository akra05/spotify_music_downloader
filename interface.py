import threading
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog
from downloader import download, DEFAULT_DOWNLOAD_DIR, load_download_dir, save_download_dir

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

selected_dir = load_download_dir()


def choose_folder():
    global selected_dir
    folder = filedialog.askdirectory(initialdir=str(selected_dir))
    if folder:
        selected_dir = Path(folder)
        folder_label.configure(text=str(selected_dir))
        save_download_dir(selected_dir)


def on_download():
    url = url_entry.get().strip()
    if not url:
        status_label.configure(text="⚠ Bitte eine URL eingeben.")
        return

    download_btn.configure(state="disabled")
    progress_bar.set(0)
    progress_bar.pack(pady=(0, 6))
    status_label.configure(text="")

    def update_status(msg):
        window.after(0, lambda m=msg: status_label.configure(text=m))
        if "%" in msg:
            try:
                percent = float(msg.split("%")[0].replace("⬇", "").strip()) / 100
                window.after(0, lambda p=percent: progress_bar.set(p))
            except ValueError:
                pass
        elif "Konvertiere" in msg or "Finalisiere" in msg:
            window.after(0, lambda: progress_bar.set(0.95))
        elif "Fertig" in msg:
            window.after(0, lambda: progress_bar.set(1.0))

    def run():
        download(url, progress_callback=update_status, download_dir=selected_dir)
        window.after(0, lambda: download_btn.configure(state="normal"))

    threading.Thread(target=run, daemon=True).start()


# --- Window ---
window = ctk.CTk()
window.title("Music Downloader")
window.geometry("620x380")
window.resizable(False, False)

# --- Titel ---
ctk.CTkLabel(
    window,
    text="Music Downloader",
    font=("Arial", 24, "bold")
).pack(pady=(24, 4))

ctk.CTkLabel(
    window,
    text="YouTube oder SoundCloud Link:",
    font=("Arial", 13)
).pack()

# --- URL Eingabe ---
url_entry = ctk.CTkEntry(window, width=460, placeholder_text="https://...")
url_entry.pack(pady=10)

# --- Ordner Auswahl ---
folder_frame = ctk.CTkFrame(window, fg_color="transparent")
folder_frame.pack(pady=(0, 10))

ctk.CTkButton(
    folder_frame,
    text="📁 Ordner wählen",
    command=choose_folder,
    width=140
).grid(row=0, column=0, padx=(0, 10))

folder_label = ctk.CTkLabel(
    folder_frame,
    text=str(selected_dir),  # zeigt gespeicherten Ordner direkt beim Start
    font=("Arial", 11),
    text_color="gray",
    wraplength=300,
    anchor="w"
)
folder_label.grid(row=0, column=1, sticky="w")

# --- Download Button ---
download_btn = ctk.CTkButton(
    window,
    text="Download",
    command=on_download,
    width=200,
    height=40,
    font=("Arial", 14, "bold")
)
download_btn.pack(pady=10)

# --- Fortschrittsbalken ---
progress_bar = ctk.CTkProgressBar(window, width=460)
progress_bar.set(0)
progress_bar.pack(pady=(0, 6))
progress_bar.pack_forget()

# --- Status ---
status_label = ctk.CTkLabel(window, text="", font=("Arial", 12), wraplength=500)
status_label.pack()

window.mainloop()