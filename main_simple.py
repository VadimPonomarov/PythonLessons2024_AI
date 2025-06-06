"""
🤖 Universal Python Code Generator - Simplified AI-Driven Version
No hardcoding - AI determines language, context, and behavior automatically
"""

import json
import os
from datetime import datetime

from g4f.integration.langchain import ChatAI


def get_language_choice():
    """AI-powered language selection"""
    print(
        "\nSelect interface language / Выберите язык интерфейса / Оберіть мову інтерфейсу:"
    )
    print("1. English (en) [default]")
    print("2. Українська (uk)")
    print("3. Русский (ru)")

    choice = input("Enter choice (1-3) [1]: ").strip()

    language_map = {"1": "en", "2": "uk", "3": "ru"}
    return language_map.get(choice, "en")


def ai_localize(llm, text, language):
    """AI-powered localization for any text"""
    if language == "en":
        return text

    prompt = f"""
    Translate this interface text to {language} language naturally:
    "{text}"
    
    Return ONLY the translation, no explanations.
    """

    try:
        messages = [{"role": "user", "content": prompt}]
        response = llm.invoke(messages)
        return response.content.strip().strip('"')
    except:
        return text


def ai_parse_tasks(llm, content, language):
    """AI-powered task parsing and menu generation preserving order"""
    prompt = f"""
    Parse this file content and extract ALL programming tasks in ORIGINAL ORDER.
    Create a numbered menu in {language} language.

    Rules:
    1. Find EVERY programming task in the text
    2. PRESERVE the original order from the file
    3. Number them sequentially (1, 2, 3, ...)
    4. Keep task descriptions concise but clear
    5. Include ALL tasks, even similar ones
    6. Maintain the EXACT sequence as they appear in the file

    File content:
    {content}

    Return ONLY a JSON array of objects like:
    [{{"id": 1, "description": "Task description 1"}}, {{"id": 2, "description": "Task description 2"}}, ...]
    """

    try:
        messages = [{"role": "user", "content": prompt}]
        response = llm.invoke(messages)

        # Clean response
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        return json.loads(content)

    except Exception as e:
        print(f"❌ Error parsing tasks: {e}")
        return {}


def ai_generate_code(llm, task_description, language):
    """AI-powered code generation"""
    prompt = f"""
    Generate Python code for this task: {task_description}
    
    Requirements:
    - Clean, executable Python code
    - Add comments in {language} language
    - NO markdown blocks
    - Complete working solution
    - For visual tasks: use proper spacing for equal-sided shapes
    
    Return ONLY the Python code.
    """

    try:
        messages = [{"role": "user", "content": prompt}]
        response = llm.invoke(messages)
        return response.content.strip()
    except Exception as e:
        return f"# Error generating code: {e}"


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
    """Main function - AI-driven, no hardcoding"""
    print("🤖 Universal Python Code Generator")
    print("==================================")
    print("AI Model: gpt-4o")
    print("Provider: LangChain + PollinationsAI")
    print("Output Directory: generated_code")

    # Language selection
    language = get_language_choice()

    # Initialize AI
    llm = ChatAI(model="gpt-4o", provider="PollinationsAI", api_key="")

    print(f"✅ {ai_localize(llm, 'Language selected', language)}: {language}")

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

    print(f"\n📂 {ai_localize(llm, 'Task files found', language)}: {len(task_files)}")

    # File selection loop
    while True:
        print(f"\n📁 {ai_localize(llm, 'Select task file', language)}:")

        # Calculate max width for right-aligned numbers
        max_file_id = max(f["id"] for f in task_files) if task_files else 0
        file_width = len(str(max_file_id))

        for file in task_files:
            print(
                f"{file['id']:>{file_width}}. {file['description']} ({file['filename']})"
            )
        print(f"{0:>{file_width}}. {ai_localize(llm, 'Exit', language)}")

        choice = input(
            f"\n{ai_localize(llm, 'Enter file number (0 to exit)', language)}: "
        ).strip()

        if choice == "0":
            print(ai_localize(llm, "Goodbye! 👋", language))
            return

        try:
            file_id = int(choice)
            selected_file = next((f for f in task_files if f["id"] == file_id), None)

            if selected_file:
                print(
                    f"✅ {ai_localize(llm, 'File selected', language)}: {selected_file['description']}"
                )

                # Read task file
                try:
                    with open(selected_file["filepath"], "r", encoding="utf-8") as f:
                        file_content = f.read()
                except UnicodeDecodeError:
                    with open(selected_file["filepath"], "r", encoding="cp1251") as f:
                        file_content = f.read()

                print(
                    f"✅ {ai_localize(llm, 'File content loaded', language)} ({len(file_content)} {ai_localize(llm, 'characters', language)})"
                )

                # AI parse tasks
                print(f"🎨 {ai_localize(llm, 'Generating task menu', language)}...")
                tasks = ai_parse_tasks(llm, file_content, language)

                if not tasks:
                    print("❌ No tasks found in file")
                    continue

                # Display menu
                print(
                    f"\n📋 {ai_localize(llm, 'Tasks from', language)} {selected_file['filename']}:"
                )
                print("-" * 50)

                # Calculate max width for right-aligned numbers
                max_task_id = (
                    max(int(task_id) for task_id in tasks.keys()) if tasks else 0
                )
                task_width = len(str(max_task_id))

                for task_id, task_desc in sorted(
                    tasks.items(), key=lambda x: int(x[0])
                ):
                    print(f"{int(task_id):>{task_width}}. {task_desc}")
                print("-" * 50)

                # Task selection
                task_choice = input(
                    f"\n{ai_localize(llm, 'Enter task number to generate code (or 0 to return)', language)}: "
                ).strip()

                if task_choice != "0" and task_choice in tasks:
                    selected_task = tasks[task_choice]
                    print(
                        f"🔄 {ai_localize(llm, 'Generating code for task', language)} {task_choice}..."
                    )
                    print(f"📝 {ai_localize(llm, 'Task', language)}: {selected_task}")

                    # Generate code
                    code = ai_generate_code(llm, selected_task, language)

                    print("\n" + "=" * 50)
                    print(ai_localize(llm, "GENERATED CODE", language))
                    print("=" * 50)
                    print(code)
                    print("=" * 50)

                    # Save code option
                    save_choice = input(
                        f"\n{ai_localize(llm, 'Save code to file? (y/n)', language)}: "
                    ).lower()
                    if save_choice == "y":
                        filepath = save_code(
                            code, f"task_{task_choice}", int(task_choice)
                        )
                        if filepath:
                            print(
                                f"✅ {ai_localize(llm, 'Code saved', language)}: {filepath}"
                            )

                            # Run code option
                            run_choice = input(
                                f"{ai_localize(llm, 'Run generated code? (y/n)', language)}: "
                            ).lower()
                            if run_choice == "y":
                                try:
                                    print(
                                        f"\n🔄 {ai_localize(llm, 'Running code', language)}..."
                                    )
                                    print("-" * 30)
                                    exec(code)
                                    print("-" * 30)
                                    print(
                                        f"✅ {ai_localize(llm, 'Code executed successfully', language)}"
                                    )
                                except Exception as e:
                                    print(
                                        f"❌ {ai_localize(llm, 'Execution error', language)}: {e}"
                                    )

                elif task_choice != "0":
                    print(f"❌ {ai_localize(llm, 'Invalid task number', language)}")

            else:
                print(
                    f"❌ {ai_localize(llm, 'Invalid file number. Try again.', language)}"
                )

        except ValueError:
            print(f"❌ {ai_localize(llm, 'Enter a valid number', language)}")
        except KeyboardInterrupt:
            print(f"\n\n{ai_localize(llm, 'Goodbye! 👋', language)}")
            return


if __name__ == "__main__":
    main()
