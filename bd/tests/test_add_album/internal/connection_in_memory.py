class ConnInMemory:
    worksheet = []
    client = {"bd": {"BD": [], "Test": []}}
    __OFFSET__ = 0

    def open(self, doc_name, sheet_name=None):
        if sheet_name is None:
            return self.client[doc_name]
        else:
            return self.client[doc_name][sheet_name]

    def append(self, liste):
        self.worksheet.append(liste)

    def get(self, i, j):
        i += self.__OFFSET__
        j += self.__OFFSET__
        return self.worksheet[i][j]

    def get_line(self, i):
        i += self.__OFFSET__
        return [self.get(i, j) for j in range(len(self.worksheet[i]))]

    def get_column(self, j):
        j += self.__OFFSET__

        return [row[j] for row in self.worksheet]

    def get_all(self):
        return self.worksheet

    def set(self, valeur, i, j):
        i += self.__OFFSET__
        j += self.__OFFSET__
        if isinstance(valeur, str):
            self.worksheet[i][j] = valeur
        else:
            raise TypeError(f"{valeur} n'est pas un type texte")

    def set_line(self, valeur, i):
        i += self.__OFFSET__
        if isinstance(valeur, list):
            self.worksheet[i] = valeur
        else:
            self.worksheet[i] = [valeur]

    def set_column(self, valeur, j):
        for i in range(len(self.worksheet)):
            self.worksheet[i][j] = valeur[i]

    def delete_row(self, i):
        self.set_line([""] * 26, i)

    def double(self, isbn):
        row_values = self.get_column(0)
        for cell_value in row_values:
            if cell_value == isbn:
                return True
        return False
