import discord
import datetime
import time
import threading

client = discord.Client()

men_hoje = 0


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
            
            #salvar data
            dia1 = False
            
        while True:

            time.sleep(86400)
            men_hoje = 0
            #salvar data
temporizador = threading.Thread(target=checador_diario, daemon = True)

def salvar():
    global men_hoje
    with open('cccp.csv', 'a') as arquivo:
        arquivo.write('\n' + str(data_atual()) + ',' + str(men_hoje))
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

    global men_hoje

    men_hoje += 1
    
    if str(message.channel) == 'cccp' and message.author != client.user:

        if 'slava' in message.content:

            await message.channel.send("Viva a Rússia")

        elif 'hoje' in message.content:
            
            await message.channel.send(f'Foram registradas {men_hoje}!')

        elif message.content.startswith('teste'):
            print(type(message.content))
            print(message.content)
            
    else:
        
        return

client.run('NjI4ODAwMjQwOTc5Mjc5ODky.XeHdNQ.SOa20pH1u5NvrlKVPxA0i-1e-Sw')