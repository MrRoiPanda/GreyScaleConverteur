import tkinter as tk
from tkinter import filedialog, ttk # Import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk

class GreyscaleConverterApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Greyscale Converter")
        self.geometry("600x500")

        # --- Add a style ---
        self.style = ttk.Style(self)
        # You can experiment with themes if available on your system, e.g.:
        # print(self.style.theme_names()) # See available themes
        # self.style.theme_use('clam') # Or 'alt', 'default', 'classic'

        self.image_path = None
        self.original_image = None
        self.processed_image = None
        self.image_display_label = None

        self._setup_ui()

    def _setup_ui(self):
        # Main frame for content
        content_frame = ttk.Frame(self, padding="10 10 10 10")
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Drop target
        self.drop_target_label = ttk.Label(content_frame, text="Drag and drop an image here", padding="20 20", relief=tk.SOLID, borderwidth=1, anchor=tk.CENTER, style="Drop.TLabel") # Added anchor and custom style
        self.drop_target_label.pack(fill=tk.X, padx=10, pady=(10,5)) # Adjusted padding
        self.drop_target_label.drop_target_register(DND_FILES)
        self.drop_target_label.dnd_bind('<<Drop>>', self.handle_drop)

        # Configure a style for the drop target label for better visual
        self.style.configure("Drop.TLabel", background="lightgrey", foreground="dim gray", font=('Helvetica', 10, 'italic'))


        # Image display area
        # Using a frame to better control the image label's size and position
        image_frame = ttk.Frame(content_frame, relief=tk.SUNKEN, borderwidth=1)
        image_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.image_display_label = ttk.Label(image_frame, anchor=tk.CENTER) # Use ttk.Label and anchor
        # We'll pack this when an image is loaded to center it better
        # self.image_display_label.pack(padx=10, pady=10, expand=True)


        # Download button
        self.download_button = ttk.Button(content_frame, text="Download Grayscale Image", command=self.save_image, state=tk.DISABLED, style="Accent.TButton") # Use ttk.Button and style
        self.download_button.pack(pady=(5,10)) # Adjusted padding

        # Configure a style for the button
        self.style.configure("Accent.TButton", font=('Helvetica', 10, 'bold'))

    def handle_drop(self, event):
        # This function will be called when a file is dropped.
        # We'll need to get the file path from event.data
        filepath = event.data
        # Basic validation for now, can be improved
        if filepath and (filepath.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))):
            # Remove text from drop target
            self.drop_target_label.config(text="") # Clear text on successful drop
            self.load_image(filepath)
        else:
            print("Invalid file type. Please drop an image file.")
            # Optionally, provide feedback in the UI
            self.drop_target_label.config(text="Invalid file type. Drop a PNG, JPG, BMP, or GIF.")


    def load_image(self, filepath):
        self.image_path = filepath
        try:
            self.original_image = Image.open(filepath)
            self.convert_to_grayscale()
            self.display_image(self.processed_image) # This will now also pack the image label
            self.download_button.config(state=tk.NORMAL)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.image_path = None
            self.original_image = None
            self.processed_image = None
            self.download_button.config(state=tk.DISABLED)
            if self.image_display_label:
                self.image_display_label.pack_forget() # Hide if error
                self.image_display_label.config(image='')
            self.drop_target_label.config(text="Error loading image. Try another.") # Update drop label


    def convert_to_grayscale(self):
        if not self.original_image:
            return

        img_copy = self.original_image.convert("RGB") # Ensure it's RGB
        width, height = img_copy.size
        new_img = Image.new("L", (width, height)) # "L" mode for grayscale

        for x in range(width):
            for y in range(height):
                r, g, b = img_copy.getpixel((x, y))
                # Formula: (R*11 + G*16 + B*5) / 32
                gray_value = (r * 11 + g * 16 + b * 5) // 32
                new_img.putpixel((x, y), gray_value)
        
        self.processed_image = new_img


    def display_image(self, image_to_display):
        if not image_to_display:
            if self.image_display_label:
                self.image_display_label.pack_forget()
            return
        
        # Resize image to fit within the image_frame
        # Get image_frame dimensions dynamically
        self.update_idletasks() # Ensure dimensions are up-to-date
        frame_width = self.image_display_label.master.winfo_width() - 20 # -20 for some padding
        frame_height = self.image_display_label.master.winfo_height() - 20

        max_width = max(50, frame_width) # Ensure at least 50px
        max_height = max(50, frame_height)
        
        img_copy = image_to_display.copy()
        img_copy.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        photo_image = ImageTk.PhotoImage(img_copy)
        
        if not self.image_display_label.winfo_ismapped(): # If not already packed
            self.image_display_label.pack(expand=True) # Pack it in the center of its frame

        self.image_display_label.config(image=photo_image)
        self.image_display_label.image = photo_image



    def save_image(self):
        if not self.processed_image:
            return

        # Ask user where to save the file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
            initialfile="grayscale_image.png" # Default filename
        )
        if file_path:
            try:
                self.processed_image.save(file_path)
                print(f"Image saved to {file_path}")
            except Exception as e:
                print(f"Error saving image: {e}")

if __name__ == "__main__":
    app = GreyscaleConverterApp()
    app.mainloop()


