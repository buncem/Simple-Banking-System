import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

# cur.execute('SELECT tbl_name FROM sqlite_master WHERE type = "table";')
# tables = cur.fetchall()
# if tables == [] or 'card' not in tables[0]:
#     cur.execute('CREATE TABLE card (id INTEGER PRIMARY KEY, number VALCHAR(16), pin VALCHAR(4), balance INT DEFAULT 0);')
#     #cur.execute('CREATE TABLE card (id INTEGER PRIMARY KEY, number VALCHAR(16), pin VALCHAR(4), balance INT DEFAULT 0);')
#     conn.commit()

cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER);')
def get_checksum(bank_account_str):
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

def create_card_num():
    bank_id = 400000
    account_id = random.randint(0, 999999999)
    new_bank_account_str = str(bank_id) + str(account_id).zfill(9)
    return new_bank_account_str + get_checksum(new_bank_account_str)

    # control_list = list(str(bank_id) + str(account_id).zfill(9))
    # control_num = 0
    # for i in range(len(control_list)):
    #     control_list[i] = int(control_list[i])
    #     if i % 2 == 0:
    #         control_list[i] *= 2
    #     if control_list[i] > 9:
    #         control_list[i] -= 9
    #     control_num += control_list[i]
    # if control_num % 10 == 0:
    #     checksum = 0
    # else:
    #     checksum = 10 - control_num % 10
    # return str(bank_id) + str(account_id).zfill(9) + str(checksum)

def check_transfer_card_num(transfer_card_num):
    checksum = get_checksum(transfer_card_num[:-1])
    print(checksum)
    if checksum != transfer_card_num[-1]:
        print('Probably you made a mistake in the card number. Please try again!\n')
    else:
        print('algorithm worked')
        pass

class Account:
    def __init__(self, card_num):
        self.card_num = card_num
        self.pin = None
        self.balance = 0
        Account.create_pin(self)
        Account.add_to_database(self)

    def create_pin(self):
        self.pin = str(random.randint(0, 9999)).zfill(4)

    def add_to_database(self):
        cur.execute('INSERT INTO card (number, pin) VALUES ({}, {})'.format(self.card_num, self.pin))
        conn.commit()

    def add_income(self, income):
        self.balance += income




accounts = {}

while True:
    print('1. Create an account')
    print('2. Log into account')
    print('0. Exit')
    user_input = input().strip()
    print()
    if user_input == '1':
        card_num = create_card_num()
        accounts[card_num] = Account(card_num)
        print('Your card has been created')
        print('Your card number:')
        print(card_num)
        print('Your card PIN:')
        print(accounts[card_num].pin)
        print()
    elif user_input == '2':
        card_num = input('Enter your card number:\n').strip()
        pin = input('Enter your PIN:\n').strip()
        print()
        if card_num in accounts and pin == accounts[card_num].pin:
                print('You have successfully logged in!')
                print()
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
                        print('Balance: {}\n'.format(accounts[card_num].balance))
                    elif inside_user_input == '2':
                        income = int(input('Enter income:\n').strip())
                        accounts[card_num].add_income()
                        print('Income was added!\n')
                    elif inside_user_input == '3':
                        transfer_card_num = input('Enter card number:\n').strip()
                        check_transfer_card_num(transfer_card_num)

                    elif inside_user_input == '5':
                        print('You have successfully logged out!')
                        print()
                        break
                    elif inside_user_input == '0':
                        break
                    else:
                        print('Not a valid choice')
                if inside_user_input == '0':
                    break

        else:
            print('Wrong card number or PIN!')
            print()
    elif user_input == '0':
        break
    else:
        print('Not a valid choice')

print('Bye!')
