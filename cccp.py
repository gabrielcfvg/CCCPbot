import discord
import datetime
import asyncio
from time import sleep, time
from threading import Thread
import database
from pickle import loads
from traceback import print_exc, format_exc
from copy import deepcopy
import os
from PIL import Image, ImageDraw, ImageFont

##################################################################################################################
#                                                                                                                #
#                                            Variaveis e constantes                                              #
#                                                                                                                #
##################################################################################################################



PATH = os.path.abspath(__file__).replace("\\", "/")
PATH = PATH[:PATH.rfind("/")]
print(PATH)

INTENTS = discord.Intents.default()
INTENTS.members = True
CLIENT = discord.Client(intents=INTENTS)


DATABASE = loads(open(f"{PATH}/data.cccp", 'rb').read())
CANAIS_PERMITIDOS = ['off-topic', 'floodbot']
SERVER_ID = 272166101025161227
START_DATE = time()

TIME_DIFF = 0
DEBUG = False

##################################################################################################################
#                                                                                                                #
#                                              Funções e Classes                                                 #
#                                                                                                                #
##################################################################################################################

class Dados:

    @staticmethod
    def tempday():
        return deepcopy(DATABASE.tempday)
    
    @staticmethod
    def incrementar_tempday():
        DATABASE.tempday += 1

    @staticmethod
    def resetar_tempday():
        DATABASE.tempday = 0
    
    @staticmethod
    def mudar_tempday(num):
        DATABASE.tempday = num

    @staticmethod
    def incrementar_data_dias(data, num):
        DATABASE.data_dias.append([data, num])

    @staticmethod
    def atualizar_rank(id, num):
        
        if id in DATABASE.data_rank:
            DATABASE.data_rank[id] += float(num)
        else:
            DATABASE.data_rank[id] = float(num)

    @staticmethod
    def deletar_usuário(id):
        del DATABASE.data_rank[id]

    @staticmethod
    def tabela_dias():
        return deepcopy(DATABASE.data_dias)

    @staticmethod
    def tabela_rank(modo=1):
        """
        Modo 1 = list
        Modo 2 = dict
        """

        if modo == 2:
            
            return deepcopy(DATABASE.data_rank)

        elif modo == 1:

            return [[A, B] for A, B in DATABASE.data_rank.items()]

    @staticmethod
    def alterar_tabela_dias(dia, valor):


        posição = [DATABASE.data_dias.index(A) for A in DATABASE.data_dias if A[0] == dia]
        
        if posição:
            DATABASE.data_dias[posição[0]][1] = valor
        else:
            DATABASE.data_dias.append([dia, valor])
            DATABASE.data_dias.sort(key=lambda x:x[0])

    @staticmethod
    def resetar_rank():

        DATABASE.data_rank = {}

    @staticmethod
    def change_user_rank(id, num):

        DATABASE.data_rank[id] = num


class Tempo:

    @staticmethod
    def posixtime():
        return time() + TIME_DIFF

    @staticmethod
    def datetime():

        return datetime.datetime.fromtimestamp(Tempo.posixtime())

    @staticmethod
    def intdata():

        return int(Tempo.datetime().strftime(r"%Y%m%d"))


class Funções:

    @staticmethod
    def passar_dia():

        data = Tempo.datetime()
        alvo = datetime.datetime(data.year, data.month, data.day, 23, 59, 40)
        data = datetime.datetime.timestamp(data)
        alvo = datetime.datetime.timestamp(alvo) + TIME_DIFF

        sleep(alvo-data)
        Funções.salvar_dia()

        while True:
            sleep(86400)
            Funções.salvar_dia()


    @staticmethod
    def salvar_banco():

        while True:

            sleep(20)
            DATABASE.dump_to_text(PATH)
            sleep(10)
            DATABASE.salvar(PATH)


    @staticmethod
    def salvar_dia():

        print('='*30, "\npasou o dia", str(Tempo.datetime().strftime(r"%Y %m %d | %H %M %S")))
        Dados.incrementar_data_dias(Tempo.intdata(), Dados.tempday())
        Dados.resetar_tempday()


    @staticmethod
    def contagem_rank(message):

        def calc(conteudo):

            if ">" in conteudo:

                valor = 0
                for A in conteudo.split("\n"):
                    if ">" not in A or A.count(">") == A.count("<"):
                        valor += len(A)

                return valor/33

            else:
                return len(conteudo)/33

        Dados.atualizar_rank(message.author.id, calc(message.content))


    @staticmethod
    def buraco_negro(*args, **kwargs):
        pass


    @staticmethod
    def checar_permissão(cargo_ou_id):

        def decorador(func):
            
            async def interna(*args, **kwargs):

                ###################################
                #      Validação de permissão     #
                ###################################

                autor_id = kwargs.get("autor")

                async def negado():

                    send = kwargs.get("send", Funções.buraco_negro)
                    await send("Você não tem permissão para usar esse comando!!!")
                
                if type(cargo_ou_id) == str:

                    if cargo_ou_id not in [A.name for A in CLIENT.get_guild(SERVER_ID).get_member(autor_id).roles]:

                        await negado()
                        return

                elif type(cargo_ou_id) == int:

                    if cargo_ou_id != autor_id:

                        await negado()
                        return

                elif type(cargo_ou_id) == list:

                    if autor_id not in cargo_ou_id:

                        await negado()
                        return

                ###################################
                #            Execução             #
                ###################################

                await func(*args)

            return interna

        return decorador


class Comandos:

    @staticmethod
    async def slava(send):

        await send("Viva a Rússia", file=discord.File("RUS.png"))

    
    @staticmethod
    async def hoje(send):

        await send(f"Foram enviadas {Dados.tempday()} mensagens")


    @staticmethod
    async def atras(send, mensagem):

        dia = int(mensagem[6:]) if len(mensagem) >= 6 else 1
        data = Dados.tabela_dias()

        if len(data) >= dia:

            await send(f"Foram registradas {data[len(data)-dia][1]} mensagens a {dia} {'dias' if dia > 1 else 'dia'}.")
        
        else:
            await send(f"Não temos dados desse dia, nosso registro mais antigo é de {len(data)} dias atrás.")


    @staticmethod
    async def ontem(send):

        await send(f"Ontem foram registradas {Dados.tabela_dias()[-1][1]} mensagens")


    @staticmethod
    async def ping(send):

        time = str((CLIENT.latency*1000)).split(".")[0]
        await send(f"{time}ms!")


    @staticmethod
    async def recorde(send):

        data = Dados.tabela_dias()
        data.sort(key=lambda x: x[1], reverse=True)
        
        
        saida = "```"
        for A in range(15):
            temp = str(data[A][0])
            dia = [f'{temp[6]}{temp[7]}', f'{temp[4]}{temp[5]}', f'{temp[0]}{temp[1]}{temp[2]}{temp[3]}']
            saida += f'+{str(A+1):<2} - {dia[0]}/{dia[1]}/{dia[2]} === {data[A][1]}\n'
        saida += "```"

        embed = discord.Embed(title="Recorde", description="Tabela com os dias mais ativos do servidor")
        embed.add_field(name='.', value=saida)

        await send(embed=embed)


    @staticmethod
    async def backup(send):

        arquivos_ignorados = ("backup.zip", "token.txt", ".git")

        from zipfile import ZipFile
        from os import walk
        
        with ZipFile("backup.zip", 'w') as arquivo:

            for root, dirs, files in os.walk('.'):# pylint: disable=unused-variable
                for file in files:
                    if all([A not in (os.path.join(root, file)) for A in arquivos_ignorados]):
                        arquivo.write(os.path.join(root, file))
        
        await send(file=discord.File("backup.zip"))
        os.remove("backup.zip")


    @staticmethod
    async def tabela(send, mensagem):

        periodo = int(mensagem[7:])*10 if len(mensagem) >= 7 else 10

        data = Dados.tabela_dias()
        
        if periodo-9 <= len(data):

            data.reverse()
            men_num = 0
            saida = ''

            for A in range(periodo-10, periodo):

                if A <= len(data)-1:
                    saida += f'{str(A+1):<2} dias atrás === {str(data[A][1]):>3}\n'
                    men_num += int(data[A][1])
            
            saida = "```" + saida + "```"

            embed = discord.Embed(title="Tabela", description="Mensagens enviadas em determinado periodo", color=0xFF0000)
            embed.add_field(name=f'Dados de {periodo-9} a {periodo}', value=saida)
            embed.add_field(name="Média", value=(f"```A média do periodo foi de {men_num//10} mensagens diárias```"))

            await send(embed=embed)
        
        else:
            await send(f"Não temos nenhum registro entre {periodo-10} e {periodo}, nosso registro mais antigo é de {len(data)} dias atrás.")


    @staticmethod
    async def rank(send, autor):


        server = CLIENT.get_guild(SERVER_ID)

        data = Dados.tabela_rank(1)
        data.sort(reverse=True, key=lambda x: x[1])
        data = list(map(lambda a:[a[0], int(a[1])], data))

        rang = 20 if len(data) >= 20 else len(data)
        pré_saida = ""
        for A in range(rang):

            member = server.get_member(data[A][0])

            if (member != None):

                if (member.nick):
                    nome = "".join([B for B in str(member.nick) if ord(B) < 128 ])[:24]
                else:
                    nome = "".join([B for B in str(member) if ord(B) < 128 ])[:24]

                temp1 = f"""{"-" if data[A][0] == autor else '+'}{("0"+str(A+1)) if A+1 < 10 else str(A+1)} {nome}"""
                temp2 = f"""{"-"*(30-len(temp1))}{data[A][1]}\n"""

                pré_saida += temp1+temp2

        
        pré_saida = f"```diff\n{pré_saida}\n```"

        saida = discord.Embed(title="Rank", description="Ranking dos camaradas mais ativos do servidor", color=0xFF0000)
        saida.add_field(name="OBS: Esse ranking é resetado a cada 7 séculos", value=pré_saida)

        await send(embed=saida)


    @staticmethod
    async def hora(send):

        hora = Tempo.datetime()
        await send(f"{hora.hour}:{hora.minute}:{hora.second}")

    
    @staticmethod
    async def renderGraph(send, mensagem):
    
        valor = mensagem[6:]
        
        if len(mensagem) <= 6:
            time = 7
        elif valor in ["tudo", "all"]:
            time = len(Dados.tabela_dias())
        else:
            time = int(valor)


        def formatDataGraph(date):
            #insere uma barra no formato de data int
            return date[2:]+"/"+date[:2]
        
        
        table = Dados.tabela_dias()

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

        img.save(f"tmp.png")
        await send(file=discord.File("tmp.png"))


    @staticmethod
    async def renderRankGraph(send):
        
        server = CLIENT.get_guild(SERVER_ID)

        colors = [(0,0,128,255),(0,0,255,255),(0,128,0,255),(0,255,0,255),(0,255,255,255),(128,0,0,255),(128,0,128,255),(128,128,0,255),(128,128,128,255),(192,192,192,255),(255,0,0,255),(255,0,255,255),(6, 40, 26, 255),(255,255,0,255)]
        font = ImageFont.truetype("font.ttf",25)#fonte pontos
        def readData():
            #itera por todas as linhas do arquivo
            #remove todos os caracteres de quebra de linha
            #separa todas as linhas por vírgula
            #retorna uma matriz bidimensional'''
            temp = Dados.tabela_rank(1)
            CSV = []
            for A in temp:
                CSV.append([A[0], str(int(float(A[1])))])
            
            return CSV
        def sortGraph(matrix):
            #ordena os dados do rank com base no maior numero de mensagens
            sortKey = lambda matrix : int(matrix[1])
            matrix.sort(key=sortKey,reverse=True)

        ranks = readData()
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

        imgg.save("tmp.png")
        await send(file=discord.File("tmp.png"))


    @staticmethod
    async def uptime(send):

        tmp = Tempo.datetime() - datetime.datetime.fromtimestamp(START_DATE)
        await send(str(tmp))


    @staticmethod
    async def amanha(send):

        data = Dados.tabela_dias()
        data.reverse()

        média = sum([data[A][1] for A in range(7)]) / 7

        await send(f"Amanha teremos {int(média)} mensagens!!!")

    @staticmethod
    async def ajuda(send):

        await send("```slava\nhoje\natras\nontem\nping\nrecorde\nbackup\ntabela\nrank\nhora\ngraph\ngrank\nuptime\namanha\nmtempday\nmtabela\nmuserrank\nmrank\nmchangerank```")


    ####################################################
    #                                                  #
    #                  Administração                   #
    #                                                  #
    ####################################################

    @staticmethod
    @Funções.checar_permissão(cargo_ou_id=197477133675659264)
    async def alterar_tempday(send, mensagem):
        
        novo_valor = int(mensagem.split(" ")[-1])
        Dados.mudar_tempday(novo_valor)

        await send("Valor alterado com sucesso!!!")

    
    @staticmethod
    @Funções.checar_permissão(cargo_ou_id=197477133675659264)
    async def alterar_tabela(send, mensagem):

        dia = int(mensagem.split(" ")[1])
        valor = int(mensagem.split(" ")[2])

        Dados.alterar_tabela_dias(dia, valor)

        await send("Valor alterado com sucesso!!!")


    @staticmethod
    @Funções.checar_permissão(cargo_ou_id=[197477133675659264, 178527034606092288])
    async def resetar_rank(send):

        await Comandos.backup(send)
        
        await send("Rank resetado com sucesso!!!")

        server = CLIENT.get_guild(SERVER_ID)
        
        lock_cargo = ["Officers", "Old Boar", "High Boar"]
        result = []

        data = Dados.tabela_rank(1)
        data.sort(reverse=True, key=lambda x: x[1])
        data = list(map(lambda a:[a[0], int(a[1])], data))
        
        rang = 20 if len(data) >= 20 else len(data)

        for A in range(rang):

            member = server.get_member(data[A][0])
            if member == None:
                continue
            
            member_roles = [A.name for A in member.roles]

            if len([0 for A in lock_cargo if A in member_roles]) > 0:
                continue
    
            if (member.nick):
                result.append("".join([B for B in str(member.nick) if ord(B) < 128 ])[:24])
            else:
                result.append("".join([B for B in str(member) if ord(B) < 128 ])[:24])

            if len(result) > 2:
                break
        
        result_str = "```"
        result_str += "".join([A+" " for A in result])
        result_str += "```"
        Dados.resetar_rank()
        await send(f"Novos most activies: {result_str}")


    @staticmethod
    @Funções.checar_permissão(cargo_ou_id="Officers")
    async def resetar_usuário(send, mensagem):

        _id = int(mensagem[10:])
        Dados.deletar_usuário(_id)
        await send("Usuário resetado com sucesso!!!")
        
    @staticmethod
    @Funções.checar_permissão(cargo_ou_id="Officers")
    async def change_user_rank(send, message):
        
        user_id = int(message.split(" ")[1])
        num = int(message.split(" ")[2])

        Dados.change_user_rank(user_id, num)

        await send("valores alterados com sucesso")




async def parser(message):

    send = message.channel.send if not DEBUG else Funções.buraco_negro
    mensagem = message.content[3:]
    autor = message.author.id

    try:
        
        if mensagem.startswith("slava"): await Comandos.slava(send)

        elif mensagem.startswith("hoje"): await Comandos.hoje(send)

        elif mensagem.startswith("atras"): await Comandos.atras(send, mensagem)

        elif mensagem.startswith("ontem"): await Comandos.ontem(send)

        elif mensagem.startswith("ping"): await Comandos.ping(send)

        elif mensagem.startswith("recorde"): await Comandos.recorde(send)

        elif mensagem.startswith("backup"): await Comandos.backup(send)

        elif mensagem.startswith("tabela"): await Comandos.tabela(send, mensagem)

        elif mensagem.startswith("rank"): await Comandos.rank(send, autor)

        elif mensagem.startswith("hora"): await Comandos.hora(send)
        
        elif mensagem.startswith("graph"): await Comandos.renderGraph(send, mensagem)

        elif mensagem.startswith("grank"): await Comandos.renderRankGraph(send)

        elif mensagem.startswith("uptime"): await Comandos.uptime(send)

        elif mensagem.startswith("amanha"): await Comandos.amanha(send)

        elif mensagem.startswith("ajuda"): await Comandos.ajuda(send)


        ###################################
        #     Comandos Administrativos    #
        ###################################
        
        elif mensagem.startswith("mtempday"): await Comandos.alterar_tempday(send, mensagem, autor=autor, send=send)# pylint: disable=unexpected-keyword-arg, redundant-keyword-arg
        
        elif mensagem.startswith("mtabela"): await Comandos.alterar_tabela(send, mensagem, autor=autor, send=send)# pylint: disable=unexpected-keyword-arg, redundant-keyword-arg

        elif mensagem.startswith("mrank"): await Comandos.resetar_rank(send, autor=autor, send=send)# pylint: disable=unexpected-keyword-arg, redundant-keyword-arg

        elif mensagem.startswith("muserrank"): await Comandos.resetar_usuário(send, mensagem, autor=autor, send=send)# pylint: disable=unexpected-keyword-arg, redundant-keyword-arg

        elif mensagem.startswith("mchangerank"): await Comandos.change_user_rank(send, mensagem, autor=autor, send=send)# pylint: disable=unexpected-keyword-arg, redundant-keyword-arg

        else:
            await send("Comando não existente")

    except Exception as error:

        await send("Ocorreu um erro ao tentar executar o seu comando, tente novamente!")
        print(f"erro = |{error}|")
        print_exc()



##################################################################################################################
#                                                                                                                #
#                                             Programa principal                                                 #
#                                                                                                                #
##################################################################################################################

Thread(target=Funções.passar_dia, daemon=True).start()
Thread(target=Funções.salvar_banco, daemon=True).start()



@CLIENT.event
async def on_ready():

    print('\n', end='')
    print("=============")
    print("===CCCPBOT===")
    print("=============")
    print(str(datetime.datetime.now()))
    print(CLIENT.get_user(197477133675659264))


@CLIENT.event
async def on_message(message):

    # print("teste")

    Dados.incrementar_tempday()
    if (not message.author.bot) and str(message.channel.id) != "770107741585932339": 
        Thread(target=Funções.contagem_rank, args=[message], daemon=True).start()

        # print(str(message.guild.get_member(message.author.id).nick))

    if (str(message.channel) in CANAIS_PERMITIDOS) and (message.content.startswith("cp")) and (message.author.bot == False):
        await parser(message)


@CLIENT.event
async def on_message_delete(message):
    
    channell = CLIENT.get_channel(652777247455051806)

    msg = message.content.replace('```', '')

    if str(message.channel) == 'logs' or str(message.channel) == 'politburo':
        return
    else:
        await channell.send(f'```diff\n---------------------------\n-Uma mensagem foi deletada!\n---------------------------\nMensagem = \n'+
        f'{msg}\n---------------------------\nUsuario = {message.author}\nCanal = {message.channel}\n'+
        f'hora = {Tempo.datetime().hour}:{Tempo.datetime().minute}:'+
        f'{Tempo.datetime().second}\n```')


@CLIENT.event
async def on_message_edit(before, after):
    
    channell = CLIENT.get_channel(652777247455051806)
    
    bef = before.content.replace('```', '')
    aft = after.content.replace('```', '')
    
    if str(before.channel) == 'logs' or str(before.channel) == 'politburo':
        return
    else:
        
        if before.content != after.content:
            await channell.send(f'```diff\n---------------------------\n+Uma mensagem foi editada\n---------------------------\n'+
            f'Mensagem anterior = \n{bef}\n---------------------------\nMensagem atual = \n{aft}\n---------------------------\n'+
            f'Usuario = {before.author}\nCanal = {before.channel}\nhora = {Tempo.datetime().hour}:'+
            f'{Tempo.datetime().minute}:{Tempo.datetime().second}\n```')


@CLIENT.event
async def on_member_join(member):

    print("------------")
    print(member)

    role = discord.utils.get(member.guild.roles, name = "Boars")
    await member.add_roles(role)



CLIENT.run(open(f'{PATH}/token.txt', 'r', encoding='utf-8').read())
