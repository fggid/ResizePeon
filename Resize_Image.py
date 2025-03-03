from PIL import Image
import os
import time
import json
import tkinter as tk
from tkinter import filedialog

SETTINGS_FILE = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)

def get_directory_path(setting_name, prompt_text):
    settings = load_settings()
    if setting_name in settings:
        return settings[setting_name]
    
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    path = filedialog.askdirectory(title=prompt_text)  # 让用户选择文件夹
    
    if not path:
        raise RuntimeError("未选择文件夹，程序终止。")

    settings[setting_name] = path
    save_settings(settings)
    return path

def resize_image(input_path, output_path, target_size_kb=1024, output_format='JPEG', quality=85):
    target_size = target_size_kb * 1024
    img = Image.open(input_path)

    if img.mode == 'RGBA':
        img = img.convert('RGB')

    img_format = img.format if output_format is None else output_format

    width, height = img.size
    scale_factor = 1.0

    while True:
        img_resized = img.resize((int(width * scale_factor), int(height * scale_factor)), Image.LANCZOS)
        img_resized.save(output_path, format=img_format, quality=quality)

        if os.path.getsize(output_path) <= target_size or scale_factor <= 0.1:
            break

        scale_factor *= 0.9

    if img_format == 'JPEG':
        while os.path.getsize(output_path) > target_size and quality > 10:
            quality -= 5
            img_resized.save(output_path, format=img_format, quality=quality)

    print(f"图片已保存至 {output_path}，最终大小 {os.path.getsize(output_path) / 1024:.2f} KB")

def process_directory(input_dir, output_dir, target_size_kb=1024, output_format='JPEG'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        if os.path.isfile(input_path) and filename.lower().endswith(('png', 'jpg', 'jpeg', 'webp')):
            timestamp = os.path.getctime(input_path)
            formatted_time = time.strftime("%Y%m%d%H%M%S", time.localtime(timestamp))
            
            new_input_path = os.path.join(input_dir, f"{formatted_time}{os.path.splitext(filename)[1]}")
            os.rename(input_path, new_input_path)
            
            if os.path.getsize(new_input_path) <= target_size_kb * 1024:
                print(f"{new_input_path} 已重命名，文件小于 {target_size_kb}KB，无需转换。")
                continue
            
            output_filename = f"{formatted_time}.jpg"
            output_path = os.path.join(output_dir, output_filename)
            resize_image(new_input_path, output_path, target_size_kb, output_format)

if __name__ == "__main__":
    input_directory = get_directory_path("input_directory", "请选择输入文件夹")
    output_directory = get_directory_path("output_directory", "请选择输出文件夹")
    process_directory(input_directory, output_directory)
