import random
import numpy as np
import copy
import sys
import csv

#deklarowanie potrzebych dla symulacji list i zmienncyh
frames = list()
amount_of_series = 0
amount_of_references = 0
amount_of_pages = 0
data = list()
resultsFIFO = list()
resultsLRU = list()

#Ustawianie ziarna random
random.seed(9999)


#funkcja która generuje ciąg liczb potrzenych dla pomiarów i wpisuje je do pliku tekstowego
def generator(path):
    file = open(path, 'w')
    for i in range(amount_of_series):
        for j in range(amount_of_references):
            file.write(str(random.randint(0, amount_of_pages)))
            file.write('\n')
    file.close()

#funkcja który wczytuje dane potrzebne dla eksperymentów z pliku tekstowego
def readData(path):
    file = open(path, 'r')
    for i in range(amount_of_series):
        data.append(list())
        for j in range(amount_of_references):
            line = file.readline()
            data[i].append(int(line))
    file.close()


#Funckja symulacyjna FIFO.
def FIFO(amount_of_references, Data, frames):
    queue = []
    faults = 0
    for reference in Data:
        print("Potrzebuje: " + str(reference))
        if queue: #Jeżeli mamy elementy w lisćie queue to:
            if reference in queue:
                print("Nie ma błędów")
                pass
            elif len(queue) < frames:
                queue.append(reference)
                faults += 1
                print("Wystąpił błąd")
            else:
                #Usuwujemy pierwszy element z listy queue i dodajemy nowy element na koniec
                for j in range(frames-1):
                    queue[j] = queue[j+1]
                queue[frames-1] = reference
                print("Wystąpił błąd")
                faults += 1
        else: #Jeśli lista jest pusta to dodajemy pierwsze element
            queue.append(reference)
            faults += 1
            print("Wystąpił błąd")
        print("Ramki pamięci: " + str(queue))
    return faults

#Funkcja symulacyjna LRU.
def LRU(amount_of_references, Data, frames):
    queue = []
    faults = 0
    for reference in Data:
        print("Potrzebuje: " + str(reference))
        if queue:
            if reference in queue:
                print("Nie ma błądu")
                id = queue.index(reference)
                #przemosimy potrzebny element na koniec listy
                queue.pop(id)
                queue.append(reference)
            elif len(queue) < frames:
                queue.append(reference)
                faults += 1
                print("Wystąpił błąd")
            else:
                for j in range(frames - 1):
                    queue[j] = queue[j + 1]
                queue[frames - 1] = reference
                print("Wystąpił błąd")
                faults += 1
        else:
            queue.append(reference)
            faults += 1
            print("Wystąpił błąd")
        print("Ramki pamięci: " + str(queue))
    return faults

#Funkcja zapisująca wyniki do pliku csv
def write_to_csv(path, algoritm, List, Serie, Ilość_ramek):
    file = open(path, 'w', newline='')
    header = ["Seria", "Ilość błędów"]
    csv_writer = csv.writer(file)
    csv_writer.writerow([algoritm])
    for i in range(Ilość_ramek):
        csv_writer.writerow(["Ramki: ", frames[i]])
        csv_writer.writerow(header)
        for j in range(Serie):
            csv_writer.writerow([j+1, List[i][j]])
        csv_writer.writerow(["Średnia: ", np.mean(List[i])])
    file.close()


#program główny
if __name__=="__main__":
    while True:
        amount_of_frames = int(input("Wpisz ilość ramek pamięci na których będą przeprowadzane testy: "))
        for i in range(amount_of_frames):
            frames.append(int(input("Wpisz " + str(i+1) + " bramkę pamięci: ")))
        print(frames)
        amount_of_references = int(input("Wpisz ilość odłowań do pamięci w czasie jednej serii testu: "))
        amount_of_series = int(input("Wpisz ilość serii testów: "))
        amount_of_pages = int(input("Wpisz ilość stron pamięci: "))

        generator("data.txt")
        readData("data.txt")
        CopyforFIFO = copy.deepcopy(data)
        CopyforLRU = copy.deepcopy(data)

        sys.stdout = open("output.txt", 'w')

        print("_________________FIFO____________________________")
        for i in range(amount_of_frames):
            resultsFIFO.append(list())
            for j in range(amount_of_series):
                print("Seria: " + str(j+1))
                resultsFIFO[i].append(FIFO(amount_of_references, CopyforFIFO[j], frames[i]))


        print("_________________LRU____________________________")
        for i in range(amount_of_frames):
            resultsLRU.append(list())
            for j in range(amount_of_series):
                print("Seria: " + str(j + 1))
                resultsLRU[i].append(LRU(amount_of_references, CopyforLRU[j], frames[i]))
        sys.stdout.close()
        sys.stdout = sys.__stdout__

        write_to_csv("FIFO.csv", "FIFO", resultsFIFO, amount_of_series, amount_of_frames)
        write_to_csv("LRU.csv", "LRU", resultsLRU, amount_of_series, amount_of_frames)
