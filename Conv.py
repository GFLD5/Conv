import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp


def browse_folder():

    selected_dir = filedialog.askdirectory()
    if selected_dir:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, selected_dir)


def download_video():
    url = url_entry.get().strip()
    output_dir = folder_entry.get().strip()

    if not url:
        messagebox.showwarning("Input Error", "Please paste a YouTube URL first!")
        return
    if not output_dir:
        messagebox.showwarning("Input Error", "Please select a save destination!")
        return


    download_button.config(state=tk.DISABLED)
    status_label.config(text="Processing... Please wait.", fg="blue")
    progress_bar.start(10)

    def run():

        ydl_opts = {
            "format": "bestaudio/best",
            "source_address": "0.0.0.0",
            "ffmpeg_location": ".",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],

            "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
            "quiet": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            root.after(0, lambda: download_success())
        except Exception as e:
            root.after(0, lambda: download_failed(str(e)))

    threading.Thread(target=run, daemon=True).start()


def download_success():
    progress_bar.stop()
    download_button.config(state=tk.NORMAL)
    status_label.config(text="Success! MP3 saved.", fg="green")
    url_entry.delete(0, tk.END)
    messagebox.showinfo("Done!", "Your MP3 has been downloaded successfully!")


def download_failed(error_msg):
    progress_bar.stop()
    download_button.config(state=tk.NORMAL)
    status_label.config(text="Download Failed.", fg="red")
    messagebox.showerror(
        "Error", f"Could not download video.\nMake sure ffmpeg.exe is next to the app."
    )



root = tk.Tk()
root.title("YouTube to MP3 Converter")
root.geometry("500x260")
root.resizable(False, False)


instruction_label = tk.Label(
    root, text="Paste YouTube URL below:", font=("Arial", 10, "bold")
)
instruction_label.pack(pady=(15, 2))
url_entry = tk.Entry(root, width=55, font=("Arial", 10))
url_entry.pack(pady=5)
url_entry.focus()


folder_label = tk.Label(root, text="Save Destination:", font=("Arial", 10, "bold"))
folder_label.pack(pady=(10, 2))

folder_frame = tk.Frame(root)
folder_frame.pack(pady=5)

folder_entry = tk.Entry(folder_frame, width=42, font=("Arial", 10))
folder_entry.pack(side=tk.LEFT, padx=(0, 5))

default_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
folder_entry.insert(0, default_downloads)

browse_button = tk.Button(
    folder_frame, text="Browse...", font=("Arial", 9), command=browse_folder
)
browse_button.pack(side=tk.LEFT)


progress_bar = ttk.Progressbar(
    root, orient="horizontal", length=400, mode="indeterminate"
)
progress_bar.pack(pady=10)


download_button = tk.Button(
    root,
    text="Convert to MP3",
    bg="#107C41",
    fg="white",
    font=("Arial", 11, "bold"),
    width=22,
    command=download_video,
)
download_button.pack(pady=5)


status_label = tk.Label(root, text="Ready", font=("Arial", 9, "italic"), fg="gray")
status_label.pack(pady=(2, 10))

root.mainloop()
