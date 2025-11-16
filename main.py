import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# ----------------------------------------------------
# 画像処理アプリ（Tkinter）
#  - 読込 → グレースケール → パターン①/② → PNG保存
# ----------------------------------------------------

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        self.root.geometry("1400x1000")  # Window size

        # ---------------------------
        # Preview size in pixels
        # ---------------------------
        self.preview_width = 1200
        self.preview_height = 800

        # ---------------------------
        # Original & processed images
        # ---------------------------
        self.original_img = None
        self.processed_img = None

        # ---------------------------
        # Image display label
        # ---------------------------
        self.img_label = tk.Label(root, text="No Image", bg="gray")
        self.img_label.pack(pady=10)

        # ---------------------------
        # Buttons frame
        # ---------------------------
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        # Load button
        tk.Button(btn_frame, text="画像読込", command=self.load_image, width=20).grid(row=0, column=0, padx=5)

        # Show Original button
        tk.Button(
            btn_frame,
            text="元画像表示",
            command=self.show_original,
            width=20
        ).grid(row=0, column=1, padx=5)
        
        # Pattern 1 button
        tk.Button(
            btn_frame,
            text="画像処理（1）白透明・黒不透明",
            command=self.process_pattern1,
            width=30
        ).grid(row=0, column=2, padx=5)

        # Pattern 2 button
        tk.Button(
            btn_frame,
            text="画像処理（2）黒透明・白不透明",
            command=self.process_pattern2,
            width=30
        ).grid(row=0, column=3, padx=5)

        # Save button
        tk.Button(btn_frame, text="画像保存", command=self.save_image, width=20).grid(row=0, column=4, padx=5)

    # ---------------------------
    # Load image
    # ---------------------------
    def load_image(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if not filepath:
            return

        self.original_img = Image.open(filepath).convert("RGB")
        self.processed_img = None

        self.display_image(self.original_img)

    # ---------------------------
    # Display image on label
    # ---------------------------
    def display_image(self, img):
        # Make a copy and scale to preview size
        preview = img.copy()
        preview.thumbnail((self.preview_width, self.preview_height))

        self.tk_img = ImageTk.PhotoImage(preview)
        self.img_label.config(image=self.tk_img)

    # ---------------------------    
    # Show Original Image 
    # ---------------------------    
    def show_original(self):
        if self.original_img is None:
            messagebox.showwarning("Warning", "画像を読み込んでください。")
            return
        self.display_image(self.original_img)

    # ---------------------------
    # Pattern 1: White transparent, black opaque
    # Background white, alpha = 255 - grayscale
    # ---------------------------
    def process_pattern1(self):
        if self.original_img is None:
            messagebox.showwarning("Warning", "画像を読み込んでください。")
            return

        gray = self.original_img.convert("L")  # Grayscale

        # White → transparent (α0), Black → opaque (α255)
        alpha = gray.point(lambda x: 255 - x)

        # White background
        white_bg = Image.new("RGB", self.original_img.size, (255, 255, 255))

        # Merge RGBA
        self.processed_img = Image.merge("RGBA", (*white_bg.split(), alpha))

        self.display_image(self.processed_img)

    # ---------------------------
    # Pattern 2: Black transparent, white opaque
    # Background black, alpha = grayscale
    # ---------------------------
    def process_pattern2(self):
        if self.original_img is None:
            messagebox.showwarning("Warning", "画像を読み込んでください。")
            return

        gray = self.original_img.convert("L")  # Grayscale

        # Black → transparent (α0), White → opaque (α255)
        alpha = gray.copy()

        # Black background
        black_bg = Image.new("RGB", self.original_img.size, (0, 0, 0))

        # Merge RGBA
        self.processed_img = Image.merge("RGBA", (*black_bg.split(), alpha))

        self.display_image(self.processed_img)

    # ---------------------------
    # Save processed image as PNG
    # ---------------------------
    def save_image(self):
        if self.processed_img is None:
            messagebox.showwarning("Warning", "処理後の画像がありません。")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png")]
        )
        if not filepath:
            return

        self.processed_img.save(filepath)
        messagebox.showinfo("Saved", "画像を保存しました。")



# ---------------------------
# Run application
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
