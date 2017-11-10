from oving3 import crypto_utils as cu
from math import gcd
import random

#-------------Cipher------------
class Cipher:
    def __init__(self):
        self.alphabet_size = 95
        self.legal_alphabet = " !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

        #self.legal_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        #self.alphabet_size = 26

    def encode(self, text, key):       #KODE
        return None            # Initialiseres i subklasser

    def decode(self, text, key):       #DEKODE
        return None            # Initialiseres i subklasser

    def verify(self, decodedText, encodedText): # Sjekker om teksten er riktig begge veier
        return decodedText == self.decode(encodedText) and encodedText == self.encode(decodedText)


    def generate_keys(self):
        return None            # Initialiseres i subklasser





#-----------Subclass_Caesar----------
class Caesar(Cipher):
    def __init__(self):
        super().__init__()


    def encode(self, text, key): # Gjøre om original tekst til kodet tekst/kryptere
        self.encoded_text = ""

        for symbol in text:
            index_in_alphabet = self.legal_alphabet.index(symbol)
            self.encoded_text += self.legal_alphabet[(index_in_alphabet+key)%self.alphabet_size]

        return self.encoded_text

    def decode(self, text, key):
        self.decoded_text = ""

        for symbol in text:
            index_in_alphabet = self.legal_alphabet.index(symbol)
            self.decoded_text += self.legal_alphabet[(index_in_alphabet-key)%self.alphabet_size]

        return self.decoded_text



class Mult_Cipher(Cipher):

    def __init__(self):
        super().__init__()

    def encode(self, text, key):
        self.encoded_text = ""
        for symbol in text:
            index_in_alphabet = self.legal_alphabet.index(symbol)
            self.encoded_text += self.legal_alphabet[(index_in_alphabet*key)%self.alphabet_size]

        return self.encoded_text

    def decode(self, text, key):
        self.decoded_text = ""
        self.secret_key_mod_inverse = cu.modular_inverse(key, self.alphabet_size)


        for symbol in text:
            index_in_alphabet = self.legal_alphabet.index(symbol)
            self.decoded_text += self.legal_alphabet[(index_in_alphabet*self.secret_key_mod_inverse)%self.alphabet_size]

        return self.decoded_text

    def generate_keys(self, key):
        return cu.modular_inverse(key, self.alphabet_size)

#----------Affine_cipher_subclass----------

class Affine_cipher(Cipher):
    def __init__(self):
        super().__init__()

    def encode(self, text, key):
        mult_cipher = Mult_Cipher()     # Oppretter mult_cipher
        mult_encoded = mult_cipher.encode(text, key[0])

        caesar = Caesar()
        encoded_text = caesar.encode(mult_encoded, key[1])
        return encoded_text

    def decode(self, text, key):
        caesar = Caesar()
        caesar_text = caesar.decode(text, key[1])

        mult_cipher = Mult_Cipher()
        decoded_text =  mult_cipher.decode(caesar_text, key[0])

        return decoded_text



#-------------Unbreakable subclass Cipher -----

class Unbreakable(Cipher):
    def __init__(self):
        super().__init__()

    def encode(self, text, keyword):
        encoded_text = ""
        keyword_index = 0
        self.text = text

        if len(keyword) == 0:
            return ""

        for symbol in self.text:
            symbol_index_in_alphabet = self.legal_alphabet.index(symbol)
            keyword_index_in_alphabet = self.legal_alphabet.index(keyword[keyword_index%len(keyword)])

            code_key = symbol_index_in_alphabet + keyword_index_in_alphabet

            encoded_text += self.legal_alphabet[code_key%self.alphabet_size]
            keyword_index += 1

        return encoded_text

    def decode(self, text, keyword):

        decode_keyword = ""

        for symbol in keyword:
            if len(keyword) == 0:
                continue
            else:
                symbol_index_in_alphahet = self.legal_alphabet.index(symbol)
                decode_keyword += self.legal_alphabet[(self.alphabet_size-symbol_index_in_alphahet) % self.alphabet_size]


        return self.encode(text, decode_keyword)



class RSA(Cipher):

    def __init__(self):
        super().__init__()


    def encode(self, text, key):
        n, public_key = key

        blocks = cu.blocks_from_text(text, 2)

        # Returnerer encoded text
        return [pow(t, public_key, n) for t in blocks]

    def decode(self, text, key):
        # Tar inn tekst som består av tall
        # key er (n, d)

        decoded_numb = [pow(int(t), int(key[1]), int(key[0])) for t in text]

        decoded_text = cu.text_from_blocks(decoded_numb, 2)

        return decoded_text



#-------------Person--------------
class Person:

    def __init__(self, key, cipher):
        self.key = key
        self.cipher = cipher


    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key

    def operate_cipher(self): # Initialisere i sub-klasse
        None


#----------Subclass SENDER----------

class Sender(Person):
    def __init__(self, key, cipher):
        super().__init__(key, cipher)

    def operate_cipher(self, text):
        # generere encoded text med egen cipher og nøkkel
        self.encoded_text = self.cipher.encode(text, self.key)
        return self.encoded_text

    def send_cipher(self, recevier, text):
        # Hvis cipher er RSA

        if isinstance(self.cipher, RSA):
            recevier.generate_keys()
            self.key = recevier.senderKey()

        recevier.recieve_cipher(self.operate_cipher(text))


    def test_print(self):
        return self.encoded_text

#-----------Subclass RECIEVER--------

class Receiver(Person):

    def __init__(self, key, cipher):
        super().__init__(key, cipher)

    def operate_cipher(self, text):
        self.encoded_text = text
        self.decoded_text = self.cipher.decode(text, self.key)
        return self.decoded_text

    def recieve_cipher(self, text):
        self.operate_cipher(text)

    def senderKey(self):
        return self.sender_key


    def generate_keys(self):
        p = cu.generate_random_prime(8)
        q = p
        _gcd = 0

        while q == p or _gcd != 1:
            q = cu.generate_random_prime(8)
            p = cu.generate_random_prime(8)
            phi = (p - 1) * (q - 1)
            e = random.randint(3, phi-1)
            _gcd = gcd(e, phi)
            print("p: ", p, "q: ", q, "gcd: ", _gcd)



        n = p * q
        d = cu.modular_inverse(e, phi)

        self.sender_key = (n,e)
        self.key = (n,d)

    def test_print(self):
        return self.decoded_text



#----------Subclass HACKER--------------

class Hacker(Person):
    '''Skal kunne hacke alle ciphers bortsett fra RSA
    Dvs: Caesar, Mult, Affine, Unbreakable'''

    def __init__(self, cipher):
        self.cipher = cipher
        self.createWords()

    def createWords(self):
        self.words = [line.rstrip('\n') for line in open('english_words.txt')]


    def find_possible_keys(self):

        # Maa finne ut hvilke nokler vi må teste, avhengig av hvilken cipher vi har
        # Vil telle antall treff i ordboka per nøkkel

        if isinstance(self.cipher, Caesar) or isinstance(self.cipher, Mult_Cipher):
            self.match = [0]*self.cipher.alphabet_size
            return [j for j in range(self.cipher.alphabet_size)]

        elif isinstance(self.cipher, Affine_cipher):
            self.match = [0] * (self.cipher.alphabet_size)**2
            return [(k,l) for k in range(0,self.cipher.alphabet_size) for l in range(0,self.cipher.alphabet_size)]

        elif isinstance(self.cipher, Unbreakable):
            self.match = [0] * len(self.words)
            return self.words

    def decode_text(self, text):

        possible_keys = self.find_possible_keys()

        for key in possible_keys:
            decoded_text = self.cipher.decode(text, key)

            for word in decoded_text.split():
                if self.words.__contains__(word):
                    self.match[possible_keys.index(key)] += 1
                    if self.match[possible_keys.index(key)] == 1:
                        print("possible key", key)


        best_key = possible_keys[self.match.index(max(self.match))]

        print(best_key)

        toreturn = self.cipher.decode(text, best_key)

        return toreturn



def main():
    text = "dette er en tekst som skal kodes"

    print("Opprinnelig tektst:",text, '\n')

    caesar = Caesar()
    mult = Mult_Cipher()
    affine = Affine_cipher()
    unbreak = Unbreakable()
    rsa = RSA()

    print("CAESAR")
    s1 = Sender(3, caesar)
    r1 = Receiver(3, caesar)
    s1.send_cipher(r1, text)

    print("Sender koder teksten til:\n", s1.test_print())
    print("Mottaker dekoder teksten til:\n", r1.test_print())
    print("")

    print("MULT")
    s2 = Sender(2, mult)
    r2 = Receiver(2, mult)

    s2.send_cipher(r2, text)
    print("Sender koder teksten til:\n", s2.test_print())
    print("Mottaker dekoder teksten til:\n", r2.test_print())
    print("")

    print(("AFFINE"))
    s3 = Sender((3,2), affine)
    r3 = Receiver((3,2), affine)

    s3.send_cipher(r3, text)
    print("Sender koder teksten til:\n", s3.test_print())
    print("Mottaker dekoder teksten til:\n", r3.test_print())
    print("")


    print("RSA")
    s4 = Sender("RSA", rsa)
    r4 = Receiver("RSA", rsa)


    s4.send_cipher(r4, text)
    print("Sender koder teksten til:\n", s4.test_print())
    print("Mottaker dekoder teksten til:\n", r4.test_print())
    print("")



    print("Unbreak")
    s5 = Sender("pizza", unbreak)
    r5 = Receiver("pizza", unbreak)

    s5.send_cipher(r5, text)

    print("Sender koder teksten til:\n", s5.test_print())
    print("Mottaker dekoder teksten til:\n", r5.test_print())

    print("")

    # print("HACKER")
    # text_to_code = "hello this is a sentence in english"
    #
    # hacker = Hacker(unbreak)
    # sender = Sender("hello", unbreak)
    # to_decode_by_hacker = sender.operate_cipher(text_to_code)
    # print("Text to decode:", text_to_code)
    # print("Sender encode to this:", to_decode_by_hacker, '\n')
    #
    # print(hacker.decode_text(to_decode_by_hacker))






    text_to_code = "hello this is a sentence in english"

    h = Hacker(Unbreakable())
    s = Sender("gland", Unbreakable())

    to_decode = s.operate_cipher(text_to_code)
    print("Text to decode:", text_to_code)
    print("Sender encode to this:", to_decode, '\n')
    print("Hacker decodes to:", h.decode_text(to_decode))





main()
