from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import random
import ast

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.server = server

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.server.nword = self.get_new_word()
        self.server.c_left = 10
        self.server.g_word_list = ['-' for i in range(0, len(self.server.nword))]
        self.server.g_letters = []
        self.server.e_message = '  Start guessing. ' + str(self.server.c_left) + \
                ' Chances left.'
        #return jsonify({'word':''.join(self.g_word_list), 'message':self.e_message})
        response = BytesIO()
        response.write(b'New Word: ')
        response.write(bytes(''.join(self.server.g_word_list), 'utf-8'))
        response.write(bytes(self.server.e_message,'utf-8'))
        self.wfile.write(response.getvalue())

    def get_new_word(self):
        with open('nm_names.txt') as f:
            movie_list_str = f.read()
            movie_list = movie_list_str.split('\n')
        print("list length = ", len(movie_list))

        index = random.randint(0, len(movie_list))
        print ("index = ", index)
        print ("movie_list[index] = ", movie_list[index])
        return movie_list[index].lower()

    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(content_length)
        user_guess_str = put_data.decode('utf-8')
        #print ('user_guess = ', user_guess)
        user_guess = ast.literal_eval(user_guess_str)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()

        if self.server.c_left == 0:
            response.write(b'GAME OVER.RESTART THE GAME.')    
            self.wfile.write(response.getvalue())
            return

        self.server.c_left -= 1

        if len(user_guess['letter']) > 1:
            self.server.e_message = ' You can guess only one letter a time. '+ \
                    str(self.server.c_left) + ' Guesses left'
            response.write(bytes(''.join(self.server.g_word_list),'utf-8'))
            response.write(bytes(self.server.e_message,'utf-8'))
            self.wfile.write(response.getvalue())
            return

        if not user_guess['letter'].isalpha():
            self.server.e_message = ' You pressed Non-Alphabet. '+ \
                    str(self.server.c_left) + ' Guesses left.'
            response.write(bytes(''.join(self.server.g_word_list),'utf-8'))
            response.write(bytes(self.server.e_message,'utf-8'))
            self.wfile.write(response.getvalue())
            return

        if user_guess['letter'].lower() in self.server.g_letters:
            self.server.e_message = ' You already guessed this alphabet. '+ \
                    str(self.server.c_left) + ' Guesses left'
            response.write(bytes(''.join(self.server.g_word_list),'utf-8'))
            response.write(bytes(self.server.e_message,'utf-8'))
            self.wfile.write(response.getvalue())
            return

        self.server.g_letters.append(user_guess['letter'].lower())
        if user_guess['letter'].lower() in self.server.nword:
            for i in range(0, len(self.server.nword)):
                if self.server.nword[i] == user_guess['letter'].lower():
                    self.server.g_word_list[i] = user_guess['letter'].lower()
            
            if '-' not in self.server.g_word_list:
                self.server.e_message = 'YOU WON !!!'
                self.server.c_left = 0
                response.write(bytes(''.join(self.server.g_word_list),'utf-8'))
                response.write(bytes(self.server.e_message,'utf-8'))
                self.wfile.write(response.getvalue())
            else:
                if self.server.c_left == 0:
                    self.server.e_message = 'Sorry You LOST !! Correct word was: '+ \
                            self.server.nword
                else:
                    self.server.e_message = 'correct_guess.' + \
                            str(self.server.c_left) + ' Guesses left'
                response.write(bytes(''.join(self.server.g_word_list),'utf-8'))
                response.write(bytes(self.server.e_message, 'utf-8'))
                self.wfile.write(response.getvalue())
        else:
            if self.server.c_left == 0:
                self.server.e_message = 'Sorry You LOST !! Correct word was: ' + \
                        self.server.nword
            else:
                self.server.e_message = 'Incorrect guess. ' + \
                        str(self.server.c_left) + ' Guesses left.'

            response.write(bytes(''.join(self.server.g_word_list),'utf-8'))
            response.write(bytes(self.server.e_message,'utf-8'))
            self.wfile.write(response.getvalue())

        #response.write(bytes(''.join(self.server.g_word_list),'utf-8'))
        #self.wfile.write(response.getvalue())


class MyServer(HTTPServer):
    def __init__(self, server_address, request_handler):
        super().__init__(server_address, request_handler)
        self.nword = None
        self.c_left = 0
        self.g_word_list = []
        self.g_letters = []
        self.e_message = None

httpd = MyServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()

