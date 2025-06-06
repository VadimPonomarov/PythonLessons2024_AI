"""
Универсальные агенты для генерации кода
"""

import os
from typing import Literal

from g4f.integration.pydantic_ai import AIModel

# Импортируем провайдеры
from g4f.Provider import PollinationsAI


# Простое исправление для PollinationsAI
class SimpleFixedPollinationsAI(PollinationsAI):
    @classmethod
    async def create_async_generator(
        cls, model: str, messages: list, proxy=None, **kwargs
    ):
        """Исправляем create_async_generator"""
        print(f"🔧 SimpleFixedPollinationsAI.create_async_generator: исправляем kwargs")

        # Исправляем None extra_body
        if "extra_body" in kwargs and kwargs["extra_body"] is None:
            print("🔧 Исправляем None extra_body")
            kwargs["extra_body"] = {}

        if "extra_body" not in kwargs:
            print("🔧 Добавляем отсутствующий extra_body")
            kwargs["extra_body"] = {}

        print(f"🔧 kwargs после исправления: extra_body = {kwargs.get('extra_body')}")

        try:
            async for chunk in super().create_async_generator(
                model, messages, proxy=proxy, **kwargs
            ):
                yield chunk
        except Exception as e:
            print(f"❌ Ошибка в super().create_async_generator: {e}")
            # Возвращаем простой ответ в правильном формате
            if "logprobs" in str(e):
                print("🔧 Обнаружена ошибка logprobs, возвращаем fallback ответ")
                yield '{"title": "Fallback Menu", "items": [{"id": 1, "intent": "Test Task", "task": "This is a test task"}], "exit_option": "Exit"}'
            else:
                yield "AI service temporarily unavailable. Please try again later."


from pydantic_ai import Agent, RunContext

from core.models import GeneratedCode, InterfaceMessages, TaskMenu


class UniversalAgentSystem:
    """Универсальная система агентов для генерации кода"""

    def __init__(self, model_name: str = "gpt-4o", provider=SimpleFixedPollinationsAI):
        self.text_model = AIModel(model_name, provider)
        self._setup_agents()

    def _setup_agents(self):
        """Настройка всех агентов"""

        # АГЕНТ 1: Генерация меню с тулзом чтения файла
        self.menu_agent = Agent(
            model=self.text_model,
            system_prompt="""You are a universal menu generator for programming tasks.
            
            Your job:
            1. Use read_task_file tool to get file content from specified path
            2. Parse all tasks from the file
            3. Create menu items with structure: {id, intent, task}
            
            For each task:
            - id: task number (starting from 1)
            - intent: brief description (2-4 words) in specified language
            - task: full task description in specified language
            
            Create user-friendly menu with proper title and exit option.
            Handle any file format - extract tasks regardless of structure.""",
            output_retries=3,
            output_type=TaskMenu,
        )

        @self.menu_agent.tool
        def read_task_file(ctx: RunContext[None], file_path: str) -> str:
            """Читает содержимое файла с заданиями по указанному пути"""
            try:
                if not os.path.exists(file_path):
                    return f"Файл {file_path} не найден"

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                return content
            except Exception as e:
                return f"Ошибка при чтении файла {file_path}: {e}"

        # АГЕНТ 2: Переводчик интерфейса
        self.translator_agent = Agent(
            model=self.text_model,
            system_prompt="""You are a universal interface translator.
            Translate standard interface messages to the specified language naturally.
            Handle any number of tasks and adapt messages accordingly.""",
            output_retries=3,
            output_type=InterfaceMessages,
        )

        @self.translator_agent.tool
        def get_base_messages(ctx: RunContext[None], task_count: int) -> str:
            """Получает базовые сообщения для перевода"""
            return f"""
            Base messages to translate:
            1. input_prompt: "Enter task number (0-{task_count}): "
            2. goodbye: "Goodbye! 👋"
            3. invalid_choice: "Invalid choice. Please try again."
            4. generating: "Generating code for task"
            5. generated_code_header: "GENERATED CODE:"
            6. save_prompt: "Save code to file? (y/n): "
            7. saved_message: "Code saved to file:"
            8. error_message: "Error generating code:"
            """

        # АГЕНТ 3: Универсальный генератор кода
        self.code_agent = Agent(
            model=self.text_model,
            system_prompt="""You are a universal Python code generator.
            Generate clean, executable Python code based on any task description.
            
            Requirements:
            - Code must be ready for execution
            - Add comments in specified language
            - Use Python best practices
            - NO markdown blocks
            - NO explanations, only code
            - Handle any programming task type
            - Generate complete, working solutions""",
            output_retries=3,
            output_type=GeneratedCode,
        )

    async def generate_menu(
        self, file_path: str, language: Literal["en", "uk", "ru"]
    ) -> TaskMenu | None:
        """Генерирует меню из файла с заданиями"""
        try:
            prompt = f"""
            Create a menu in {language} language.
            Use read_task_file tool to get tasks from file: {file_path}
            
            Language: {language}
            Menu title: {
                "Select task for code generation:"
                if language == "en"
                else "Выберите задачу для генерации кода:"
                if language == "ru"
                else "Оберіть завдання для генерації коду:"
            }
            Exit option: {
                "Exit" if language == "en" else "Выход" if language == "ru" else "Вихід"
            }
            
            For each task create menu item with:
            - id: task number (starting from 1)
            - intent: brief description (2-4 words) in {language}
            - task: full task description in {language}
            
            File path: {file_path}
            """

            result = await self.menu_agent.run(prompt)
            return result.output
        except Exception as e:
            print(f"❌ Ошибка генерации меню: {e}")
            return None

    async def translate_messages(
        self, language: Literal["en", "uk", "ru"], task_count: int
    ) -> InterfaceMessages:
        """Переводит сообщения интерфейса"""
        if language == "en":
            return InterfaceMessages(
                locale="en",
                input_prompt=f"\nEnter task number (0-{task_count}): ",
                goodbye="Goodbye! 👋",
                invalid_choice="❌ Invalid choice. Please try again.",
                generating="🔄 Generating code for task",
                generated_code_header="GENERATED CODE:",
                save_prompt="\nSave code to file? (y/n): ",
                saved_message="Code saved to file:",
                error_message="❌ Error generating code:",
            )

        try:
            target_language = "Ukrainian" if language == "uk" else "Russian"

            prompt = f"""
            Translate interface messages to {target_language} language.
            Use the get_base_messages tool to get the base messages for translation.
            Task count: {task_count}
            Target language: {language}
            """

            result = await self.translator_agent.run(prompt)
            return result.output
        except Exception as e:
            print(f"❌ Ошибка перевода сообщений: {e}")
            # Fallback переводы
            if language == "uk":
                return InterfaceMessages(
                    locale="uk",
                    input_prompt=f"\nВведіть номер завдання (0-{task_count}): ",
                    goodbye="До побачення! 👋",
                    invalid_choice="❌ Невірний вибір. Спробуйте ще раз.",
                    generating="🔄 Генеруємо код для завдання",
                    generated_code_header="ЗГЕНЕРОВАНИЙ КОД:",
                    save_prompt="\nЗберегти код у файл? (y/n): ",
                    saved_message="Код збережено у файл:",
                    error_message="❌ Помилка при генерації коду:",
                )
            else:  # ru
                return InterfaceMessages(
                    locale="ru",
                    input_prompt=f"\nВведите номер задачи (0-{task_count}): ",
                    goodbye="До свидания! 👋",
                    invalid_choice="❌ Неверный выбор. Попробуйте еще раз.",
                    generating="🔄 Генерирую код для задачи",
                    generated_code_header="СГЕНЕРИРОВАННЫЙ КОД:",
                    save_prompt="\nСохранить код в файл? (y/n): ",
                    saved_message="Код сохранен в файл:",
                    error_message="❌ Ошибка при генерации кода:",
                )

    async def generate_code(
        self, task_item, language: Literal["en", "uk", "ru"]
    ) -> str:
        """Генерирует код для задачи"""
        try:
            language_instructions = {
                "uk": "Add comments in Ukrainian",
                "ru": "Add comments in Russian",
                "en": "Add comments in English",
            }

            prompt = f"""
            Generate Python code for the following task:
            
            Task ID: {task_item.id}
            Intent: {task_item.intent}
            Task: {task_item.task}
            
            Code language: {language}
            Instructions: {language_instructions[language]}
            
            Requirements:
            - Generate clean, executable Python code
            - NO markdown blocks (```python)
            - NO explanations, only code
            - Use Python best practices
            - Create complete working solution
            """

            result = await self.code_agent.run(prompt)
            generated_code = result.output

            # Очищаем код от возможной markdown разметки
            cleaned_code = self._clean_code(generated_code.code)
            return cleaned_code

        except Exception as e:
            print(f"❌ Ошибка генерации кода: {e}")
            # Fallback код
            if language == "uk":
                return f"""# Завдання {task_item.id}: {task_item.intent}
# {task_item.task}

def main():
    \"\"\"Основна функція для завдання {task_item.id}\"\"\"
    print("Розв'язання завдання {task_item.id}")
    print("Опис: {task_item.intent}")
    print("Повний опис: {task_item.task}")
    
    # TODO: Реалізувати логіку завдання
    pass

if __name__ == "__main__":
    main()
"""
            elif language == "ru":
                return f"""# Задача {task_item.id}: {task_item.intent}
# {task_item.task}

def main():
    \"\"\"Основная функция для задачи {task_item.id}\"\"\"
    print("Решение задачи {task_item.id}")
    print("Описание: {task_item.intent}")
    print("Полное описание: {task_item.task}")
    
    # TODO: Реализовать логику задачи
    pass

if __name__ == "__main__":
    main()
"""
            else:  # en
                return f"""# Task {task_item.id}: {task_item.intent}
# {task_item.task}

def main():
    \"\"\"Main function for task {task_item.id}\"\"\"
    print("Solution for task {task_item.id}")
    print("Description: {task_item.intent}")
    print("Full description: {task_item.task}")
    
    # TODO: Implement task logic
    pass

if __name__ == "__main__":
    main()
"""

    def _clean_code(self, code: str) -> str:
        """Очищает код от markdown"""
        if not code:
            return code

        code = code.strip()

        # Удаляем markdown блоки
        if code.startswith("```python"):
            code = code[9:]
        elif code.startswith("```"):
            code = code[3:]

        if code.endswith("```"):
            code = code[:-3]

        return code.strip()
        return code.strip()
        return code.strip()
