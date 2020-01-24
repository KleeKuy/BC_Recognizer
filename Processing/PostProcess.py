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
        name = self.get_name(sub, self.names)
        last_name = self.get_name(sub, self.lastnames)
        full_name = name
        if last_name:
            full_name += " " + last_name
        result[full_name] = result.pop("temp")
        mail = self.get_email(sub)
        if mail:
            result[full_name]["email"] = mail
        website = self.get_website(sub)
        if website:
            result[full_name]["website"] = website
        i = 0
        for phone in self.get_phone(sub):
            i += 1
            result[full_name]["phone" + str(i)] = phone
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
            if "@" in string and "." in string:
                return string    # is it possible that there is more thank one email?

    def get_website(self,
                    inp):
        for string in inp:
            if "www" in string and "@" not in string:
                return string

    def get_name(self,      #todo optimization?
                 inp,
                 names):
        for string in inp:
            if string is "":
                continue
            whole_word = '\n'
            whole_word += string
            whole_word += '\n'
            if whole_word.lower() in names.lower() and string is not "":
                return string

    def get_phone(self,
                  inp):
        ret = []
        part = ""
        for string in inp:
            if any(i.isdigit() for i in string):
                if string.isdigit():
                    if not part:
                        part = string
                    else:
                        part += string
                if sum(c.isdigit() for c in string) >= 9:
                    ret.append(string)
            elif len(part) >= 9:
                ret.append(part)
                part = ""
        return ret
