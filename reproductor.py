import cv2
import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
from tkinter import filedialog

def seleccionar_directorio():
    video = filedialog.askopenfilename(filetypes=[("Videos", "*.mkv")])
    if not video:
        exit()
    return Path(video)

class Reproductor:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(str(self.video_path))

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.current_frame = 0

        self.root = tk.Tk()
        self.root.title("Frame Picker")

        self.label = tk.Label(self.root)
        self.label.pack()

        self.slider = tk.Scale(
            self.root,
            from_=0,
            to=self.total_frames,
            orient="horizontal",
            command=self.on_slider,
            length=500
        )
        self.slider.pack()

        self.btn = tk.Button(self.root, text="Capturar frame", command=self.capture)
        self.btn.pack()

        self.show_frame(0)


    def show_frame(self, frame_id):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(img)

            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

    def on_slider(self, val):
        self.current_frame = int(val)
        self.show_frame(self.current_frame)

    def capture(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        ret, frame = self.cap.read()
        if ret:
            cv2.imwrite(f"temp/captures/{self.video_path.name[:18]}.png", frame)
            print("Guardado frame:", self.current_frame)
        self.close()
        
    def run(self):
        self.root.mainloop()

    def close(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    video = seleccionar_directorio()
    app = Reproductor(video)
    app.run()