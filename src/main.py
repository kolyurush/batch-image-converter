import sys
import argparse
from src.logic import get_image_files, batch_process_parallel, AVAILABLE_FORMATS

def parse_arguments():
    """Настройка argparse для работы через командную строку."""
    parser = argparse.ArgumentParser(description="Пакетный конвертер изображений на Python")
    
    parser.add_argument("-i", "--input", type=str, help="Путь к папке с исходными изображениями")
    parser.add_argument("-o", "--output", type=str, help="Путь к папке для сохранения результата")
    parser.add_argument("-f", "--format", type=str, choices=AVAILABLE_FORMATS, 
                        help="Целевой формат изображений")
    
    return parser.parse_args()

def main():
    """Точка входа в приложение. Переключает режимы CLI/GUI."""
    args = parse_arguments()

    if args.input and args.output and args.format:
        print(f"Запуск в консольном режиме...")
        files = get_image_files(args.input)
        
        if not files:
            print("В указанной папке не найдены поддерживаемые изображения.")
            sys.exit(1)
            
        print(f"Найдено файлов для обработки: {len(files)}")
        successful = batch_process_parallel(files, args.output, args.format)
        print(f"Успешно конвертировано файлов: {successful}")
        
    else:
        print("Аргументы командной строки не обнаружены. Запуск GUI...")
        from gui import ImageConverterApp
        app = ImageConverterApp()
        app.mainloop()

if __name__ == "__main__":
    main()