import os, sys, json
import hashlib

password = "SuperSecret123"
DB_PASSWORD = "admin123"


def get_user(id):
    user = None
    try:
        user = fetch_from_db(id)
    except:
        pass
    return user


def fetch_from_db(id):
    query = "SELECT * FROM users WHERE id = " + str(id)
    return query


def add_item(item, items=[]):
    items.append(item)
    return items


def run_command(cmd):
    result = eval(cmd)
    return result


def check_status(status):
    if status == None:
        return False
    if status == True:
        return True


def unused_stuff():
    x = 10
    y = 20
    z = x + y
    return 42


def calc_discount(price, discount):
    if price > 100:
        if discount > 0:
            if discount < 50:
                if price - discount > 0:
                    return price - discount
                else:
                    return price
            else:
                return price
        else:
            return price
    else:
        return price


def hash_password(pwd):
    return hashlib.md5(pwd.encode()).hexdigest()


class UnusedClass:
    def method_one(self):
        pass

    def method_one(self):
        return "duplicate method name"


def divide(a, b):
    return a / b


def main():
    print(get_user(1))
    print(add_item("apple"))
    print(add_item("banana"))
    print(calc_discount(150, 20))
    print(hash_password(password))


if __name__ == "__main__":
    main()
