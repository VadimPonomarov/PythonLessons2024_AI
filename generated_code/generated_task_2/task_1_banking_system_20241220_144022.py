# Task 1: Banking System
# Create a class-based implementation of a simple banking system

class Account:
    """Base account class"""
    
    def __init__(self, account_number, owner, balance=0):
        self.account_number = account_number
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        """Deposit money to account"""
        if amount > 0:
            self.balance += amount
            print(f"Deposited ${amount}. New balance: ${self.balance}")
        else:
            print("Deposit amount must be positive")
    
    def withdraw(self, amount):
        """Withdraw money from account"""
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew ${amount}. New balance: ${self.balance}")
        else:
            print("Invalid withdrawal amount")
    
    def get_balance(self):
        """Get current balance"""
        return self.balance

class SavingsAccount(Account):
    """Savings account with interest"""
    
    def __init__(self, account_number, owner, balance=0, interest_rate=0.02):
        super().__init__(account_number, owner, balance)
        self.interest_rate = interest_rate
    
    def add_interest(self):
        """Add interest to balance"""
        interest = self.balance * self.interest_rate
        self.balance += interest
        print(f"Interest added: ${interest}. New balance: ${self.balance}")

class CheckingAccount(Account):
    """Checking account with overdraft protection"""
    
    def __init__(self, account_number, owner, balance=0, overdraft_limit=100):
        super().__init__(account_number, owner, balance)
        self.overdraft_limit = overdraft_limit
    
    def withdraw(self, amount):
        """Withdraw with overdraft protection"""
        if amount > 0 and amount <= (self.balance + self.overdraft_limit):
            self.balance -= amount
            print(f"Withdrew ${amount}. New balance: ${self.balance}")
        else:
            print("Withdrawal exceeds overdraft limit")

# Example usage
if __name__ == "__main__":
    # Create accounts
    savings = SavingsAccount("SAV001", "John Doe", 1000)
    checking = CheckingAccount("CHK001", "Jane Smith", 500)
    
    # Test operations
    savings.deposit(200)
    savings.add_interest()
    
    checking.withdraw(600)  # Uses overdraft
    print(f"Checking balance: ${checking.get_balance()}")
