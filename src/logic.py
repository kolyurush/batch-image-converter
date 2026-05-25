import os
from pathlib import Path
from typing import List, Tuple
from multiprocessing import Pool
from PIL import Image

SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff', '.ico'}
AVAILABLE_FORMATS = ["JPEG", "PNG", "WEBP", "BMP", "ICO"]

def convert_single_image(args: Tuple[Path, Path, str]) -> bool:
    """
    Конвертирует одиночное изображение в целевой формат.
    Включает безопасное масштабирование для формата ICO.
    """
    input_path, output_folder, target_format = args
    try:
        with Image.open(input_path) as img:
            target_fmt_upper = target_format.upper()
            
            if target_fmt_upper in ["JPEG", "JPG"]:
                img = img.convert("RGB")
            elif target_fmt_upper == "ICO":
                if img.size != (256, 256):
                    img = img.resize((256, 256), Image.Resampling.LANCZOS)
            
            target_ext = target_format.lower()
            output_path = output_folder / f"{input_path.stem}.{target_ext}"
            img.save(output_path, target_fmt_upper)
        return True
    except Exception as e:
        print(f"\nОшибка при обработке {input_path.name}: {e}")
        return False

def get_image_files(folder_path: str) -> List[Path]:
    """
    Возвращает список путей к поддерживаемым изображениям в папе.
    """
    path = Path(folder_path)
    if not path.exists():
        return []
    return [f for f in path.iterdir() if f.suffix.lower() in SUPPORTED_EXTENSIONS]

def batch_process_parallel(files: List[Path], output_dir: str, target_format: str) -> int:
    """
    Пакетная обработка файлов с использованием multiprocessing.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    tasks = [(file, output_path, target_format) for file in files]
    
    with Pool() as pool:
        results = pool.map(convert_single_image, tasks)
            
    return sum(1 for r in results if r)