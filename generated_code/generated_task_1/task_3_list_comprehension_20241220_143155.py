# Завдання 3: List Comprehension
# є строка: greeting = 'Hello, world'
# записати кожний символ, як окремий елемент списку, і зробити його заглавним

def string_to_uppercase_list(input_string):
    """Перетворює строку в список заглавних символів"""
    result = [char.upper() for char in input_string]
    print(result)
    return result

# Приклад використання
if __name__ == "__main__":
    greeting = 'Hello, world'
    print(f"Початкова строка: {greeting}")
    uppercase_list = string_to_uppercase_list(greeting)
    # Виведе: ['H', 'E', 'L', 'L', 'O', ',', ' ', 'W', 'O', 'R', 'L', 'D']
