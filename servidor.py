import socket
from tkinter import *
import threading 
lista_clientes = []

class Aplicacao():
    def __init__(self):
        self.janela = Tk()
        self.tela()
        self.frames_tela()
        self.atributos_f1()
        self.atributos_f2()
        self.ip_Servidor()
        self.janela.mainloop()
        
    def tela(self):
        self.janela.title("SASUKE-Servidor")
        self.janela.configure(background="#212C33")
        self.janela.geometry("600x450")
        self.janela.resizable(False, False)
        self.janela.iconbitmap("icone.ico")

    def frames_tela(self):
        self.frame_1 = Frame(self.janela, bd=4, bg="white", highlightbackground="#5DB3A3", highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.45)

        self.frame_2 = Frame(self.janela, bd=4, bg="white", highlightbackground="#5DB3A3", highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.45)

    def atributos_f1(self):
        self.lb_ip = Label(self.frame_1, text="Seu Ip")
        self.lb_ip.place(relx=0.1, rely=0.1)
        self.lb_ipserv = Label(self.frame_1, text="", bg="#E6EAFF", highlightbackground="#1D1D1D", highlightthickness=1)
        self.lb_ipserv.place(relx=0.1, rely=0.2)

        self.lb_porta = Label(self.frame_1, text="PORTA")
        self.lb_porta.place(relx=0.6, rely=0.40)
        self.porta_entry = Entry(self.frame_1, bg="#E6EAFF")
        self.porta_entry.place(relx=0.6, rely=0.50, relwidth=0.3)

        self.lb_num = Label(self.frame_1, text="Escolha um número de 0 a 10", bg="white")
        self.lb_num.place(relx=0.1, rely=0.40)
        self.num_entry = Entry(self.frame_1, bg="#E6EAFF")
        self.num_entry.place(relx=0.1, rely=0.50, relwidth=0.3)

        self.bt_conc = Button(self.frame_1, text="Conectar", command=self.start)
        self.bt_conc.place(relx=0.1, rely=0.8, relwidth=0.10, relheight=0.15)

        self.bt_envia = Button(self.frame_1, text="Enviar", command=self.envia)
        self.bt_envia.place(relx=0.5, rely=0.8, relwidth=0.10, relheight=0.15)

        
        self.lb_status = Label(self.frame_1, text="", bg="white",foreground="green")
        self.lb_status.place(relx=0.8, rely=0.01)
        self.lb_status.config(text="Servidor desligado!",foreground="red")
    def atributos_f2(self):
        self.lb_aviso = Label(self.frame_2, text="", bg="white",foreground="red")
        self.lb_aviso.place(relx=0.1, rely=0.4)

        self.lb_resposta = Label(self.frame_2, text="", bg="white")
        self.lb_resposta.place(relx=0.1, rely=0.5)

        self.lb_ligado = Label(self.frame_2, text="", bg="white",foreground="green")
        self.lb_ligado.place(relx=0.8, rely=0.8)

    def limpa_lb_resposta(self):
        self.lb_resposta.config(text="")
    def mostrar_mensagem_temporaria_resposta(self, mensagem, tempo):
        self.lb_resposta.config(text=mensagem)
        self.janela.after(tempo, self.limpa_lb_resposta)
    
    def limpa_lb_aviso(self):
        self.lb_aviso.config(text="")
    def mostrar_mensagem_temporaria_aviso(self, mensagem, tempo):
        self.lb_aviso.config(text=mensagem)
        self.janela.after(tempo, self.limpa_lb_aviso)

    def limpa_lb_ligado(self):
        self.lb_ligado.config(text="")
    def mostrar_mensagem_temporaria_ligado(self, mensagem, tempo):
        self.lb_ligado.config(text=mensagem)
        self.janela.after(tempo, self.limpa_lb_ligado)
    
    def start(self):
        comeca=threading.Thread(target=self.serv)
        comeca.start()
    
    def envia(self):
        for client in lista_clientes:
            thread1 = threading.Thread(target=self.mandaMSRV, args=[client])
            thread1.start()
    
    def ip_Servidor(self):
        servidor = socket.gethostbyname(socket.gethostname())
        self.lb_ipserv.config(text=servidor)


    
    def serv(self):
        porta = self.porta_entry.get()
        if not porta:
            self.mostrar_mensagem_temporaria_aviso("Por favor, insira o número da porta do servidor!", 4000)
            return
        
        try:
            porta = int(porta)
            host = '0.0.0.0'

            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((host, porta))
            server.listen()
            self.lb_status.config(text="Servidor Ligado!",foreground="green")

            while True:
                client, addr = server.accept()
                lista_clientes.append(client)
                thread2 = threading.Thread(target=self.broadcast, args=[client])
                thread2.start()

        except ValueError:
            self.mostrar_mensagem_temporaria_aviso("Por favor, insira um número válido para a porta do servidor!", 4000)
        except OSError:
            self.mostrar_mensagem_temporaria_aviso("Não foi possível iniciar o servidor", 4000)



    def mandaMSRV(self, client):
        
        mensagem = self.num_entry.get()
        if not mensagem:
            self.mostrar_mensagem_temporaria_aviso("Por favor, insira um número!", 4000)
            return
        try:
            numero = int(mensagem)
            if numero < 1 or numero > 10:
                self.mostrar_mensagem_temporaria_aviso("Apenas números entre 1 e 10 são permitidos.",3000)
                return
            self.lb_resposta.config(text="Número enviado")
            # client.send(bytes(mensagem.encode("UTF-8")))
            numerorecebido = client.recv(1024).decode("UTF-8")
            if numero == int(numerorecebido):
                self.mostrar_mensagem_temporaria_resposta(f'{client.getpeername()[0]} acertou', 2000)
                mensagem = f'\n{client.getpeername()[0]} acertou!'
                
            else:
                self.mostrar_mensagem_temporaria_resposta(f'{client.getpeername()[0]} errou!', 2000)
                mensagem = f'{client.getpeername()[0]} errou!'
            
            self.broadcast(mensagem,client)
        except ValueError:
            self.mostrar_mensagem_temporaria_aviso("Mensagem não enviada-Digite apenas números",2000)
               
               

    def broadcast(self,mensagem,client):
        for client in lista_clientes:
            try:
                client.sendall(bytes(mensagem.encode("UTF-8")))
            except:
                self.remove_cliente(client)
    

    def remove_cliente(client):
        lista_clientes.remove(client)


if __name__ == "__main__":
    app = Aplicacao()
