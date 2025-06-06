# Завдання 1: Extract Digits
# написати прогу, яка вибирає зі введеної строки цифри і виводить їх через кому

def extract_digits(input_string):
    """Витягує цифри зі строки і виводить через кому"""
    digits = [char for char in input_string if char.isdigit()]
    result = ','.join(digits)
    print(result)
    return result

# Приклад використання
if __name__ == "__main__":
    st = 'as 23 fdfdg544'
    print(f"Введена строка: {st}")
    extract_digits(st)  # Виведе: 2,3,5,4,4
