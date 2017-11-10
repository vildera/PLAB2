from math import gcd
import random
from oving3 import crypto_utils as cu



# --------- Superclass Cipher ----------
class Cipher:



    def __init__(self):
        self.alphabet_size = 95
        self.legal_alphabet = " !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
        #self.legal_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        #self.alphabet_size = 26

    def encode(self,text,key):
        return NotImplementedError

    def decode(self,text,key):
        return NotImplementedError

    def verify(self, decodedText,encodedText):
        return decodedText == self.decode(encodedText) and encodedText == self.encode(decodedText)


    def generate_keys(self, key):
        return NotImplementedError




#--------Sublclass Caesar-------------

class Caesar(Cipher):

    def __init__(self):
        super().__init__()

    #fra orginal tekst til kodet tekst
    def encode(self,text,key):
        self.encoded_str = ""

        for character in text:
            index = self.legal_alphabet.index(character)
            self.encoded_str += self.legal_alphabet[(index + key) % self.alphabet_size]

        return self.encoded_str


    #fra kodet tekst til orginal tekst
    def decode(self,text, key):
        self.decoded_str = ""

        for character in text:
            index = self.legal_alphabet.index(character)
            self.decoded_str += self.legal_alphabet[(index - key) % self.alphabet_size]
        return self.decoded_str




#--------Subclass Multiplikasjons-cipher--------

class Multiplication(Cipher):

    def __init__(self):
        super().__init__()


    def encode(self, text, key):
        self.encoded_str = ""

        for character in text:
            index = self.legal_alphabet.index(character)
            self.encoded_str += self.legal_alphabet[(index * key)%self.alphabet_size]

        return self.encoded_str


    def decode(self,text,key):
        self.decoded_str = ""

        #modular_inverse returnerer modulo-inversen, a = nøkkel, m= lengden av alfabetet
        #OBS: En nøkkel n virker bare bare dersom den har en modulo-invers

        for character in text:
            index = self.legal_alphabet.index(character)
            new_key = cu.modular_inverse(key,self.alphabet_size)

            self.decoded_str += self.legal_alphabet[(index * new_key) % self.alphabet_size]

        return self.decoded_str


# Genererer motsatt nøkkel, slik at den krypterte meldingen kan dekrypteres
    def generate_keys(self, key):
        return cu.modular_inverse(key,self.alphabet_size)


#---------Subclqss Affline cipher---------

#Kombinasjon av multiplikasjons-cipher og Caesar-cipher

#bruker tuple av to heltall som nøkkel n = (n1,n2) der
# n1: brukes til mullt - cipher
# n2: brukes til caesar - cipher
# Først skal text krypteres med multiplicative, derretter krypteres med Caesar

class Affline(Cipher):

    def __init__(self):
        super().__init__()



    def encode(self,text, keys):
        mult = Multiplication()
        encodedByMult = mult.encode(text,keys[0])

        caesar = Caesar()
        encodedByCaesar = caesar.encode(encodedByMult,keys[1])

        return encodedByCaesar




    def decode(self,text,keys):

        caesar = Caesar()
        decodedByCaesar = caesar.decode(text,keys[1])

        mult = Multiplication()
        decodedByMult = mult.decode(decodedByCaesar,keys[0])

        return decodedByMult


class Unbreakable(Cipher):

    # key er her secret word / et helt ord
    def __init__(self):
        super().__init__()





    def encode(self,text, keyword):
        i = 0
        encoded_str = ""

        if len(keyword) == 0:
            return""

        # Finner indeks i i nøkkelordet (tallverdi) + tallverdien til meldingen mod alfabetstrl
        for character in text:
            index = (self.legal_alphabet.index(keyword[i % len(keyword)]) + self.legal_alphabet.index(character)) % self.alphabet_size
            encoded_str += self.legal_alphabet[index]
            i +=1

        return encoded_str


    def decode(self,text, keyword):
        inverted_keyword = self.generate_inverted_key(keyword)
        decoded_str =""
        i=0


        for character in text:
            index = (self.legal_alphabet.index(inverted_keyword[i % len(inverted_keyword)]) + self.legal_alphabet.index(character)) % self.alphabet_size
            decoded_str += self.legal_alphabet[index]
            i+=1
        return decoded_str


    #Motsatt nøkkel for dekrypteringen
    def generate_inverted_key(self,key):
        inverted_key = ""
        for char in key:
            inverted_key += self.legal_alphabet[(self.alphabet_size - self.legal_alphabet.index(char)) % self.alphabet_size]
        return inverted_key




#----------Subclass RSA------------

class RSA(Cipher):

    def __init__(self):
        super().__init__()



    def encode(self,text,key):
        n,public_key = key
        blocks = cu.blocks_from_text(text,2)

        return [pow(t,public_key,n) for t in blocks] # encodet tekst


    def decode(self,text,key): #key er (n,d)      tekst er tall
        decoded_num = [pow(int(t), int(key[1]), int(key[0])) for t in text]
        decoded_str = cu.text_from_blocks(decoded_num,2)
        return decoded_str




#---------Superclass Person -----------
class Person:

    def __init__(self,key, cipher):
        self.key = key
        self.cipher = cipher

    def setKey(self,key):
        self.key = key

    def get_key(self):
        return self.key

    def operate_cipher(self,text): #Initialisere i sub-klassr
        return NotImplementedError



#----------Subclass SENDER---------


class Sender(Person):
    def __init__(self, key, cipher):
        super().__init__(key, cipher)


    def operate_cipher(self,text):
        #Genererer encodet tekst med egen cipher og nøkkel
        self.encoded_str = self.cipher.encode(text,self.key)
        return self.encoded_str

    # Hvis cipher er RSA
    def send_cipher(self,reciever,text):

        if isinstance(self.cipher,RSA):
            reciever.generate_keys()
            self.key = reciever.senderKey()

        reciever.recieve_cipher(self.operate_cipher(text))

    def test_print(self):
        return self.encoded_str





#-----------Subclass RECIEVER--------

class Receiver(Person):

    def __init__(self,key,cipher):
        super().__init__(key,cipher)

    def operate_cipher(self,text):
        self.encoded_str = text
        self.decoded_str = self.cipher.decode(text,self.key)
        return self.decoded_str


    def recieve_cipher(self,text):
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
        return self.decoded_str




#----------Subclass HACKER--------------
#Skal hacke alle cipher bortsett fra RSA
class Hacker(Person):

    def __init__(self, cipher):
        self.cipher = cipher
        self.createWords()

        #lager ordliste med ord fra fil (alle mulige ord som brukes)
    def createWords(self):
        self.words = [line.rstrip('n') for line in open('english_words.txt')]


    #finner alle mulige nøkler
    def find_possible_keys(self):
        #Sjekker hvilke nøkler som skal testes - basert på  cipher
        #teller antall treff i ordboken

        #Når den skal hacke: Vil for hver nøkkel telle hvor mange trekk det er i ordlisten
        # --> returnerer nøkkel med flest treff
        if isinstance(self.cipher, Caesar) or isinstance(self.cipher,Multiplication):
            self.match = [0] * self.cipher.alphabet_size
            return [j for j in range(self.cipher.alphabet_size)]

        elif isinstance(self.cipher,Affline):
            self.match = [0] * (self.cipher.alphabet_size)**2
            return [(k,l) for k in range(0,self.cipher.alphabet_size) for l in range(0,self.cipher.alphabet_size)]

        elif isinstance(self.cipher,Unbreakable):
            self.match = [0] * len(self.words)
            return self.words


        #liste med alle nøkler
        #Vil gå igjennom for hver nøkkel - dekode med teksten og den nøkkelen (for alle mulige nøkler)
        #for hvert ord den får der, vil den plusse på en for hvert treff i ordlisten
        # best_key = flest treff
        #returnerer teksten med den beste nøkkelen

    def decode_text(self,text):

        possible_keys = self.find_possible_keys()

        for key in possible_keys:
            decoded_str = self.cipher.decode(text,key)

            for word in decoded_str.split():
                if self.words.__contains__(word):
                    self.match[possible_keys.index(key)] += 1
                    if self.match[possible_keys.index(key)] ==1:
                        print("possible key",key)

        best_key = possible_keys[self.match.index(max(self.match))]

        print(best_key)

        return self.cipher.decode(text,best_key)

def main():
    text = "dette er en tekst som skal kodes"

    print("Opprinnelig tektst:",text, '\n')

    caesar = Caesar()
    mult = Multiplication()
    affine = Affline()
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
    s5 = Sender("gland", Unbreakable())
    r5 = Receiver("gland", Unbreakable())

    s5.send_cipher(r5, text)

    print("Sender koder teksten til:\n", s5.test_print())
    print("Mottaker dekoder teksten til:\n", r5.test_print())

    print("")




main()
