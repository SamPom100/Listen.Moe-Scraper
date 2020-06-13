import requests
from lxml import html
import re


class parser:
    def getFavs(self):
        username = self.lower()
        URL = 'https://listen.moe/u/'+username+'/favorites'
        response = requests.get(URL)
        source = response.text
        substring = 'class="name" data-v-3d9f43f6'
        matches = re.finditer(substring, source)
        match_positions = [match.start() for match in matches]
        size = len(match_positions)
        print("Number of Favorites: "+str(size))
        resultList = []
        count = 0
        for item in match_positions:
            nextEnd = source.index('<', item)
            artistBeg = source.index('/artists/', item)
            artistEnd = source.index('data', artistBeg)
            result = (str(count) + " - " + source[item+29:nextEnd] +
                      " by: "+parser.getArtist(source[artistBeg+9:artistEnd-2])+"\n")
            resultList.append(result)
            print(result)
            count = count + 1
        parser.saveFile(resultList, username)

    def getArtist(self):
        ID = self
        URL = 'https://listen.moe/artists/'+str(ID)
        response = requests.get(URL)
        source = response.text
        substring = 'class="title" data-v-4f5bebba data-v-2bb9577b'
        name = source.index(substring)+46
        return(source[name:source.index("<", name)])

    def saveFile(self, username):
        f = open(username+"_favorites.txt", "w+")
        f.write("********** Listen.Moe Favorites for " +
                username+" **********\n\n")
        for item in self:
            f.write(item)
        f.close()


# driver

parser.getFavs("SamPom100")
