# 🤖 Universal Python Code Generator

An AI-powered system for generating Python code from task descriptions with intelligent task parsing, multi-language support, and visual code improvements.

## ✨ Key Features

- **🤖 AI Task Parsing**: Intelligent extraction of ALL programming tasks from text files
- **🔄 Smart Code Generation**: Uses g4f with PollinationsAI for reliable code generation
- **🌍 Multi-Language Support**: Interface in English, Ukrainian, and Russian
- **🎨 Visual Improvements**: Automatic fixes for square spacing and visual elements
- **📁 Organized Output**: Timestamped files with clean directory structure
- **🎯 Interactive Menus**: User-friendly navigation with proper formatting
- **🛡️ Robust Error Handling**: Fallback mechanisms and graceful degradation

## 🚀 Quick Start

**Ready to use?** Simply run:

```bash
python main.py
```

This is the main entry point that includes:
1. 🤖 AI parsing tasks from text files
2. 🔄 Code generation with proper comments
3. 🎨 Visual spacing fixes for equal-sided squares
4. 💾 Saving and running generated code

## 📁 Project Structure

```
📁 PythonLessons2024_AI/
├── 🚀 main.py                   # Main application - START HERE!
├── 📄 README.md                 # This documentation
├── 📄 pyproject.toml           # Poetry configuration
├── 📁 tasks/                   # Task files directory
│   ├── 📄 task_1.txt          # Programming tasks (Ukrainian) - 17+ tasks
│   └── 📄 task_2.txt          # Additional tasks
├── 📁 generated_code/          # Output directory for YOUR generated code
│   └── 📄 *.py                 # Your generated Python files
├── 📁 demo_files/              # Demonstration and example files
│   ├── 📄 README.md           # Demo documentation
│   └── 📄 demo_*.py           # Example generated code
├── 📁 agents/                  # AI agent modules (advanced features)
│   ├── 📄 fixed_pollinations.py # Fixed PollinationsAI provider
│   └── 📄 universal_agents.py   # Universal AI agents
├── 📁 core/                    # Core functionality (advanced features)
│   ├── 📄 models.py            # Pydantic models
│   └── 📄 universal_generator.py # Code generation logic
└── 📁 config/                  # Configuration constants
    └── 📄 constants.py         # Localization and settings
```

**For beginners**: You only need `main.py` and the `tasks/` folder!
**For advanced users**: Explore `agents/` and `core/` for extensibility.
**For examples**: Check `demo_files/` to see what the system can generate.

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd PythonLessons2024_AI
   ```

2. **Install dependencies using Poetry**:
   ```bash
   poetry install
   ```

3. **Activate the virtual environment**:
   ```bash
   poetry shell
   ```

## 🎮 Usage

### 🚀 Main Application (Start Here!)
```bash
python main.py
```

This is the complete application with:
- AI-powered task parsing
- Multi-language interface
- Visual code improvements
- All features included

### 📋 Workflow

1. **🌍 Language Selection**: Choose interface language (en/uk/ru)
2. **📁 File Selection**: Pick a task file from `tasks/` directory
3. **🎯 Task Selection**: Choose from AI-parsed task list
4. **🤖 Code Generation**: AI creates Python code with proper comments
5. **💾 Save & Execute**: Save code and optionally run it immediately

## 🎯 AI Task Parsing Excellence

The system finds **ALL** tasks including:

✅ **Numbered tasks**: `1) Task description`
✅ **Dash tasks**: `– Task description`
✅ **Function tasks**: `створити функцію...`
✅ **Display tasks**: `вивести...`
✅ **List comprehension**: Complex parsing
✅ **Multiplication tables**: `табличку множення`
✅ **While/for loops**: All loop types

**Example**: From `task_1.txt` → **17+ tasks found** (vs 7 with manual parsing)

## 🎯 What You'll See

When you run `python main.py`:

```
🤖 Universal Python Code Generator
==================================
AI-powered code generation with intelligent task parsing

Select interface language / Выберите язык интерфейса / Оберіть мову інтерфейсу:
1. English (en) [default]
2. Українська (uk)
3. Русский (ru)
Enter choice (1-3) [1]:

📂 Task files found: 2

📁 Select task file:
1. Task 1 (task_1.txt)
2. Task 2 (task_2.txt)
0. Exit

🤖 AI parsing tasks...
✅ Found 17 tasks in file:
   1. Write a program that selects digits from an input string...
   2. Write a program that selects numbers from an input string...
   ...
   12. Display an empty square made of '*' characters...
   13. Display multiplication table using while loop...
```

## 🎨 Visual Improvements

### Square Spacing Fix
**Before** (rectangular):
```
*******
*     *
*     *
*******
```

**After** (equal-sided):
```
* * * * * * *
*           *
*           *
* * * * * * *
```

## 📝 Adding New Tasks

Create `.txt` files in `tasks/` directory with any format:

```
1) написати прогу, яка вибирає зі введеної строки цифри

2) створити функцію, яка приймає три числа та повертає найбільше

– вивести на екран пустий квадрат з "*"

function:
– створити функцію, яка виводить List
```

## ⚙️ Technical Details

### 🤖 AI Configuration
- **Model**: gpt-4o
- **Provider**: PollinationsAI (with custom fixes)
- **Parsing**: JSON-structured responses
- **Languages**: Dynamic comment generation

### 📁 File Organization
- **Input**: `tasks/*.txt` files
- **Output**: `generated_code/task_{id}_{name}_{timestamp}.py`
- **Encoding**: UTF-8 for proper character support

### 🌍 Multi-Language Support
- **English**: Default interface
- **Ukrainian**: Full localization + AI comments
- **Russian**: Complete translation + AI comments

## 🔧 Dependencies

```toml
[tool.poetry.dependencies]
python = "^3.8"
g4f = "*"
pydantic = "*"
pydantic-ai = "*"
```

## 🎉 Success Examples

### ✅ Found Tasks (AI Parsing)
From `task_1.txt`, the AI finds **17+ tasks** including:

1. Extract digits from string
2. Extract numbers from string
3. List comprehension - uppercase characters
4. List comprehension - odd numbers squared
5. Function - display list
6. Function - max of three numbers
7. Function - min/max of any numbers
8. Function - max from list
9. Function - min from list
10. Function - sum of list elements
11. Function - arithmetic mean
12. **Empty square with asterisks** ⭐
13. **Multiplication table with while loop** ⭐⭐
14. Convert to menu system
15. Find minimum number in list
16. Remove duplicates from list
17. Replace every 4th element with 'X'

### 🎨 Generated Code Quality
- ✅ Clean, executable Python
- ✅ Proper comments in selected language
- ✅ Visual fixes for squares (equal-sided)
- ✅ Error handling and edge cases
- ✅ Python best practices
- ✅ Complete working solutions

**See examples**: Check the `demo_files/` folder for sample generated code!

## 🚨 Troubleshooting

### Common Issues
1. **AI Provider Errors**: System includes fallback mechanisms
2. **Task Parsing**: AI handles various formats automatically
3. **File Encoding**: UTF-8 support for all languages
4. **Visual Elements**: Automatic spacing fixes

### Error Messages
- 🌍 Localized error messages
- 📝 Detailed logging
- 🛡️ Graceful degradation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Test with `python main.py`
4. Submit a pull request

## 📄 License

MIT License - Open source and free to use.

---

## 🚀 Ready to Start?

Simply run:
```bash
python main.py
```

The system will guide you through:
- Language selection
- Task file selection
- AI task parsing
- Code generation
- Saving and execution

**Everything you need is in one file!** 🎯
