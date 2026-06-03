from http.server import HTTPServer, BaseHTTPRequestHandler
import pymysql
import json

HOST = "localhost"
PORT = 8000

conn = pymysql.connect(
        host='localhost',
        user='beni', 
        password = "ionescubeni",
        db='beni_postman',
        )

class NeuralHTP(BaseHTTPRequestHandler):
     def do_GET(self):
        if(self.path == '/'):
            cur = conn.cursor()
            cur.execute("SELECT * FROM books")
            data = cur.fetchall()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(str(data), "utf-8"))
        else:
            split_1 = self.path.split("?")
            split_2 = split_1[1].split("=")
            id = split_2[1]
            cur = conn.cursor()
            cur.execute("SELECT * FROM books where id = %s", id)
            data = cur.fetchall()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(str(data), "utf-8")) 
        

     def do_POST(self):
                content_length = int(self.headers['Content-Length'])
                body_len = self.rfile.read(content_length)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                data = body_len.decode("utf-8")
                body = json.loads(data)
                cur = conn.cursor()
                cur.execute("INSERT INTO books(id, title, author, price, language) VALUES('%s', '%s', '%s', '%s', '%s')" %(body['id'], body['title'], body['author'], body['price'], body['language']))
                conn.commit()

     def do_DELETE(self):
                cur = conn.cursor()
                cur.execute("SELECT id FROM books;")
                id_db = cur.fetchall()
                print(id_db)
                split_1 = self.path.split("?")
                split_2 = split_1[1].split("=")
                id = split_2[1]
                ok = False
                l = list(id_db)
                lista = []
                for i in l:
                        lista.append(list(i))
                for elem in lista:
                        for x in elem:
                                if id == str(x):
                                        ok = True
                if split_1[1] and ok == True and split_2[0] == "id":
                        cur = conn.cursor()
                        cur.execute("DELETE FROM books WHERE id = %s" %id)        
                        conn.commit()
                else:
                        self.send_response(404)
                        print(self.path)
                        print("Make sure the querystring is written corectly")
                self.send_response(200)
                self.send_header("Content-type", "aplication/json")
                self.end_headers()
                
                

     def do_PUT(self):
                cur = conn.cursor()
                cur.execute("SELECT id FROM books;")
                id_db = cur.fetchall()
                print(id_db)
                split_1 = self.path.split("?")
                split_2 = split_1[1].split("=")
                id = split_2[1]
                ok = False
                l = list(id_db)
                lista = []
                for i in l:
                        lista.append(list(i))
                for elem in lista:
                        for x in elem:
                                if id == str(x):
                                        ok = True
                if ok == True:
                        content_length = int(self.headers['Content-Length'])
                        body_len = self.rfile.read(content_length)
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        data = body_len.decode("utf-8")
                        body = json.loads(data)
                        cur.execute("UPDATE books SET title = '%s', author = '%s', price = '%s', language = '%s' WHERE id = %s" %(body["title"], body["author"], body["price"], body["language"], id))
                        conn.commit()
                else:
                        self.send_response(404)
                        print("Make sure the querystring is written corectly")

server = HTTPServer((HOST, PORT), NeuralHTP)
print("Server now running...")
server.serve_forever()
server.server_close()
print("Server stopped!")  
