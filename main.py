import time
import telebot
import spacy
import textacy
import wikipedia
from telebot import types

# Bot:TOKEN
# 1757432372:AAHNMbgLfYR6Yb4nR76cAY67Voju8MGTzpQ
TOKEN = '1757432372:AAHNMbgLfYR6Yb4nR76cAY67Voju8MGTzpQ'

#List of users
knownUsers = []  

#Available commands for now
commands = {
    'start'       : 'Get used to the bot',
    'help'        : 'Available commands',
	'search'	  : 'We will try to search what you describe'
}

#Write logged users in file before shutdown bot
def memorize_users():
	with open('users.txt', 'w') as f:
		for item in knownUsers:
			f.write("%s\n" % item)

#Read users from file after running bot
def remember_users():
	with open('users.txt', 'r') as f:
		knownUsers = f.read().splitlines()

nlp = spacy.load("en_core_web_sm")
bot = telebot.TeleBot(TOKEN)
#Read users from file
remember_users() 

#Start with writing info about user
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  
        knownUsers.append(cid) 
        bot.send_message(cid, "Hello, traveler, let me memorize you...")
        bot.send_message(cid, "Okey, I know you now")
        command_help(m)  
    else:
        bot.send_message(cid, "I remember you, no need for me to memorize you again!")
	#Write users in file
	#memorize_users()

#Help user - display all commands
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  

#Search what user desribe
@bot.message_handler(commands=['search'])
def command_search(m):
    cid = m.chat.id
    mes_text = m.text[7:]
    #bot.send_message(cid, "Message: " + mes_text)
    doc = wikipedia.search(mes_text, results = 5)
    outtext = ""
    for res in doc:
        bot.send_message(cid, res)
    #bot.send_message(cid, 'Fat cock')  

#If user write some shit, show help
@bot.message_handler(func=lambda m: True)
def echo_all(m):
	command_help(m)

#Work
bot.polling()


