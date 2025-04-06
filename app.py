#ПРОЭКТ В АЛЬФА ВЕРСИИ!!!!!!!!!!!!! ТАК ЧТО ИЗВИНИТЕ ЗА БАГИ. THE PROJECT IS IN ALPHA VERSION!!!!!!!!!!!!! SO SORRY FOR THE BUGS.
import os
import requests
import tkinter as tk
from tkinter import filedialog, messagebox
import time


languages = {
    "ru": {
        "choose_language": "Выберите язык:",
        "choose_method": "Как будете скачивать?",
        "txt_file_option": "1. Из файла (txt)",
        "url_option": "2. Вставить ссылки",
        "enter_urls": "Вставьте ссылки скачивания (разделённые пробелами):",
        "file_dialog": "Выберите файл с URL",
        "folder_dialog": "Выберите папку для сохранения файлов",
        "download_started": "Загрузка началась...",
        "file_downloaded": "Файл '{filename}' был загружен.",
        "download_finished": "Загрузка завершена!",
        "error": "Ошибка при скачивании. Попробуйте снова.",
        "max_retries": "Превышено количество попыток. Переход к следующему файлу.",
    },
    "en": {
        "choose_language": "Choose your language:",
        "choose_method": "How will you download?",
        "txt_file_option": "1. From a txt file",
        "url_option": "2. Insert URLs",
        "enter_urls": "Paste the download links (separated by spaces):",
        "file_dialog": "Choose a file with URLs",
        "folder_dialog": "Choose a folder to save files",
        "download_started": "Download started...",
        "file_downloaded": "File '{filename}' was downloaded.",
        "download_finished": "Download finished!",
        "error": "Download error. Please try again.",
        "max_retries": "Max retries exceeded. Moving to the next file.",
    }
}


def choose_language():
    print(languages["en"]["choose_language"])
    print("1. Русский")
    print("2. English")
    language_choice = input("Введите номер: ")
    if language_choice == "1":
        return "ru"
    elif language_choice == "2":
        return "en"
    else:
        print("Неверный выбор, по умолчанию выбран русский.")
        return "ru"


def download_file_with_retries(url, folder_path, lang, max_retries=10):
    attempts = 0
    while attempts < max_retries:
        try:
            filename = url.split("/")[-1]
            file_path = os.path.join(folder_path, filename)

            response = requests.get(url, stream=True)
            response.raise_for_status()  

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(languages[lang]["file_downloaded"].format(filename=filename))
            return True 
        except requests.exceptions.RequestException as e:
            attempts += 1
            print(f"{languages[lang]['error']} Попытка {attempts} из {max_retries}. Ошибка: {e}.")
            time.sleep(2) 
    print(languages[lang]["max_retries"])
    return False  


def download_files_from_list(urls, download_folder, lang):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    for url in urls:
        url = url.strip()  
        if url:
            success = download_file_with_retries(url, download_folder, lang)
            if not success:
                print(f"{languages[lang]['max_retries']}. Переход к следующему файлу.")
                continue  

def select_files_and_folder(lang):

    root = tk.Tk()
    root.withdraw()  


    urls_file = filedialog.askopenfilename(title=languages[lang]["file_dialog"], filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if not urls_file:
        messagebox.showerror("Ошибка", "Вы не выбрали файл с ссылками.")
        return

    download_folder = filedialog.askdirectory(title=languages[lang]["folder_dialog"])
    if not download_folder:
        messagebox.showerror("Ошибка", "Вы не выбрали папку для сохранения.")
        return

    with open(urls_file, 'r') as file:
        urls = file.readlines()

    download_files_from_list(urls, download_folder, lang)
    messagebox.showinfo("Завершено", languages[lang]["download_finished"])

def enter_urls_and_download(lang):
    
    print(languages[lang]["enter_urls"])
    urls_input = input("Введите ссылки через пробел: ")

    
    urls = [url.strip() for url in urls_input.split()]

    if not urls:
        print("Вы не ввели ссылки.")
        return

    
    root = tk.Tk()
    root.withdraw()  
    download_folder = filedialog.askdirectory(title=languages[lang]["folder_dialog"])
    if not download_folder:
        messagebox.showerror("Ошибка", "Вы не выбрали папку для сохранения.")
        return


    download_files_from_list(urls, download_folder, lang)
    messagebox.showinfo("Завершено", languages[lang]["download_finished"])

def main():
    lang = choose_language()  
    print(languages[lang]["choose_method"])
    print(languages[lang]["txt_file_option"])
    print(languages[lang]["url_option"])

    method_choice = input("Введите номер: ")

    if method_choice == "1":
        select_files_and_folder(lang)  
    elif method_choice == "2":
        enter_urls_and_download(lang)  
    else:
        print("Неверный выбор. Программа завершена.")

if __name__ == "__main__":
    main()
