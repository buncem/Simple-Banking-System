import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER);')
conn.commit()

class Account:
    def __init__(self, card_num=None, pin=None, balance=0):
        self.card_num = card_num
        self.pin = pin
        self.balance = balance
        self.bank_id = 40000

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

    def create_card_num(self):
        account_id = random.randint(0, 999999999)
        new_bank_account_str = str(self.bank_id) + str(account_id).zfill(9)
        self.card_num =  new_bank_account_str + Account.get_checksum(self, new_bank_account_str)

    def create_pin(self):
        self.pin = str(random.randint(0, 9999)).zfill(4)

    def add_to_database(self):
        cur.execute('INSERT INTO card (number, pin, balance) VALUES ({}, {}, {})'.format(self.card_num, self.pin, self.balance))
        conn.commit()

    def retrieve_from_database(self, card_number, pin):
        cur.execute('SELECT * FROM card WHERE number={};'.format(card_number))
        print(cur.fetchall())

    def add_income(self, income):
        self.balance += income

    def check_transfer_card_num(self, transfer_card_num):
        checksum = Account.get_checksum(self, transfer_card_num[:-1])
        print(checksum)
        if checksum != transfer_card_num[-1]:
            print('Probably you made a mistake in the card number. Please try again!\n')
        else:
            print('algorithm worked')
            pass

accounts = {}

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
        account.add_to_database()
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
        account.retrieve_from_database(card_num, pin)

        # if card_num in accounts and pin == accounts[card_num].pin:
        #         print('You have successfully logged in!')
        #         print()
        #         while True:
        #             print('1. Balance')
        #             print('2. Add income')
        #             print('3. Do transfer')
        #             print('4. Close account')
        #             print('5. Log out')
        #             print('0. Exit')
        #             inside_user_input = input().strip()
        #             print()
        #             if inside_user_input == '1':
        #                 print('Balance: {}\n'.format(accounts[card_num].balance))
        #             elif inside_user_input == '2':
        #                 income = int(input('Enter income:\n').strip())
        #                 accounts[card_num].add_income()
        #                 print('Income was added!\n')
        #             elif inside_user_input == '3':
        #                 transfer_card_num = input('Enter card number:\n').strip()
        #                 check_transfer_card_num(transfer_card_num)
        #
        #             elif inside_user_input == '5':
        #                 print('You have successfully logged out!')
        #                 print()
        #                 break
        #             elif inside_user_input == '0':
        #                 break
        #             else:
        #                 print('Not a valid choice')
        #         if inside_user_input == '0':
        #             break
        #
        # else:
        #     print('Wrong card number or PIN!')
        #     print()
    elif user_input == '0':
        break
    else:
        print('Not a valid choice')

print('Bye!')
