import discord
import datetime
import time
import threading

client = discord.Client()

men_hoje = 0


def tempday(modo):

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

temporizador = threading.Thread(target=checador_diario, daemon = True)

def salvar():
    global men_hoje
    with open('cccp.csv', 'a') as arquivo:
        arquivo.write('\n' + str(data_atual()-1) + ',' + str(tempday(2)))
        arquivo.close()

def ler():

    with open('cccp.csv', 'r') as arquivo:
        saida = [A.strip().split(',') for A in arquivo]
        arquivo.close()
        return saida

def tabela():

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

    dados = ler()
    dados.reverse()
    saida = []
    for A in range(num):
        saida.append(int(dados[A][1]))

    media = sum(saida)/num

    return f'a média de mensagens dos ultimos {num} dias é de {media} mensagens.'

def ajuda():

    saida = '''```
Comandos do Bot
---------------
"slava" = O bot responde "Viva a Rússia", usado para fins de teste.

"hoje" = Diz o numero de mensagens postada até o momento atual no dia de hoje.

"atras []" = Esse comado, quando acompanhado de um numero, diz quantas mensagens foram mandadas no dia em especifico,"atras 1" irá mostrar o numero de mensagens postadas ontem.

"tabela" = Esse comando mostra uma tabela com as mensagens dos ultimos 10 dias.

"media []" = Esse comando, quando acompanhado de um numero(assim como o "atras") mostrará a media das mensagens do dia correspondente ao numero que você escolheu até agora, pode ser utilizado com a palavra "tudo" no lugar de um numero, assim ele mostrará a media de todas as mensagens desde o inicio.
```
'''

    return saida
#====================================================================================================================================================================

temporizador.start()


@client.event
async def on_ready():
	print('######\n  ON\n######\n\n\n')


@client.event
async def on_message(message):


    tempday(1)
    
    if str(message.channel) == 'cccp' and message.author != client.user:

        try:
            if 'slava' in message.content:

                await message.channel.send("Viva a Rússia")

            elif 'hoje' in message.content:
                
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
    
    #elif str(message.channel) == 'escriba-javâliano' and message.author.id == 647455830530326533:
        #await message.channel.send('Viva a Rússia, seu yanke imperialista')
    
    else:
        
        return

client.run('NjI4ODAwMjQwOTc5Mjc5ODky.XeHdNQ.SOa20pH1u5NvrlKVPxA0i-1e-Sw')