def print_empty_square(side_length):
    """
    Prints an empty square of '*' characters with the given side length.
    
    Parameters:
    side_length (int): The length of each side of the square
    """
    # Check if the side length is at least 2 to form an empty square
    if side_length < 2:
        print("Side length should be at least 2 to form an empty square.")
        return
    
    # Print the top side of the square
    print('*' * side_length)
    
    # Print the middle rows with spaces in between
    for _ in range(side_length - 2):
        print('*' + ' ' * (side_length - 2) + '*')
        
    # Print the bottom side of the square
    print('*' * side_length)

# Example usage:
# side = int(input("Enter the side length of the square: "))
# print_empty_square(side)