import re
import os
import copy
import math

__author__ = "Vilde Arntzen"


class Reader:




    def __init__(self):
        positive = []
        negative = []

        pos_paths = os.listdir("data/alle/train/pos")
        neg_paths = os.listdir("data/alle/train/neg")

        for path in pos_paths:
            positive += self.fileToList("data/alle/train/pos/" + path )
        for path in neg_paths:
            negative += self.fileToList("data/alle/train/neg/" + path )


        #positive,negative = self.n_gram(positive,negative)


        self.pos_wordcount = self.countOccurences(positive)
        self.neg_wordcount = self.countOccurences(negative)

        totalWords = positive + negative

        #pruner alle lister
        self.pruning(0.0000001, totalWords)

        self.pos_infoValues = self.allInformativeWords(True)
        self.neg_infoValues = self.allInformativeWords(False)







    #Del 1 - lese far fil til liste
    #Del 3 - fjerne stop-ord

    def fileToList(self,filename):
        text = ""
        file = open(filename, encoding= 'utf-8')
        stop_file = open("./data/stop_words.txt", encoding= 'utf-8')
        stopwords = set([word.rstrip("\n") for word in stop_file])
        stop_file.close()

        for line in file:
            text += line.lower().rstrip('\n')

        file.close()
        text = re.sub("[.,#+();?<>'-'/'!:*]"," ",text).replace("br ","")

        words = self.n_gram(text.split())

        return list(set(word for word in words if word not in stopwords))









    #Del 2 - lese alle filer, finne 25 mest populære ord

    def mostPopular25Words(self, input):
        new_wordcount = copy.deepcopy(input)
        pop_words =[]
        for index in range(25):
            max_key = max(new_wordcount, key= new_wordcount.get)
            new_wordcount[max_key] = 0
            pop_words.extend([max_key])

        return pop_words



    def countOccurences(self,list):
        # key = ordet, value = antall forekomster i type-filene
        wordcount = {}
        for word in list:
            if word in wordcount:
                wordcount[word] += 1
                continue
            wordcount[word] = 1
        return wordcount


# set default



    # Del 4 - finne informajsonsverdien av ord

    #type: True - pos / False - neg
    def wordValue(self, word, type):
        if type:
            if word in self.neg_wordcount:
                return self.pos_wordcount[word] / (self.pos_wordcount[word] + self.neg_wordcount[word])
            return 1

        else:
            if word in self.pos_wordcount:
                return self.neg_wordcount[word] / (self.pos_wordcount[word] + self.neg_wordcount[word])
            return 1



    def mostInformativeWords(self, type):
        values = {}

        if type:
            dict = self.pos_wordcount
        else:
            dict = self.neg_wordcount

        for word in dict:
            values[word] = self.wordValue(word,type)

        res = {}
        for index in range(25):
            max_key = max(values, key= values.get)
            res[max_key] = values[max_key]
            values[max_key] = 0
        return res


    # Gir infoverdi til alle ord
    def allInformativeWords(self,type):
        values = {}
        if type:
            dict = self.pos_wordcount
        else:
            dict = self.neg_wordcount

        for word in dict:
            values[word] = self.wordValue(word,type)

        return values






    # Del 5 - pruning
    def pruning(self, percentage, totalWords):
        totalOccurences = self.countOccurences(totalWords)

        for word in totalOccurences:
            try:
                if (totalOccurences[word]/ len(totalWords)) <= percentage:
                    self.pos_wordcount.pop(word)
            except KeyError:
                pass
            try:
                if totalOccurences[word]/ len(totalWords) <= percentage:
                    self.neg_wordcount.pop(word)

            except KeyError:
                pass







    # Del 6 - n_gram - sette sammen ord
    def n_gram(self,list):
        n_list = []
        for i in range(len(list)-2):
            n_list.append(list[i] + '_' + list[i+1])
            n_list.append(list[i] + '_' + list[i+1] + '_' + list[i+2])
        return n_list + list







# Kap 4
class Classificationsystem:

    def __init__(self):
        self.reader = Reader()


    #leser fra fil --> Sjekker for hvert ord i filen om den finnes i pos og neg
    #verdi pos_sum += log ( infoValue(ord) )
    #verdi neg_neg += log (infoValue(ord)  )
    # pluss på epsilon hvis den ikke finnes i dict

    #filename = path til en fil
    def get_type(self, filename):
        words = self.reader.fileToList(filename)
        pos_sum = 0
        neg_sum = 0

        for word in words:
            if word in self.reader.pos_infoValues:
                pos_sum += math.log(self.reader.pos_infoValues[word])
            if word not in self.reader.pos_infoValues:
                pos_sum += math.log(0.0005)


            if word in self.reader.neg_infoValues:
                neg_sum += math.log(self.reader.neg_infoValues[word])
            if word not in self.reader.neg_infoValues:
                neg_sum += math.log(0.0005)

        # print("pos_sum : ",pos_sum)
        # print("neg_sum : ",neg_sum)
        #returnerer true hvis artikkel er pos, false hvis den er neg
        return pos_sum > neg_sum




def main():
    # r = Reader()
    # print(r.mostPopular25Words(r.pos_wordcount))
    # print(r.mostInformativeWords(True))
    # print()
    c = Classificationsystem()
    print("neg: ")
    print(c.get_type("data/subset/test/neg/2_3.txt"))
    print(c.get_type("data/subset/test/neg/1_3.txt"))
    print(c.get_type("data/subset/test/neg/2_3.txt"))
    print(c.get_type("data/subset/test/neg/3_4.txt"))
    print()
    print("pos: ")

    print(c.get_type("data/subset/test/pos/0_10.txt"))
    print(c.get_type("data/subset/test/pos/1_10.txt"))
    print(c.get_type("data/subset/test/pos/2_7.txt"))
    print(c.get_type("data/subset/test/pos/9_7.txt"))

    pos_paths = os.listdir("data/alle/test/pos")
    neg_paths = os.listdir("data/alle/test/neg")
    pos_cor = 0
    neg_cor = 0
    for path in pos_paths:
        if c.get_type("data/alle/test/pos/" + path) == True:
            pos_cor+=1

    for path in neg_paths:
        if c.get_type("data/alle/test/neg/" + path ) == False:
            neg_cor +=1



    print("pos %:  "+ str(pos_cor/len(pos_paths)))
    print("neg %:  "+ str(neg_cor/len(neg_paths)))
    print("total %: "+ str((neg_cor+pos_cor)/(len(pos_paths)+len(neg_paths))))

main()
