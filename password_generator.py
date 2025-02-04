import random
import string

# Função para gerar uma senha aleatória
def generate_random_password(length=8):
    # Define os caracteres possíveis para a senha
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Gera 1000 senhas aleatórias
passwords = [generate_random_password(random.randint(8, 16)) for _ in range(1000)]

# Cria um arquivo chamado "password_generator.txt" e grava as senhas
with open('passwords.txt', 'w') as file:
    for password in passwords:
        file.write(password + "\n")

print("Arquivo 'password_generator.txt' foi gerado com sucesso!")