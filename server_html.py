from http.server import HTTPServer, BaseHTTPRequestHandler
import pymysql
from urllib.parse import urlparse, parse_qs

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
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        cur = conn.cursor()
        cur.execute("SELECT * FROM books;")
        data = cur.fetchall()
        i = """<a href="/insert">Add a book</a>"""
        self.wfile.write(bytes(str(i).encode()))
        table = """
        <html>
        <body>
        <table bgcolor = "black" width = "500">
        <tr bgcolor = "grey">
            <th width = "100">id</th>
            <th width = "100">title</th>
            <th width = "100">author</th>
            <th width = "100">price</th>
            <th width = "100">language</th>
        </tr>
        """
        for x in data:
                table += """
                <tr bgcolor = "lightgrey" align = "center">
                        <td> %s </td>
                        <td> %s </td>
                        <td> %s </td>
                        <td> %s </td>
                        <td> %s </td>
                        <td><a href="/delete?id=%s"><button>Delete</button></a></td>
                        <td><a href="/update?id=%s"><button>Update</button></a></td>
                </tr> 
                """ % (x[0], x[1], x[2], x[3], x[4], x[0], x[0])
        table += "</table> </body> </html>"
        self.wfile.write(bytes(str(table), "utf-8"))  
        if self.path == "/insert":
                formular = """
                <html>
                <body>
                <form action = "/insert" method = "POST">
                                
                                <label for="id">id: </label><br>
                                <input type="text" id="id" name="id"><br>
                                <label for="title">title:</label><br>
                                <input type="text" id="title" name="title"><br>
                                <label for="author">author: </label><br>
                                <input type="text" id="author" name="author"><br>
                                <label for="price">price:</label><br>
                                <input type="text" id="price" name="price"><br>
                                <label for="language">language: </label><br>
                                <input type="text" id="language" name="language"><br>
                                <input type="submit" value="Submit">
                </form>
                </body>
                </html>
                """
                self.wfile.write(bytes(str(formular), "utf-8"))
        if self.path.split("?")[0] == "/delete":
                split_1 = self.path.split("?")
                split_2 = split_1[1].split("=")
                id = split_2[1]
                cur = conn.cursor()
                cur.execute("DELETE FROM books WHERE id = %s" %id)
                conn.commit()
                i = """<a href="/get"><button>Book deleted succesfully!</button></a>"""
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(str(i).encode()))
        if self.path.split("?")[0] == "/update":
                split_1 = self.path.split("?")
                split_2 = split_1[1].split("=")
                id = split_2[1]
                cur = conn.cursor()
                cur.execute("SELECT * FROM books WHERE id = %s" % id)
                data = cur.fetchall()
                for x in data:
                        formular = """
                        <html>
                        <body>
                        <form action = "/update?id=%s" method = "POST">
                            <label for="title">title:</label><br>
                            <input type<"text" id= "title" name="title" value = %s><br>
                            <label for="author">author:</label><br>
                            <input type<"text" id= "author" name="author" value = %s><br>
                            <label for="price">price:</label><br>
                            <input type<"text" id= "price" name="price" value = %s><br>
                            <label for="language">language:</label><br>
                            <input type<"text" id= "language" name="language" value = %s><br>
                            <input type="submit" value="Submit">
                        </form>
                        </body>
                        </html>""" % (x[0], x[1], x[2], x[3], x[4])
                self.send_response(200)
                self.end_headers()
                self.send_header("Content-type", "text/html")
                self.wfile.write(bytes(str(formular).encode()))


     def do_POST(self):
        if self.path == "/insert":
                content_length = int(self.headers['Content-Length'])
                body_len = self.rfile.read(content_length)
                body = body_len.decode("utf-8")
                parsed_url = urlparse('?' + body)
                body = parse_qs(parsed_url.query)
                cur = conn.cursor()
                cur.execute("INSERT INTO books(id, title, author, price, language) VALUES('%s', '%s', '%s', '%s', '%s')" %(body['id'][0], body['title'][0], body['author'][0], body['price'][0], body['language'][0]))
                conn.commit()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                i = """<a href="/select"><button type = "button">Book added succesfully!</a>"""
                self.wfile.write(bytes(str(i).encode()))
        if self.path.split("?")[0] == "/update":
                split_1 = self.path.split("?")
                split_2 = split_1[1].split("=")
                id = split_2[1]
                content_length = int(self.headers['Content-Length'])
                body_len = self.rfile.read(content_length)
                body = body_len.decode("utf-8")
                parsed_url = urlparse('?' + body)
                body = parse_qs(parsed_url.query)
                cur = conn.cursor()
                cur.execute("UPDATE books SET title = '%s', author = '%s', price = '%s', language = '%s' WHERE id = %s" %(body["title"][0], body["author"][0], body["price"][0], body["language"][0], id))
                conn.commit()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                i = """<a href="/select"><button type = "button">Book updated succesfully</a>"""
                self.wfile.write(bytes(str(i).encode()))

server = HTTPServer((HOST, PORT), NeuralHTP)
print("Server now running...")
server.serve_forever()
server.server_close()
print("Server stopped!") 
