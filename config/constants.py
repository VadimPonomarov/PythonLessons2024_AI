"""
Configuration constants and localization
"""

# Localization dictionaries
TRANSLATIONS = {
    "en": {
        "title": "🤖 Universal Python Code Generator",
        "subtitle": "📁 AI-powered task parsing and code generation",
        "lang_prompt": "\nSelect interface language / Выберите язык интерфейса / Оберіть мову інтерфейсу:",
        "lang_choice": "Enter choice (1-3) [1]: ",
        "files_found": "📂 Task files found:",
        "select_file": "\n📁 Select task file:",
        "exit": "Exit",
        "file_prompt": "\nEnter file number (0 to exit): ",
        "goodbye": "Goodbye! 👋",
        "file_selected": "✅ File selected:",
        "tasks_found": "🔍 Tasks found in file:",
        "tasks_loaded": "✅ Tasks loaded:",
        "tasks_from_file": "📋 Tasks from file",
        "back_to_files": "Back to file selection",
        "task_prompt": "\nSelect task (0 to return): ",
        "task_selected": "📝 Task selected",
        "description": "📋 Description:",
        "generating": "🔄 Generating code for:",
        "code_generated": "✅ Code generated successfully",
        "generated_code": "GENERATED CODE:",
        "save_prompt": "\nSave code to file? (y/n): ",
        "file_saved": "File saved:",
        "run_prompt": "Run generated code? (y/n): ",
        "running_code": "🔄 Running code...",
        "code_executed": "✅ Code executed successfully",
        "execution_error": "❌ Execution error:",
        "generation_error": "❌ Code generation error:",
        "error": "Error:",
        "fallback_code": "Fallback code:",
        "invalid_task": "❌ Invalid task number",
        "invalid_number": "❌ Enter a valid number",
        "invalid_file": "❌ Invalid file number. Try again.",
        "folder_not_found": "❌ Folder not found!",
        "no_task_files": "❌ No task files (.txt) found in tasks folder",
        "file_load_error": "❌ Could not load tasks from file",
        "save_error": "❌ Save error:",
        "file_read_error": "❌ File read error"
    },
    "uk": {
        "title": "🤖 Універсальний генератор Python коду",
        "subtitle": "📁 AI-парсинг завдань та генерація коду",
        "lang_prompt": "\nОберіть мову інтерфейсу / Select interface language / Выберите язык интерфейса:",
        "lang_choice": "Введіть вибір (1-3) [1]: ",
        "files_found": "📂 Знайдено файлів завдань:",
        "select_file": "\n📁 Оберіть файл завдань:",
        "exit": "Вихід",
        "file_prompt": "\nВведіть номер файлу (0 для виходу): ",
        "goodbye": "До побачення! 👋",
        "file_selected": "✅ Обрано файл:",
        "tasks_found": "🔍 Знайдено завдань у файлі:",
        "tasks_loaded": "✅ Завдання завантажено:",
        "tasks_from_file": "📋 Завдання з файлу",
        "back_to_files": "Назад до вибору файлу",
        "task_prompt": "\nОберіть завдання (0 для повернення): ",
        "task_selected": "📝 Обрано завдання",
        "description": "📋 Опис:",
        "generating": "🔄 Генеруємо код для:",
        "code_generated": "✅ Код згенеровано успішно",
        "generated_code": "ЗГЕНЕРОВАНИЙ КОД:",
        "save_prompt": "\nЗберегти код у файл? (y/n): ",
        "file_saved": "Файл збережено:",
        "run_prompt": "Запустити згенерований код? (y/n): ",
        "running_code": "🔄 Запускаємо код...",
        "code_executed": "✅ Код виконано успішно",
        "execution_error": "❌ Помилка виконання:",
        "generation_error": "❌ Помилка генерації коду:",
        "error": "Помилка:",
        "fallback_code": "Резервний код:",
        "invalid_task": "❌ Невірний номер завдання",
        "invalid_number": "❌ Введіть правильний номер",
        "invalid_file": "❌ Невірний номер файлу. Спробуйте ще раз.",
        "folder_not_found": "❌ Папку не знайдено!",
        "no_task_files": "❌ У папці tasks не знайдено файлів завдань (.txt)",
        "file_load_error": "❌ Не вдалося завантажити завдання з файлу",
        "save_error": "❌ Помилка збереження:",
        "file_read_error": "❌ Помилка читання файлу"
    },
    "ru": {
        "title": "🤖 Универсальный генератор Python кода",
        "subtitle": "📁 AI-парсинг заданий и генерация кода",
        "lang_prompt": "\nВыберите язык интерфейса / Select interface language / Оберіть мову інтерфейсу:",
        "lang_choice": "Введите выбор (1-3) [1]: ",
        "files_found": "📂 Найдено файлов заданий:",
        "select_file": "\n📁 Выберите файл заданий:",
        "exit": "Выход",
        "file_prompt": "\nВведите номер файла (0 для выхода): ",
        "goodbye": "До свидания! 👋",
        "file_selected": "✅ Выбран файл:",
        "tasks_found": "🔍 Найдено заданий в файле:",
        "tasks_loaded": "✅ Задания загружены:",
        "tasks_from_file": "📋 Задания из файла",
        "back_to_files": "Назад к выбору файла",
        "task_prompt": "\nВыберите задание (0 для возврата): ",
        "task_selected": "📝 Выбрано задание",
        "description": "📋 Описание:",
        "generating": "🔄 Генерируем код для:",
        "code_generated": "✅ Код сгенерирован успешно",
        "generated_code": "СГЕНЕРИРОВАННЫЙ КОД:",
        "save_prompt": "\nСохранить код в файл? (y/n): ",
        "file_saved": "Файл сохранен:",
        "run_prompt": "Запустить сгенерированный код? (y/n): ",
        "running_code": "🔄 Запускаем код...",
        "code_executed": "✅ Код выполнен успешно",
        "execution_error": "❌ Ошибка выполнения:",
        "generation_error": "❌ Ошибка генерации кода:",
        "error": "Ошибка:",
        "fallback_code": "Резервный код:",
        "invalid_task": "❌ Неверный номер задания",
        "invalid_number": "❌ Введите корректный номер",
        "invalid_file": "❌ Неверный номер файла. Попробуйте еще раз.",
        "folder_not_found": "❌ Папка не найдена!",
        "no_task_files": "❌ В папке tasks не найдено файлов заданий (.txt)",
        "file_load_error": "❌ Не удалось загрузить задания из файла",
        "save_error": "❌ Ошибка сохранения:",
        "file_read_error": "❌ Ошибка чтения файла"
    }
}

# AI Configuration
AI_CONFIG = {
    "model": "gpt-4o",
    "provider": "PollinationsAI",
    "max_retries": 3,
    "timeout": 30
}

# File Configuration
FILE_CONFIG = {
    "tasks_dir": "tasks",
    "output_dir": "generated_code",
    "file_extension": ".txt",
    "encoding": "utf-8"
}

# UI Configuration
UI_CONFIG = {
    "separator_length": 70,
    "description_max_length": 60,
    "menu_padding": 2
}


def get_text(key: str, language: str) -> str:
    """Gets localized text"""
    return TRANSLATIONS.get(language, TRANSLATIONS["en"]).get(key, key)
