import discord
import datetime
import time
import threading

client = discord.Client()

men_hoje = 0


def tempday(modo):

    ''' 
    Função que manipula o arquivo temporario de mensagens.
    Modo 1 = adiciona +1 mensagem ao arquivo.
    Modo 2 = Lê a quantidade de mensagens.
    Modo 3 = Reseta a quantidade de mensagens
    
    '''

    if modo == 1:

        temp = int(tempday(2))
        
        with open('tempday.txt', 'w') as artemp:

            artemp.write(str(1 + temp))
        

    elif modo == 2:

        with open('tempday.txt', 'r') as artemp:
            A = artemp.read()
            
            return A
    
    elif modo == 3:

        with open('tempday.txt', 'w') as artemp:

            artemp.write('0')

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
    
    global men_hoje
    dia1 = True
    while True:
        
        while (dia1 == True):
            while (hora_atual() > 10):
                
                time.sleep(30)
            
            salvar()
            tempday(3)
            dia1 = False
            print('passou o dia')
            
        while True:
            
            time.sleep(86400)
            salvar()
            tempday(3)
            print('passou o dia')

def salvar():
    
    '''
    Função para salvar a data seguida do numero de mensagens do dia no arquivo CSV.
    É utilizada na passagem dos dias.
    '''

    global men_hoje
    with open('cccp.csv', 'a') as arquivo:
        arquivo.write('\n' + str(data_atual()-1) + ',' + str(tempday(2)))
        arquivo.close()

def ler():

    '''
    Função que retorna uma lista de listas, cada uma das listas internas representa uma linha no CSV.
    Cada lista interna possui 2 valores, 1° = data, 2° = número de mensagens.
    '''

    with open('cccp.csv', 'r') as arquivo:
        saida = [A.strip().split(',') for A in arquivo]
        arquivo.close()
        return saida

def tabela():

    '''
    Função que cria uma tabela que mostra o numero de mensagens de cada um dos ultimos 10 dias.
    '''
    
    dados = ler()
    saida = ''
    dados.reverse()
    
    saida += '```diff\n-TABELA\n'
    saida += ('-'*25)+'\n'
    for A in range(10):
        saida += str(A+1) + ' dias atrás = ' + str(dados[A][1]) + '\n'
    saida += ('-'*25)+ '\n```'
    
    return saida

def media(num):

    '''
    Função que retorna uma média que mensagens com base no numero inserido pelo usuario.
    Caso o valor seja "tudo", será estregue a média de todos os dias no CSV.
    '''
    
    dados = ler()
    dados.reverse()
    saida = []
    for A in range(num):
        saida.append(int(dados[A][1]))

    media = sum(saida)/num

    return f'a média de mensagens dos ultimos {num} dias é de {media} mensagens.'

def ajuda():

    return open('doc.txt', 'r', encoding='UTF-8').read()

#====================================================================================================================================================================

threading.Thread(target=checador_diario, daemon = True).start()

@client.event
async def on_ready():
	print('######\n  ON\n######\n\n\n')


@client.event
async def on_message(message):


    tempday(1)
    
    if str(message.channel) == 'cccp' and message.author != client.user or str(message.channel) == 'floodbot' and message.author != client.user:

        try:
            if message.content.startswith('slava'):

                await message.channel.send("Viva a Rússia")

            elif message.content.startswith('hoje'):
                
                await message.channel.send(f'Foram registradas {tempday(2)}!')

            elif message.content.startswith('atras'):

                
                diaat = int(message.content[6:])

                if diaat > len(ler()):
                    await message.channel.send('Não temos registros dessa data')
                
                else:
                    atmen = ler()
                    atmen1 = ler()[len(atmen)-diaat][1]
                    
                    await message.channel.send(f'foram registradas {atmen1} mensagens {diaat} dias atrás')

            elif message.content.startswith('ajuda'):

                await message.channel.send(ajuda())

            elif message.content.startswith('tabela'):
                
                await message.channel.send(tabela())

            elif message.content.startswith('media'):

                numm = message.content[6:]

                if numm == 'tudo':

                    numm = len(ler())

                elif numm.isnumeric() == True:
                    numm = int(numm)

                await message.channel.send(media(numm))

                
        except Exception as error:
            await message.channel.send('Você digitou errado, camarada!\nDigite "ajuda" para ver os comandos disponiveis!')
            print(error)
    
    else:
        
        return

client.run('NjI4ODAwMjQwOTc5Mjc5ODky.XeHdNQ.SOa20pH1u5NvrlKVPxA0i-1e-Sw')