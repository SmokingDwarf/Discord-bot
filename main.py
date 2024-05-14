import discord # type: ignore
import os
import json
import discord_user
from random import randint, choice

def reply_to_self(client, user):
	id = user

	def reply_to_self_impl(func):
		@client.event
		async def on_message(message):
			if str(message.author.id) != str(id):
				return
			reply = func(message)
			if reply != None and reply != "":
				await message.channel.send(reply)
		return on_message
	return reply_to_self_impl


def reply_to_all(client):
	def reply_to_all_impl(func):
		@client.event
		async def on_message(message):
			if message.author == client.user:
				return
			if message.author.bot:
				return
			reply = func(message)
			if reply != None and reply != "":
				await message.channel.send(reply)
		return on_message
	return reply_to_all_impl

TOKEN = discord_user.TOKEN
USERNAME = discord_user.USERNAME

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#States
initialize_state = True
activity_asking_state = False
new_user_state = False
skill_asking_state = False

#Lists & dicts
activity_list = ["work"]
skill_dict = {"acrobatics": "dexterity", "animal handling": "wisdom"}

@reply_to_all(client)
def send_message(message):
	global initialize_state
	global activity_asking_state
	global new_user_state
	global skill_asking_state
	global activity_list
	global skill_dict
	username = str(message.author)
	
	if message.content and message.channel.name == 'michs-bot':
		with open ("discord_bot_users.json", "r") as file:
			users = json.load(file)
		
		if initialize_state == True:
			initialize_state = False
			for key, value in users.items():
				if key == username:
					activity_asking_state = True
					return f"Hello {(users[key]["name"])}! Select a downtime activity from: work, ..."
				elif key is not username:
					new_user_state == True
					return f"Welcome, new adventurer! What is your name?"
		
		elif activity_asking_state == True:
			if "work" in message.content.lower():
				activity_asking_state = False
				skill_asking_state = True
				return f"Great. Select a skill from {skill_dict.keys}."
			else:
				return f"Please select from: work, ..."
		
		elif skill_asking_state == True:
			if message.content.lower() in skill_dict:
				skill_asking_state = False
				chosen_skill = message.content.lower()
				for key, value in skill_dict.items():
					if key == chosen_skill:
						associated_ability = value
						print(f"associated_ability_score = {associated_ability}")
				for value in users[username]["ability scores"]:
						associated_ability_score = value
						return f"your {associated_ability} score is {associated_ability_score}."





# @reply_to_all(client) #tweede stukje code
# def check_wages(message):
# 	try:
# 		roll_result = int(message.content)
# 		if roll_result <= 9:
# 			return "a small gemstone worth 20 VP"
# 		elif roll_result >= 10 and roll_result <= 14:
# 			return "a medium gemstone worth 100 VP"
# 		elif roll_result >= 15 and roll_result <= 19:
# 			return "a large gemstone worth 200 VP"
# 		elif roll_result >= 20:
# 			return "a massive gemstone worth 250 VP"
# 	except:
# 		return


try:
  print("De bot is online.")
  client.run(TOKEN)
except Exception as e:
  print(e)
  os.system("kill 1")


# downtime_activities_list = ["Work"]

# work_type_list = ["Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History", "Insight", "Intimidation", "Medicine", "Nature", "Perception", "Performance", "Persuasion", "Religion", "Sleight of Hand", "Stealth", "Survival"]

# spelers = dict()

# ability_score_dictionary = {"Strength": 0, "Dexterity": 0, "Constitution": 0, "Intelligence": 0, "Wisdom": 0, "Charisma": 0}

# def check_wages(roll_result):
#   if roll_result <= 9:
#     return "a small gemstone worth 20 VP"
#   elif roll_result == 10 or 11 or 12 or 13 or 14:
#     return "a medium gemstone worth 100 VP"
#   elif roll_result == 15 or 16 or 17 or 18 or 19:
#     return "a large gemstone worth 200 VP"
#   elif roll_result >= 20:
#     return "a massive gemstone worth 250 VP"

# def work_roll (input):
#   if input == key:
#     return f"What is your {key.value} Dexterity modifier?"
#   elif input == "Animal Handling":
#     return "What is your Wisdom modifier?"
#   elif input == "Arcana":
#     return "What is your Intelligence modifier?"
#   elif input == "Athletics":
#     return "What is your Strength modifier?"
#   elif input == "Deception":
#     return "What is your Charisma modifier?"
#   elif input == "History":
#     return "What is your Intelligence modifier?"
#   elif input == "Insight":
#     return "What is your Wisdom modifier?"
#   elif input == "Intimidation":
#     return "What is your Charisma modifier?"
#   elif input == "Investigation":
#     return "What is your Intelligence modifier?"
#   elif input == "Medicine":
#     return "What is your Wisdom modifier?"
#   elif input == "Nature":
#     return "What is your Intelligence modifier?"
#   elif input == "Perception":
#     return "What is your Wisdom modifier?"
#   elif input == "Performance":
#     return "What is your Charisma modifier?"
#   elif input == "Persuasion":
#     return "What is your Charisma modifier?"
#   elif input == "Religion":
#     return "What is your Intelligence modifier?"
#   elif input == "Sleight of Hand":
#     return "What is your Dexterity modifier?"
#   elif input == "Stealth":
#     return "What is your Dexterity modifier?"
#   elif input == "Survival":
#     return "What is your Wisdom modifier?"
  
# spelers = ""
# spelernaam = message.author
# if message.author not in spelers: