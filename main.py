from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar
from PyPDF4 import PdfFileReader
from pdfminer.high_level import extract_text
import pyttsx3
from pygame import mixer
import threading
from datetime import datetime

class App(Tk):
    def __init__(self):
        super().__init__()
        self.engine = pyttsx3.init()
        self.mixer = mixer
        self.rate = 150
        self.volume = 0.5
        self.voices = self.engine.getProperty("voices")
        self.title("DIY Audiobooks")
        self.background_color = "#93B5C6"
        self.canvas_bg_color = "#C9CCD5"
        self.config(padx=20, pady=20, bg=self.background_color)
        self.heading_font = "Cambria"
        self.body_font = "Times New Roman"
        self.title_label = Label(text="DIY Audiobooks",
                                 font=(self.heading_font, 40, "bold"),
                                 bg=self.background_color)
        self.title_label.grid(row=0, column=0, columnspan=3)
        ## Convert Audio Buttons ##
        self.convert_canvas = Canvas(bg=self.canvas_bg_color)
        self.convert_canvas.grid(row=1, column=0, sticky="n", pady=20)
        self.convert_label = Label(self.convert_canvas,
                                   text="Convert a Book to Audio",
                                   font=(self.body_font, 16),
                                   bg=self.canvas_bg_color)
        self.convert_label.grid(row=1, column=0, columnspan=2, padx=20, pady=10)
        self.male = PhotoImage(file="male.png")
        self.female = PhotoImage(file="woman.png")
        self.select_voice_label = Label(self.convert_canvas,
                                        text="Choose a male or female voice.",
                                        font=(self.body_font, 14),
                                        bg=self.canvas_bg_color)
        self.select_voice_label.grid(row=2, column=0, columnspan=2)
        self.male_voice = Button(self.convert_canvas,
                                 image=self.male,
                                 command=self.change_to_male)
        self.female_voice = Button(self.convert_canvas,
                                   image=self.female,
                                   command=self.change_to_female)
        self.male_voice.grid(row=3, column=0, pady=10)
        self.female_voice.grid(row=3, column=1, pady=10)
        self.convert_button = Button(self.convert_canvas,
                                     text="Open File",
                                     font=(self.body_font, 14),
                                     command=self.run_convert_function)
        self.convert_button.grid(row=4, column=0, columnspan=3, pady=20)
        self.progress_label = Label(self.convert_canvas,
                                    text="",
                                    font=(self.body_font, 12),
                                    bg=self.canvas_bg_color)
        self.progress_bar = Progressbar(self.convert_canvas,
                                        orient="horizontal",
                                        length=250,
                                        mode="indeterminate")
        ## Open Buttons ##
        self.or_label = Label(text="or",
                              font=(self.heading_font, 20),
                              bg=self.background_color)
        self.or_label.grid(row=1, column=1, padx=20)
        self.open_canvas = Canvas(bg=self.canvas_bg_color)
        self.open_canvas.grid(row=1, column=2, sticky="n", pady=20)
        self.open_label = Label(self.open_canvas,
                                text="Open an Audiobook",
                                font=(self.body_font, 16),
                                bg=self.canvas_bg_color)
        self.open_label.grid(row=1, column=2, padx=43, pady=10)
        self.open_button = Button(self.open_canvas,
                                  text="Open File",
                                  font=(self.body_font, 14),
                                  command=self.open_file)
        self.open_button.grid(row=3, column=2, pady=20)
        ## Book Title Label ##
        self.book_label = Label(text="",
                                font=(self.body_font, 20),
                                bg=self.background_color)
        ## Play and Pause Buttons ##
        self.play_canvas = Canvas(bg=self.canvas_bg_color)
        self.play_img = PhotoImage(file="play-button.png")
        self.play_button = Button(self.play_canvas,
                                  image=self.play_img,
                                  command=self.resume_book)
        self.pause_img = PhotoImage(file="pause-button.png")
        self.pause_button = Button(self.play_canvas,
                                   image=self.pause_img,
                                   command=self.pause_book)
        ## Volume Buttons ##
        self.volume_canvas = Canvas(bg=self.canvas_bg_color)
        self.volume_up_img = PhotoImage(file="volume-up.png")
        self.volume_down_img = PhotoImage(file="volume-down.png")
        self.mute_image = PhotoImage(file="silent.png")
        self.volume_up_button = Button(self.volume_canvas,
                                       image=self.volume_up_img,
                                       command=self.increase_volume)
        self.volume_down_button = Button(self.volume_canvas,
                                         image=self.volume_down_img,
                                         command=self.decrease_volume)
        self.mute_button = Button(self.volume_canvas,
                                  image=self.mute_image,
                                  command=self.mute_volume)
        ## Copyright ##
        self.copyright_label = Label(text=f"Copyright © Shauna Ross {datetime.now().year}"
                                          f"\nVideo icons created by SumberRejeki - Flaticon",
                                     bg=self.background_color)
        self.copyright_label.grid(row=5, column=0, columnspan=3, pady=(10, 0))

        self.run_app()

    def run_app(self):
        self.volume_up_status()
        self.volume_down_status()

    ## Convert PDF to Audio ##
    def run_convert_function(self):
        thread = threading.Thread(target=self.extract_text)
        thread.start()

    def extract_text(self):
        open_path = filedialog.askopenfilename(initialdir="/", title="Select A PDF", filetypes=[("PDF", "*.pdf")])
        if open_path:
            self.progress_label.config(text="Extracting text...")
            self.progress_label.grid(row=5, column=0, columnspan=3)
            self.progress_bar.grid(row=6, column=0, columnspan=3)
            self.progress_bar.start()
            text = extract_text(open_path)
            with open(open_path, "rb") as file:
                book = PdfFileReader(file)
                info = book.getDocumentInfo()
            book_title = info.title
            self.progress_bar.stop()
            self.convert_book(text, book_title)

    def convert_book(self, text, book_title):
        save_path = filedialog.asksaveasfilename(title="Save as a Sound File", filetypes=[("Sound File", "*.wav")])
        if save_path:
            self.progress_label.config(text="Converting to audio...")
            self.progress_bar.start()
            self.engine.save_to_file(text=text, filename=save_path)
            self.engine.runAndWait()
            self.progress_bar.destroy()
            self.progress_label.destroy()
            self.create_book_label(book_title)
            self.play_book(save_path)
        else:
            self.progress_label.destroy()
            self.progress_bar.destroy()

    def open_file(self):
        open_path = filedialog.askopenfilename(title="Open a Sound File", filetypes=[("Sound File", "*.wav *.mp3")])
        if open_path:
            name = open_path.split("/")
            title = name[len(name) - 1]
            book_title = title.split(".")[0]
            self.create_book_label(book_title)
            self.play_book(open_path)

    def create_book_label(self, title):
        self.book_label.config(text=f"Now Playing: {title}")
        self.book_label.grid(row=2, column=0, pady=20, padx=10, columnspan=3)

    def create_buttons(self):
        self.play_canvas.grid(row=3, column=0, columnspan=3)
        self.play_button.grid(row=0, column=0, sticky="e", padx=55, pady=20)
        self.pause_button.grid(row=0, column=1, sticky="w", padx=55)
        self.volume_canvas.grid(row=4, column=0, columnspan=3)
        self.volume_up_button.grid(row=0, column=0, padx=41, pady=20)
        self.volume_down_button.grid(row=0, column=1)
        self.mute_button.grid(row=0, column=2, padx=41)

    ## Voice Controls ##
    def change_to_male(self):
        self.engine.setProperty("voice", self.voices[0].id)

    def change_to_female(self):
        self.engine.setProperty("voice", self.voices[1].id)

    ## Play and Pause ##
    def play_book(self, filename):
        self.create_buttons()
        mixer.init()
        mixer.music.load(filename)
        mixer.music.play()

    def pause_book(self):
        mixer.music.pause()

    def resume_book(self):
        mixer.music.unpause()

    ## Volume Controls
    def volume_up_status(self):
        if self.volume < 0.99:
            self.volume_up_button["state"] = ACTIVE
        else:
            self.volume_up_button["state"] = DISABLED
        self.after(1, self.volume_up_status)

    def volume_down_status(self):
        if self.volume > 0.01:
            self.volume_down_button["state"] = ACTIVE
        else:
            self.volume_down_button["state"] = DISABLED
        self.after(1, self.volume_down_status)

    def increase_volume(self):
        self.volume += 0.10
        mixer.music.set_volume(self.volume)

    def decrease_volume(self):
        self.volume -= 0.10
        mixer.music.set_volume(self.volume)

    def mute_volume(self):
        self.volume = 0
        mixer.music.set_volume(self.volume)


app = App()
app.mainloop()