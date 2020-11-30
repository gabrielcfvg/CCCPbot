from database import Database
from pickle import loads
import os




PATH = os.path.abspath(__file__).replace("\\", "/")
PATH = PATH[:PATH.rfind("/")]

data_dias = PATH+"/data_text_files/cccp.csv"
data_rank = PATH+"/data_text_files/rank.csv"
tempday = PATH+"/data_text_files/tempday.txt"

print("\n", "="*30,
      "(1) = banco -> texto",
      "(2) = texto -> banco",
      sep='\n')

ent = int(input(">>>"))

if ent not in [1, 2]:
    print("opção inválida!!!")
    input("<<<")


if ent == 2:

    data = Database()
    data.load_from_text(data_dias, data_rank, tempday)
    data.salvar(PATH)

if ent == 1:

    data = loads(open("data.cccp", 'rb').read())
    data.dump_to_text(PATH)

