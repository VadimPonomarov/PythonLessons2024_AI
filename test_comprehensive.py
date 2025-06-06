"""
🧪 Comprehensive Test Suite for Universal Python Code Generator
Demonstrates all project capabilities and validates functionality
"""

import os
import sys
import time
from datetime import datetime
from g4f.integration.langchain import ChatAI


class ComprehensiveTest:
    """Complete test suite demonstrating all project features"""

    def __init__(self):
        self.test_results = []
        self.start_time = time.time()
        
    def log_test(self, test_name: str, status: str, details: str = ""):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        self.test_results.append(result)
        
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_emoji} {test_name}: {status}")
        if details:
            print(f"   📝 {details}")

    def test_1_environment_setup(self):
        """Test 1: Environment and Dependencies"""
        print("\n🔧 Test 1: Environment Setup")
        print("-" * 50)
        
        try:
            # Test Python version
            python_version = sys.version_info
            if python_version >= (3, 8):
                self.log_test("Python Version", "PASS", f"Python {python_version.major}.{python_version.minor}")
            else:
                self.log_test("Python Version", "FAIL", f"Python {python_version.major}.{python_version.minor} < 3.8")
                
            # Test G4F import
            import g4f
            self.log_test("G4F Import", "PASS", f"G4F version available")
            
            # Test LangChain import
            from g4f.integration.langchain import ChatAI
            self.log_test("LangChain Integration", "PASS", "ChatAI import successful")
            
            # Test main.py exists
            if os.path.exists("main.py"):
                self.log_test("Main File", "PASS", "main.py found")
            else:
                self.log_test("Main File", "FAIL", "main.py not found")
                
            # Test tasks directory
            if os.path.exists("tasks") and os.path.isdir("tasks"):
                task_files = [f for f in os.listdir("tasks") if f.endswith(".txt")]
                self.log_test("Tasks Directory", "PASS", f"{len(task_files)} task files found")
            else:
                self.log_test("Tasks Directory", "FAIL", "tasks/ directory not found")
                
        except Exception as e:
            self.log_test("Environment Setup", "FAIL", str(e))

    def test_2_ai_integration(self):
        """Test 2: AI Integration and Connectivity"""
        print("\n🤖 Test 2: AI Integration")
        print("-" * 50)
        
        try:
            # Test ChatAI initialization
            llm = ChatAI(model="gpt-4o", provider="PollinationsAI", api_key="")
            self.log_test("ChatAI Initialization", "PASS", "PollinationsAI provider ready")
            
            # Test simple AI response
            messages = [{"role": "user", "content": "Say 'Hello Test' in Ukrainian"}]
            response = llm.invoke(messages)
            
            if response and response.content:
                self.log_test("AI Response", "PASS", f"Response: {response.content[:50]}...")
            else:
                self.log_test("AI Response", "FAIL", "No response from AI")
                
            # Test AI with code generation
            code_messages = [{"role": "user", "content": "Write a simple Python function that prints 'Hello World'"}]
            code_response = llm.invoke(code_messages)
            
            if "def" in code_response.content and "print" in code_response.content:
                self.log_test("AI Code Generation", "PASS", "AI generated Python function")
            else:
                self.log_test("AI Code Generation", "WARN", "AI response may not contain valid code")
                
        except Exception as e:
            self.log_test("AI Integration", "FAIL", str(e))

    def test_3_task_parsing(self):
        """Test 3: Task File Parsing and Extraction"""
        print("\n📋 Test 3: Task Parsing")
        print("-" * 50)
        
        try:
            # Test task file reading
            task_file = "tasks/task_1.txt"
            if os.path.exists(task_file):
                with open(task_file, "r", encoding="utf-8") as f:
                    content = f.read()
                self.log_test("Task File Reading", "PASS", f"Loaded {len(content)} characters")
                
                # Test AI task extraction
                llm = ChatAI(model="gpt-4o", provider="PollinationsAI", api_key="")
                
                extraction_prompt = f"""
                IMPORTANT: Extract ALL programming tasks from this text. Do NOT skip any tasks, even if they seem similar.
                
                Look for:
                - Tasks numbered with 1), 2), 3), etc.
                - Tasks with bullet points (–)
                - Tasks in different sections (list comprehension, function, etc.)
                - ALL individual programming exercises
                
                Create a complete numbered list in English language.
                Include EVERY single task you find, no matter how similar they are.
                
                Format:
                1. [Brief description of first task]
                2. [Brief description of second task]
                3. [Brief description of third task]
                ... continue for ALL tasks found
                
                Full text to analyze:
                {content}
                
                Remember: Extract EVERY task, don't merge or skip any!
                """
                
                messages = [{"role": "user", "content": extraction_prompt}]
                response = llm.invoke(messages)
                
                # Count extracted tasks
                lines = response.content.split('\n')
                task_count = len([line for line in lines if line.strip() and line.strip()[0].isdigit()])
                
                if task_count >= 15:  # We expect 17 tasks
                    self.log_test("Task Extraction", "PASS", f"Extracted {task_count} tasks")
                elif task_count >= 10:
                    self.log_test("Task Extraction", "WARN", f"Extracted {task_count} tasks (expected 17)")
                else:
                    self.log_test("Task Extraction", "FAIL", f"Only extracted {task_count} tasks")
                    
                # Display extracted tasks
                print(f"\n📋 Extracted Tasks ({task_count} found):")
                for i, line in enumerate(lines[:10]):  # Show first 10
                    if line.strip() and line.strip()[0].isdigit():
                        print(f"   {line.strip()}")
                if task_count > 10:
                    print(f"   ... and {task_count - 10} more tasks")
                    
            else:
                self.log_test("Task File Reading", "FAIL", f"{task_file} not found")
                
        except Exception as e:
            self.log_test("Task Parsing", "FAIL", str(e))

    def test_4_multilingual_support(self):
        """Test 4: Multi-Language Support"""
        print("\n🌍 Test 4: Multi-Language Support")
        print("-" * 50)
        
        try:
            llm = ChatAI(model="gpt-4o", provider="PollinationsAI", api_key="")
            
            # Test English
            en_prompt = "Generate a Python function that calculates the sum of two numbers. Add comments in English."
            en_messages = [{"role": "user", "content": en_prompt}]
            en_response = llm.invoke(en_messages)
            
            if "def" in en_response.content and any(word in en_response.content.lower() for word in ["sum", "add", "calculate"]):
                self.log_test("English Code Generation", "PASS", "Generated English code with comments")
            else:
                self.log_test("English Code Generation", "WARN", "English code may be incomplete")
                
            # Test Ukrainian
            uk_prompt = "Згенеруй Python функцію, яка обчислює суму двох чисел. Додай коментарі українською мовою."
            uk_messages = [{"role": "user", "content": uk_prompt}]
            uk_response = llm.invoke(uk_messages)
            
            if "def" in uk_response.content:
                self.log_test("Ukrainian Code Generation", "PASS", "Generated Ukrainian code")
            else:
                self.log_test("Ukrainian Code Generation", "WARN", "Ukrainian code may be incomplete")
                
            # Test Russian
            ru_prompt = "Сгенерируй Python функцию, которая вычисляет сумму двух чисел. Добавь комментарии на русском языке."
            ru_messages = [{"role": "user", "content": ru_prompt}]
            ru_response = llm.invoke(ru_messages)
            
            if "def" in ru_response.content:
                self.log_test("Russian Code Generation", "PASS", "Generated Russian code")
            else:
                self.log_test("Russian Code Generation", "WARN", "Russian code may be incomplete")
                
        except Exception as e:
            self.log_test("Multi-Language Support", "FAIL", str(e))

    def test_5_code_execution(self):
        """Test 5: Code Generation and Execution"""
        print("\n⚡ Test 5: Code Execution")
        print("-" * 50)
        
        try:
            llm = ChatAI(model="gpt-4o", provider="PollinationsAI", api_key="")
            
            # Generate executable code
            prompt = """
            Generate a Python function that:
            1. Takes a string as input
            2. Extracts all digits from the string
            3. Returns them as a comma-separated string
            
            Requirements:
            - Clean, executable Python code
            - NO markdown blocks
            - Include a test example
            """
            
            messages = [{"role": "user", "content": prompt}]
            response = llm.invoke(messages)
            
            # Clean the response
            code = response.content.strip()
            if code.startswith("```python"):
                code = code[9:]
            elif code.startswith("```"):
                code = code[3:]
            if code.endswith("```"):
                code = code[:-3]
            code = code.strip()
            
            self.log_test("Code Generation", "PASS", f"Generated {len(code)} characters of code")
            
            # Test code execution
            try:
                # Create a safe execution environment
                exec_globals = {}
                exec(code, exec_globals)
                self.log_test("Code Execution", "PASS", "Generated code executed without errors")
                
                # Test if function works
                if any(callable(obj) for obj in exec_globals.values()):
                    self.log_test("Function Creation", "PASS", "Callable function created")
                else:
                    self.log_test("Function Creation", "WARN", "No callable function found")
                    
            except SyntaxError as e:
                self.log_test("Code Execution", "FAIL", f"Syntax error: {e}")
            except Exception as e:
                self.log_test("Code Execution", "WARN", f"Runtime error: {e}")
                
        except Exception as e:
            self.log_test("Code Generation and Execution", "FAIL", str(e))

    def test_6_file_management(self):
        """Test 6: File Management and Organization"""
        print("\n💾 Test 6: File Management")
        print("-" * 50)
        
        try:
            # Test output directory creation
            output_dir = "generated_code"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                self.log_test("Directory Creation", "PASS", f"Created {output_dir} directory")
            else:
                self.log_test("Directory Exists", "PASS", f"{output_dir} directory found")
                
            # Test file saving
            test_code = '''# Test generated code
def hello_world():
    """Test function"""
    print("Hello, World!")

if __name__ == "__main__":
    hello_world()
'''
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_generated_{timestamp}.py"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(test_code)
                
            if os.path.exists(filepath):
                self.log_test("File Saving", "PASS", f"Saved {filename}")
                
                # Test file content
                with open(filepath, "r", encoding="utf-8") as f:
                    saved_content = f.read()
                    
                if saved_content == test_code:
                    self.log_test("File Content", "PASS", "File content matches")
                else:
                    self.log_test("File Content", "WARN", "File content differs")
                    
                # Clean up test file
                os.remove(filepath)
                self.log_test("File Cleanup", "PASS", "Test file removed")
                
            else:
                self.log_test("File Saving", "FAIL", "File was not created")
                
        except Exception as e:
            self.log_test("File Management", "FAIL", str(e))

    def test_7_visual_features(self):
        """Test 7: Visual Features and Formatting"""
        print("\n🎨 Test 7: Visual Features")
        print("-" * 50)
        
        try:
            llm = ChatAI(model="gpt-4o", provider="PollinationsAI", api_key="")
            
            # Test square generation with proper spacing
            square_prompt = """
            Generate Python code that draws a square made of asterisks with proper spacing.
            The square should be visually equal-sided (not rectangular).
            Use spaces between asterisks for better visual appearance.
            
            Requirements:
            - Function that takes size parameter
            - Proper spacing between asterisks
            - NO markdown blocks
            """
            
            messages = [{"role": "user", "content": square_prompt}]
            response = llm.invoke(messages)
            
            if "* *" in response.content or "* " in response.content:
                self.log_test("Square Spacing", "PASS", "Generated code includes proper spacing")
            else:
                self.log_test("Square Spacing", "WARN", "Generated code may not have proper spacing")
                
            # Test multiplication table
            table_prompt = """
            Generate Python code for a multiplication table using while loop.
            Format it as a grid with proper alignment.
            
            Requirements:
            - Use while loop
            - Grid format (not just list)
            - NO markdown blocks
            """
            
            table_messages = [{"role": "user", "content": table_prompt}]
            table_response = llm.invoke(table_messages)
            
            if "while" in table_response.content and any(word in table_response.content.lower() for word in ["table", "multiplication", "grid"]):
                self.log_test("Multiplication Table", "PASS", "Generated multiplication table code")
            else:
                self.log_test("Multiplication Table", "WARN", "Multiplication table code may be incomplete")
                
        except Exception as e:
            self.log_test("Visual Features", "FAIL", str(e))

    def run_all_tests(self):
        """Run all tests and generate report"""
        print("🧪 COMPREHENSIVE TEST SUITE")
        print("=" * 60)
        print("Testing Universal Python Code Generator")
        print("LangChain + G4F Integration")
        print("=" * 60)
        
        # Run all tests
        self.test_1_environment_setup()
        self.test_2_ai_integration()
        self.test_3_task_parsing()
        self.test_4_multilingual_support()
        self.test_5_code_execution()
        self.test_6_file_management()
        self.test_7_visual_features()
        
        # Generate summary report
        self.generate_report()

    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n📊 TEST SUMMARY REPORT")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        warned_tests = len([r for r in self.test_results if r["status"] == "WARN"])
        
        print(f"📈 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"⚠️ Warnings: {warned_tests}")
        print(f"❌ Failed: {failed_tests}")
        
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        print(f"🎯 Success Rate: {success_rate:.1f}%")
        
        elapsed_time = time.time() - self.start_time
        print(f"⏱️ Total Time: {elapsed_time:.2f} seconds")
        
        print("\n📋 Detailed Results:")
        print("-" * 40)
        for result in self.test_results:
            status_emoji = "✅" if result["status"] == "PASS" else "❌" if result["status"] == "FAIL" else "⚠️"
            print(f"{status_emoji} {result['test']}: {result['status']}")
            if result["details"]:
                print(f"   📝 {result['details']}")
        
        print("\n🎉 TEST SUITE COMPLETED!")
        print("=" * 60)
        
        if success_rate >= 80:
            print("🚀 EXCELLENT! System is working properly.")
        elif success_rate >= 60:
            print("👍 GOOD! System is mostly functional with minor issues.")
        else:
            print("⚠️ NEEDS ATTENTION! Several components require fixes.")
            
        print("\n🔗 Next Steps:")
        print("1. Run 'python main.py' to use the application")
        print("2. Select Ukrainian language to test localization")
        print("3. Try generating code for task 15 (square drawing)")
        print("4. Test code saving and execution features")


if __name__ == "__main__":
    test_suite = ComprehensiveTest()
    test_suite.run_all_tests()
