"""
Test menu formatting with right-aligned numbers
"""

def test_menu_formatting():
    """Test right-aligned menu formatting"""
    
    # Test data - simulating tasks with different number lengths
    tasks = {
        1: "створити функцію, яка виводить List",
        2: "вивести на екран пустий квадрат з '*'",
        3: "вивести табличку множення за допомогою циклу while",
        4: "переробити це завдання під меню",
        5: "створити функцію, яка повертає найменше число з List",
        6: "створити функцію, яка приймає List чисел та складає значення елементів",
        7: "створити функцію, яка приймає List чисел та повертає середнє арифметичне",
        8: "знайти мін. число",
        9: "видалити усі дублікати",
        10: "замінити кожне 4-те значення на 'X'",
        11: "додаткове завдання для тестування",
        12: "ще одне завдання",
        100: "завдання з великим номером"
    }
    
    print("🧪 Testing menu formatting:")
    print("=" * 60)
    
    # Calculate max width for right-aligned numbers
    max_num = max(tasks.keys()) if tasks else 0
    width = len(str(max_num))
    
    print(f"Max number: {max_num}, Width: {width}")
    print("-" * 60)
    
    for task_num in sorted(tasks.keys()):
        task_desc = tasks[task_num]
        # Right-align the number with proper spacing
        print(f"{task_num:>{width}}. {task_desc}")
    
    print("-" * 60)
    print("✅ Formatting test completed!")
    
    # Test file menu formatting
    print("\n🧪 Testing file menu formatting:")
    print("=" * 60)
    
    files = [
        {"id": 1, "description": "Task 1", "filename": "task_1.txt"},
        {"id": 2, "description": "Task 2", "filename": "task_2.txt"},
        {"id": 3, "description": "Task 3", "filename": "task_3.txt"},
        {"id": 4, "description": "Task 4", "filename": "task_4.txt"},
    ]
    
    # Calculate max width for right-aligned numbers
    max_file_id = max(f['id'] for f in files) if files else 0
    file_width = len(str(max_file_id))
    
    for file in files:
        print(f"{file['id']:>{file_width}}. {file['description']} ({file['filename']})")
    print(f"{0:>{file_width}}. Exit")
    
    print("-" * 60)
    print("✅ File menu formatting test completed!")


if __name__ == "__main__":
    test_menu_formatting()
