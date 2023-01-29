import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import photoeditor as pe

class ImageEditor:
    def __init__(self):

        # creating the main window
        self.root = tk.Tk()
        self.root.title("Image Editor")
        self.root.geometry("1000x1000")

        # call the open image 
        self.open_button = tk.Button(self.root, text="Open Image", command=self.open_image)
        self.open_button.pack()


        self.canvas = tk.Canvas(self.root, width=800, height=500)
        self.canvas.pack()


        # CROP
        # rectangle to crop the image
        self.create_rect() 

        # button to crop
        self.crop_button = tk.Button(self.root, text="Crop", command=self.crop_image)
        self.crop_button.pack()

        # RESIZE
        # textbox to resize image
        self.pixel_ip_textbox = tk.Entry()
        self.pixel_ip_textbox.pack()
        
        # button to perform resize
        self.resize_button = tk.Button(self.root, text="To resize, enter pixels", command=self.resize_image)
        self.resize_button.pack()       

        # ROTATE    
        self.rotate_button = tk.Button(self.root, text="Rotate 90", command=self.rotate_image)
        self.rotate_button.pack()

        self.remove_noise_button = tk.Button(self.root, text="Remove noise", command=self.remove_noise)
        self.remove_noise_button.pack()

        # # Create a slider to control the brightness
        # self.brightness_slider = tk.Scale(self.root, from_=0, to=0.5, resolution=0.01, orient="horizontal", command=self.change_brightness)
        # self.brightness_slider.pack()

        self.root.mainloop()

    def open_image(self):
        # called on clicking the 'open' button
        # opens file explorer dialogue box from which user can select image
        self.filepath = filedialog.askopenfilename()
        self.img = Image.open(self.filepath)
        self.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        
        
    
    # ------ RESIZE -------
    # The following three functions perform the draw-rectangle functionality
    # the coordinates of the rectangle's corners are stored in self.rect_coords in the self.end_rect function
    def create_rect(self):
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.canvas.bind("<Button-1>", self.start_rect)
        self.canvas.bind("<B1-Motion>", self.draw_rect)
        self.canvas.bind("<ButtonRelease-1>", self.end_rect)

    def start_rect(self, event):
        self.start_x = event.x
        self.start_y = event.y
    
    def draw_rect(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        self.end_x = event.x
        self.end_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline="red")

    def end_rect(self, event):
        self.rect_coords = [self.start_x, self.start_y, self.end_x, self.end_y]
        print(f'Coordinates of the rectangle: {self.rect_coords}')
        
    
    def crop_image(self):
        self.to_crop = [self.filepath, self.rect_coords]
        print(self.to_crop)
        # calls the crop_image function from photoeditor (which uses numpy slicing to crop the image)
        self.new_img_fp = pe.crop_image(self.to_crop)
        self.canvas.delete(self.rect)   # makes the rectangle disappear
        self.show_new_img()   # show the cropped image
        self.filepath = self.new_img_fp 

    # ------- RESIZE --------   
    def resize_image(self):
        self.pixels = self.pixel_ip_textbox.get()
        print('pixels = ', self.pixels)
        self.to_resize = [self.filepath, self.pixels]
        self.new_img_fp = pe.resize_image(self.to_resize)
        self.show_new_img()
        self.filepath = self.new_img_fp
    
    # -------- ROTATE -------
    def rotate_image(self):
        to_rotate = self.filepath 
        self.new_img_fp = pe.rotate_image(to_rotate)
        self.show_new_img()
        self.filepath = self.new_img_fp 


    # -------- REMOVE NOISE ---------
    def remove_noise(self):
        to_rm_n = self.filepath
        self.new_img_fp = pe.median_noise_remove(to_rm_n)
        # self.new_img_fp = pe.gauss_noise_remove(self.new_img_fp)
        self.show_new_img()
        self.filepath = self.new_img_fp

    
    # -------- BRIGHTNESS ---------
    # def change_brightness(self, brightness):
    #     print('brighness: ', brightness)
    #     to_change_brightness = [self.filepath, brightness]
    #     self.new_img_fp = pe.change_brightness(to_change_brightness)
    #     self.show_new_img()
    #     self.filepath = self.new_img_fp


        

    # ------- SHOW NEW IMAGE -------
    def show_new_img(self):
        # show the edited image
        self.img = Image.open(self.new_img_fp)
        self.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")


if __name__ == "__main__":
    editor = ImageEditor()
    
    


