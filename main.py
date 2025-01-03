import os
import glob
import cv2
from tkinter import Tk, Label, Button, Frame
from PIL import Image, ImageTk
import shutil
import numpy as np
import time

class ImageViewer:
    def __init__(self, master, image_folder, mask_folder, batch_size=100, delay=0.5):
        self.master = master
        self.image_folder = image_folder
        self.mask_folder = mask_folder
        self.batch_size = batch_size
        self.images = []
        self.image_files = sorted(glob.glob(os.path.join(image_folder, '*.tif')) + glob.glob(os.path.join(image_folder, '*.tiff')))
        self.mask_files = sorted(glob.glob(os.path.join(mask_folder, '*.tif')) + glob.glob(os.path.join(mask_folder, '*.tiff')))
        self.index = 0
        self.delay = delay  # Delay para bloquear os inputs
        self.last_action_time = 0  # Tempo da última ação

        self.load_next_batch()

        self.label = Label(master)
        self.label.pack()

        self.show_image()

        self.nav_frame = Frame(master)
        self.nav_frame.pack(pady=5)

        button_options = {'side': 'left', 'padx': 5, 'pady': 5}
        button_size = {'width': 10, 'height': 2}

        self.prev_button = Button(self.nav_frame, text="ANTERIOR", command=self.prev_image, bg="lightblue", fg="black", **button_size)
        self.prev_button.pack(**button_options)

        self.next_button = Button(self.nav_frame, text="PRÓXIMO", command=self.next_image, bg="lightblue", fg="black", **button_size)
        self.next_button.pack(**button_options)

        self.class_frame = Frame(master)
        self.class_frame.pack(pady=5)

        self.bad_button = Button(self.class_frame, text="RUIM", command=self.move_to_bad_data, bg="#B22222", fg="white", **button_size)
        self.bad_button.pack(side="left", padx=5, pady=5)

        self.good_button = Button(self.class_frame, text="BOM", command=self.move_to_good_data, bg="#228B22", fg="white", **button_size)
        self.good_button.pack(side="left", padx=5, pady=5)

        self.quit_frame = Frame(master)
        self.quit_frame.pack(pady=5)

        self.quit_button = Button(self.quit_frame, text="SAIR", command=master.quit, bg="gray", fg="white", **button_size)
        self.quit_button.pack(side="left", padx=5, pady=5)

        master.bind('<Left>', lambda event: self.handle_key_event(self.prev_image))
        master.bind('<Right>', lambda event: self.handle_key_event(self.next_image))
        master.bind('<Up>', lambda event: self.handle_key_event(self.move_to_good_data))
        master.bind('<Down>', lambda event: self.handle_key_event(self.move_to_bad_data))

    def handle_key_event(self, action):
        # Verificar se o delay passou
        current_time = time.time()
        if current_time - self.last_action_time >= self.delay:
            action()
            self.last_action_time = current_time

    def load_next_batch(self):
        start = (self.index // self.batch_size) * self.batch_size
        end = start + self.batch_size
        self.images = []

        for image_path in self.image_files[start:end]:
            base_name = os.path.basename(image_path).rsplit('.', 1)[0]
            for ext in ['.tif', '.tiff']:
                mask_path = os.path.join(self.mask_folder, base_name + ext)
                if mask_path in self.mask_files:
                    rgb_image = cv2.imread(image_path)
                    mask_image = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
                    self.images.append((rgb_image, mask_image, base_name))
                    break

        if not self.images:
            self.master.quit()

    def create_overlay(self, rgb_image, mask_image):
        mask_colored = cv2.cvtColor(mask_image, cv2.COLOR_GRAY2BGR)
        overlay = cv2.addWeighted(rgb_image, 0.8, mask_colored, 0.2, 0)
        return overlay

    def show_image(self):
        if self.images:
            self.rgb_image, self.mask_image, self.base_name = self.images[self.index % self.batch_size]
            self.overlay_image = self.create_overlay(self.rgb_image, self.mask_image)

            spacer = np.ones((self.rgb_image.shape[0], 10, 3), dtype=np.uint8) * 255
            combined_image = cv2.hconcat([self.rgb_image, spacer, self.overlay_image])
            combined_image = cv2.cvtColor(combined_image, cv2.COLOR_BGR2RGB)
            combined_image = Image.fromarray(combined_image)
            imgtk = ImageTk.PhotoImage(image=combined_image)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

    def prev_image(self):
        if self.index > 0:
            self.index -= 1
            if self.index % self.batch_size == self.batch_size - 1:
                self.load_next_batch()
            self.show_image()

    def next_image(self):
        self.index += 1
        if self.index % self.batch_size == 0:
            self.load_next_batch()
        self.show_image()

    def move_to_folder(self, folder_name):
        image_dest_folder = os.path.join(folder_name, 'images')
        mask_dest_folder = os.path.join(folder_name, 'masks')

        os.makedirs(image_dest_folder, exist_ok=True)
        os.makedirs(mask_dest_folder, exist_ok=True)

        for ext in ['.tif', '.tiff']:
            rgb_path = os.path.join(self.image_folder, self.base_name + ext)
            mask_path = os.path.join(self.mask_folder, self.base_name + ext)

            if os.path.exists(rgb_path) and os.path.exists(mask_path):
                shutil.move(rgb_path, os.path.join(image_dest_folder, self.base_name + ext))
                shutil.move(mask_path, os.path.join(mask_dest_folder, self.base_name + ext))
                break

        self.images.pop(self.index % self.batch_size)
        if not self.images:
            self.load_next_batch()
        else:
            self.index = self.index % self.batch_size
            self.show_image()

    def move_to_bad_data(self):
        self.move_to_folder(os.path.join(self.image_folder, '..', 'bad_data'))

    def move_to_good_data(self):
        self.move_to_folder(os.path.join(self.image_folder, '..', 'good_data'))

if __name__ == "__main__":
    image_folder = "data/images"
    mask_folder = "data/masks"

    root = Tk()
    root.title("Classificação de Terraços")
    viewer = ImageViewer(root, image_folder, mask_folder)
    root.mainloop()
