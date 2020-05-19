class Database:

    def salvar(self):
        
        from pickle import dumps
        
        open("data.cccp", 'wb').write(dumps(self))


    def load_from_text(self, data_dias, data_rank, tempday):

        """
        Abertura e parseamento databela de dias-mensagens
        """
        self.data_dias = [[int(B) for B in A.split(",")] for A in open(data_dias, 'r', encoding="utf-8").readlines()]
        

        """
        Abertura e parseamento do arquivo de rank
        """

        self.data_rank = {}
        for A in [A.split(",") for A in open(data_rank, 'r', encoding="utf-8").readlines()]:

            self.data_rank[int(A[0])] = float(A[1])

        """
        Carregamento das mensagens enviadas no dia
        """

        self.tempday = int(open(tempday, 'r').read())

    
    def dump_to_text(self):

        from os import mkdir, getcwd
        from os.path import exists
        
        saida = getcwd()+"\\data_text_files"

        if not exists(saida):
            mkdir(saida)

        with open(saida+"\\cccp.csv", 'w', encoding="utf-8") as arquivo:

            for A in self.data_dias:
                arquivo.write(f"{A[0]},{A[1]}\n")

        with open(saida+"\\rank.csv", 'w', encoding="utf-8") as arquivo:

            for A in self.data_rank.items():

                arquivo.write(f"{A[0]},{A[1]}\n")

        with open(saida+"\\tempday.txt", "w", encoding="utf-8") as arquivo:

            arquivo.write(str(self.tempday))

