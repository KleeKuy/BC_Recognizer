class PostProcess:

    def __init__(self,
                 input):
        self.input = input
        with open("names.txt") as n:
            self.names = n.read()
        with open("lastnames.txt") as n:
            self.lastnames = n.read()

    def get_record(self):
        result = {"temp": {}}
        sub = self.getsub()
        name = self.get_name(sub)
        last_name = self.get_last_name(sub)
        full_name = name + " " + last_name
        result[full_name] = result.pop("temp")
        result[full_name]["email"] = self.get_email(sub)   # todo is email
        result[full_name]["website"] = self.get_website(sub)   # todo if website

        strings = self.getsub()
        return result

    def getsub(self):
        nowhitespace = (str(self.input).split(" "))
        finalstring = []
        for string in nowhitespace:
            finalstring += string.splitlines()
        print(finalstring)
        return finalstring

    def get_email(self,
                  inp):
        for string in inp:
            if "@" in string:
                return string    # is it possible that there is more thank one email?

    def get_website(self,
                    inp):
        for string in inp:
            if "www" in string and "@" not in string:
                return string

    def get_name(self,      #todo optimization?
                 inp):
        for string in inp:
            if string in self.names:
                return string

    def get_last_name(self,      #todo optimization?
                      inp):
        for string in inp:
            if string in self.lastnames and string is not "":
                print(string)
                return string