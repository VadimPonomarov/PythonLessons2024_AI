"""
🤖 Universal Python Code Generator
AI-powered code generation with intelligent task parsing and visual improvements
"""

import json
import os
import re
from datetime import datetime

import g4f


def clean_code(code: str) -> str:
    """Cleans code from markdown blocks"""
    if not code:
        return code

    code = code.strip()

    # Remove markdown blocks
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


def generate_code(task_description: str, language: str = "ru") -> dict:
    """Generates code for task with structured response"""
    try:
        print(f"🔄 Generating code for: {task_description[:60]}...")

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
                - {lang_instructions.get(language, "Add comments in Russian")}
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
        # Fix squares for visual equal-sidedness
        cleaned_code = fix_square_spacing(cleaned_code)

        print("✅ Code generated successfully")

        return {
            "success": True,
            "code": cleaned_code,
            "task": task_description,
            "language": language,
            "error": None,
        }

    except Exception as e:
        print(f"❌ Code generation error: {e}")
        fallback_code = f"""# Code generation error: {e}
# Task: {task_description}

def main():
    print("Code was not generated due to error")
    print("Task: {task_description}")

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


def save_code(code: str, task_name: str, task_id: int = 1) -> str:
    """Сохраняет код в файл с организованной структурой"""
    try:
        # Создаем папку для сгенерированного кода
        output_dir = "generated_code"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Создаем имя файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(
            c for c in task_name if c.isalnum() or c in (" ", "-", "_")
        ).strip()
        safe_name = safe_name.replace(" ", "_").lower()

        filename = f"task_{task_id}_{safe_name}_{timestamp}.py"
        filepath = os.path.join(output_dir, filename)

        # Сохраняем код
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)

        print(f"✅ Код сохранен: {filepath}")
        return filepath

    except Exception as e:
        print(f"❌ Ошибка сохранения: {e}")
        return ""


def get_language_choice():
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


def load_tasks_from_file(filepath: str):
    """Loads tasks from file using AI parsing"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Use AI to parse tasks
        print("🤖 AI parsing tasks...")

        response = g4f.ChatCompletion.create(
            model="gpt-4o",
            provider=g4f.Provider.PollinationsAI,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                Parse this text and extract ALL programming tasks. Return ONLY a JSON array:
                [
                    {{"id": 1, "description": "Task description here"}},
                    {{"id": 2, "description": "Task description here"}},
                    ...
                ]

                Rules:
                - Find ALL tasks (1), 2), –, functions, etc.)
                - Remove task numbers like "1)", "2)" from descriptions
                - Make first letter uppercase
                - Include multiplication tables and squares
                - Include ALL tasks, don't merge duplicates
                - Return ONLY valid JSON, no explanations

                Text: {content}
                """,
                }
            ],
        )

        # Parse JSON response
        import json
        import re

        cleaned_response = clean_code(response)

        try:
            tasks_data = json.loads(cleaned_response)
            if isinstance(tasks_data, list):
                print(f"🔍 Found {len(tasks_data)} tasks in file:")
                for i, task in enumerate(tasks_data, 1):
                    desc = task.get("description", "")
                    short_desc = desc[:60] + "..." if len(desc) > 60 else desc
                    print(f"   {i}. {short_desc}")
                return tasks_data
        except json.JSONDecodeError:
            # Try to extract JSON array from text
            json_match = re.search(r"\[.*\]", cleaned_response, re.DOTALL)
            if json_match:
                try:
                    tasks_data = json.loads(json_match.group())
                    if isinstance(tasks_data, list):
                        print(f"🔍 Found {len(tasks_data)} tasks in file:")
                        for i, task in enumerate(tasks_data, 1):
                            desc = task.get("description", "")
                            short_desc = desc[:60] + "..." if len(desc) > 60 else desc
                            print(f"   {i}. {short_desc}")
                        return tasks_data
                except json.JSONDecodeError:
                    pass

        print("❌ AI parsing failed, using fallback")
        return []

    except Exception as e:
        print(f"❌ Error reading file {filepath}: {e}")
        return []


def main():
    """Главная функция"""
    print("🤖 Universal Python Code Generator")
    print("==================================")
    print("📁 Автоматический выбор файлов заданий из папки 'tasks'")

    # Выбор языка
    language = get_language_choice()

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
        print("❌ В папке tasks не найдено файлов с заданиями (.txt)")
        return

    print(f"\n📂 Найдено файлов заданий: {len(task_files)}")

    # Выбор файла заданий
    while True:
        print("\n📁 Выберите файл с заданиями:")
        for file in task_files:
            print(f"{file['id']}. {file['description']} ({file['filename']})")
        print("0. Выход")

        choice = input("\nВведите номер файла (0 для выхода): ").strip()

        if choice == "0":
            print("До свидания! 👋")
            return

        try:
            file_id = int(choice)
            selected_file = next((f for f in task_files if f["id"] == file_id), None)

            if selected_file:
                print(f"✅ Выбран файл: {selected_file['description']}")

                # Загружаем задачи из файла
                tasks = load_tasks_from_file(selected_file["filepath"])

                if not tasks:
                    print("❌ Не удалось загрузить задачи из файла")
                    continue

                print(f"✅ Загружено задач: {len(tasks)}")

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

                    task_choice = input("\nВыберите задачу (0 для возврата): ").strip()

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
                                print("СГЕНЕРИРОВАННЫЙ КОД:")
                                print("=" * 50)
                                print(result["code"])
                                print("=" * 50)

                                # Сохраняем код
                                save_choice = input(
                                    "\nСохранить код в файл? (y/n): "
                                ).lower()
                                if save_choice == "y":
                                    filepath = save_code(
                                        result["code"], f"task_{task_id}", task_id
                                    )
                                    if filepath:
                                        print(f"Файл сохранен: {filepath}")

                                        # Предлагаем запустить код
                                        run_choice = input(
                                            "Запустить сгенерированный код? (y/n): "
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
                                print("Fallback код:")
                                print(result["code"])
                                print("=" * 50)
                        else:
                            print("❌ Неверный номер задачи")

                    except ValueError:
                        print("❌ Введите корректный номер")

            else:
                print("❌ Неверный номер файла. Попробуйте еще раз.")

        except ValueError:
            print("❌ Введите корректный номер файла.")
        except KeyboardInterrupt:
            print("\n\nДо свидания! 👋")
            return


if __name__ == "__main__":
    main()
