import requests

class customer:
    def __init__(self, customerNumber, customerName, contactLastName, contactFirstName, phone, addressLine1, addressLine2, city, state, postalCode, country, salesRepEmployeeNumber, creditLimit):
        self.customerNumber = customerNumber
        self.customerName = customerName
        self.contactLastName = contactLastName
        self.contactFirstName = contactFirstName
        self.phone = phone
        self.addressLine1 = addressLine1
        self.addressLine2 = addressLine2
        self.city = city
        self.state = state
        self.postalCode = postalCode
        self.country = country
        self.salesRepEmployeeNumber = salesRepEmployeeNumber





class orders:
    def __init__(self, orderNumber, orderDate, requieredDate, shippedDate, status, comments, customerNumber):
        self.orderNumber = orderNumber
        self.orderDate = orderDate
        self.requiredDate = requieredDate
        self.shippedDate = shippedDate
        self.status = status
        self.comments = comments
        self.customerNumber = customerNumber



req = requests.get('http://localhost:8080/customers')

l = req.text.split("\n")

custList = []

for x in l:
    if(x != ""):
        if(x != "\t"):
            custList.append(x.split(": "))

i = 0
cust = []

while(i < len(custList)):
    cust.append(customer(custList[i][1], custList[i+1][1], custList[i+2][1], custList[i+3][1], custList[i+4][1], custList[i+5][1], custList[i+6][1], custList[i+7][1], custList[i+8][1], custList[i+9][1], custList[i+10][1], custList[i+11][1], custList[i+12][1]))
    i += 13



req_2 = requests.get('http://localhost:8080/orders')

l_2 = req_2.text.split("\n")

ordList = []

for x in l_2:
    if(x != ""):
        if(x != "\t"):
            ordList.append(x.split(": "))


j = 0
ord = []

while(j < len(ordList)):
    ord.append(orders(ordList[j][1], ordList[j+1][1], ordList[j+2][1], ordList[j+3][1], ordList[j+4][1], ordList[j+5][1], ordList[j+6][1]))
    j += 7


import pymysql

conn = pymysql.connect(
    host = 'localhost',
    user = 'beni',
    password = 'ionescubeni',
    database = 'classicmodels'
)

cur = conn.cursor()
y = 0

try:
   
    cur.execute("INSERT INTO customers(customerNumber, customerName, contactLastName, contactFirstName, phone, addressLine1, addressLine2, city, state, postalCode, country, salesRepEmployeeNumber, creditLimit) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (custList[y+13][1], custList[y+14][1], custList[y+15][1], custList[y+16][1], custList[y+17][1], custList[y+18][1], custList[y+19][1], custList[y+20][1], custList[y+21][1], custList[y+22][1], custList[y+23][1], custList[y+24][1], custList[y+25][1]))
    conn.commit()
except:
    if(len(custList[y+14][1]) > 50 and len(custList[y+15][1]) > 50 and len(custList[y+16][1]) > 50 and len(custList[y+17][1]) > 50 and len(custList[y+18][1]) > 50 and len(custList[y+19][1]) > 50 and len(custList[y+20][1]) > 50 and len(custList[y+21][1]) > 50 and len(custList[y+23][1]) > 50):
        print("Sirul introdus este prea lung. Va rugam sa introduceti un sir mai mic de 50 de caractere")
    elif(len(custList[y+22][1]) > 15):
        print("Sirul introdus este prea lung. Va rugam sa introduceti un sir mai mic de 15 caractere")
    elif(len(custList[y+25][1]) > 1000000000):
        print("Numarul introdus este prea mare. Va rugam sa introduceti un numar de cel mult 10 cifre")



conn.close()
