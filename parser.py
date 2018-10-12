'''
Created by Jakub 'Gorigon' Matysiak on 2018.09.27

Description:
    It parses messages so that variables from discord.py
    can be included in messages from the database in form
    of 'tags' constructed by enclosing command in {}
    e.g. {name}, {usermention}, etc.
'''
class Parser:

    def __init__(self):
        #A dictionary of characters which should be striped from
        #words in the command so that tags could be read properly
        self.signs = {'!':'','?':'','.':'',
                      ',':'','.':'','\'':'',
                      '"':'',';':'',':':''}

    def parser(self, message, member = None):
        #For some tags - this FIXME:If user is not provided a
        #TypeError appears - None has no attribute member.name etc
        self.member = member
        #A dictionary of said tags. For now it's hardcoded
        #but could be transfered to a database in the future
        self.tagDictionary = {'{name}': self.member.name,
                              '{usermention}': self.member.mention}
        #Replaces {n} with \n - newline because for some reason \n
        #doesnt work when loaded from the DB
        self.message = message.replace('{n}', '\n')
        #Splits the message being parsed to a list of separate words
        #so that tags can be analyzed
        messageList = self.message.split()
        #Loops through words, checks if the word is a tag (key in the dict),
        #and replaces the tag with a discord.py variable
        for word in messageList:
            #Sanitizes the words - strips the characters from self.signs
            word = word.translate(str.maketrans(self.signs))
            if word in self.tagDictionary:
                self.message = self.message.replace(word, self.tagDictionary.get(word))
                print("I replaced {0} with {1}".format(word, self.tagDictionary.get(word)))
        return self.message
