"""
Code generator with AI task parsing - simple and efficient
"""

import json
import os
import re
from datetime import datetime

import g4f

# Localization dictionaries (shortened)
TRANSLATIONS = {
    "en": {
        "title": "🤖 Universal Python Code Generator",
        "generating": "🔄 Generating code for:",
        "code_generated": "✅ Code generated successfully",
        "generated_code": "GENERATED CODE:",
        "tasks_found": "🔍 Tasks found in file:",
        "save_prompt": "\nSave code to file? (y/n): ",
        "run_prompt": "Run generated code? (y/n): ",
        "file_saved": "File saved:",
        "goodbye": "Goodbye! 👋",
    },
    "uk": {
        "title": "🤖 Універсальний генератор Python коду",
        "generating": "🔄 Генеруємо код для:",
        "code_generated": "✅ Код згенеровано успішно",
        "generated_code": "ЗГЕНЕРОВАНИЙ КОД:",
        "tasks_found": "🔍 Знайдено завдань у файлі:",
        "save_prompt": "\nЗберегти код у файл? (y/n): ",
        "run_prompt": "Запустити згенерований код? (y/n): ",
        "file_saved": "Файл збережено:",
        "goodbye": "До побачення! 👋",
    },
    "ru": {
        "title": "🤖 Универсальный генератор Python кода",
        "generating": "🔄 Генерируем код для:",
        "code_generated": "✅ Код сгенерирован успешно",
        "generated_code": "СГЕНЕРИРОВАННЫЙ КОД:",
        "tasks_found": "🔍 Найдено заданий в файле:",
        "save_prompt": "\nСохранить код в файл? (y/n): ",
        "run_prompt": "Запустить сгенерированный код? (y/n): ",
        "file_saved": "Файл сохранен:",
        "goodbye": "До свидания! 👋",
    },
}


def get_text(key: str, language: str) -> str:
    """Gets localized text"""
    return TRANSLATIONS.get(language, TRANSLATIONS["en"]).get(key, key)


def clean_code(code: str) -> str:
    """Cleans code from markdown blocks"""
    if not code:
        return code

    code = code.strip()

    if code.startswith("```python"):
        code = code[9:]
    elif code.startswith("```"):
        code = code[3:]

    if code.endswith("```"):
        code = code[:-3]

    return code.strip()


def fix_square_spacing(code: str) -> str:
    """Fixes square code for visual equal-sidedness"""
    if "квадрат" in code.lower() or "square" in code.lower() or "*" in code:
        # Replace asterisk sequences with spaced asterisks
        code = re.sub(r'"(\*+)"', lambda m: '"' + " ".join(m.group(1)) + '"', code)
        code = re.sub(r"'(\*+)'", lambda m: "'" + " ".join(m.group(1)) + "'", code)

        # Replace single asterisks with spaced asterisks
        code = code.replace('print("*", end="")', 'print("* ", end="")')
        code = code.replace("print('*', end='')", "print('* ', end='')")
        code = code.replace('print(" ", end="")', 'print("  ", end="")')
        code = code.replace("print(' ', end='')", "print('  ', end='')")

    return code


def parse_tasks_with_ai(content: str, language: str = "en") -> list:
    """Parses tasks using AI - simple and efficient approach"""
    try:
        print("🤖 AI task parsing...")

        response = g4f.ChatCompletion.create(
            model="gpt-4o",
            provider=g4f.Provider.PollinationsAI,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                Parse this text and extract ALL programming tasks. Return ONLY a JSON array with this exact format:
                [
                    {{"id": 1, "description": "Task description here"}},
                    {{"id": 2, "description": "Task description here"}},
                    ...
                ]

                Rules:
                - Find ALL tasks, including those with numbers 1), 2), etc.
                - Find tasks that start with "–" (dash)
                - Find tasks about "створити функцію" (create function)
                - Find tasks about "вивести" (output/display)
                - Find tasks about list comprehension
                - Find tasks about multiplication tables (табличку множення)
                - Find tasks about while loops and for loops
                - Remove task numbers like "1)", "2)" from descriptions
                - Make first letter uppercase
                - Include ALL tasks, don't merge duplicates
                - Return ONLY valid JSON, no explanations

                Text to parse:
                {content}
                """,
                }
            ],
        )

        # Clean response from markdown
        cleaned_response = clean_code(response)

        # Try to parse JSON
        try:
            tasks_data = json.loads(cleaned_response)
            if isinstance(tasks_data, list):
                return tasks_data
        except json.JSONDecodeError:
            # If JSON is invalid, try to extract array
            json_match = re.search(r"\[.*\]", cleaned_response, re.DOTALL)
            if json_match:
                try:
                    tasks_data = json.loads(json_match.group())
                    if isinstance(tasks_data, list):
                        return tasks_data
                except json.JSONDecodeError:
                    pass

        print("❌ Task parsing error")
        return []

    except Exception as e:
        print(f"❌ AI parsing error: {e}")
        return []


def generate_code(task_description: str, language: str = "en") -> dict:
    """Генерирует код для задачи"""
    try:
        print(f"{get_text('generating', language)} {task_description[:60]}...")

        lang_instructions = {
            "ru": "Add comments in Russian",
            "uk": "Add comments in Ukrainian",
            "en": "Add comments in English",
        }

        response = g4f.ChatCompletion.create(
            model="gpt-4o",
            provider=g4f.Provider.PollinationsAI,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                Generate Python code for this task: {task_description}

                Requirements:
                - Clean, executable Python code
                - {lang_instructions.get(language, "Add comments in English")}
                - Use Python best practices
                - NO markdown blocks
                - NO explanations, only code
                - Create complete working solution
                
                Return ONLY the Python code, nothing else.
                """,
                }
            ],
        )

        cleaned_code = clean_code(response)
        # Исправляем квадраты для визуальной равносторонности
        cleaned_code = fix_square_spacing(cleaned_code)

        print(get_text("code_generated", language))

        return {
            "success": True,
            "code": cleaned_code,
            "task": task_description,
            "language": language,
            "error": None,
        }

    except Exception as e:
        print(f"❌ Ошибка генерации кода: {e}")
        fallback_code = f"""# Ошибка генерации кода: {e}
# Задача: {task_description}

def main():
    print("Код не был сгенерирован из-за ошибки")
    print("Задача: {task_description}")

if __name__ == "__main__":
    main()
"""
        return {
            "success": False,
            "code": fallback_code,
            "task": task_description,
            "language": language,
            "error": str(e),
        }


def save_code(code: str, task_name: str, task_id: int = 1, language: str = "en") -> str:
    """Сохраняет код в файл"""
    try:
        output_dir = "generated_code"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(
            c for c in task_name if c.isalnum() or c in (" ", "-", "_")
        ).strip()
        safe_name = safe_name.replace(" ", "_").lower()

        filename = f"task_{task_id}_{safe_name}_{timestamp}.py"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)

        print(f"✅ {get_text('file_saved', language)} {filepath}")
        return filepath

    except Exception as e:
        print(f"❌ Ошибка сохранения: {e}")
        return ""


def get_language_choice() -> str:
    """Выбор языка интерфейса"""
    print(
        "\nSelect interface language / Выберите язык интерфейса / Оберіть мову інтерфейсу:"
    )
    print("1. English (en) [default]")
    print("2. Українська (uk)")
    print("3. Русский (ru)")

    choice = input("Enter choice (1-3) [1]: ").strip()

    if choice == "2":
        return "uk"
    elif choice == "3":
        return "ru"
    else:
        return "en"


def main():
    """Главная функция с AI-парсингом"""
    # Выбор языка
    language = get_language_choice()

    print(f"\n{get_text('title', language)}")
    print("=" * 50)
    print("📁 AI-парсинг задач для точного извлечения")

    # Сканируем папку tasks
    tasks_dir = "tasks"
    if not os.path.exists(tasks_dir):
        print(f"❌ Папка {tasks_dir} не найдена!")
        return

    # Находим файлы заданий
    task_files = []
    for filename in os.listdir(tasks_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(tasks_dir, filename)
            description = filename.replace(".txt", "").replace("_", " ").title()
            task_files.append(
                {
                    "id": len(task_files) + 1,
                    "filename": filename,
                    "filepath": filepath,
                    "description": description,
                }
            )

    if not task_files:
        print("❌ В папке tasks не найдено файлов заданий (.txt)")
        return

    print(f"\n📂 Найдено файлов заданий: {len(task_files)}")

    # Выбор файла заданий
    while True:
        print("\n📁 Выберите файл заданий:")
        for file in task_files:
            print(f"{file['id']}. {file['description']} ({file['filename']})")
        print("0. Выход")

        choice = input("\nВведите номер файла (0 для выхода): ").strip()

        if choice == "0":
            print(get_text("goodbye", language))
            return

        try:
            file_id = int(choice)
            selected_file = next((f for f in task_files if f["id"] == file_id), None)

            if selected_file:
                print(f"✅ Выбран файл: {selected_file['description']}")

                # Загружаем содержимое файла
                try:
                    with open(selected_file["filepath"], "r", encoding="utf-8") as f:
                        content = f.read()

                    # Парсим задачи с помощью AI
                    tasks = parse_tasks_with_ai(content, language)

                    if not tasks:
                        print("❌ Не удалось извлечь задачи из файла")
                        continue

                    print(f"✅ {get_text('tasks_found', language)} {len(tasks)}")

                    # Показываем меню задач
                    while True:
                        print(f"\n📋 Задачи из файла {selected_file['filename']}:")
                        print("-" * 70)

                        # Находим максимальную длину номера для выравнивания
                        max_num_width = len(str(len(tasks)))

                        for i, task in enumerate(tasks, 1):
                            # Показываем краткое описание (первые 60 символов)
                            desc = task.get("description", "")
                            short_desc = desc[:60] + "..." if len(desc) > 60 else desc
                            # Форматируем с одинаковыми отступами
                            print(f"{i:>{max_num_width}}. {short_desc}")

                        print(f"{0:>{max_num_width}}. Назад к выбору файла")
                        print("-" * 70)

                        task_choice = input(
                            "\nВыберите задачу (0 для возврата): "
                        ).strip()

                        if task_choice == "0":
                            break

                        try:
                            task_id = int(task_choice)
                            if 1 <= task_id <= len(tasks):
                                selected_task = tasks[task_id - 1]

                                print(f"\n📝 Выбрана задача {task_id}:")
                                print(
                                    f"📋 Описание: {selected_task.get('description', '')}"
                                )

                                # Генерируем код
                                result = generate_code(
                                    selected_task.get("description", ""), language
                                )

                                # Показываем код
                                print("\n" + "=" * 50)
                                if result["success"]:
                                    print(get_text("generated_code", language))
                                    print("=" * 50)
                                    print(result["code"])
                                    print("=" * 50)

                                    # Сохраняем код
                                    save_choice = input(
                                        get_text("save_prompt", language)
                                    ).lower()
                                    if save_choice == "y":
                                        filepath = save_code(
                                            result["code"],
                                            f"task_{task_id}",
                                            task_id,
                                            language,
                                        )
                                        if filepath:
                                            # Предлагаем запустить код
                                            run_choice = input(
                                                get_text("run_prompt", language)
                                            ).lower()
                                            if run_choice == "y":
                                                try:
                                                    print("\n🔄 Запускаем код...")
                                                    print("-" * 30)
                                                    exec(result["code"])
                                                    print("-" * 30)
                                                    print("✅ Код выполнен успешно")
                                                except Exception as e:
                                                    print(f"❌ Ошибка выполнения: {e}")
                                else:
                                    print("ОШИБКА ГЕНЕРАЦИИ КОДА:")
                                    print("=" * 50)
                                    print(f"Ошибка: {result['error']}")
                                    print("Резервный код:")
                                    print(result["code"])
                                    print("=" * 50)
                            else:
                                print("❌ Неверный номер задачи")

                        except ValueError:
                            print("❌ Введите корректный номер")

                except Exception as e:
                    print(f"❌ Ошибка чтения файла: {e}")
                    continue

            else:
                print("❌ Неверный номер файла. Попробуйте еще раз.")

        except ValueError:
            print("❌ Введите корректный номер файла.")
        except KeyboardInterrupt:
            print(f"\n\n{get_text('goodbye', language)}")
            return


if __name__ == "__main__":
    main()
