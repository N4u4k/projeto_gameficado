import socket
from tkinter import *
import threading
import time
class Aplicacao():
    def __init__(self):
        self.janela = Tk()
        self.tela()
        self.frames_tela()
        self.atributos_f1()
        self.atributos_f2()
        self.ip_Cliente()
        self.janela.mainloop()
        self.usuario = None

    def tela(self):
        self.janela.title("SASUKE-Cliente")
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

        self.lb_ipcliente = Label(self.frame_1, text="Seu Ip")
        self.lb_ipcliente.place(relx=0.1, rely=0.1)
        self.lb_ipclt = Label(self.frame_1, text="", bg="#E6EAFF", highlightbackground="#1D1D1D", highlightthickness=1)
        self.lb_ipclt.place(relx=0.1, rely=0.2)

        self.lb_ip = Label(self.frame_1, text="IP do servidor")
        self.lb_ip.place(relx=0.1, rely=0.35)
        self.ip_entry = Entry(self.frame_1, bg="#E6EAFF")
        self.ip_entry.place(relx=0.1, rely=0.45, relwidth=0.3)

        self.lb_porta = Label(self.frame_1, text="PORTA")
        self.lb_porta.place(relx=0.6, rely=0.35)
        self.porta_entry = Entry(self.frame_1, bg="#E6EAFF")
        self.porta_entry.place(relx=0.6, rely=0.45, relwidth=0.3)
        
        self.lb_num = Label(self.frame_1, text="Escolha um número de 0 a 10", bg="white")
        self.lb_num.place(relx=0.1, rely=0.55)
        self.num_entry = Entry(self.frame_1, bg="#E6EAFF")
        self.num_entry.place(relx=0.1, rely=0.65, relwidth=0.3)
        
        self.bt_conc = Button(self.frame_1, text="Conectar", command=self.start)
        self.bt_conc.place(relx=0.1, rely=0.8, relwidth=0.10, relheight=0.15)

        self.bt_envia = Button(self.frame_1, text="Envia", command=self.envia)
        self.bt_envia.place(relx=0.5, rely=0.8, relwidth=0.10, relheight=0.15)

        self.lb_status = Label(self.frame_1, text="", bg="white",foreground="green")
        self.lb_status.place(relx=0.8, rely=0.01)
        self.lb_status.config(text="Desconectado",foreground="red")
    
    def atributos_f2(self):
        
        self.lb_aviso = Label(self.frame_2, text="", bg="white",foreground="red")
        self.lb_aviso.place(relx=0.1, rely=0.4)

        self.lb_resposta = Label(self.frame_2, text="\n", bg="white")
        self.lb_resposta.place(relx=0.1, rely=0.5)

        self.lb_ligado = Label(self.frame_2, text="", bg="white",foreground="green")
        self.lb_ligado.place(relx=0.1, rely=0.6)
    
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
        comeca = threading.Thread(target=self.clt)
        comeca.start()
    
    def envia(self):
        if self.usuario:  # Verifica se 'self.usuario' foi definido
            thread1 = threading.Thread(target=self.mandaM, args=[self.usuario])
            thread1.start()
        else:
            print("Usuário não definido ainda!")

    def ip_Cliente(self):
        cliente_ip = socket.gethostbyname(socket.gethostname())
        self.lb_ipclt.config(text=cliente_ip)
    
    def clt(self):
        porta = self.porta_entry.get()
        if not porta:
            self.mostrar_mensagem_temporaria_aviso("Por favor, insira o número da porta do servidor!", 4000)
            return
        host = self.ip_entry.get()
        if not host:
            self.mostrar_mensagem_temporaria_aviso("Por favor, insira o ip do servidor!", 4000)
            return
        

        try:
            porta=int(porta)
            self.usuario = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.usuario.connect((host, porta))
            self.lb_status.config(text="Conectado",foreground="green")
        except ValueError:
            self.mostrar_mensagem_temporaria_aviso("Por favor, insira um número válido para a porta do servidor!", 4000)
        except:
            self.mostrar_mensagem_temporaria_aviso("Não foi possível conectar ao servidor!",2000)
            
        thread2 = threading.Thread(target=self.recebeM, args=[self.usuario])
        thread2.start()
        self.envia()

    def recebeM(self, usuario):  
        try:
            while True:    
                numero = usuario.recv(1024).decode("UTF-8")
                self.mostrar_mensagem_temporaria_aviso(numero,2000)
                print(numero)

        except ConnectionAbortedError:
            self.mostrar_mensagem_temporaria_aviso("|ERRO|-Mensagem não recebida",2000)

    def mandaM(self, usuario):
        try:
            mensagem = self.num_entry.get()
            print("cliente mensagem:"+ mensagem)
            if mensagem:
                numero = int(mensagem)
                if numero < 0 or numero > 10:
                    self.mostrar_mensagem_temporaria_aviso("Apenas números entre 1 e 10 são permitidos.",2000)
                    return
                else:
                    usuario.send(bytes(f'\n{numero}'.encode("UTF-8")))
        except ValueError:
            self.mostrar_mensagem_temporaria_aviso("Digite apenas número",2000)
        
                
if __name__ == "__main__":
    app = Aplicacao()
