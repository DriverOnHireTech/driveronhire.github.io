import random

def username_gene():
    phone_digit= 1234567890
    generate=random.randint(0,1234567)
    return generate

result= username_gene()
print(f"Random number generate:{result}")