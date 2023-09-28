import random

def username_gene(phone):
    phone=123456789
    generate=random.randint(0,phone)
    return generate

result= username_gene(12365478)
print(f"Random number generate:{result}")