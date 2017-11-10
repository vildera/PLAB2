#representerer aksjonen som velges (eks. spille stein)
import random
import matplotlib.pyplot as plt
__author__ = "Vilde Arntzen"
class Aksjon:

    def __init__(self, action):
        self.action = action #0 = stein, 1 = saks, 2 = papir

    #equals
    def __eq__(self,other):
        return self.action == other.action #må kanskje caste?

    #greater than
    def __gt__(self,other):
        a = {0:2,1:0,2:1}             #value slår key
        return a[self.action] != other.action

    def __str__(self):
        ordliste = ["Stein","Saks","Papir"]
        return ordliste[self.action]

    def getAksjon(self):
        return self.action


#brukes for å gjennomføre et spill
#class EnkeltSpill:



class Spiller:

    #Dict for å legge inn trekk (value) til hver spiller (key)
    spiller_valg = {}
    trekk = {0:"Stein",1:"Saks",2:"Papir"}


    def __init__(self,spiller):
        self.spiller_navn = spiller
        Spiller.spiller_valg[self] = []

    def velg_aksjon(self, motstander):
        return


    def motta_resultat(self,motstander,trekk): #tar inn motstanders trekk
        Spiller.spiller_valg[motstander].append(trekk)

    def oppgi_navn(self,navn):
        return self.spiller_navn


    def __str__(self):
        return self.spiller_navn







class Tilfeldig(Spiller):

    def __init__(self,spiller_navn):
        Spiller.__init__(self,spiller_navn)

    def velg_aksjon(self, motstander):
       return Aksjon(random.randint(0,2))




class Sekvensiell(Spiller):

    def __init__(self, spiller_navn):
        Spiller.__init__(self,spiller_navn)
        self.a = 0


    def velg_aksjon(self,motstander):
        aksjon = Aksjon(self.a%3)
        self.a += 1
        return aksjon




class MestVanlig(Spiller):

    def __init__(self, spiller_navn):
        Spiller.__init__(self,spiller_navn)

    def velg_aksjon(self, motstander):
        antall_trekk =[0,0,0]

        for trekk in Spiller.spiller_valg[motstander]:
            antall_trekk[trekk.getAksjon()]+=1

        if antall_trekk != [0,0,0]:
            return Aksjon(motsatte_trekk(antall_trekk.index(max(antall_trekk))))

        else: return Aksjon(random.randint(0,2))




def motsatte_trekk(num):
    a = {0: 2, 1: 0, 2: 1}
    return a[num]


class Historiker(Spiller):

    def __init__(self, spillernavn, husk):
        Spiller.__init__(self,spillernavn)
        self.husk = husk

    def velg_aksjon(self, motstander):
        historie = Spiller.spiller_valg[motstander]

        subsequence = historie[-self.husk:]

                #stein, saks, papir
        antall_aksjoner = [0,0,0]


        for i in range(len(historie)- self.husk): #minus husk fordi vi må stoppe når vi har de husk-siste elementene i listen
             #sjekker om det finnes en subsequence som er lik denne subsequencen med lengde husk - slice tar ikke med siste element - ikke med self.huskz
            if historie[i:i+self.husk] == subsequence:
                antall_aksjoner[historie[i+self.husk].getAksjon()] +=1 #øker indeksen til subsequencen som var lik en subsequence i historie med lengde hsuk


        if antall_aksjoner != [0,0,0]:
            return Aksjon(motsatte_trekk(antall_aksjoner.index(max(antall_aksjoner)))) #returnerer motsat av det som forekommer mest

        # Kan legge inn tilfelle når f.eks like mange stein som saks, men ikke papir, men her returnerer den første "størst" i listen
        return Aksjon(random.randint(0,2))



class MangeSpill:


    def __init__(self,spiller1, spiller2, antall_spill):
        self.spiller1 = spiller1
        self.spiller2 = spiller2
        self.antall_spill = antall_spill
        self.resultat = [0,0]
        self.gevinstprosent = [0,0]





    def arranger_enkeltspill(self):
        enkeltspill = EnkeltSpill(self.spiller1,self.spiller2)
        enkeltspill.gjennomfoer_spill()
        print(enkeltspill)
        return enkeltspill.poeng

    def arranger_turnering(self):
        #antall spill gjort
        x_akse = []


        #prosentandel i gevinst
        y_akse = []

        spill_gjennomfoert = 0





        for spill in range(self.antall_spill):
            spill_gjennomfoert += 1
            poeng = self.arranger_enkeltspill()
            self.resultat[0]= self.resultat[0]+ poeng[0]
            self.resultat[1] = self.resultat[1] + poeng[1]
            self.gevinstprosent[0] = self.resultat[0]/spill_gjennomfoert
            self.gevinstprosent[1] = self.resultat[1]/spill_gjennomfoert


            #PYPLOT

            x_akse.append(spill_gjennomfoert)
            y_akse.append(self.gevinstprosent[0])


        #PYPLOT
        plt.plot(x_akse,y_akse)
        plt.axis([0,self.antall_spill,0,1]) #x-aksen går fra 0 til antall spill + sannsynligheten går fra 0 til 1
        plt.grid(True)
        plt.axhline(y=0.5,linewidth =0.5, color="m")
        plt.xlabel("Antall spill")
        plt.ylabel("Gevinstprosent for" + str(self.spiller1))
        plt.show()

        print("\nTotal score i turneringen:\n" + str(self.spiller1) + ": " + str(self.resultat[0]) + " poeng" +
              "\n" + str(self.spiller2) + ": " + str(self.resultat[1]) + " poeng")










#spørre aksjon, sjekke vinner, rapportere valg og resultater + tekstuell beskrivelse
class EnkeltSpill:

    # lager et enkeltspill for to eksisterende spillere
    def __init__(self, spiller1, spiller2):
        self.spiller1 = spiller1
        self.spiller2 = spiller2
        self.poeng = [0,0]
        self.vinner =""

    def gjennomfoer_spill(self):
        self.action1 = self.spiller1.velg_aksjon(self.spiller2)
        self.action2 = self.spiller2.velg_aksjon(self.spiller1)

        if self.action1 == self.action2:
            self.poeng = [0.5,0.5]
            self.vinner += "Uavgjort"

        elif self.action1 > self.action2:
            self.poeng = [1,0]
            self.vinner += ""+str(self.spiller1)+" vinner"
        elif self.action2 > self.action1:
            self.poeng = [0,1]
            self.vinner += ""+str(self.spiller2)+" vinner"

        self.spiller1.motta_resultat(self.spiller2, self.action2)
        self.spiller2.motta_resultat(self.spiller1, self.action1)



    def __str__(self):
        rapport = str(self.spiller1)+": " + str(self.action1)+".   " + str(self.spiller2)+":  "+ str(self.action2)+".  --> "+str(self.vinner)
        return rapport





def main():
    spiller1= Tilfeldig("Henrik")
    spiller2 = Sekvensiell("Robert")
    spiller3 = Historiker("Vilde",2)
    spiller4 = MestVanlig("Ingeborg")


    spill2 = MangeSpill(spiller3,spiller4,100)
    spill2.arranger_turnering()
    print(spill2)



main()



