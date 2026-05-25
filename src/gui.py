import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from src.logic import get_image_files, batch_process_parallel, AVAILABLE_FORMATS

class ImageConverterApp(ctk.CTk):
    def __init__(self):
        """Инициализация главного окна и компонентов интерфейса."""
        super().__init__()

        self.title("Batch Image Converter")
        self.geometry("550x450")
        ctk.set_appearance_mode("dark")

        self.input_folder = ""
        self.output_folder = ""

        # UI Elements
        self.label = ctk.CTkLabel(self, text="Пакетный конвертер изображений", font=("Arial", 20))
        self.label.pack(pady=20)

        self.btn_input = ctk.CTkButton(self, text="Выбрать папку с фото", command=self.select_input)
        self.btn_input.pack(pady=5)

        self.lbl_input_path = ctk.CTkLabel(self, text="Папка не выбрана", text_color="gray", font=("Arial", 12))
        self.lbl_input_path.pack(pady=5)

        # Выпадающий список использует AVAILABLE_FORMATS из logic.py (нет хардкоду!)
        self.format_menu = ctk.CTkOptionMenu(self, values=AVAILABLE_FORMATS)
        self.format_menu.pack(pady=10)

        self.btn_output = ctk.CTkButton(self, text="Выбрать папку сохранения", command=self.select_output)
        self.btn_output.pack(pady=5)

        self.lbl_output_path = ctk.CTkLabel(self, text="Папка не выбрана", text_color="gray", font=("Arial", 12))
        self.lbl_output_path.pack(pady=5)

        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.set(0)
        self.progress.pack(pady=20)

        self.btn_start = ctk.CTkButton(self, text="Начать конвертацию", fg_color="green", command=self.start_conversion)
        self.btn_start.pack(pady=10)

    def select_input(self):
        """Открывает диалог выбора исходной папки и подсчитывает файлы."""
        self.input_folder = filedialog.askdirectory()
        if self.input_folder:
            files_count = len(get_image_files(self.input_folder))
            self.lbl_input_path.configure(
                text=f"Откуда: {self.input_folder} (Найдено файлов: {files_count})", 
                text_color="white"
            )
        else:
            self.lbl_input_path.configure(text="Папка не выбрана", text_color="gray")

    def select_output(self):
        """Открывает диалог выбора папки для сохранения результатов."""
        self.output_folder = filedialog.askdirectory()
        if self.output_folder:
            self.lbl_output_path.configure(text=f"Куда: {self.output_folder}", text_color="white")
        else:
            self.lbl_output_path.configure(text="Папка не выбрана", text_color="gray")

    def start_conversion(self):
        """Инициирует процесс конвертации в фоновом потоке."""
        files = get_image_files(self.input_folder)
        if not files or not self.output_folder:
            messagebox.showerror("Ошибка", "Выберите корректные папки для работы!")
            return

        target_fmt = self.format_menu.get()
        self.btn_start.configure(state="disabled")
        
        thread = threading.Thread(target=self.run_process, args=(files, target_fmt))
        thread.start()

    def run_process(self, files, target_fmt):
        """Запускает параллельную обработку и управляет состоянием индикатора."""
        self.progress.configure(mode="indeterminate")
        self.progress.start()
        
        count = batch_process_parallel(files, self.output_folder, target_fmt)
        
        self.progress.stop()
        self.progress.configure(mode="determinate")
        self.progress.set(1.0)
        
        self.btn_start.configure(state="normal")
        messagebox.showinfo("Успех", f"Обработано файлов с помощью multiprocessing: {count}")
        self.progress.set(0)