import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps

# ----------------------------------------------------
# 画像処理アプリ（Tkinter）
#  - 読込 → グレースケール → パターン①/② → PNG保存
# ----------------------------------------------------

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")

        # 読み込んだ元画像
        self.original_img = None
        # 処理後の画像
        self.processed_img = None

        # 画像表示領域（ラベル）
        self.img_label = tk.Label(root, text="No Image", width=60, height=20, bg="gray")
        self.img_label.pack(pady=10)

        # ボタンを配置するフレーム
        btn_frame = tk.Frame(root)
        btn_frame.pack()

        # 読み込みボタン
        tk.Button(btn_frame, text="画像読込", command=self.load_image, width=20).grid(row=0, column=0, padx=5)

        # パターン1ボタン
        tk.Button(btn_frame, text="画像処理（1）白透明・黒不透明", command=self.process_pattern1, width=30).grid(row=0, column=1, padx=5)

        # パターン2ボタン
        tk.Button(btn_frame, text="画像処理（2）黒透明・白不透明", command=self.process_pattern2, width=30).grid(row=0, column=2, padx=5)

        # 保存ボタン
        tk.Button(btn_frame, text="画像保存", command=self.save_image, width=20).grid(row=0, column=3, padx=5)

    # ----------------------------------------------------
    # 画像読込
    # ----------------------------------------------------
    def load_image(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if not filepath:
            return

        self.original_img = Image.open(filepath).convert("RGB")
        self.processed_img = None

        self.display_image(self.original_img)

    # ----------------------------------------------------
    # 画面に画像をプレビュー表示
    # ----------------------------------------------------
    def display_image(self, img):
        # Tkinter表示用に縮小（画面サイズに合わせる）
        preview = img.copy()
        preview.thumbnail((600, 400))

        self.tk_img = ImageTk.PhotoImage(preview)
        self.img_label.config(image=self.tk_img)

    # ----------------------------------------------------
    # パターン（1）白透明・黒不透明
    # 背景白、α = 255 - グレースケール
    # ----------------------------------------------------
    def process_pattern1(self):
        if self.original_img is None:
            messagebox.showwarning("Warning", "画像を読み込んでください。")
            return

        gray = self.original_img.convert("L")  # グレースケール

        # 白→透明（α0）、黒→不透明（α255）
        alpha = gray.point(lambda x: 255 - x)

        # 白背景
        white_bg = Image.new("RGB", self.original_img.size, (255, 255, 255))

        # RGBA合成
        self.processed_img = Image.merge("RGBA", (*white_bg.split(), alpha))

        self.display_image(self.processed_img)

    # ----------------------------------------------------
    # パターン（2）黒透明・白不透明
    # 背景黒、α = グレースケールそのまま
    # ----------------------------------------------------
    def process_pattern2(self):
        if self.original_img is None:
            messagebox.showwarning("Warning", "画像を読み込んでください。")
            return

        gray = self.original_img.convert("L")  # グレースケール

        # 黒→透明（α0）、白→不透明（α255）
        alpha = gray.copy()

        # 黒背景
        black_bg = Image.new("RGB", self.original_img.size, (0, 0, 0))

        # RGBA合成
        self.processed_img = Image.merge("RGBA", (*black_bg.split(), alpha))

        self.display_image(self.processed_img)

    # ----------------------------------------------------
    # PNG保存（透明背景）
    # ----------------------------------------------------
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


# ----------------------------------------------------
# アプリ起動
# ----------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
