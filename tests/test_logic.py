import pytest
from pathlib import Path
from PIL import Image
from src.logic import convert_single_image, get_image_files

@pytest.fixture
def temp_workspace(tmp_path):
    """Фикстура для создания временных папок ввода и вывода."""
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()
    return input_dir, output_dir

def test_successful_conversion(temp_workspace):
    """Сценарий 1: Успешная конвертация PNG в JPEG с изменением цветового режима."""
    input_dir, output_dir = temp_workspace
    
    # Создаем тестовое PNG изображение (с альфа-каналом RGBA)
    img_path = input_dir / "test_image.png"
    img = Image.new("RGBA", (100, 100), color="blue")
    img.save(img_path, "PNG")
    
    # Запуск одиночной конвертации
    args = (img_path, output_dir, "JPEG")
    result = convert_single_image(args)
    
    # Проверки (Assertions)
    expected_file = output_dir / "test_image.jpeg"
    assert result is True, "Функция должна вернуть True при успешной обработке"
    assert expected_file.exists(), "Целевой файл должен быть создан"
    
    with Image.open(expected_file) as out_img:
        assert out_img.format == "JPEG"
        assert out_img.mode == "RGB", "PNG с прозрачностью должен успешно приводиться к RGB для JPEG"

def test_ico_conversion_resizes(temp_workspace):
    """Сценарий 2: Конвертация в ICO со специальным ресайзом до 256x256."""
    input_dir, output_dir = temp_workspace
    
    # Создаем большое изображение 1024x768
    img_path = input_dir / "large_photo.jpg"
    img = Image.new("RGB", (1024, 768), color="green")
    img.save(img_path, "JPEG")
    
    args = (img_path, output_dir, "ICO")
    result = convert_single_image(args)
    
    expected_file = output_dir / "large_photo.ico"
    assert result is True
    assert expected_file.exists()
    
    with Image.open(expected_file) as out_img:
        assert out_img.format == "ICO"
        assert out_img.size == (256, 256), "Изображение для ICO должно автоматически сжиматься до 256x256"

def test_invalid_file_error_handling(temp_workspace):
    """Сценарий 3: Обработка ошибок при попытке конвертировать «битый» или нетекстовый файл."""
    input_dir, output_dir = temp_workspace
    
    # Создаем фейковый файл, который притворяется картинкой
    fake_img_path = input_dir / "fake.png"
    fake_img_path.write_text("Это не картинка, а обычный текст")
    
    args = (fake_img_path, output_dir, "JPEG")
    result = convert_single_image(args)
    
    # Проверяем, что программа не упала с критической ошибкой, а безопасно вернула False
    assert result is False, "Функция должна обработать исключение Pillow и вернуть False"

def test_get_image_files_filtering(temp_workspace):
    """Сценарий 4: Проверка валидации расширений файлов при сканировании папки."""
    input_dir, _ = temp_workspace
    
    # Создаем один валидный файл и один невалидный (текстовый лог)
    (input_dir / "photo.jpg").write_text("fake_data")
    (input_dir / "report.txt").write_text("some_text")
    
    found_files = get_image_files(str(input_dir))
    
    assert len(found_files) == 1, "Должен найтись только файл с поддерживаемым расширением"
    assert found_files[0].name == "photo.jpg"