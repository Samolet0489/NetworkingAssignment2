# RSA encryption example

plain = 'MYPLAINTEXT'
z = 20
n = 33
d = 7
e = pow(d, -1, z)

print(f'Original plaintext = {plain}')

# encryption
ciphertext = ''
for ch in plain:
    p = ord(ch) - ord('A')
    c = (p ** e) % n
    ciphertext += chr(c)

print(f'Ciphertext = {ciphertext=!r}')

# decryption
plain_dec = ''
for ch in ciphertext:
    c = ord(ch)
    p = (c ** d) % n
    plain_dec += chr(p + ord('A'))

print(f'Decrypted ciphertext = {plain_dec}')

