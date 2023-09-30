import random

def username_gene():
    phone=12345
    generate=random.randint(0,phone)
    return generate

result= username_gene()
print(f"Random number generate:{result}")