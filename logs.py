
class Logs:

    def __init__(self):
        pass

    def embedMessage(self, discord, author, connector, title,
                     description, colour, time, target = None):
        #technical variables
        self.discord = discord              # instance of discord class
        self.author = author                # author of the message - for avatar etc.
        self.connector = connector          # connector, to get the instance of server
        #embed variables
        self.title = title                  #
        self.description = description      #
        self.colour = colour                #
        self.footer = "Wiadomość wygenerowana automatycznie przez GorigonBota"
        self.time = time
        self.target = target

        self.embed = discord.Embed(title= self.title,
                                   colour = self.colour,
                                   timestamp = self.time)

        if(self.target != None):
            self.line1 = target.mention
        else:
            self.line1 = ""

        self.embed.add_field(name= "Użytkownik", value = self.line1, inline = True)
        self.embed.add_field(name= "Moderator", value = self.author.mention, inline = True)

        self.embed.add_field(name = "Opis:", value = self.description)

        #self.embed.set_author(name = self.author.name, icon_url = self.author.avatar_url)
        self.embed.set_footer(text = self.footer, icon_url = self.author.avatar_url)

        return self.embed
