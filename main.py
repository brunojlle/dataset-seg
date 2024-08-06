import os
import glob
import cv2
from tkinter import Tk, Label, Button, Frame
from PIL import Image, ImageTk
import shutil
import numpy as np

class ImageViewer:
    def __init__(self, master, images, folder_path):
        self.master = master
        self.images = images
        self.index = 0
        self.folder_path = folder_path

        self.rgb_image, self.mask_image, self.base_name = self.images[self.index]
        self.overlay_image = self.create_overlay(self.rgb_image, self.mask_image)

        self.label = Label(master)
        self.label.pack()

        self.show_image()

        self.button_frame = Frame(master)
        self.button_frame.pack(pady=10)

        button_options = {'side': 'left', 'padx': 5, 'pady': 5}
        button_size = {'width': 10, 'height': 2}

        self.prev_button = Button(self.button_frame, text="ANTERIOR", command=self.prev_image, **button_size)
        self.prev_button.pack(**button_options)

        self.next_button = Button(self.button_frame, text="PRÓXIMO", command=self.next_image, **button_size)
        self.next_button.pack(**button_options)

        self.bad_button = Button(self.button_frame, text="RUIM", command=self.move_to_bad_data, **button_size)
        self.bad_button.pack(**button_options)

        self.good_button = Button(self.button_frame, text="BOM", command=self.move_to_good_data, **button_size)
        self.good_button.pack(**button_options)

        self.quit_button = Button(self.button_frame, text="SAIR", command=master.quit, **button_size)
        self.quit_button.pack(**button_options)

        master.bind('<Left>', lambda event: self.prev_image())
        master.bind('<Right>', lambda event: self.next_image())
        master.bind('<Up>', lambda event: self.move_to_good_data())
        master.bind('<Down>', lambda event: self.move_to_bad_data())

    def create_overlay(self, rgb_image, mask_image):
        mask_colored = cv2.cvtColor(mask_image, cv2.COLOR_GRAY2BGR)
        overlay = cv2.addWeighted(rgb_image, 0.8, mask_colored, 0.2, 0)
        return overlay

    def show_image(self):
        spacer = np.ones((self.rgb_image.shape[0], 20, 3), dtype=np.uint8) * 255
        combined_image = cv2.hconcat([self.rgb_image, spacer, self.overlay_image])
        combined_image = cv2.cvtColor(combined_image, cv2.COLOR_BGR2RGB)
        combined_image = Image.fromarray(combined_image)
        imgtk = ImageTk.PhotoImage(image=combined_image)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)

    def prev_image(self):
        self.index = (self.index - 1) % len(self.images)
        self.update_image()

    def next_image(self):
        self.index = (self.index + 1) % len(self.images)
        self.update_image()

    def update_image(self):
        self.rgb_image, self.mask_image, self.base_name = self.images[self.index]
        self.overlay_image = self.create_overlay(self.rgb_image, self.mask_image)
        self.show_image()

    def move_to_folder(self, folder_name):
        os.makedirs(folder_name, exist_ok=True)
        rgb_path = os.path.join(self.folder_path, self.base_name + 'rgb.tif')
        mask_path = os.path.join(self.folder_path, self.base_name + 'mask.tif')
        shutil.move(rgb_path, os.path.join(folder_name, self.base_name + 'rgb.tif'))
        shutil.move(mask_path, os.path.join(folder_name, self.base_name + 'mask.tif'))
        del self.images[self.index]
        if not self.images:
            self.master.quit()
        else:
            self.index = self.index % len(self.images)
            self.update_image()

    def move_to_bad_data(self):
        self.move_to_folder(os.path.join(self.folder_path, 'bad_data'))

    def move_to_good_data(self):
        self.move_to_folder(os.path.join(self.folder_path, 'good_data'))

def load_images(folder_path):
    rgb_images = glob.glob(os.path.join(folder_path, '*rgb.tif'))
    mask_images = glob.glob(os.path.join(folder_path, '*mask.tif'))

    images = []
    for rgb_path in rgb_images:
        base_name = os.path.basename(rgb_path).replace('rgb.tif', '')
        mask_path = os.path.join(folder_path, base_name + 'mask.tif')
        if mask_path in mask_images:
            rgb_image = cv2.imread(rgb_path)
            mask_image = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
            images.append((rgb_image, mask_image, base_name))
    
    return images

if __name__ == "__main__":
    folder_path = "data"
    images = load_images(folder_path)

    root = Tk()
    viewer = ImageViewer(root, images, folder_path)
    root.mainloop()