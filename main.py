import discord # type: ignore
import os
import json
import discord_user
import math
import random
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
proceed_state = False

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
	global proceed_state
	username = str(message.author)
	
	if message.content and message.channel.name == 'michs-bot':
		with open ("discord_bot_users.json", "r") as file:
			users = json.load(file)
		
		if initialize_state == True:
			initialize_state = False
			for key, value in users.items():
				
				if key == username:
					activity_asking_state = True
					return f"Hello {(users[key]["name"])}! Select a downtime activity from: {', '.join(activity_list)}."
				
				elif key is not username:
					new_user_state == True
					return f"Welcome, new adventurer! What is your name?"
		
		elif activity_asking_state == True:
			
			if "work" in message.content.lower():
				activity_asking_state = False
				skill_asking_state = True
				return f"Great. Select a skill from {', '.join(list(skill_dict.keys()))}."
			
			else:
				return f"Please select from: {', '.join(activity_list)}."
		
		elif skill_asking_state == True:
			if message.content.lower() in skill_dict:
				skill_asking_state = False
				chosen_skill = message.content.lower()
				
				for key, value in skill_dict.items():
					if key == chosen_skill:
						associated_ability = value
				
				associated_ability_score = users[username]["ability scores"][associated_ability]
				
			

				if users[username]["skill proficiencies"][chosen_skill] == True:
					proceed_state = True
					return f"{chosen_skill.capitalize()} is a {associated_ability} skill. Your {associated_ability} score is {associated_ability_score}. You are proficient with {chosen_skill}. Confirm? (confirm/cancel)"
				
				elif users[username]["skill proficiencies"][chosen_skill] == False:
					proceed_state = True
					return f"{chosen_skill.capitalize()} is a {associated_ability} skill. Your {associated_ability} score is {associated_ability_score}. You are not proficient with {chosen_skill}. Confirm? (confirm/cancel)"
			
			else:
				return f"Please select from: {', '.join(list(skill_dict.keys()))}."

		elif proceed_state == True:
			if message.content.lower() == "confirm":
				proceed_state = False

			elif message.content.lower() == "cancel":
				proceed_state = False

			else:
				return f"Please select confirm or cancel."

	def get_ability_modifier(ability_score):	
		ability_modifier = math.floor((ability_score - 10) / 2)

	def get_proficiency_die():
		level = users[username]["level"]
		proficiency_die = (math.ceil(1 + level / 4) * 2)
		proficiency_die_result = random.randint(1, proficiency_die)


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



# def check_wages(roll_result):
#   if roll_result <= 9:
#     return "a small gemstone worth 20 VP"
#   elif roll_result == 10 or 11 or 12 or 13 or 14:
#     return "a medium gemstone worth 100 VP"
#   elif roll_result == 15 or 16 or 17 or 18 or 19:
#     return "a large gemstone worth 200 VP"
#   elif roll_result >= 20:
#     return "a massive gemstone worth 250 VP"
  
# spelers = ""
# spelernaam = message.author
# if message.author not in spelers: