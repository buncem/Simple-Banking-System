import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER);')
conn.commit()

class Account:
    def __init__(self, id = None, card_num=None, pin=None, balance=0):
        self.id = id
        self.card_num = card_num
        self.pin = pin
        self.balance = balance
        self.bank_id = 400000

    def create_card_num(self):
        self.id = random.randint(0, 999999999)
        new_bank_account_str = str(self.bank_id) + str(self.id).zfill(9)
        self.card_num = new_bank_account_str + Account.get_checksum(self, new_bank_account_str)

    def create_pin(self):
        self.pin = str(random.randint(0, 9999)).zfill(4)

    def add_income(self, income):
        self.balance += income
        Account.data_to_database(self, self.card_num, self.balance)

    def account_to_database(self):
        cur.execute('INSERT INTO card (id, number, pin, balance) VALUES ({}, {}, {}, {})'.format(self.id, self.card_num, self.pin, self.balance))
        conn.commit()

    def account_from_database(self, card_number, pin):
        cur.execute('SELECT * FROM card WHERE number={} AND pin={};'.format(card_number, pin))
        card_data = cur.fetchall()
        if card_data == []:
            print('Wrong card number or PIN!\n')
            return False
        else:
            self.id = card_data[0][0]
            self.card_num = card_data[0][1]
            self.pin = card_data[0][2]
            self.balance = card_data[0][3]
            return True

    def data_to_database(self, card_number, new_balance):
        cur.execute('UPDATE card SET balance={} WHERE number={};'.format(new_balance, card_number))
        conn.commit()

    def data_from_database(self, card_number):
        cur.execute('SELECT * FROM card WHERE number={};'.format(card_number))
        return cur.fetchall()

    def delete_account_database(self):
        cur.execute('DELETE FROM card WHERE id={};'.format(self.id))
        conn.commit()

    def transfer(self, card_data):
        transfer_amount = int(input('Enter how much money you want to transfer:\n').strip())
        if transfer_amount > self.balance:
            print('Not enough money!\n')
        else:
            self.balance -= transfer_amount
            Account.data_to_database(self, self.card_num, self.balance)
            new_balance = card_data[0][3] + transfer_amount
            Account.data_to_database(self, card_data[0][1], new_balance)
            print('Success!\n')

    def inside_menu(self):
        while True:
            print('1. Balance')
            print('2. Add income')
            print('3. Do transfer')
            print('4. Close account')
            print('5. Log out')
            print('0. Exit')
            inside_user_input = input().strip()
            print()
            if inside_user_input == '1':
                print('Balance: {}\n'.format(self.balance))
            elif inside_user_input == '2':
                income = int(input('Enter income:\n').strip())
                Account.add_income(self, income)
                print('Income was added!\n')
            elif inside_user_input == '3':
                transfer_card_num = input('Transfer\nEnter card number:\n').strip()
                checksum = Account.get_checksum(self, transfer_card_num[:-1])
                card_data = Account.data_from_database(self, transfer_card_num)
                if checksum != transfer_card_num[-1]:
                    print('Probably you made a mistake in the card number. Please try again!\n')
                    continue
                elif card_data == []:
                    print('Such a card does not exist.\n')
                    continue
                else:
                    Account.transfer(self, card_data)
            elif inside_user_input == '4':
                Account.delete_account_database(self)
                print('The account has been closed!\n')
                return False
            elif inside_user_input == '5':
                print('You have successfully logged out!')
                print()
                return False
            elif inside_user_input == '0':
                return True
            else:
                print('Not a valid choice')


    def get_checksum(self, bank_account_str):
        control_list = list(bank_account_str)
        control_num = 0
        for i in range(len(control_list)):
            control_list[i] = int(control_list[i])
            if i % 2 == 0:
                control_list[i] *= 2
            if control_list[i] > 9:
                control_list[i] -= 9
            control_num += control_list[i]
        if control_num % 10 == 0:
            checksum = 0
        else:
            checksum = 10 - control_num % 10
        return str(checksum)

while True:
    print('1. Create an account')
    print('2. Log into account')
    print('0. Exit')
    user_input = input().strip()
    print()
    if user_input == '1':
        account = Account()
        account.create_card_num()
        account.create_pin()
        account.account_to_database()
        print('Your card has been created')
        print('Your card number:')
        print(account.card_num)
        print('Your card PIN:')
        print(account.pin)
        print()
    elif user_input == '2':
        card_num = input('Enter your card number:\n').strip()
        pin = input('Enter your PIN:\n').strip()
        print()
        account = Account()
        if account.account_from_database(card_num, pin) == False:
            continue
        print('You have successfully logged in!\n')
        if account.inside_menu():
            break
    elif user_input == '0':
        break
    else:
        print('Not a valid choice')

print('Bye!')
