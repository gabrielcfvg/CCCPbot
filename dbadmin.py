from database import Database
from pickle import loads


data_dias = "data_text_files\\cccp.csv"
data_rank = "data_text_files\\rank.csv"
tempday = "data_text_files\\tempday.txt"


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
    data.salvar()

if ent == 1:

    data = loads(open("data.cccp", 'rb').read())
    data.dump_to_text()

