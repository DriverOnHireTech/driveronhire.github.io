import random

def username_gene(user_name):
    phone_digit= 1234567890
    generate=random.random(phone_digit)
    return generate

result= username_gene(1235466)
print(f"Random number generate:{result}")