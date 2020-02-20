import discord, datetime, threading, time
from sys import exit as sys_exit
from sys import exc_info
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands

client = discord.Client()
client2 = commands.Bot(command_prefix= '.')
userlist = []
pseudo_timer = 0

def kill():
    sys_exit()

def tempday(modo):

    ''' 
    Função que manipula o arquivo temporario de mensagens.
    Modo 1 = adiciona +1 mensagem ao arquivo.
    Modo 2 = Lê a quantidade de mensagens.
    Modo 3 = Reseta a quantidade de mensagens
    
    '''

    if modo == 1:

        temp = str((int(tempday(2))+1))
        open('tempday.txt', 'w').write(temp)
        
    elif modo == 2:
        return open("tempday.txt", 'r').read()

         
    elif modo == 3:
        open('tempday.txt', 'w').write('0')

def data_atual():

    return int(str(datetime.date.today()).replace("-",""))

def hora_atual():

    return int(str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute))

def checador_diario():
    
    '''
    Função de Threading para a contagem do tempo e passagem dos dias.
    Consiste em 2 loops, o primeiro pra esperar até as 00:00 horas,
    e o segundo que se inicia logo após o primeiro, que roda a cada 24hrs.
    '''
    
    dia1 = True
    while True:
        
        while (dia1 == True):
            while (hora_atual() > 2):
                
                time.sleep(30)
            
            salvar(1)
            dia1 = False
            print(f'passou o dia  {datetime.datetime.now()}')
            
        while True:
            
            time.sleep(86400)
            salvar(1)
            print(f'passou o dia  {datetime.datetime.now()}')

def salvar(modo):

    '''
    Função para salvar 1a data seguida do numero de mensagens do dia no arquivo CSV.
    É utilizada na passagem dos dias.
    '''

    global userlist

    if modo == 1:
    
        '''Usado para salvar a contagem de mensagens de cada dia!'''
        
        with open('cccp.csv', 'a') as arquivo:
            arquivo.write(f'\n{str(data_atual()-1)},{str(tempday(2))}')
            arquivo.close()
        
        tempday(3)
    
    
    elif modo == 2:

        '''Usado para atualizar o arquivo rank.csv'''

        
        leitura = ler(2)
        
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

def ler(modo):

    '''
    Função utilizada para realizar leitura de arquivos
    '''

    if modo == 1:

        '''realiza a leitura do arquivo de mensagens por dia'''

        with open('cccp.csv', 'r') as arquivo:
            saida = [A.strip().split(',') for A in arquivo]
            arquivo.close()
            return saida
    
    if modo == 2:

        '''realiza a leitura do arquivo de mensagens por pessoa'''

        return [A.strip().split(',') for A in open('rank.csv', 'r', encoding='utf-8-sig').readlines()]

def tabela(dia=1):

    '''
    Função que cria uma tabela que mostra o numero de mensagens de cada um dos ultimos 10 dias.
    '''
    ndays = 0
    dados = ler(1)
    saida = ''
    dados.reverse()
    
    saida += '```diff\n-TABELA\n'
    saida += ('-'*25)+'\n'
    
    if dia == 1:
        
        '''
        Se "dia" for igual á 1, significa que estão sendo requisitados os 10 primeiros dias do arquivo
        '''
        
        for A in range(dia*10):
            saida += f'{str(A+1):<2} dias atrás = {str(dados[A][1]):>3}\n'
            ndays += 1
    

    elif (dia*10) < len(dados)-1:

        '''
        Se "dia" for maior que 1, está sendo requisitada outra seção de 10 dias do arquivo
        '''
            
        for A in range(((dia*10)-10), dia*10):
            saida += f'{str(A+1):<2} dias atrás = {str(dados[A][1]):>3}\n'
            ndays += 1
    else:

        '''
        Se ouver um erro de indexação, significa que parte da seção de 10 dias não existem no arquivo,
        então entrega-se do inicio até o ultimo dado existente
        '''
        
        for A in range(((dia*10)-10), len(dados)-1):
            saida += f'{str(A+1):<2} dias atrás = {str(dados[A][1]):>3}\n'
            ndays += 1

    
    
    '''
    Caso o "dia" seja 1, também é entregue a media dos 10 dias,
    a media não é dada em outras situações pois a função não trabalha com setores espeficios do arquivo
    '''                    
    
    if dia == 1:
        saida += ('-'*25)+ '\n'
        saida += media(10) + '\n'
    saida += ('-'*25)+ '\n```'
    
    if ndays == 0:
        return f'Não temos nenhum dado entre {(dia*10)-10} e {dia*10} dias atras'

    return saida

def media(num):

    '''
    Função que retorna uma média que mensagens com base no numero inserido pelo usuario.
    Caso o valor seja "tudo", será estregue a média de todos os dias no CSV.
    '''
    if num == 0:
        return 'a média de mensagens dos ultimos 0 dias é de 0 mensagens.'
    dados = ler(1)
    dados.reverse()
    saida = [int(dados[A][1]) for A in range(num)]

    media = sum(saida)/num

    return f'a média de mensagens dos ultimos {num} dias é de {media:.1f} mensagens.'

def ajuda():

    return open('doc.txt', 'r', encoding='UTF-8').read()

def tabela_dias():

    '''
    Função que cria uma tabela que mostra o numero de mensagens de cada um dos ultimos 20 dias seguida do dia exato em que foram enviadas.
    '''
    
    dados = ler(1)
    dados.reverse()
    saida = ''
    saida += '```diff\n-TABELA COM DIAS\n'
    saida += ('-'*25)+'\n'
    for A in range(20):
        saida += f'{dados[A][0][0:4]}/{dados[A][0][4:6]}/{dados[A][0][6:8]} = {dados[A][1]} Mensagens\n'
    saida += ('-'*25)+ '\n'
    saida += media(20) + '\n'
    saida += ('-'*25)+ '\n```'
    return saida

def ranks(user, mensagem):
    
    global userlist, pseudo_timer
    
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
    
    
    
    if len(userlist) == 0:
        userlist.append([str(user), calc(mensagem)])

    else:
        achou = False
        for A in userlist:
            if A[0] == str(user):
                
                A[1] += calc(mensagem)
                achou = True
                
                break
        
        if achou == False:
            userlist.append([str(user), calc(mensagem)])

    pseudo_timer += 1
    

    if pseudo_timer >= 20:
        
        pseudo_timer = 0
        salvar(2)
        userlist = []
            
def tabela_rank(author):

    server = client.get_guild(272166101025161227)
    dados = ler(2)
    
    dados.sort(key=lambda num: int(float(num[1])), reverse=True)
        

    if len(dados) > 20:
        rang = 20
    else:
        rang = len(dados)
    
    
    saida = ''
    saida += '```diff\n-RANK\n'
    saida += ('-'*25)+'\n'
    for A in range(rang):
    
        if str(author) == str(dados[A][0]):

            saida += f'-{A+1} {server.get_member(int(str(dados[A][0])))} === {str(int(float(dados[A][1])))}\n'

        elif str(author) != str(dados[A][0]):

            saida += f'+{A+1} {server.get_member(int(str(dados[A][0])))} === {str(int(float(dados[A][1])))}\n'

    saida += ('-'*25)+ '\n```'

    return saida

def renderGraph(name,time=7):
    
    def formatDataGraph(date):
        #insere uma barra no formato de data int
        return date[2:]+"/"+date[:2]
    
    
    table = ler(1)

    #le as 7 ultimas entradas do CSV
    tableSize = len(table)
    nums = []
    date = []
    for i in range(1,time+1):
        nums.append(int(table[tableSize-i][1]))
        date.append(formatDataGraph( table[tableSize-i][0][4:]))

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

def renderRankGraph(path):
    colors = [(0,0,128,255),(0,0,255,255),(0,128,0,255),(0,255,0,255),(0,255,255,255),(128,0,0,255),(128,0,128,255),(128,128,0,255),(128,128,128,255),(192,192,192,255),(255,0,0,255),(255,0,255,255),(6, 40, 26, 255),(255,255,0,255)]
    font = ImageFont.truetype("font.ttf",25)#fonte pontos
    def readData(path):
	    #itera por todas as linhas do arquivo
	    #remove todos os caracteres de quebra de linha
	    #separa todas as linhas por vírgula
	    #retorna uma matriz bidimensional'''
        temp = ler(2)
        CSV = []
        for A in temp:
            CSV.append([A[0], str(int(float(A[1]))), A[2]])
	    
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
        name = "".join(i for i in ranks[i][2] if ord(i)<128)
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

#====================================================================================================================================================================

threading.Thread(target=checador_diario, daemon = True).start()

@client.event
async def on_ready():
	print('######\n  ON\n######\n\n\n')

@client.event
async def on_message(message):

    
    if message.author.bot == False:
        ranks(message.author.id, message.content)
        
    
    
    tempday(1)
    
    
    '''
    comando KILL
    '''
    if str(message.channel) == 'politburo' and message.content.startswith('kill CCCP'):
        print(f'{data_atual()}/{hora_atual()} - o bot foi assasinado por {message.author}')
        await message.channel.send('CCCP desativado!')
        kill()

    '''
    Cadeia de comandos gerais
    '''
    
    if str(message.channel) == 'floodbot' and message.author != client.user or str(message.channel) == 'off-topic' and message.author != client.user:

        try:
            
            #-----------------------------------------------------------------------------------------------------
            
            if message.content.startswith('slava'):
                await message.channel.send("Viva a Rússia", file=discord.File("RUS.png"))
            
            #-----------------------------------------------------------------------------------------------------
            
            elif message.content.startswith('hoje'):               
                await message.channel.send(f'Foram registradas {tempday(2)} mensagens!')
            
            #-----------------------------------------------------------------------------------------------------
            
            elif message.content.startswith('atras'):
                diaat = int(message.content[6:])
                if diaat > len(ler(1)):
                    await message.channel.send('Não temos registros dessa data')
                else:
                    atmen = ler(1)
                    atmen1 = ler(1)[len(atmen)-diaat][1]
                    await message.channel.send(f'foram registradas {atmen1} mensagens {diaat} dias atrás')
            
            #-----------------------------------------------------------------------------------------------------
            
            elif message.content.startswith('ajuda'):
                await message.channel.send(ajuda())
            
            #-----------------------------------------------------------------------------------------------------
            
            elif message.content.startswith('tabela'):
                if message.content == 'tabela':
                    await message.channel.send(tabela())

                else:
                    await message.channel.send(tabela(int(message.content[7:])))
            
            #-----------------------------------------------------------------------------------------------------
            
            elif message.content.startswith('media'):
                numm = message.content[6:]
                if numm == 'tudo':
                    numm = len(ler(1))
                elif numm.isnumeric() == True:
                    numm = int(numm)
                await message.channel.send(media(numm))
            
            #-----------------------------------------------------------------------------------------------------
            
            elif message.content.startswith('dias tabela'):
                await message.channel.send(tabela_dias())
            
            #-----------------------------------------------------------------------------------------------------
            
            elif message.content.startswith('rank'):
                
                pseudo_timer = 0
                salvar(2)
                userlist = []
                
                await message.channel.send(tabela_rank(message.author.id))
            
            #-----------------------------------------------------------------------------------------------------
            
            elif message.content.startswith("graph"):
                try:
                    days = message.content[6:]
                    
                    if days == 'tudo':
                        renderGraph('graph', len(ler(1)))
                        await message.channel.send(f'Gráfico de mensagens dos últimos {len(ler(1))} dias: ', file=discord.File("graph.png"))
                    else:

                        days = int(days)
                        if days> len(ler(1)):
                            await message.channel.send(f'Não há entradas de {days} dias atrás, a última é de {len(ler(1))} atrás')
                        else:
                            renderGraph("graph",days)
                            await message.channel.send(f'Gráfico de mensagens dos últimos {days} dias: ', file=discord.File("graph.png"))
                except:
                    renderGraph("graph")
                    await message.channel.send('Gráfico de mensagens da última semana: ', file=discord.File("graph.png"))
            
            #----------------------------------------------------------------------------------------------------- 
            
            elif message.content.startswith("grank"):
                renderRankGraph("rank.csv")
                await message.channel.send(f'Gráfico dos membros mais ativos do servidor', file=discord.File("rank.png"))
            
            #-----------------------------------------------------------------------------------------------------

            elif message.content.startswith("ping"):
                time = str((client.latency*1000)).split(".")[0]
                await message.channel.send(f"{time}ms!")

        except Exception as error:
            await message.channel.send('Você digitou errado, camarada!\nDigite "ajuda" para ver os comandos disponiveis!')
            print(error)
            print(exc_info()[-1].tb_lineno)
    else:
        
        return

@client.event
async def on_message_delete(message):
    
    channell = client.get_channel(652777247455051806)

    msg = message.content.replace('```', '')

    if str(message.channel) == 'logs' or str(message.channel) == 'politburo':
        return
    else:
        await channell.send(f'```diff\n---------------------------\n-Uma mensagem foi deletada!\n---------------------------\nMensagem = \n{msg}\n---------------------------\nUsuario = {message.author}\nCanal = {message.channel}\nData e hora = {datetime.date.today()}--{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}\n```')

@client.event
async def on_message_edit(before, after):
    
    channell = client.get_channel(652777247455051806)
    
    bef = before.content.replace('```', '')
    aft = after.content.replace('```', '')
    
    if str(before.channel) == 'logs' or str(before.channel) == 'politburo':
        return
    else:
        
        if before.content != after.content:
            await channell.send(f'```diff\n---------------------------\n+Uma mensagem foi editada\n---------------------------\nMensagem anterior = \n{bef}\n---------------------------\nMensagem atual = \n{aft}\n---------------------------\nUsuario = {before.author}\nCanal = {before.channel}\nData e Hora = {datetime.date.today()}--{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}\n```')

@client.event
async def on_member_join(member):

    #canal = client.get_channel(598948254134042624)
    #await canal.send(f'Olá,{member.mention}, sejá bem-vindo ao grande salão da ordem do Javali!!!')

    role = discord.utils.get(member.guild.roles, name = "Boars")
    await member.add_roles(role)


client.run('')
