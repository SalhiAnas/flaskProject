class Schema():
    def __init__(self, name):
        self.__name = name
        self.__tables = []

    def get_name(self):
        return self.__name

    def add_table(self, table):
        self.__tables.append(table)

    def get_table(self,name):
        for table in self.__tables:
            if table.get_name() ==  name:
                return table


    def get_tables(self):
        return self.__tables

class Table():
    def __init__(self, name):
        self.__name = name
        self.__colums = []

    def name(self):
        return self.__name

    def get_name(self):
        return self.__name

    def add_column(self, column):
        self.__colums.append(column)

    def add_fk(self, column):
        self.__colums.append(column)
        column.set_fk()


    def get_columns(self):
        return self.__colums

    def get_pk(self):
        for column in self.get_columns():
            if column.is_primary():
                print(column.get_name())
                return column



class Column():
    def __init__(self, name, datatype, primarykey=False,foreignKey=False,nullable=True):
        self.__name = name
        self.__ds = datatype
        self.__pk = bool(primarykey)
        self.__fk = bool(foreignKey)
        self.__nl = nullable


    def get_name(self):
        return self.__name

    def get_datatype(self):
        return self.__ds


    def is_primary(self):
        return self.__pk

    def set_fk(self):
        self.__fk=True
        self.__pk = False

    def get_attributes(self):
        return {'name':self.__name,
                'dtype':self.__ds,
                'primarykey':self.__pk,
                'foreignKey':self.__fk,
                'nullable': self.__nl

                }

