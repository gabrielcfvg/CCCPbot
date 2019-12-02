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
            while (hora_atual() >= 000 or hora_atual() <= 10):
                
                time.sleep(60)
            
            salvar()
            tempday(3)
            dia1 = False
            
        while True:

            time.sleep(86400)
            salvar()
            tempday(3)
            
temporizador = threading.Thread(target=checador_diario, daemon = True)

def salvar():
    global men_hoje
    with open('cccp.csv', 'a') as arquivo:
        arquivo.write('\n' + str(data_atual()) + ',' + str(tempday(2)))
        arquivo.close()

def ler():

    with open('cccp.csv', 'r') as arquivo:
        saida = [A.strip().split(',') for A in arquivo]
        arquivo.close()
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

                
                if len(message.content) == 7:

                    diaat = int(message.content[6])
                
                elif len(message.content) == 8:

                    diaat = int(message.content[6] + message.content[7])

                if diaat > len(ler()):
                    await message.channel.send('Não temos registros dessa data')
                
                else:
                    atmen = ler()
                    atmen = ler()[len(atmen)-diaat][1]
                    
                    await message.channel.send(f'foram registradas {atmen} mensagens {diaat} dias atrás')
        except:
            await message.channel.send('Você digitou errado, camarada!\nDigite "ajuda" para ver os comandos disponiveis!')

    
    #elif str(message.channel) == 'escriba-javâliano' and message.author.id == 647455830530326533:
        #await message.channel.send('Viva a Rússia, seu yanke imperialista')
    
    else:
        
        return

client.run('NjI4ODAwMjQwOTc5Mjc5ODky.XeHdNQ.SOa20pH1u5NvrlKVPxA0i-1e-Sw')