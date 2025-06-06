"""
Test the task parser
"""

import re


def parse_tasks_from_content(content):
    """Parse tasks from file content to get exact task mapping"""
    tasks = {}
    lines = content.split("\n")
    task_counter = 1

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Look for numbered tasks like "1)", "2)", etc.
        numbered_match = re.match(r"^(\d+)\)\s*(.*)", line)
        if numbered_match:
            task_num = int(numbered_match.group(1))
            task_text = numbered_match.group(2)
            if task_text.strip():
                tasks[task_num] = task_text.strip()
            continue

        # Look for bullet point tasks "–"
        bullet_match = re.match(r"^–\s*(.*)", line)
        if bullet_match:
            task_text = bullet_match.group(1)
            if task_text.strip():
                # Find next available number
                while task_counter in tasks:
                    task_counter += 1
                tasks[task_counter] = task_text.strip()
                task_counter += 1
            continue

    return tasks


# Test with task file
with open("tasks/task_1.txt", "r", encoding="utf-8") as f:
    content = f.read()

tasks = parse_tasks_from_content(content)

print(f"Found {len(tasks)} tasks:")
for task_num in sorted(tasks.keys()):
    print(f"{task_num}. {tasks[task_num]}")
    print(f"{task_num}. {tasks[task_num]}")
