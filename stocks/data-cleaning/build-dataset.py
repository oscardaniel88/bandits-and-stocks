import os
from datetime import date, timedelta
from time import strftime

directory = 'new-stocks'
startDate = date(2014, 1, 2)
endDate = date(2018, 5, 15)
outputFilename = 'new-stocks.csv'

def daterange(startDate, endDate):
   for n in range(int((endDate - startDate).days)):
      theDate = endDate - timedelta(n)
      weekday = int(theDate.strftime("%w"))
      if weekday % 6 == 0: # no tomamos en cuenta fines de semana
         continue

      yield theDate.strftime("%d").lstrip('0') + theDate.strftime("-%b-%y")


def flatten(L):
   return [x for row in L for x in row]

stocks = {}

for filename in os.listdir(directory):
   if filename[-3:] != 'csv':
      continue

   print(filename)
   tickerSymbol = filename.split('.')[0]

   with open(directory + '/' + filename, 'r') as infile:
      infile.readline()
      lines = infile.readlines()

   for (i, line) in enumerate(lines):
      (date, openPrice, highPrice, lowPrice, closePrice, volume) = line.split(',')
      if int(volume) == 0:
         cp = float(closePrice)
         lines[i] = (date, cp, cp, cp, cp, 0)
      else:
         lines[i] = (date, float(openPrice), float(highPrice), float(lowPrice), float(closePrice), int(volume))

   print("%d total entradas" % len(lines))
   print("%d dias con volumen cero." % (len([x for x in lines if x[-1] == 0])))

   print("")

   stocks[tickerSymbol] = lines


# Alineamos las acciones en una sola tabla indexada por fecha
counters = [0] * len(stocks)
maxNumEntries = max(len(stocks[k]) for k in stocks) # 1271
newTable = []
i = 0
symbols = sorted(stocks.keys())
numMissing = 0

for theDate in daterange(startDate, endDate):
   newRow = [theDate]

   column = 1
   for i, ticker in enumerate(symbols):
      counter = counters[i]
      stockRow = stocks[ticker][counter]

      if stockRow[0] == theDate:
         newRow.append(stockRow[1])
         newRow.append(stockRow[4])
         counters[i] += 1
      else:
         print("Entrada faltante: %r" % ((stockRow, theDate, ticker),))
         newRow.append(newTable[-1][column])
         newRow.append(newTable[-1][column+1])
         numMissing += 1

      column += 2

   newTable.append(newRow)


print("filas faltantes: %d" % numMissing)
headerRow = ['Date'] + flatten([[ticker + '-open', ticker + '-close'] for ticker in symbols])
newTable = [headerRow] + newTable

with open(outputFilename, 'w') as outfile:
   for row in newTable:
      outfile.write(','.join([str(x) for x in row]) + '\n')
