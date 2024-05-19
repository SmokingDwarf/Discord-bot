import discord # type: ignore
import os
import json
import discord_user
import math
import random
from random import randint, choice
with open ("discord_bot_users.json", "r") as file:
			users = json.load(file)

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

#Lists & dicts
activity_list = ["work"]
skill_dict = {"acrobatics": "dexterity", "animal handling": "wisdom"}

@reply_to_all(client)
def send_message(message):
	global users
	global username
	username = str(message.author)
	
	if message.content and message.channel.name == 'michs-bot':
		
		for key, value in users.items():	
			if key == username:
				run_program = state_func(message)
				# update_info()
				return run_program
		
		if username not in users:
			users[username] = {}
			users[username] = {"new_user_state" : True, "initialize_state" : False, "confirm_name_state" : False, "activity_asking_state" : False, "skill_asking_state" : False, "roll_state" : False, "name_query_state" : False}
			return f"Welcome, new adventurer! What is your character's name?"

# def update_info():
	# with open ("discord_bot_users.json", "w") as file:
	# 	file.write(json.dumps(users, indent=4))

def state_func(message):
	if users[username]["initialize_state"] == True:
		return initialize()
	
	elif users[username]["new_user_state"] == True:
		return register_new_user(message)

	elif users[username]["confirm_name_state"] == True:
		return confirm_name(message)

	elif users[username]["name_query_state"] == True:
		return name_query(message)

	elif users[username]["activity_asking_state"] == True:
		return activity_query(message)

	elif users[username]["skill_asking_state"] == True:
		return skill_query(message)

	elif users[username]["roll_state"] == True:
		return roll_query(message)

def initialize():	
	users[username]["initialize_state"] = False
	users[username]["activity_asking_state"] = True
	return f"Hello {users[username]['name']}! Select a downtime activity from: {', '.join(activity_list)}."

def register_new_user(message):
	users[username] = {"name" : message.content.capitalize(), "associated_ability" : None, "associated_ability_score" : None, "chosen_skill" : None, "ability_modifier" : None, "proficiency_die_result" : None, "d20_result" : None, "register_new_user" : None, "register_new_user" : False, "confirm_name_state" : True}
	return f'You have entered the character name: {users[username]["name"]}. Please confirm that this is your character name. Select confirm or cancel.'


def confirm_name(message):
	if "confirm" in message.content.lower():
		users[username]["confirm_name_state"] = False
		users[username]["initialize_state"] = True
		# Continue

	elif "cancel" in message.content.lower():
		users[username]["name"] = None
		users[username]["confirm_name_state"] = False
		users[username]["name_query_state"] = True
		return f"Please enter your character's name."
	else:
		return f'Please select confirm or cancel.'

def name_query(message):
	users[username]["name"] = message.content.capitalize()
	users[username]["confirm_name_state"] = True
	users[username]["name_query_state"] = False
	return f'You have entered the character name: {users[username]["name"]}. Please confirm that this is your character name. Select confirm or cancel.'

def activity_query(message):
	if message.content.lower() in activity_list:
		users[username]["activity_asking_state"] = False
		users[username]["skill_asking_state"] = True
		return f"Great. Select a skill from {', '.join(list(skill_dict.keys()))}."
		
	else:
		return f"Please select from: {', '.join(activity_list)}."

def skill_query(message):
	if message.content.lower() in skill_dict:
		users[username]["skill_asking_state"] = False
		users[username]["chosen_skill"] = message.content.lower()
			
		for key, value in skill_dict.items():
			if key == users[username]["chosen_skill"]:
				users[username]["associated_ability"] = value
				users[username]["associated_ability_score"] = users[username]["ability scores"][users[username]["associated_ability"]]
				
				if users[username]["skill proficiencies"][users[username]["chosen_skill"]] == True:
					users[username]["roll_state"] = True
					return f"{users[username]['chosen_skill'].capitalize()} is a {users[username]['associated_ability']} skill. Your {users[username]['associated_ability']} score is {users[username]['associated_ability_score']}. You are proficient with {users[username]['chosen_skill']}. Ready? Please type roll or cancel."
				
				elif users[username]["skill proficiencies"][users[username]["chosen_skill"]] == False:
					users[username]["roll_state"] = True
					return f'{users[username]["chosen_skill"].capitalize()} is a {users[username]["associated_ability"]} skill. Your {users[username]["associated_ability"]} score is {users[username]["associated_ability_score"]}. You are not proficient with {users[username]["chosen_skill"]}. Ready? Please type roll or cancel.'
		
		else:
			return f"Please select from: {', '.join(list(skill_dict.keys()))}."

def roll_query(message):	
	if "roll" in message.content.lower() and "cancel" not in message.content.lower():
		users[username]["roll_state"] = False
		
		if users[username]["skill proficiencies"][users[username]["chosen_skill"]] == True:
			check_result = proficient_skill_check()
			wages = check_wages(check_result)
			return f'The result of your roll is d20 ({users[username]["d20_result"]}) + your {users[username]["associated_ability"]} modifier ({users[username]["ability_modifier"]}) + your proficiency die ({users[username]["proficiency_die_result"]}) = {check_result}! Your reward is {wages}.'
		
		elif users[username]["skill proficiencies"][users[username]["chosen_skill"]] == False:
			check_result = not_proficient_skill_check()
			check_wages(check_result)
			return f'The result of your roll is d20 ({users[username]["d20_result"]}) + your {users[username]["associated_ability"]} modifier ({users[username]["ability_modifier"]}) = {check_result}! Your reward is {wages}.'
		
	elif "cancel" in message.content.lower() and "roll" not in message.content.lower():
		users[username]["roll_state"] = False
		users[username]["activity_asking_state"] = True
		return f"Select a downtime activity from: {', '.join(activity_list)}."
	
	else:
		return f"Please select roll or cancel."

def get_ability_modifier(ability_score):	
	return math.floor((ability_score - 10) / 2)

def get_proficiency_die():
	level = users[username]["level"]
	proficiency_die = (math.ceil(1 + level / 4) * 2)
	return random.randint(1, proficiency_die)

def get_d20_die():
	return random.randint(1, 20)

def proficient_skill_check():
	users[username]["d20_result"] = get_d20_die()
	users[username]["ability_modifier"] = get_ability_modifier(users[username]["associated_ability_score"])
	users[username]["proficiency_die_result"] = get_proficiency_die()
	return users[username]["d20_result"] + users[username]["ability_modifier"] + users[username]["proficiency_die_result"]

def not_proficient_skill_check():
	users[username]["d20_result"] = get_d20_die()
	users[username]["ability_modifier"] = get_ability_modifier(users[username]["associated_ability_score"])
	return users[username]["d20_result"] + users[username]["ability_modifier"]

def check_wages(check_result):
	if check_result <= 5:
		return f"a small, uncut gemstone worth 10 VP"
	elif check_result >= 5 and check_result <= 9:
		return f"a small, cut gemstone worth 25 VP"
	elif check_result >= 10 and check_result <= 14:
		return f"a medium, uncut gemstone worth 50 VP"		
	elif check_result >= 15 and check_result <= 19:			
		return f"a medium, cut gemstone worth 100 VP"
	elif check_result >= 20 and check_result <= 24:
		return f"a large, uncut gemstone worth 250 VP"
	elif check_result >= 25:
		return f"a large, cut gemstone worth 500 VP"


try:
  print("De bot is online.")
  client.run(TOKEN)
except Exception as e:
  print(e)
  os.system("kill 1")

