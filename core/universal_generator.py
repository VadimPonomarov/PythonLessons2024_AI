"""
Универсальный генератор кода с масштабируемой архитектурой
"""

import asyncio
import os
from datetime import datetime
from typing import List, Literal

from agents.universal_agents import UniversalAgentSystem
from core.models import AgentConfig, GenerationResult, TaskFile, TaskFileMenu, TaskMenu


class UniversalCodeGenerator:
    """Универсальный генератор кода для любых заданий"""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.agent_system = UniversalAgentSystem(
            model_name=config.ai_model, provider=self._get_provider(config.provider)
        )
        self._ensure_output_directory()

    def _get_provider(self, provider_name: str):
        """Получает провайдера по имени"""
        if provider_name == "PollinationsAI":
            from agents.universal_agents import SimpleFixedPollinationsAI

            return SimpleFixedPollinationsAI
        # По умолчанию используем SimpleFixedPollinationsAI
        else:
            from agents.universal_agents import SimpleFixedPollinationsAI

            return SimpleFixedPollinationsAI

    def _ensure_output_directory(self):
        """Создает директорию для вывода если её нет"""
        if not os.path.exists(self.config.output_directory):
            os.makedirs(self.config.output_directory)

    def get_language_choice(self) -> Literal["en", "uk", "ru"]:
        """Запрашивает выбор языка интерфейса"""
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

    def get_code_language_choice(self) -> Literal["en", "uk", "ru"]:
        """Запрашивает выбор языка для комментариев в коде"""
        print("\nВыберите язык для комментариев в коде:")
        print("1. English (en) [default]")
        print("2. Українська (uk)")
        print("3. Русский (ru)")

        lang_choice = input("Enter choice (1-3) [1]: ").strip()
        return "uk" if lang_choice == "2" else "ru" if lang_choice == "3" else "en"

    def show_menu(self, menu: TaskMenu) -> None:
        """Отображает меню, построенное по id и intent"""
        print(f"\n{menu.title}")
        for item in menu.items:
            print(f"{item.id}. {item.intent}")
        print(f"0. {menu.exit_option}")

    def scan_task_files(self) -> List[TaskFile]:
        """Сканирует папку tasks и возвращает список файлов заданий"""
        task_files = []
        tasks_dir = self.config.tasks_directory

        if not os.path.exists(tasks_dir):
            print(f"❌ Папка {tasks_dir} не найдена!")
            return task_files

        file_id = 1
        for filename in os.listdir(tasks_dir):
            if filename.endswith(".txt"):
                filepath = os.path.join(tasks_dir, filename)

                # Создаем краткое описание на основе имени файла
                description = filename.replace(".txt", "").replace("_", " ").title()

                task_files.append(
                    TaskFile(
                        id=file_id,
                        filename=filename,
                        filepath=filepath,
                        description=description,
                    )
                )
                file_id += 1

        return task_files

    def show_file_menu(self, files: List[TaskFile]) -> None:
        """Отображает меню выбора файлов заданий"""
        print("\n📁 Выберите файл с заданиями:")
        for file in files:
            print(f"{file.id}. {file.description} ({file.filename})")
        print("0. Выход")

    def select_task_file(self) -> str | None:
        """Позволяет выбрать файл заданий из папки tasks"""
        task_files = self.scan_task_files()

        if not task_files:
            print("❌ В папке tasks не найдено файлов с заданиями (.txt)")
            return None

        print(f"\n📂 Найдено файлов заданий: {len(task_files)}")

        while True:
            self.show_file_menu(task_files)

            choice = input("\nВведите номер файла (0 для выхода): ").strip()

            if choice == "0":
                return None

            try:
                file_id = int(choice)
                selected_file = next((f for f in task_files if f.id == file_id), None)

                if selected_file:
                    print(f"✅ Выбран файл: {selected_file.description}")
                    return selected_file.filepath
                else:
                    print("❌ Неверный номер файла. Попробуйте еще раз.")
            except ValueError:
                print("❌ Введите корректный номер файла.")

    async def save_generated_code(
        self, code: str, task_id: int, task_intent: str, task_file_path: str
    ) -> GenerationResult:
        """Сохраняет сгенерированный код в папку с префиксом+имя файла задания"""
        try:
            # Получаем имя файла заданий без расширения
            task_filename = os.path.basename(task_file_path).replace(".txt", "")

            # Создаем папку для этого файла заданий
            task_output_dir = os.path.join(
                self.config.output_directory, f"generated_{task_filename}"
            )
            if not os.path.exists(task_output_dir):
                os.makedirs(task_output_dir)

            # Создаем имя файла с timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_intent = "".join(
                c for c in task_intent if c.isalnum() or c in (" ", "-", "_")
            ).rstrip()
            safe_intent = safe_intent.replace(" ", "_").lower()

            filename = f"task_{task_id}_{safe_intent}_{timestamp}.py"
            file_path = os.path.join(task_output_dir, filename)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)

            return GenerationResult(
                success=True,
                task_id=task_id,
                file_path=file_path,
                error_message=None,
                code_preview=code[:200] + "..." if len(code) > 200 else code,
            )
        except Exception as e:
            return GenerationResult(
                success=False,
                task_id=task_id,
                file_path=None,
                error_message=str(e),
                code_preview=None,
            )

    def show_error_and_exit(self, language: Literal["en", "uk", "ru"]) -> None:
        """Показывает сообщение об ошибке и завершает программу"""
        error_messages = {
            "uk": [
                "❌ Помилка: AI-агент недоступний.",
                "Програма не може працювати без генерації меню.",
                "Спробуйте пізніше або перевірте підключення до інтернету.",
            ],
            "ru": [
                "❌ Ошибка: AI-агент недоступен.",
                "Программа не может работать без генерации меню.",
                "Попробуйте позже или проверьте подключение к интернету.",
            ],
            "en": [
                "❌ Error: AI agent unavailable.",
                "Program cannot work without menu generation.",
                "Please try later or check your internet connection.",
            ],
        }

        for message in error_messages[language]:
            print(message)

        exit(1)

    async def run(self):
        """Главная функция универсального генератора"""
        print("🤖 Universal Python Code Generator")
        print("==================================")
        print(f"AI Model: {self.config.ai_model}")
        print(f"Provider: {self.config.provider}")
        print(f"Output Directory: {self.config.output_directory}")

        # Выбираем язык интерфейса
        interface_language = self.get_language_choice()

        # Выбираем файл заданий из папки tasks
        task_file_path = self.select_task_file()
        if not task_file_path:
            print("❌ Файл заданий не выбран. Завершение работы.")
            return

        # Генерируем меню из файла
        print("\n🎨 Генерируем меню задач...")
        menu = await self.agent_system.generate_menu(task_file_path, interface_language)
        if not menu:
            self.show_error_and_exit(interface_language)

        print(f"✅ Меню сгенерировано: {len(menu.items)} элементов")

        # Получаем переведенные сообщения интерфейса
        task_count = len(menu.items)
        print("🌐 Получаем переводы интерфейса...")
        messages = await self.agent_system.translate_messages(
            interface_language, task_count
        )

        # Основной цикл программы
        valid_choices = [str(item.id) for item in menu.items] + ["0"]

        while True:
            # Показываем меню, построенное по id и intent
            self.show_menu(menu)

            choice = input(messages.input_prompt).strip()

            if choice == "0":
                print(messages.goodbye)
                break
            elif choice in valid_choices[:-1]:  # Исключаем "0"
                task_id = int(choice)

                # Находим выбранную задачу
                selected_task = next(
                    (item for item in menu.items if item.id == task_id), None
                )
                if selected_task:
                    print(f"\n{messages.generating} {task_id}...")
                    print(f"📝 Задача: {selected_task.intent}")
                    print(f"📋 Описание: {selected_task.task}")

                    # Запрашиваем выбор языка для комментариев
                    code_language = self.get_code_language_choice()
                    print(f"🌐 Выбран язык для кода: {code_language}")

                    try:
                        # Генерируем код для выбранной задачи
                        generated_code = await self.agent_system.generate_code(
                            selected_task, code_language
                        )

                        print("\n" + "=" * 50)
                        print(messages.generated_code_header)
                        print("=" * 50)
                        print(generated_code)
                        print("=" * 50)

                        # Опция сохранения кода в файл
                        save_choice = input(messages.save_prompt).lower()
                        if save_choice == "y":
                            result = await self.save_generated_code(
                                generated_code,
                                task_id,
                                selected_task.intent,
                                task_file_path,
                            )
                            if result.success:
                                print(f"{messages.saved_message} {result.file_path}")
                            else:
                                print(
                                    f"{messages.error_message} {result.error_message}"
                                )

                    except Exception as e:
                        print(f"{messages.error_message} {e}")
                else:
                    print(messages.invalid_choice)
            else:
                print(messages.invalid_choice)


def create_default_config(task_file_path: str) -> AgentConfig:
    """Создает конфигурацию по умолчанию"""
    return AgentConfig(
        task_file_path=task_file_path,
        output_directory="generated_code",
        default_language="en",
        ai_model="gpt-4o",
        provider="PollinationsAI",
    )


async def main():
    """Точка входа для универсального генератора"""
    print("🤖 Universal Python Code Generator")
    print("==================================")
    print("📁 Автоматический выбор файлов заданий из папки 'tasks'")

    # Создаем конфигурацию с пустым файлом (будет выбран позже)
    config = create_default_config("")
    generator = UniversalCodeGenerator(config)
    await generator.run()


if __name__ == "__main__":
    asyncio.run(main())
