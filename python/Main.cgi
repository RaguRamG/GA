#!/Python27/python
print "Content-type: text/html"
print 
import random,cgi
import collections
import xlrd
from openpyxl import load_workbook
from Chromosome import Chromosome

form = cgi.FieldStorage()
param = []
param.append(form.getvalue("sec"))
param.append(form.getvalue("avail"))
param.append(form.getvalue("bpp"))
param.append(form.getvalue("cpm"))
param.append(form.getvalue("ram"))
param.append(form.getvalue("disk"))
param.append(form.getvalue("sc"))
param.append(form.getvalue("bw"))
param.append(form.getvalue("speed"))
param.append(form.getvalue("core"))


wb = load_workbook(filename = 'TabulatedSLA.xlsx') 
ws = wb['Sheet1']

data = []
userString = []
for i in range(4,14):
    data = []
    for j in range(2,len(ws.rows)):
        data.append(ws.cell(row=j,column=i).value)
        
    if param[i-4] == 0:
        userString.append(1)
    else:
        data.append(float(param[i-4])) 
        data.sort(reverse = True)
        userString.append(data.index(float(param[i-4])) + 1)

userString.append(1)

#userString = [1,2,3,4,5,6,7,8,9,10,1]

totalPopulation = 30
maxRank = 80
#userString = [1,2,3,4,5]
userChromosome = Chromosome(userString)
#print len(userChromosome.rankString)
initialPopulation = []
#print "Initializing Population"
for i in range(totalPopulation):
    initialPopulation.append(Chromosome(Chromosome.randomChromosomeString(maxRank,len(userChromosome.rankString))))

#print "Initial Population"
#Chromosome.printPopulation(initialPopulation)
for i in range(100):

    #print "ITERATION ",i
    nextPopulation = []
    initialPopulation = Chromosome.rouletteSelection(initialPopulation,userChromosome)
    #print "Undergoing Elitism"

    #print "Best Four Chromosomes in Gen",i+1
    for i in range(4):
        index = Chromosome.getFittestChromosome(initialPopulation)
        nextPopulation.append(initialPopulation[index])
        #print initialPopulation[index].rankString , "<br/>"
        initialPopulation.pop(index)

    #print "Undergoing Crossover and Mutation"

    for i in range(totalPopulation/2 - 2):

        firstParentIndex = random.randrange(0,len(initialPopulation),1)
        firstParent = initialPopulation[firstParentIndex]
        initialPopulation.pop(firstParentIndex)

        secondParentIndex = random.randrange(0,len(initialPopulation),1)
        secondParent = initialPopulation[secondParentIndex]
        initialPopulation.pop(secondParentIndex)

        result = Chromosome.crossover(firstParent,secondParent)
        result[0].mutate(maxRank)
        result[1].mutate(maxRank)

        nextPopulation = nextPopulation + result
    initialPopulation = nextPopulation
finalPopulation = Chromosome.calculateProbability(initialPopulation,userChromosome)
#print "Final Population"
#Chromosome.printPopulation(finalPopulation)
#print "--------"
#print "Best Chromosome : ", finalPopulation[Chromosome.getFittestChromosome(finalPopulation)].rankString

bestChromosome = finalPopulation[Chromosome.getFittestChromosome(finalPopulation)]

#print bestChromosome.rankString,"<br>"

book = xlrd.open_workbook("TabulatedSLA.xlsx")
sheet = book.sheet_by_index(1)
s1 = book.sheet_by_index(0)
dist = {}
dists = {}
for i in range(1,sheet.nrows):
    row = []
    for j in range(3,14):
        row.append(sheet.cell(i,j).value)
    rowChromosome = Chromosome(row)
    dist[i] = Chromosome.distance(bestChromosome,rowChromosome)

for i in range(1,sheet.nrows):
    row = []
    for j in range(3,14):
        row.append(sheet.cell(i,j).value)
    rowChromosome = Chromosome(row)
    dists[i] = Chromosome.distance(userChromosome,rowChromosome)


    #print bestChromosome.rankString
    

b = collections.OrderedDict(sorted(dist.items(), key = lambda temp: temp[1],reverse=False))
c = collections.OrderedDict(sorted(dists.items(), key = lambda temp: temp[1],reverse=False))
print "<html><head><link rel='stylesheet' href='http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css'><link rel='stylesheet' href='../css/index.css'><script src='https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js'></script><script src='http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js'></script><script src='js/index.js'></script></head><body>" 
print "<div class='container-fluid'>"


l1 = []
l2 = []

j = 0
for key in b:
    if j >= 5:
        break
    l1.append(key)
    j = j + 1

j = 0
for key in c:
    if j >= 5:
        break
    l2.append(key)
    j = j + 1

final1 = list((set(l1)-set(l2)))
final2 = list((set(l2)-set(l1)))

n1 = {}
n2 = {}

for i in range(len(final1)):
    n1[final1[i]] = b[final1[i]]
    n2[final2[i]] = c[final2[i]]

f1 = collections.OrderedDict(sorted(n1.items(), key = lambda temp: temp[1],reverse=False))
f2 = collections.OrderedDict(sorted(n2.items(), key = lambda temp: temp[1],reverse=False))

dis = 0

for i in range(len(f1)):
    dis += (f1.items()[i][1] - f2.items()[i][1]) ** 2

sqrdis = (dis ** 0.5 )* (float(len(f1))/5.0)

'''print "<h1>",sqrdis,"</h1>"

#writing to file(input)
target = open("input5.txt", 'a')
target.write(str(sqrdis))
target.write("\n")
target.close()
'''
i = 0
print "<h2>GA OUTPUT</h2>"
for key,value in b.items():
    i = i + 1
    #for j in range(1,13):
    #print key,"<br>"
    print "<div style='border:1px dotted black;padding:6px;border-radius:10px;'>"
    print "<h2 style='font-family:Arial;'>",i,".<u>",s1.cell(key,2).value,"</u></h2>"
    print "<p><b>Service Name:</b>",s1.cell(key,1).value,"</p>"
    print "<p><b>Availability:</b>",s1.cell(key,4).value*100,"%</p>"
    print "<p><b>Service Credit:</b>",s1.cell(key,9).value*100,"%</p>"
    print "<p><b>Base Plan Price:</b>",s1.cell(key,5).value,"$/hr</p>"
    print "<p><b>RAM:</b>",s1.cell(key,7).value,"MB</p>"
    print "<p><b>Disk Space:</b>",s1.cell(key,8).value,"GB</p>"
    print "<p><b>Virtual CPU Cores:</b>",s1.cell(key,12).value,"vCPU(s)</p>"
    print "</div>"
    print "<br>"
    if i == 5:
        break 

i = 0
print "<h2>Direct Search</h2>"

for key,value in c.items():
    i = i + 1
    #for j in range(1,13):
    print "<div style='border:1px dotted black;padding:6px;border-radius:10px;'>"
    print "<h2 style='font-family:Arial;'>",i,".<u>",s1.cell(key,2).value,"</u></h2>"
    print "<p><b>Service Name:</b>",s1.cell(key,1).value,"</p>"
    print "<p><b>Availability:</b>",s1.cell(key,4).value*100,"%</p>"
    print "<p><b>Service Credit:</b>",s1.cell(key,9).value*100,"%</p>"
    print "<p><b>Base Plan Price:</b>",s1.cell(key,5).value,"$/hr</p>"
    print "<p><b>RAM:</b>",s1.cell(key,7).value,"MB</p>"
    print "<p><b>Disk Space:</b>",s1.cell(key,8).value,"GB</p>"
    print "<p><b>Virtual CPU Cores:</b>",s1.cell(key,12).value,"vCPU(s)</p>"
    print "</div>"
    print "<br>"
    if i == 5:
        break 


print "</div>"
print "</body></html>"
