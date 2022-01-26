from bs4 import BeautifulSoup
import requests

main_url = "https://www.paginebianche.it/cerca-da-indirizzo?dv="

address = input("Inserisci l'indirizzo: ")
filename = address + ".txt"
filename = filename.replace(" ", "-")

csvfilename = filename.replace("txt", "csv")

address = address.replace(" ", "+")
address = address.replace("(", "%28")
address = address.replace(")", "%28")
main_url = main_url + address

req = requests.get(main_url)
soup = BeautifulSoup(req.text, "html.parser")

pages = []

for i in soup.findAll('p', attrs={'class':'listing-n-result'}):
    pages = i.findChildren('b')[0].text

pages = int(pages)
print("## Trovati " + str(pages) + " risultati...")
pages = (pages // 20) + 1

print("## Trovate " + str(pages) + " pagine...")

textFile = open(filename, "w")

csvFile = open(csvfilename, "w")
csvFile.write("N;Nome;Indirizzo1;Indirizzo2;CAP;Telefono\n")

num = 0

linePrinter = "------------------------------------"
print(linePrinter)
textFile.write(linePrinter)
textFile.write("\n")

linePrinter = "N - Nome\t\t\t-\t\t\tIndirizzo\t\t\t-\tTelefono"
print(linePrinter)
textFile.write(linePrinter)
textFile.write("\n")

linePrinter = "------------------------------------"
print(linePrinter)
textFile.write(linePrinter)
textFile.write("\n")

page = 1

while page <= pages:
    for div in soup.findAll('div', attrs={'class':'item_sx'}):
        num = num +1

        try:    
            linePrinter = str(num) + " - " + (div.find('a').contents[0]) + " - " + div.findChildren('span', attrs={'class':'street-address'})[0].text + " - " + div.findChildren('span', attrs={'class':'locality'})[0].text + " | " + div.findChildren('span', attrs={'class':'value'})[0].text
            csvFile.write(str(num)+ ";" + div.find('a').text + ";" + div.findChildren('span', attrs={'class':'street-address'})[0].text + ";" + div.findChildren('span', attrs={'class':'locality'})[0].text + ";" + div.findChildren('span', attrs={'itemprop':'postalCode'})[0].text + ";" + div.findChildren('span', attrs={'class':'value'})[0].text + "\n")
        except:
            linePrinter = str(num) + " - Errore di lettura dati"
            csvFile.write(str(num) + " - Errore di lettura dati\n")
        
        print(linePrinter)
        textFile.write(linePrinter)
        textFile.write("\n")
        print("\n")

    page = page +1
    main_url = main_url + "&p=" + str(page)
    req = requests.get(main_url)
    soup = BeautifulSoup(req.text, "html.parser")

textFile.close()
csvFile.close()
    
input("Premi un tasto per chiudere...")
