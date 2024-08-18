from cryptography.fernet import Fernet

























# Encrypt the sensitive value
key = Fernet.generate_key()  # This should be stored securely
cipher_suite = Fernet(key)
cipher_text = cipher_suite.encrypt(b"my_secret_value")

# At runtime, decrypt it
print(cipher_text)
plain_text = cipher_suite.decrypt(b'gAAAAABmv2J4RGyP1LGvB0Q1ApCdZD4v-CBLWpFuSNZ3LPj-YNmoWUnTT-PhQKdIgyoLwSBi7BTWgKThazPjz3VScdkZkcivyA==').decode()
print(plain_text)