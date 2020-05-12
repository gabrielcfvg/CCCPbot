import discord
import threading
import datetime
from time import sleep
from traceback import print_exc
from PIL import Image, ImageDraw, ImageFont
from pytz import timezone
from pickle import loads
from copy import deepcopy

from database import Database

##################################################################################################################
#                                                                                                                #
#                                            Variaveis e constantes                                              #
#                                                                                                                #
##################################################################################################################

client = discord.Client()

CANAIS_PERMITIDOS = ['off-topic', 'floodbot']
TIMEZONE = "America/Sao_Paulo"

database = loads(open("data.cccp", 'rb').read())

##################################################################################################################
#                                                                                                                #
#                                              Funções e Classes                                                 #
#                                                                                                                #
##################################################################################################################


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
        
        print(f"passou o dia {datetime.datetime.now(timezone(TIMEZONE))}")
        Funcoes.salvar_dia()
        database.tempday = 0

        while True:
            sleep(86400)

            print(f"passou o dia {datetime.datetime.now(timezone(TIMEZONE))}")
            Funcoes.salvar_dia()
            database.tempday = 0


    @staticmethod
    def hora_atual():

        """
        Retorna a hora atual formatada e pronta para uso.
        """

        hora = str(datetime.datetime.now(timezone(TIMEZONE)).hour)
        minutos = str(datetime.datetime.now(timezone(TIMEZONE)).minute)

        if len(hora) == 1:
            hora = '0' + hora
        
        elif len(hora) == 0:
            hora = '00'


        if len(minutos) == 1:
            minutos = '0' + minutos

        elif len(minutos) == 0:
            minutos = '00'

        return hora + minutos


    @staticmethod
    def salvar_dia():

        """
        Função que salva o número do arquivo "tempday.txt" no CSV principal
        """

        ano = str(datetime.datetime.now(timezone(TIMEZONE)).year)
        mês = str(datetime.datetime.now(timezone(TIMEZONE)).month)
        dia = str((datetime.datetime.now(timezone(TIMEZONE)).day)-1)

        if len(mês) == 1:
            mês = '0' + mês
        
        elif len(mês) == 0:
            mês = '00'


        if len(dia) == 1:
            dia = '0' + dia

        elif len(dia) == 0:
            dia = '00'

        data = int(f"{ano}{mês}{dia}")

        database.data_dia.append([data], [database.tempday])

    """
    @staticmethod
    def salvar(modo):

        global pseudo_timer
        pseudo_timer = 0


        if modo == 1:

            '''Usado para atualizar o arquivo rank.csv'''

            global userlist
        
            leitura = Funcoes.ler(2)
            
            with open('rank.csv', 'w', encoding="UTF-8") as arquivo:

                saida = []
                
                '''
                Aqui checamos quais nomes já existem no arquivo e que também estão na "userlist" e os atualizamos e adicionamos á "saida" 
                '''
                for A in leitura:
                    
                    for B in userlist:

                        if A[0] == B[0]:

                            saida.append([A[0], (float(A[1])+float(B[1]))])
                
                '''
                Aqui checamos todos que existem no no arquivo mas não existem no "userlist", e então adicionamos á saida
                '''   
                temp = [A[0] for A in saida]
                for A in leitura:
                    if A[0] not in temp:
                        saida.append([A[0], float(A[1])])

                '''
                Aqui checamos todos que existem no "userlist" mas não existem no arquivo, e então os adicionamos á saida
                '''
                for A in userlist:
                    if A[0] not in temp:
                        saida.append([A[0], float(A[1])])
        
                

                server = client.get_guild(272166101025161227)
                texto = ''
                for A in saida:

                    texto += f'{str(A[0]).strip()},{str(A[1])},{server.get_member(int(str(A[0]).strip()))}\n'

                arquivo.write(texto)

            userlist = []"""


    @staticmethod
    def ler(modo:int=1):
        
        """
        Função que realiza a leitura de arquivos
        Modos:
            1 = retorna a leitura do arquivo "cccp.csv.
        """

        if modo == 1:
            return deepcopy(database.data_dias)
            
        elif modo == 2:
            
            return [[A[0], A[1]] for A in database.data_rank.items()]


    @staticmethod
    def tabela(periodo):

 
        data = Funcoes.ler(1)
        data.reverse()
        saida = "```"
        men_num = 0

        if periodo <= len(data):

            for A in range(periodo-10, periodo):

                saida += f'{str(A+1):<2} dias atrás === {str(data[A][1]):>3}\n'
                men_num += int(data[A][1])

            saida += "```"
        else:
            return None, None

        return saida, men_num/10


    @staticmethod
    def rank(author):
        server = client.get_guild(272166101025161227)
        dados = Funcoes.ler(2)
        
        dados.sort(key=lambda num: int(float(num[1])), reverse=True)
            

        if len(dados) > 20:
            rang = 20
        else:
            rang = len(dados)
        
        
        saida = ''
        saida += '```diff\n'
        for A in range(rang):

            nome = "".join([A for A in str(server.get_member(int(str(dados[A][0])))) if ord(A) < 128])

            temp1 = f"{'-' if str(author) == str(dados[A][0]) else '+'}{('0'+str(A+1)) if A+1 < 10 else A+1}-{nome}"
            temp2 = f"{'-'*(30-len(temp1))}{str(int(float(dados[A][1])))}\n"

            saida += temp1+temp2


        saida += '```'

        return saida


    @staticmethod
    def contagem_rank(user, mensagem):

        def calc(men):

            if '>' in men:
                
                saida = 0
                lista = men.split('\n')
                for A in lista:
                    if ">" not in A:
                        saida += len(A)
                    
                    elif '<' in A and '>' in A:
                        saida += len(A)
                        
                return saida/33

            else:
                return len(men)/33

        valor = calc(mensagem)

        if database.data_rank[user]:
            database.data_rank[user] += float(valor)

        else:
            database.data_rank[user] = float(valor)


    @staticmethod
    def recorde():

        data = Funcoes.ler(1)
        data.sort(key=lambda num: int(float(num[1])), reverse=True)

        saida = "```"
        for A in range(15):
            temp = str(data[A][0])
            dia = [f'{temp[6]}{temp[7]}', f'{temp[4]}{temp[5]}', f'{temp[0]}{temp[1]}{temp[2]}{temp[3]}']
            saida += f'+{str(A+1):<2} - {dia[0]}/{dia[1]}/{dia[2]} === {data[A][1]}\n'
        saida += "```"

        return saida

    
    @staticmethod
    def renderGraph(name,time=7):
    
        def formatDataGraph(date):
            #insere uma barra no formato de data int
            return date[2:]+"/"+date[:2]
        
        
        table = Funcoes.ler(1)

        #le as 7 ultimas entradas do CSV
        tableSize = len(table)
        nums = []
        date = []
        for i in range(1,time+1):
            nums.append(int(table[tableSize-i][1]))
            date.append(formatDataGraph( str(table[tableSize-i][0])[4:]))

        #cria uma imagem branca, com o tamanho de um quinto do maior valor de mensagens+uma sobrinha
        top = int(sorted(nums,reverse=True)[0])+200
        size = ((len(nums)-1)*150)+150,int(top/5)
        img = Image.new("RGBA",(size[0],size[1]),(54,57,63,255))#código de cor do discord
        draw = ImageDraw.Draw(img)

        #fonts e listas de dados
        font = ImageFont.truetype("font.ttf",30)#fonte pontos
        font2 = ImageFont.truetype("font.ttf",24)#fonte eixos
        points = []
        #inverte a ordem dos dados para que fiquem em ordem cronológica
        nums = nums[::-1]
        date = date [::-1]

        #define onde os pontos do gráfico passarão
        for i in range(time):
            cY = int(top/5)-nums[i]/5-30
            cX = (150*i)+80
            points.append((cX,cY))
        draw.line(points,"black",5)#desenha os pontos na imagem

        #desenha as margens
        draw.line(((0,size[1]-30),(10000,size[1]-30)),(142, 138, 138,255),3)#horizontal(x)
        draw.line(((75,size[1]-30),(75,0)),(142, 138, 138,255),3)#vertical(y)

        #escreve textos
        for i in range(time):
            cY = int(top/5)-nums[i]/5-30
            cX = (150*i)+80
            draw.text((cX,cY),str(nums[i]),"Gold",font=font)#insere o texto com o valor
            draw.text((cX-20,size[1]-25),str(date[i]),"Gold",font=font2)#insere valores no eixo x(data),devidamente formatados
            
        for i in range(20):
            draw.text((10,size[1]-30-(i*50)),str(i*50*5),"Gold",font=font2)#insere valores no eixo y(qtd mensagens)

        img.save(f"{name}.png")


    @staticmethod
    def renderRankGraph(path):
        
        server = client.get_guild(272166101025161227)

        colors = [(0,0,128,255),(0,0,255,255),(0,128,0,255),(0,255,0,255),(0,255,255,255),(128,0,0,255),(128,0,128,255),(128,128,0,255),(128,128,128,255),(192,192,192,255),(255,0,0,255),(255,0,255,255),(6, 40, 26, 255),(255,255,0,255)]
        font = ImageFont.truetype("font.ttf",25)#fonte pontos
        def readData(path):
            #itera por todas as linhas do arquivo
            #remove todos os caracteres de quebra de linha
            #separa todas as linhas por vírgula
            #retorna uma matriz bidimensional'''
            temp = Funcoes.ler(2)
            CSV = []
            for A in temp:
                CSV.append([A[0], str(int(float(A[1])))])
            
            return CSV
        def sortGraph(matrix):
            #ordena os dados do rank com base no maior numero de mensagens
            sortKey = lambda matrix : int(matrix[1])
            matrix.sort(key=sortKey,reverse=True)

        ranks = readData(path)
        sortGraph(ranks)

        #calcula o total de mensagens para as proporções do gráfico
        total = 0
        for i in ranks:
            total+=int(i[1])
        reasonDeg = 360/total
        reasonCent = 100/total

        #gera a nova imagem 
        imgg = Image.new("RGBA",(800,400),(54,57,63,255))#código de cor do discord
        draw = ImageDraw.Draw(imgg)


        #variaveis de controle
        lastAng = 0
        perCent = 0
        lastPos = 10



        for i in range(len(ranks)):
            #le o nome e retira caracteres especiais e ID
            name = "".join(i for i in str(server.get_member(ranks[i][0])) if ord(i)<128)
            name = name.split("#")[0]+ " "
            msgs = int(ranks[i][1])

            #para os usuarios do top 10, é gerado um setor para cada
            if(i<10):
                #renderização do setor
                draw.pieslice([(20, 20), (380, 380)],lastAng,lastAng+reasonDeg*msgs,colors[i],(0,0,0,255))
                lastAng+= reasonDeg*int(ranks[i][1])
                #renderização da legenda
                draw.rectangle((420,lastPos,430,lastPos+25),colors[i],(0,0,0,255))
                perCent+=round(msgs*reasonCent,1)
                draw.text((435,lastPos,780,lastPos+25),f"{name}- {round(msgs*reasonCent,1)}%".replace(" ",""),(255,215,0,255),font)
                lastPos+=35
        #todos os outros usuários são aglutinados em um único setor
        draw.pieslice([(20, 20), (380, 380)],lastAng,360,(0,0,0,255),(0,0,0,255))
        draw.rectangle((420,lastPos,430,lastPos+25),(0,0,0,255),(0,0,0,255))
        draw.text((435,lastPos,780,lastPos+25),f"Other {round(100-perCent,1)}%",(255,215,0,255),font)

        imgg.save("rank.png")


    @staticmethod
    def salvar_banco():

        while True:

            database.salvar()
            sleep(30)


class Resposta:

    """
    Grupo de funções responsaveis pelo parseamento, tratamento de erros e invocação de funções de processamento.
    """

    @staticmethod
    async def slava(send):
        
        """
        Comando para teste.
        """
        
        
        await send("Viva a Rússia", file=discord.File("RUS.png"))

    
    @staticmethod
    async def hoje(send):

        """
        Comando que retorna o número de mensagens enviadas no dia de hoje.
        """

        await send(f"Foram registradas {database.tempday} mensagens")


    @staticmethod
    async def atras(send, mensagem):

        """
        Comando que retorna o número de mensagens enviadas X dias atrás.
        """

        dia = int(mensagem[6:]) if len(mensagem) >= 6 else 1
        data = Funcoes.ler(1)

        if len(data) >= dia:

            await send(f"Foram registradas {data[len(data)-dia][1]} mensagens a {dia} {'dias' if dia > 1 else 'dia'}.")
        
        else:
            await send(f"Não temos dados desse dia, nosso registro mais antigo é de {len(data)} dias atrás.")


    @staticmethod
    async def tabela(send, mensagem):


        periodo = int(mensagem[7:])*10 if len(mensagem) >= 7 else 10

        saida, media = Funcoes.tabela(periodo)

        if saida:

            embed = discord.Embed(title="Tabela", description="Mensagens enviadas em determinado periodo", color=0xFF0000)
            embed.add_field(name=f'Dados de {periodo-10} a {periodo}', value=saida)
            embed.add_field(name="Média", value=(f"```A média do periodo foi de {media} mensagens diárias```"))

            await send(embed=embed)

        else:
            await send(f"Não temos nenhum registro entre {periodo-10} e {periodo}, nosso registro mais antigo é de {len(Funcoes.ler())} dias atrás.")

    
    @staticmethod
    async def rank(send, author):
        
        saida = discord.Embed(title="Rank", description="Ranking dos camaradas mais ativos do servidor", color=0xFF0000)
        saida.add_field(name="OBS: Esse ranking é resetado a cada 7 séculos", value= Funcoes.rank(author))

        await send(embed=saida)


    @staticmethod
    async def recorde(send):

        data = Funcoes.recorde()

        embed = discord.Embed(title="Recorde", description="Tabela com os dias mais ativos do servidor")
        embed.add_field(name='.', value=data)

        await send(embed=embed)


    @staticmethod
    async def ping(send):

        time = str((client.latency*1000)).split(".")[0]
        await send(f"{time}ms!")


    @staticmethod
    async def graph(send, mensagem):

        if len(mensagem) <= 6:
            Funcoes.renderGraph("graph")
            await send('Gráfico de mensagens da última semana: ', file=discord.File("graph.png"))
            return

        days = mensagem[6:]
        
        if days == 'tudo':
            Funcoes.renderGraph('graph', len(Funcoes.ler(1)))
            await send(f'Gráfico de mensagens dos últimos {len(Funcoes.ler(1))} dias: ', file=discord.File("graph.png"))
        else:

            days = int(days)
            if days> len(Funcoes.ler(1)):
                await send(f'Não há entradas de {days} dias atrás, a última é de {len(Funcoes.ler(1))} atrás')
            else:
                Funcoes.renderGraph("graph",days)
                await send(f'Gráfico de mensagens dos últimos {days} dias: ', file=discord.File("graph.png"))


    @staticmethod
    async def grank(send):
        
        Funcoes.renderRankGraph("rank.csv")
        await send(f'Gráfico dos membros mais ativos do servidor', file=discord.File("rank.png"))


    @staticmethod
    async def ontem(send):

        data = Funcoes.ler(1)
        await send(f"Ontem foram registradas {data[-1][1]} mensagens")
        

    @staticmethod
    async def censurar(send, message):
        
        if "Officers" not in [A.name for A in message.author.roles] and "High Boar" not in [A.name for A in message.author.roles]:
            await send("Você não tem permissão para usar esse comando")
            return

        alvo = message.guild.get_member(int(message.content[12:]))

        cargo_censurado = discord.utils.get(message.guild.roles, name = "Censurado")
        cargo_boar = discord.utils.get(message.guild.roles, name = "Boars")


        await alvo.add_roles(cargo_censurado)
        await alvo.remove_roles(cargo_boar)

        await send("Usuário censurado com sucesso!!!")

        '''
        gulag = [A.strip() for A in open("gulag.txt", 'r', encoding='utf-8').readlines()]
        if str(alvo) not in gulag:
            open("gulag.txt", 'a', encoding='utf-8').write(f"\n{alvo}")'''


    @staticmethod
    async def descensurar(send, message):

        if "Officers" not in [A.name for A in message.author.roles] and "High Boar" not in [A.name for A in message.author.roles]:
            await send("Você não tem permissão para usar esse comando")
            return

        alvo = message.guild.get_member(int(message.content[15:]))

        cargo_censurado = discord.utils.get(message.guild.roles, name = "Censurado")
        cargo_boar = discord.utils.get(message.guild.roles, name = "Boars")


        await alvo.add_roles(cargo_boar)
        await alvo.remove_roles(cargo_censurado)

        await send("Usuário descensurado com sucesso!!!")
        
        '''
        gulag = [A.strip() for A in open("gulag.txt", 'r', encoding='utf-8').readlines()]
        if str(alvo) in gulag:
            open("gulag.txt", 'w', encoding='utf-8').write("".join([]))'''


    @staticmethod
    async def hora(send):

        await send(Funcoes.hora_atual())



async def parser(message):
    
    send = message.channel.send
    mensagem = message.content[3:]
    author = message.author.id

    try:
        if mensagem.startswith("slava"): await Resposta.slava(send)

        elif mensagem.startswith("hoje"): await Resposta.hoje(send)

        elif mensagem.startswith("teste"): await send(Funcoes.hora_atual())

        elif mensagem.startswith("atras"): await Resposta.atras(send, mensagem)

        elif mensagem.startswith("ontem"): await Resposta.ontem(send)

        elif mensagem.startswith("tabela"): await Resposta.tabela(send, mensagem)

        elif mensagem.startswith("rank"): await Resposta.rank(send, author)

        elif mensagem.startswith("recorde"): await Resposta.recorde(send)

        elif mensagem.startswith("ping"): await Resposta.ping(send)

        elif mensagem.startswith("graph"): await Resposta.graph(send, mensagem)

        elif mensagem.startswith("grank"): await Resposta.grank(send)

        elif mensagem.startswith("censurar"): await Resposta.censurar(send, message)

        elif mensagem.startswith("descensurar"): await Resposta.descensurar(send, message)

        elif mensagem.startswith("hora"): await Resposta.hora(send)

    except Exception as erro:

        await send("Ocorreu um erro ao tentar executar o seu comando, tente novamente!")
        print(f"erro = |{erro}|")
        print_exc()


##################################################################################################################
#                                                                                                                #
#                                             Programa principal                                                 #
#                                                                                                                #
##################################################################################################################

threading.Thread(target=Funcoes.passagem_de_dias, daemon=True).start()
threading.Thread(target=Funcoes.salvar_banco, daemon=True).start()

@client.event
async def on_ready():

    print('\n', end='')
    print("=============")
    print("===CCCPBOT===")
    print("=============")
    print(datetime.datetime.now(timezone(TIMEZONE)), '\n\n')


@client.event
async def on_message(message):


    database.tempday += 1
    if not message.author.bot: threading.Thread(target=Funcoes.contagem_rank, args=(message.author.id, message.content)).start()


    if (str(message.channel) in CANAIS_PERMITIDOS) and (message.content.startswith("cp")) and (message.author.bot == False):
        await parser(message)


@client.event
async def on_message_delete(message):
    
    channell = client.get_channel(652777247455051806)

    msg = message.content.replace('```', '')

    if str(message.channel) == 'logs' or str(message.channel) == 'politburo':
        return
    else:
        await channell.send(f'```diff\n---------------------------\n-Uma mensagem foi deletada!\n---------------------------\nMensagem = \n{msg}\n---------------------------\nUsuario = {message.author}\nCanal = {message.channel}\nhora = {datetime.datetime.now(timezone(TIMEZONE)).hour}:{datetime.datetime.now(timezone(TIMEZONE)).minute}:{datetime.datetime.now(timezone(TIMEZONE)).second}\n```')


@client.event
async def on_message_edit(before, after):
    
    channell = client.get_channel(652777247455051806)
    
    bef = before.content.replace('```', '')
    aft = after.content.replace('```', '')
    
    if str(before.channel) == 'logs' or str(before.channel) == 'politburo':
        return
    else:
        
        if before.content != after.content:
            await channell.send(f'```diff\n---------------------------\n+Uma mensagem foi editada\n---------------------------\nMensagem anterior = \n{bef}\n---------------------------\nMensagem atual = \n{aft}\n---------------------------\nUsuario = {before.author}\nCanal = {before.channel}\nhora = {datetime.datetime.now(timezone(TIMEZONE)).hour}:{datetime.datetime.now(timezone(TIMEZONE)).minute}:{datetime.datetime.now(timezone(TIMEZONE)).second}\n```')


@client.event
async def on_member_join(member):

    role = discord.utils.get(member.guild.roles, name = "Boars")
    await member.add_roles(role)


client.run(open('token.txt', 'r', encoding='utf-8').read())
