import customtkinter as ctk
from downloader import download

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


def on_download():
    url = url_entry.get()
    status_label.configure(text="Download running...")
    download(url)
    status_label.configure(text="Finished!")


window = ctk.CTk()
window.title("Music Downloader")
window.geometry("600x300")

ctk.CTkLabel(window, text="Music Downloader", font=("Arial", 24, "bold")).pack(pady=20)
ctk.CTkLabel(window, text="YouTube or SoundCloud Link:").pack()

url_entry = ctk.CTkEntry(window, width=400, placeholder_text="https://...")
url_entry.pack(pady=10)

ctk.CTkButton(window, text="Download", command=on_download, width=200).pack(pady=10)

status_label = ctk.CTkLabel(window, text="")
status_label.pack()

window.mainloop()