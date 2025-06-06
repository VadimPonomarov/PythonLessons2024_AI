"""
🎯 DEMONSTRATION TEST
Universal Python Code Generator with AI Task Parsing

This demo shows how the system works:
1. AI parses tasks from text files
2. Generates Python code for selected tasks
3. Fixes visual issues (like square spacing)
4. Saves and runs generated code
"""

import g4f
import json
import re
import os
from datetime import datetime


def clean_code(code: str) -> str:
    """Clean code from markdown blocks"""
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
    """Fix square code for visual equal-sidedness"""
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


def demo_ai_parsing():
    """Demo: AI task parsing"""
    print("🎯 DEMO: AI Task Parsing")
    print("=" * 50)
    
    # Read sample task file
    try:
        with open("tasks/task_1.txt", "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return []
    
    print("📄 Sample content from task_1.txt:")
    print("-" * 30)
    print(content[:200] + "..." if len(content) > 200 else content)
    print("-" * 30)
    
    # Parse with AI
    try:
        print("\n🤖 AI parsing tasks...")
        
        response = g4f.ChatCompletion.create(
            model="gpt-4o",
            provider=g4f.Provider.PollinationsAI,
            messages=[{
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
                - Remove task numbers from descriptions
                - Make first letter uppercase
                - Include multiplication tables and squares
                - Return ONLY valid JSON
                
                Text: {content}
                """
            }]
        )
        
        # Parse JSON response
        cleaned_response = clean_code(response)
        tasks_data = json.loads(cleaned_response)
        
        if isinstance(tasks_data, list):
            print(f"✅ Found {len(tasks_data)} tasks:")
            for i, task in enumerate(tasks_data[:5], 1):  # Show first 5
                desc = task.get("description", "")
                print(f"  {i}. {desc[:60]}{'...' if len(desc) > 60 else ''}")
            
            if len(tasks_data) > 5:
                print(f"  ... and {len(tasks_data) - 5} more tasks")
            
            return tasks_data
        
    except Exception as e:
        print(f"❌ AI parsing error: {e}")
        return []


def demo_code_generation(task_description: str):
    """Demo: Code generation"""
    print(f"\n🎯 DEMO: Code Generation")
    print("=" * 50)
    print(f"📝 Task: {task_description}")
    
    try:
        print("\n🔄 Generating code...")
        
        response = g4f.ChatCompletion.create(
            model="gpt-4o",
            provider=g4f.Provider.PollinationsAI,
            messages=[{
                "role": "user",
                "content": f"""
                Generate Python code for: {task_description}
                
                Requirements:
                - Clean, executable Python code
                - Add comments in English
                - NO markdown blocks
                - Return ONLY code
                """
            }]
        )
        
        cleaned_code = clean_code(response)
        # Fix squares for visual equal-sidedness
        cleaned_code = fix_square_spacing(cleaned_code)
        
        print("✅ Code generated successfully!")
        print("\n" + "=" * 40)
        print("GENERATED CODE:")
        print("=" * 40)
        print(cleaned_code)
        print("=" * 40)
        
        return cleaned_code
        
    except Exception as e:
        print(f"❌ Code generation error: {e}")
        return None


def demo_save_and_run(code: str, task_name: str):
    """Demo: Save and run code"""
    print(f"\n🎯 DEMO: Save and Run Code")
    print("=" * 50)
    
    # Save code
    try:
        output_dir = "generated_code"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"demo_{task_name}_{timestamp}.py"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        
        print(f"✅ Code saved to: {filepath}")
        
        # Run code
        print("\n🔄 Running generated code...")
        print("-" * 30)
        exec(code)
        print("-" * 30)
        print("✅ Code executed successfully!")
        
        return filepath
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def main():
    """Main demo function"""
    print("🎉 UNIVERSAL PYTHON CODE GENERATOR - DEMO")
    print("=" * 60)
    print("This demo shows the complete workflow:")
    print("1. 🤖 AI parses tasks from text files")
    print("2. 🔄 Generates Python code for selected task")
    print("3. 🎨 Fixes visual issues (square spacing)")
    print("4. 💾 Saves and runs the generated code")
    print("=" * 60)
    
    # Step 1: Parse tasks
    tasks = demo_ai_parsing()
    
    if not tasks:
        print("\n❌ Demo failed: No tasks found")
        return
    
    # Step 2: Select a demo task (square drawing)
    demo_task = None
    for task in tasks:
        desc = task.get("description", "").lower()
        if "квадрат" in desc or "square" in desc or "*" in desc:
            demo_task = task
            break
    
    if not demo_task:
        # Fallback to first task
        demo_task = tasks[0]
    
    # Step 3: Generate code
    code = demo_code_generation(demo_task.get("description", ""))
    
    if not code:
        print("\n❌ Demo failed: No code generated")
        return
    
    # Step 4: Save and run
    filepath = demo_save_and_run(code, "square")
    
    if filepath:
        print(f"\n🎉 DEMO COMPLETED SUCCESSFULLY!")
        print(f"📁 Generated file: {filepath}")
        print(f"🎯 Task completed: {demo_task.get('description', '')}")
    else:
        print("\n❌ Demo failed at save/run step")


if __name__ == "__main__":
    main()
