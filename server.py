import socket
from _thread import *
from email.utils import formatdate


ThreadCount = 0


def ourserver(conn, threadcount):

  print("Starting Thread Number " + str(threadcount))


  data = conn.recv(8192)


  if not data:
   print("No data")
  else:

   print("DATA IS: " + str(data))


   msg = data.decode()

   msglines = msg.splitlines()

   msgfl = msglines[0].split(' ');

   resour = msgfl[1];


   if resour == '/':
     resour = '/index.html'


   cresour = resour

   resour = "./DATA/" + resour
 

   headers = ""

   headers = headers + "Date: " + formatdate(timeval=None, localtime=False, usegmt=True) + "\n"

   headers = headers + "Content-type: text/html; charset=UTF-8\n"

   headers = headers + "Server: Our brand new Python Web Server\n"

   headers = headers + "Connection: close\n"


   try:
       myfile = open(resour, "r")

       data = myfile.read()

       datasize = len(data.encode())

       headers = headers + "Content-Length: " + str(datasize) + "\n"

       resp = "HTTP/1.1 200 OK\n" + headers + "\n\n" + data

       myfile.close()
   except IOError:

       resp = "HTTP/1.1 404 Not Found\n" + headers + "\n\n" + "FILE " + cresour + " WAS NOT FOUND!"


   conn.sendall(resp.encode())


  print("Closing Thread Number " + str(threadcount) + "\n")
  conn.close()


sock = socket.socket()
sock.bind(('', 8080))
sock.listen(5)


while True:
 # Если нашлось подключение
 conn, addr = sock.accept()
 print("Connected", addr)
 # Плюс один поток
 ThreadCount += 1
 # Запускаем обработчик потока
 start_new_thread(ourserver, (conn,ThreadCount))

# Закрываем сокет. Этого никогда не случится, так как цикл выше бесконечный
sock.close()
