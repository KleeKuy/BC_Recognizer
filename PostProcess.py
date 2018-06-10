class PostProcess:

    def getname(self,
                inputstring):
        strings = self.getsub(string=inputstring)

        return

    def getsub(self,    #get substrings
               string):
        print(string)
        nowhitespace = (str(string).split(" "))
        finalstring = []
        for string in nowhitespace:
            finalstring += string.splitlines()
        print(finalstring)
        return
