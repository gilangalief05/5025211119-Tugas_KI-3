import random
import math

# A set will be the collection of prime numbers,
# where we can select random primes p and q
prime = set()

public_key = None
private_key = None
n = None

# We will run the function only once to fill the set of
# prime numbers
def primefiller():
    # Method used to fill the primes set is Sieve of
    # Eratosthenes (a method to collect prime numbers)
    seive = [True] * 250
    seive[0] = False
    seive[1] = False
    for i in range(2, 250):
        for j in range(i * 2, 250, i):
            seive[j] = False

    # Filling the prime numbers
    for i in range(len(seive)):
        if seive[i]:
            prime.add(i)


# Picking a random prime number and erasing that prime
# number from list because p!=q
def pickrandomprime():
    global prime
    k = random.randint(0, len(prime) - 1)
    it = iter(prime)
    for _ in range(k):
        next(it)

    ret = next(it)
    prime.remove(ret)
    return ret


def setkeys():
    global public_key, private_key, n
    prime1 = pickrandomprime()  # First prime number
    prime2 = pickrandomprime()  # Second prime number

    n = prime1 * prime2
    fi = (prime1 - 1) * (prime2 - 1)

    e = 2
    while True:
        if math.gcd(e, fi) == 1:
            break
        e += 1

    # d = (k*Φ(n) + 1) / e for some integer k
    public_key = e

    d = 2
    while True:
        if (d * e) % fi == 1:
            break
        d += 1

    private_key = d


# To encrypt the given number
def encrypt(message, private_key, n):
    e = private_key
    encrypted_text = 1
    while e > 0:
        encrypted_text *= message
        encrypted_text %= n
        e -= 1
    return encrypted_text


# To decrypt the given number
def decrypt(encrypted_text, public_key, n):
    d = public_key
    decrypted = 1
    while d > 0:
        decrypted *= encrypted_text
        decrypted %= n
        d -= 1
    return decrypted


# First converting each character to its ASCII value and
# then encoding it then decoding the number to get the
# ASCII and converting it to character
def encoder(message, private_key, n):
    encoded = []
    # Calling the encrypting function in encoding function
    for letter in message:
        encoded.append(encrypt(ord(letter), private_key, n))
    return encoded


def decoder(encoded, public_key, n):
    s = ''
    # Calling the decrypting function decoding function
    for num in encoded:
        s += chr(decrypt(num, public_key, n))
    return s

def call_key():
    primefiller()
    setkeys()
    return [private_key, public_key, n]

if __name__ == '__main__':
    # key = call_key()
    message = "17CJones"
    # Uncomment below for manual input
    # message = input("Enter the message\n")
    # Calling the encoding function
    # PU, PR, N
    # 3 2347 3649
    # 5 3629 4687
    coded = encoder(message, 2347, 3649)
    print("Initial message:")
    print(message)
    print("Prime:")
    print(prime)
    print("\nThe encoded message(encrypted by private key)")
    print(coded)
    print(' '.join(str(p) for p in coded))

    message = decoder(coded, 5, 4687)
    print("\nThe decoded message(decrypted by public key)")
    print(' '.join(str(p) for p in message))

    coded = encoder(message, 3629, 4687)
    print("Initial message:")
    print(message)
    print("Prime:")
    print(prime)
    print("\nThe encoded message(encrypted by private key)")
    print(' '.join(str(p) for p in coded))

    message = decoder(coded, 3, 3649)
    print("\nThe decoded message(decrypted by public key)")
    print(' '.join(str(p) for p in message))
    
    
# 1. Implementasi Pengiriman key DES pada percakapan menggunakan algoritma RSA
# 2. Public key dari RSA harus diperoleh melalui Public Key Authority
# 3. Pengiriman Key DES harus menggunakan Public-Key Cryptosystems