import os
import glob
import cv2
from tkinter import Tk, Label, Button, Frame
from PIL import Image, ImageTk
import shutil
import numpy as np

class ImageViewer:
    def __init__(self, master, images, image_folder, mask_folder):
        self.master = master
        self.images = images
        self.index = 0
        self.image_folder = image_folder
        self.mask_folder = mask_folder

        self.rgb_image, self.mask_image, self.base_name = self.images[self.index]
        self.overlay_image = self.create_overlay(self.rgb_image, self.mask_image)

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

        master.bind('<Left>', lambda event: self.prev_image())
        master.bind('<Right>', lambda event: self.next_image())
        master.bind('<Up>', lambda event: self.move_to_good_data())
        master.bind('<Down>', lambda event: self.move_to_bad_data())

    def create_overlay(self, rgb_image, mask_image):
        mask_colored = cv2.cvtColor(mask_image, cv2.COLOR_GRAY2BGR)
        overlay = cv2.addWeighted(rgb_image, 0.8, mask_colored, 0.2, 0)
        return overlay

    def show_image(self):
        spacer = np.ones((self.rgb_image.shape[0], 10, 3), dtype=np.uint8) * 255
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
        # Cria as pastas para imagens e máscaras
        image_dest_folder = os.path.join(folder_name, 'images')
        mask_dest_folder = os.path.join(folder_name, 'masks')

        os.makedirs(image_dest_folder, exist_ok=True)
        os.makedirs(mask_dest_folder, exist_ok=True)

        # Move as imagens e máscaras para as pastas respectivas
        rgb_path = os.path.join(self.image_folder, self.base_name + '.tif')
        mask_path = os.path.join(self.mask_folder, self.base_name + '.tif')

        shutil.move(rgb_path, os.path.join(image_dest_folder, self.base_name + '.tif'))
        shutil.move(mask_path, os.path.join(mask_dest_folder, self.base_name + '.tif'))

        del self.images[self.index]
        if not self.images:
            self.master.quit()
        else:
            self.index = self.index % len(self.images)
            self.update_image()

    def move_to_bad_data(self):
        self.move_to_folder(os.path.join(self.image_folder, '..', 'bad_data'))

    def move_to_good_data(self):
        self.move_to_folder(os.path.join(self.image_folder, '..', 'good_data'))

def load_images(image_folder, mask_folder):
    image_files = glob.glob(os.path.join(image_folder, '*.tif'))
    mask_files = glob.glob(os.path.join(mask_folder, '*.tif'))

    images = []
    for image_path in sorted(image_files):
        base_name = os.path.basename(image_path).replace('.tif', '')
        mask_path = os.path.join(mask_folder, base_name + '.tif')
        if mask_path in mask_files:
            rgb_image = cv2.imread(image_path)
            mask_image = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
            images.append((rgb_image, mask_image, base_name))
    
    return images

if __name__ == "__main__":
    image_folder = "data/aug/images"
    mask_folder = "data/aug/masks"
    images = load_images(image_folder, mask_folder)

    root = Tk()
    root.title("Classificação de Terraços")
    viewer = ImageViewer(root, images, image_folder, mask_folder)
    root.mainloop()
