"""
🤖 Universal Python Code Generator
AI-powered code generation with LangChain + G4F integration
"""

import os
from datetime import datetime

from g4f.integration.langchain import ChatAI


def get_language_choice():
    """Language selection for interface"""
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


def ai_translate(llm, text, language):
    """AI-powered translation - no hardcoding"""
    if language == "en":
        return text

    prompt = f"""
    Translate this interface text to {language} language naturally and appropriately:
    "{text}"

    Keep emojis and formatting. Return ONLY the translation.
    """

    try:
        messages = [{"role": "user", "content": prompt}]
        response = llm.invoke(messages)
        return response.content.strip().strip('"')
    except:
        return text


def get_ui_messages(language, llm):
    """AI-generated localized UI messages - no hardcoding"""
    base_messages = {
        "language_selected": "✅ Language selected:",
        "task_files_found": "📂 Task files found:",
        "select_task_file": "📁 Select task file:",
        "exit": "Exit",
        "enter_file_number": "Enter file number (0 to exit):",
        "goodbye": "Goodbye! 👋",
        "file_selected": "✅ File selected:",
        "initializing_ai": "🔧 Initializing AI agent...",
        "ai_ready": "✅ AI agent ready",
        "file_loaded": "✅ File content loaded",
        "characters": "characters",
        "generating_menu": "🎨 Generating task menu...",
        "tasks_from": "📋 Tasks from",
        "enter_task_number": "Enter task number to generate code (or 0 to return):",
        "generating_code": "🔄 Generating code for task",
        "generated_code": "GENERATED CODE:",
        "save_code": "Save code to file? (y/n):",
        "code_saved": "✅ Code saved:",
        "run_code": "Run generated code? (y/n):",
        "running_code": "🔄 Running code...",
        "code_executed": "✅ Code executed successfully",
        "execution_error": "❌ Execution error:",
        "ai_error": "❌ AI generation error:",
        "invalid_file": "❌ Invalid file number. Try again.",
        "invalid_number": "❌ Enter a valid number.",
        "save_error": "❌ Save error:",
    }

    # AI translates all messages dynamically
    translated_messages = {}
    for key, text in base_messages.items():
        translated_messages[key] = ai_translate(llm, text, language)

    return translated_messages


def parse_tasks_from_content(content):
    """Parse tasks from file content preserving original order"""
    import re

    tasks = []  # Use list to preserve order
    lines = content.split("\n")
    task_counter = 1

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Look for various task patterns
        patterns = [
            r"^(\d+)\)\s*(.*)",  # "1) task description"
            r"^(\d+)\.\s*(.*)",  # "1. task description"
            r"^–\s*(.*)",  # "– task description"
            r"^\*\s*(.*)",  # "* task description"
            r"^-\s*(.*)",  # "- task description"
        ]

        task_found = False
        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                if pattern.startswith(r"^(\d+)"):
                    # Numbered task
                    task_num = int(match.group(1))
                    task_text = match.group(2)
                else:
                    # Bullet point task
                    task_num = task_counter
                    task_text = match.group(1)
                    task_counter += 1

                if task_text.strip():
                    tasks.append((task_num, task_text.strip()))
                task_found = True
                break

        # Also look for tasks that start with keywords
        if not task_found:
            keywords = [
                "створити функцію",
                "написати програму",
                "вивести",
                "знайти",
                "видалити",
                "замінити",
            ]
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in keywords):
                tasks.append((task_counter, line))
                task_counter += 1

    return tasks


def save_code(code, task_name, task_id=1):
    """Save generated code to file"""
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

        return filepath

    except Exception as e:
        print(f"❌ Save error: {e}")
        return ""


def main():
    """Main function"""
    print("🤖 Universal Python Code Generator")
    print("==================================")
    print("AI Model: gpt-4o")
    print("Provider: LangChain + PollinationsAI")
    print("Output Directory: generated_code")

    # Language selection
    language = get_language_choice()

    # Initialize AI first for translations
    llm = ChatAI(model="gpt-4o", provider="PollinationsAI", api_key="")
    ui = get_ui_messages(language, llm)
    print(f"{ui['language_selected']} {language}")

    # Check tasks folder
    tasks_dir = "tasks"
    if not os.path.exists(tasks_dir):
        print(f"❌ Folder {tasks_dir} not found!")
        return

    # Find task files
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
        print("❌ No task files (.txt) found in tasks folder")
        return

    print(f"\n{ui['task_files_found']} {len(task_files)}")

    # File selection loop
    while True:
        print(f"\n{ui['select_task_file']}")

        # Calculate max width for right-aligned numbers
        max_file_id = max(f["id"] for f in task_files) if task_files else 0
        file_width = len(str(max_file_id))

        for file in task_files:
            print(
                f"{file['id']:>{file_width}}. {file['description']} ({file['filename']})"
            )
        print(f"{0:>{file_width}}. {ui['exit']}")

        choice = input(f"\n{ui['enter_file_number']} ").strip()

        if choice == "0":
            print(ui["goodbye"])
            return

        try:
            file_id = int(choice)
            selected_file = next((f for f in task_files if f["id"] == file_id), None)

            if selected_file:
                print(f"{ui['file_selected']} {selected_file['description']}")

                # Read task file
                try:
                    with open(selected_file["filepath"], "r", encoding="utf-8") as f:
                        file_content = f.read()
                except UnicodeDecodeError:
                    with open(selected_file["filepath"], "r", encoding="cp1251") as f:
                        file_content = f.read()

                print(f"{ui['file_loaded']} ({len(file_content)} {ui['characters']})")

                # Parse tasks from content for exact mapping
                parsed_tasks = parse_tasks_from_content(file_content)
                print(
                    f"📋 {ai_translate(llm, f'Found {len(parsed_tasks)} tasks in file', language)}"
                )

                # Generate menu using AI
                print(ui["generating_menu"])

                # Create structured menu from parsed tasks
                print(f"\n{ui['tasks_from']} {selected_file['filename']}:")
                print("-" * 50)

                if parsed_tasks:
                    # Calculate max width for right-aligned numbers
                    max_num = (
                        max(task_num for task_num, _ in parsed_tasks)
                        if parsed_tasks
                        else 0
                    )
                    width = len(str(max_num))

                    # Display tasks in original file order
                    for task_num, task_desc in parsed_tasks:
                        # Right-align the number with proper spacing
                        print(f"{task_num:>{width}}. {task_desc}")
                else:
                    print(
                        f"❌ {ai_translate(llm, 'Failed to parse tasks from file', language)}"
                    )

                print("-" * 50)

                # Simple task selection
                task_choice = input(f"\n{ui['enter_task_number']} ").strip()

                if task_choice != "0":
                    try:
                        task_num = int(task_choice)
                        # Find task in list
                        exact_task = None
                        for num, desc in parsed_tasks:
                            if num == task_num:
                                exact_task = desc
                                break

                        if exact_task:
                            print(f"{ui['generating_code']} {task_choice}...")
                            print(
                                f"📝 {ai_translate(llm, f'Exact task: {exact_task}', language)}"
                            )

                            code_prompt = f"""
                                Generate Python code for this EXACT task:

                                Task number: {task_num}
                                Task description: {exact_task}

                                Requirements:
                                - Generate code ONLY for this specific task description
                                - Clean, executable Python code
                                - Add comments in {language} language
                                - NO markdown blocks
                                - Complete working solution
                                - For squares: use spaces between asterisks for visual equal-sidedness

                                Task to implement: {exact_task}
                                """
                        else:
                            print(
                                f"❌ {ai_translate(llm, f'Task {task_choice} not found in file', language)}"
                            )
                            continue
                    except ValueError:
                        print(
                            f"❌ {ai_translate(llm, f'Invalid task number: {task_choice}', language)}"
                        )
                        continue

                    code_messages = [{"role": "user", "content": code_prompt}]
                    code_response = llm.invoke(code_messages)

                    print("\n" + "=" * 50)
                    print(ui["generated_code"])
                    print("=" * 50)
                    print(code_response.content)
                    print("=" * 50)

                    # Save code option
                    save_choice = input(f"\n{ui['save_code']} ").lower()
                    if save_choice == "y":
                        filepath = save_code(
                            code_response.content,
                            f"task_{task_choice}",
                            int(task_choice),
                        )
                        if filepath:
                            print(f"{ui['code_saved']} {filepath}")
                            # Offer to run code
                            run_choice = input(f"{ui['run_code']} ").lower()
                            if run_choice == "y":
                                try:
                                    print(f"\n{ui['running_code']}")
                                    print("-" * 30)
                                    exec(code_response.content)
                                    print("-" * 30)
                                    print(ui["code_executed"])
                                except Exception as e:
                                    print(f"{ui['execution_error']} {e}")
            else:
                print(ui["invalid_file"])

        except ValueError:
            print(ui["invalid_number"])
        except KeyboardInterrupt:
            print(f"\n\n{ui['goodbye']}")
            return


if __name__ == "__main__":
    main()
