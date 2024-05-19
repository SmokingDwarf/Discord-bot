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
skill_dict = {
	"acrobatics": "dexterity", 
	"animal handling": "wisdom"
}

@reply_to_all(client)
def send_message(message):
	'''Function that responds to messages, 
	and checks if user exists or not.
	if not, then create and add new user to json'''
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
			print("de fout ligt op lijn 66")
			users[username] = {}
			users[username] = {
				"new_user_state" : True, 
				"initialize_state" : False, 
				"confirm_name_state" : False, 
				"activity_asking_state" : False, 
				"skill_asking_state" : False, 
				"roll_state" : False, 
				"name_query_state" : False,
				"ability_scores" : {},
				"skill_proficiencies" : {}
			}
			return f"Welcome, new adventurer! What is your character's name?"

# def update_info():
	# with open ("discord_bot_users.json", "w") as file:
	# 	file.write(json.dumps(users, indent=4))

def state_func(message):
	'''This function checks which states are on, 
	and then executes the associated function.'''
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
	'''Welcome returning user and ask user to select an activity from activity_list'''
	users[username]["initialize_state"] = False
	users[username]["activity_asking_state"] = True
	return f"Hello {users[username]['name']}! Select a downtime activity from: {', '.join(activity_list)}."

def register_new_user(message):
	'''Set the user's message as their new name, and confirm the name with the user.'''
	users[username] = {"name" : message.content.capitalize(), "associated_ability" : None, "associated_ability_score" : None, "chosen_skill" : None, "ability_modifier" : None, "proficiency_die_result" : None, "d20_result" : None, "register_new_user" : None, "register_new_user" : False, "confirm_name_state" : True}
	return f'You have entered the character name: {users[username]["name"]}. Please confirm that this is your character name. Select confirm or cancel.'

def confirm_name(message):
	'''Geef de naam terug en check met de user of de naam correct is. Ga daarna verder.'''
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
		
		skill = message.content.lower()
		users[username]["chosen_skill"] = skill
		ability = skill_dict[skill]
		score = get_ability_score(skill)

		is_proficient = users[username]["skill proficiencies"][skill]

		if is_proficient:
			users[username]["roll_state"] = True
			return f"{skill.capitalize()} is a {ability.capitalize()} skill. Your {ability.capitalize()} score is {score}. You are proficient with {skill}. Please type 'roll' to proceed, or 'cancel' to return to skill selection."
		
		else:
			users[username]["roll_state"] = True
			return f"{skill.capitalize()} is a {ability.capitalize()} skill. Your {ability.capitalize()} score is {score}. You are not proficient with {skill}. Please type 'roll' to proceed, or 'cancel' to return to skill selection."
	
	else:
		return f"Please select from: {', '.join(list(skill_dict.keys()))}."

def get_ability_score(skill):
	ability = skill_dict[skill]
	score = users[username]["ability_scores"][ability]
	return score

def roll_query(message):	
	if "roll" in message.content.lower() and "cancel" not in message.content.lower():
		users[username]["roll_state"] = False
		skill = users[username]["chosen_skill"]
		score = get_ability_score(skill)
		
		if users[username]["skill proficiencies"][skill] == True:
			check_result = proficient_skill_check(score)	
			return f'You rolled a {check_result}! Your reward is {check_wages(check_result)}.'
		
		elif users[username]["skill proficiencies"][skill] == False:
			check_result = not_proficient_skill_check(score)
			return f'You rolled a {check_result}! Your reward is {check_wages(check_result)}.'
		
	elif "cancel" in message.content.lower() and "roll" not in message.content.lower():
		users[username]["chosen_skill"] = None
		users[username]["roll_state"] = False
		users[username]["skill_asking_state"] = True
		return f"Select a skill from {', '.join(list(skill_dict.keys()))}."
	
	else:
		return f"Please select roll or cancel."

def get_ability_modifier(score):
	'''Return an ability modifier based on a formula that uses an ability score.'''
	return math.floor((score - 10) / 2)

def get_proficiency_die():
	'''Determine the proficiency die based on player level, 
	then return a number between 1 and the maximum of the appropriate die.'''
	level = users[username]["level"]
	proficiency_die = (math.ceil(1 + level / 4) * 2)
	return random.randint(1, proficiency_die)

def get_d20_die():
	'''Return a random number between 1 and 20'''
	return random.randint(1, 20)

def proficient_skill_check(score):
	d20_result = get_d20_die()
	ability_modifier = get_ability_modifier(score)
	proficiency_die_result = get_proficiency_die()
	return d20_result + ability_modifier + proficiency_die_result

def not_proficient_skill_check(score):
	d20_result = get_d20_die()
	ability_modifier = get_ability_modifier(score)
	return d20_result + ability_modifier

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

