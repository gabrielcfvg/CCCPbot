import discord
import datetime
from threading import Thread
from time import sleep


client = discord.Client()

#=====================================================================================================================
#=====================================================================================================================
#VARIAVEIS
#------------------------


client = discord.Client()
canais_permitidos = ['off-topic', 'floodbot']


#=====================================================================================================================
#=====================================================================================================================
#FUNCOES E CLASSES
#------------------------


class Funcoes:

    """
        Classe que grupa todas as funções de processamento de dados e relacionados.
        """

    @staticmethod
    def passagem_de_dias():

        """
            Função que gerencia a passagem de dias e realiza o salvamento de dados.
            """
        
        while(int(Funcoes.hora_atual()) > 2):
            sleep(30)
        
        print(f"passou o dia {datetime.datetime.now()}")
        Funcoes.salvar_dia()
        Funcoes.numero_de_mensagens(3)

        while True:
            sleep(86400)

            print(f"passou o dia {datetime.datetime.now()}")
            Funcoes.salvar_dia()
            Funcoes.numero_de_mensagens(3)


    @staticmethod
    def numero_de_mensagens(modo: int):

        """
            Função que gerencia o arquivo de armazenamento de mensagens do dia.
            
            Modos:
                1 = Incrementar +1;
                2 = Ler valor atual;
                3 = Resetar valor para 0;
            """


        if modo == 1:

            valor_atual = Funcoes.numero_de_mensagens(2)
            open('tempday.txt', 'w').write(str(valor_atual+1))

        elif modo == 2:

            return int(open('tempday.txt', 'r').read())

        elif modo == 3:

            open('tempday.txt', 'w').write('0')


    @staticmethod
    def hora_atual():

        """
            Retorna a hora atual formatada e pronta para uso.
            """

        hora = str(datetime.datetime.hour())
        minuto = str(datetime.datetime.minute())

        if len(hora) == 1:
            hora = '0' + hora
        
        elif len(hora) == 0:
            hora = '00'


        if len(minuto) == 1:
            minuto = '0' + minuto

        elif len(minuto) == 0:
            minuto = '00'

        return hora + minuto

    
    @staticmethod
    def salvar_dia():

        """
            Função que salva o número do arquivo "tempday.txt" no CSV principal
            """

        open("dados_dias.csv", 'a').write(f"{str(datetime.date.today()).replace('-','')},{Funcoes.numero_de_mensagens(2)}")

#=====================================================================================================================
#=====================================================================================================================
#CODIGO PRINCIPAL
#------------------------

Thread(target=Funcoes.passagem_de_dias, daemon=True).start()


@client.event
async def on_ready():

    """
        Função de inicialização do bot
        """

    print('\n', end='')
    print("=============")
    print("===CCCPBOT===")
    print("=============")
    print(datetime.datetime.now(), '\n\n')


@client.event
async def on_message(message):

    """
        Função que monitora todas as mensagens e responde caso necessario.
        """

    """
        Incrementa o número de mensagens em +1
        """
    Funcoes.numero_de_mensagens(1)
    

    """
        A função é terminada caso:

            Não tenha sido enviada num canal permitido;
            Não possua o prefixo "cp";
            Tenha sido enviada por um BOT
        """
    if (message.channel not in canais_permitidos) and (message.content.startswith("cp")) and (message.author.bot == True):
        return



client.run(open('token.txt', 'r', encoding='utf-8').read())