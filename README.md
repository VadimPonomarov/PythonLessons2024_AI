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

## 🚀 Quick Demo

**First time using the project?** Run the demonstration:

```bash
python demo.py
```

This will show you:
1. 🤖 AI parsing tasks from `task_1.txt`
2. 🔄 Code generation for a square drawing task
3. 🎨 Visual spacing fixes for equal-sided squares
4. 💾 Saving and running the generated code

## 📁 Project Structure

```
📁 PythonLessons2024_AI/
├── 🎯 demo.py                   # Demonstration test - START HERE!
├── 🚀 main.py                   # Main application entry point
├── 🤖 ai_parser_main.py         # AI-powered version with task parsing
├── 📄 README.md                 # This documentation
├── 📄 pyproject.toml           # Poetry configuration
├── 📁 agents/                  # AI agent modules
│   ├── 📄 fixed_pollinations.py # Fixed PollinationsAI provider
│   └── 📄 universal_agents.py   # Universal AI agents
├── 📁 core/                    # Core functionality
│   ├── 📄 models.py            # Pydantic models
│   └── 📄 universal_generator.py # Code generation logic
├── 📁 tasks/                   # Task files directory
│   ├── 📄 task_1.txt          # Programming tasks (Ukrainian) - 14 tasks
│   └── 📄 task_2.txt          # Additional tasks
└── 📁 generated_code/          # Output directory for generated code
    └── 📄 *.py                 # Generated Python files
```

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

### 🎯 Demo (Recommended for first-time users)
```bash
python demo.py
```

### 🚀 Full Application
```bash
python ai_parser_main.py  # AI-powered version (recommended)
# or
python main.py           # Original version
```

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

**Example**: From `task_1.txt` → **14 tasks found** (vs 7 with manual parsing)

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

### 🎨 Generated Code Quality
- ✅ Clean, executable Python
- ✅ Proper comments in selected language
- ✅ Visual fixes for squares
- ✅ Error handling
- ✅ Best practices

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
3. Test with `python demo.py`
4. Submit a pull request

## 📄 License

MIT License - Open source and free to use.
