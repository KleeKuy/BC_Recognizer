from Record import Record


class DataBase:

    def addrecord(self,
                  name=None,
                  surname=None,
                  record=None):
        if record:
            self.records.append(record)
        elif surname:
            newrecord = Record(name, surname)
            self.records.append(newrecord)
        else:
            print("no value given!")
        return
