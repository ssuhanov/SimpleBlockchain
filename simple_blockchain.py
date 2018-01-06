import hashlib

HASH_STARTS_WITH = "777"
OUTPUT_FORMAT = "{0} ({1}) -> {2}"
PLUS_SIGN = " + "
RIGHT_ARROW = " -> "
START_HASH = ""


def encrypt_sha256(str_data):
    return hashlib.sha256(str_data.encode()).hexdigest()


def encrypt_with_nonce(str_data, previous_hash, _nonce):
    _string = str_data + previous_hash + str(_nonce)
    _encrypted_string = encrypt_sha256(_string)
    return _string, _encrypted_string


def encrypt(str_data, previous_hash, hash_start):
    _nonce = 0
    _string, _encrypted_string = encrypt_with_nonce(str_data, previous_hash, _nonce)
    while not _encrypted_string.startswith(hash_start):
        _nonce += 1
        _string, _encrypted_string = encrypt_with_nonce(str_data, previous_hash, _nonce)

    return _encrypted_string, _nonce


def encrypt_with_output(str_data, previous_hash):
    _encrypted_string, nonce = encrypt(str_data, previous_hash, HASH_STARTS_WITH)
    _str_array = filter(lambda x: len(x)>0, [str_data, previous_hash, str(nonce)])
    print(PLUS_SIGN.join(_str_array) + RIGHT_ARROW + _encrypted_string)
    # print(OUTPUT_FORMAT.format(str_data, nonce, _encrypted_string))
    return _encrypted_string


my_previous_hash = START_HASH

print("Encrypting array:")
my_str_array = ["Hello, World!",
                "My name is Bob",
                "How are you?",
                "Some digits: 123456789",
                "Something else"]

for my_str in my_str_array:
    my_previous_hash = encrypt_with_output(my_str, my_previous_hash)

print("\nSimple encrypting:")
print("Iteration 0:")
my_previous_hash = encrypt_with_output("Hello, World!", my_previous_hash)
for i in range(1000):
    print("\nIteration {0}:".format(i+1))
    my_previous_hash = encrypt_with_output("", my_previous_hash)
