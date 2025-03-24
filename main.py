import hashlib
import random
import os
import pickle

def create_pin(pin):
    hashed_pin = hashlib.sha512(pin.encode('utf-8')).hexdigest()
    return hashed_pin

def verify_pin(pin, hashed_pin):
    return hashed_pin == create_pin(pin)


def generate_bank_code() -> str:
    first_digit = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])

    rest_digits = ''.join(str(random.randint(0, 9)) for _ in range(7))

    bank_code = f"{first_digit}{rest_digits}"

    return bank_code

def generate_iban(bank_code: str) -> str:

    account_number = str(random.randint(0, 9999999999)).zfill(10)

    country_code = "DE"
    pseudo_iban = bank_code + account_number + "131400"

    check_digits = 98 - (int(pseudo_iban) % 97)

    iban = f"{country_code}{check_digits:02}{bank_code}{account_number}"

    return iban



class System:
    def __init__(self):
        self.banks = []

    def __repr__(self):
        return f"System:\nBanks: {self.banks}"

    def get_bank(self, name):
        for bank in self.banks:
            if bank.name == name:
                return bank
        return False

    def get_bank_by_blz(self, blz):
        for bank in self.banks:
            if bank.blz == blz:
                return bank
        return False

    def find_account_by_iban(self, search_iban):
        for bank in self.banks:
            for account in bank.accounts:
                if account.iban == search_iban:
                    return account
        return False

    def create_bank(self):
        name = input("Bank Name: ")
        capital = input("Capital: ")
        while isinstance(capital, int):
            print("Capital must be a Number!")
            capital = input("Capital: ")
        pin = input("Admin Pin: ")
        while isinstance(pin, int):
            print("Pin must be a Number!")
            pin = input("Admin Pin: ")
        self.banks.append(Bank(name, [], capital, pin))
        print(f"Bank {name} successful created!")

    def create_account(self):
        name = input("Your Name: ")
        capital = input("Start Capital: ")
        while isinstance(capital, int):
            print("Capital must be a Number!")
            capital = input("Capital: ")
        pin = input("Card Pin: ")
        while isinstance(pin, int):
            print("Pin must be a Number!")
            pin = input("Card Pin: ")
        max_credit = input("Max Credit Amount: ")
        while isinstance(max_credit, int):
            print("Max Credit Amount must be a Number!")
            max_credit = input("Max Credit Amount: ")
        bank_name = input("Bank Name: ")
        while not self.get_bank(bank_name):
            print("Bank doesn't exist!")
            bank_name = input("Bank Name: ")
        bank = self.get_bank(bank_name)
        bank.create_account(name, capital, max_credit, pin)

    def deposit(self):
        bank_name = input("Bank Name: ")
        while not self.get_bank(bank_name):
            print("Bank doesn't exist!")
            bank_name = input("Bank Name: ")
        bank = self.get_bank(bank_name)
        iban = input("Your IBAN: ")
        while not self.find_account_by_iban(iban):
            print("Account doesn't exist!")
            iban = input("Your IBAN: ")
        amount = input("Amount: ")
        while isinstance(amount, int):
            print("Amount must be a Number!")
            amount = input("Amount: ")
        pin = input("Card Pin: ")
        while isinstance(pin, int):
            print("Pin must be a Number!")
            pin = input("Card Pin: ")
        bank.deposit(iban, amount, pin)

    def withdraw(self):
        bank_name = input("Bank Name: ")
        while not self.get_bank(bank_name):
            print("Bank doesn't exist!")
            bank_name = input("Bank Name: ")
        bank = self.get_bank(bank_name)
        iban = input("Your IBAN: ")
        while not self.find_account_by_iban(iban):
            print("Account doesn't exist!")
            iban = input("Your IBAN: ")
        amount = input("Amount: ")
        while isinstance(amount, int):
            print("Amount must be a Number!")
            amount = input("Amount: ")
        pin = input("Card Pin: ")
        while isinstance(pin, int):
            print("Pin must be a Number!")
            pin = input("Card Pin: ")
        bank.withdraw(iban, amount, pin)

    def take_out_credit(self):
        bank_name = input("Bank Name: ")
        while not self.get_bank(bank_name):
            print("Bank doesn't exist!")
            bank_name = input("Bank Name: ")
        bank = self.get_bank(bank_name)
        iban = input("Your IBAN: ")
        while not self.find_account_by_iban(iban):
            print("Account doesn't exist!")
            iban = input("Your IBAN: ")
        amount = input("Amount: ")
        while isinstance(amount, int):
            print("Amount must be a Number!")
            amount = input("Amount: ")
        pin = input("Card Pin: ")
        while isinstance(pin, int):
            print("Pin must be a Number!")
            pin = input("Card Pin: ")
        bank.take_out_credit(iban, amount, pin)

    def transfer(self):
        bank_name = input("Bank Name: ")
        while not self.get_bank(bank_name):
            print("Bank doesn't exist!")
            bank_name = input("Bank Name: ")
        bank = self.get_bank(bank_name)
        iban = input("Your IBAN: ")
        while not self.find_account_by_iban(iban):
            print("Account doesn't exist!")
            iban = input("Your IBAN: ")
        iban2 = input("The IBAN you want to transfer to: ")
        while not self.find_account_by_iban(iban2):
            print("Account doesn't exist!")
            iban2 = input("The IBAN you want to transfer to: ")
        print(iban2[:8])
        bank2 = self.get_bank_by_blz(iban2[:8])
        amount = input("Amount: ")
        while isinstance(amount, int):
            print("Amount must be a Number!")
            amount = input("Amount: ")
        pin = input("Card Pin: ")
        while isinstance(pin, int):
            print("Pin must be a Number!")
            pin = input("Card Pin: ")
        bank.transfer(iban, amount, pin, bank2)

    def check_balance(self):
        bank_name = input("Bank Name: ")
        while not self.get_bank(bank_name):
            print("Bank doesn't exist!")
            bank_name = input("Bank Name: ")
        bank = self.get_bank(bank_name)
        iban = input("Your IBAN: ")
        while not self.find_account_by_iban(iban):
            print("Account doesn't exist!")
            iban = input("Your IBAN: ")
        bank.check_balance(iban)



class Bank:

    def __init__(self, name, accounts, balance, admin_pin):
        self.name = name
        self.accounts = accounts
        self.balance = int(balance)
        self.admin_pin = create_pin(admin_pin)
        self.blz = generate_bank_code()

    def __repr__(self):
        return f"Bank Name: {self.name} \nBank Accounts: {len(self.accounts)} \nBank Balance: {self.balance}€ \nBank Admin Pin: {self.admin_pin} \nBank BLZ: {self.blz}\n"

    def create_account(self, owner_name, start_capital, max_credit_amount, pin):
        account = Account(owner_name, start_capital, max_credit_amount, pin, self.blz)
        start_capital = int(start_capital)
        self.balance += start_capital
        self.accounts.append(account)
        print(f"Account successful created for {owner_name} with IBAN {account.iban}. Please keep this IBAN in a safe place. You can't change it later!")

    def deposit(self, iban, amount, pin):
        amount = int(amount)
        if not system.find_account_by_iban(iban):
            print("Account doesn't exist!")
            return False
        account = system.find_account_by_iban(iban)
        if not verify_pin(pin, account.pin):
            print("Incorrect Account Pin!")
            return False
        account.balance += amount
        self.balance += amount
        print(f"You habe successfully deposited {amount}€ to IBAN: {iban} with owner {account.owner_name}!")

    def withdraw(self, iban, amount, pin):
        amount = int(amount)
        if not system.find_account_by_iban(iban):
            print("Account doesn't exist!")
            return False
        account = system.find_account_by_iban(iban)
        if not verify_pin(pin, account.pin):
            print("Incorrect Account Pin!")
            return False
        if amount > account.balance:
            print("Not enough Money!")
            print(f"Do you want to take out a loan of of {round((amount - account.balance)*1.1, 2)}€ (fixed loan rate included)?")
            return round((amount - account.balance)*1.1, 2)
        account.balance -= amount
        self.balance -= amount
        print(f"You have successfully withdrawn {amount}€ from IBAN: {iban} with owner {account.owner_name}!")

    def take_out_credit(self, iban, amount, pin):
        amount = int(amount)
        if not system.find_account_by_iban(iban):
            print("Account doesn't exist!")
            return False
        account = system.find_account_by_iban(iban)
        if not verify_pin(pin, account.pin):
            print("Incorrect Account Pin!")
            return False
        if account.max_credit_amount < amount*-1:
            print("You can't take a credit that high!")
        account.balance = amount*-1
        self.balance -= amount
        print(f"You have successfully taken out a loan of {account.balance}€ on the IBAN {iban} with owner {account.owner_name}!")

    def transfer(self, iban, iban2, amount, pin):
        amount = int(amount)
        if not system.find_account_by_iban(iban):
            print("Account doesn't exist!")
            return False
        account = system.find_account_by_iban(iban)
        if not system.find_account_by_iban(iban2):
            print("Account you want so send money doesn't exist!")
            return False
        account2 = system.find_account_by_iban(iban2)
        if not verify_pin(pin, account.pin):
            print("Incorrect Account Pin!")
            return False
        if amount > account.balance:
            print("Not enough Money!")
            return False
        account.balance -= amount
        self.balance -= amount
        account2.balance += amount
        system.get_bank_by_blz(account2.blz).balance += amount
        print(f"You paid {amount}€ to {account2.name} ({account2.iban})!")

    def check_balance(self, iban, pin):
        if not system.find_account_by_iban(iban):
            print("Account doesn't exist!")
            return False
        account = system.find_account_by_iban(iban)
        if not verify_pin(pin, account.pin):
            print("Incorrect Account Pin!")
            return False
        return account.balance


class Account:

    def __init__(self, owner_name, start_balance, max_credit_amount, pin, blz):
        self.iban = generate_iban(blz)
        self.owner_name = owner_name
        self.balance = int(start_balance)
        self.max_credit_amount = int(max_credit_amount)
        self.pin = create_pin(pin)

    def __repr__(self):
        return f"\nAccount IBAN: {self.iban} \nAccount Owner Name: {self.owner_name} \nAccount Balance: {self.balance}€ \nAccount maximal Credit Amount: {self.max_credit_amount} \nAccount Pin: {self.pin}\n"


system = System()
print(f"Commands: \nLoad Session: 0 \nCreate Bank: 1 \nCreate Account: 2 \nDeposit: 3 \nWithdraw: 4 \nTake out credit: 5 \nTransfer: 6 \nExit: exit \n")
run = True
while run:
    command = input("\nWhat do you want to do? ")
    if command == "exit":
        run = False
    if command not in ["0", "1", "2", "3", "4", "5", "6"]:
        print("Command not found!")
        continue
    command = int(command)
    if command == 0:
        if not os.path.exists("bank_data.pkl"):
            print("No session found!")
            continue
        with open("bank_data.pkl", "rb") as file:
            system = pickle.load(file)
            print("Session loaded successfully!")
    if command == 1:
        system.create_bank()
    if command == 2:
        system.create_account()
    if command == 3:
        system.deposit()
    if command == 4:
        system.withdraw()
    if command == 5:
        system.take_out_credit()
    if command == 6:
        system.transfer()
    if command == 7:
        print(system)

if input("Do you want to save your session? (y/n) ") == "y":
    with open("bank_data.pkl", "wb") as file:
        pickle.dump(system, file)
        print("Session saved successfully!")


print("Thank you for using our banking system!")