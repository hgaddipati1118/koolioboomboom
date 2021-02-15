# bot.py
import os
import csv
import random
import ast
from Database import *
from cricketWriteups import *
from keep_alive import keep_alive
import discord
from dotenv import load_dotenv
from discord.ext import commands
import sqlite3
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='', self_bot=True)


makeTables()
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
Database = cursor.execute("SELECT teamName, userId FROM users").fetchall()

conn.commit()


def sum_list(items):
	sum_numbers = 0
	for x in items:
		sum_numbers += x
	return sum_numbers


class Game(object):
	def __init__(self, channelId, team1, team2, player1Id, player2Id, gameId):
		self.channelId = channelId
		self.player1 = player1Id
		self.player2 = player2Id
		self.gameId = gameId
		self.runs = 0
		self.bowlerNumber = 0
		self.userTurn = 0
		self.currentInningWickets = 0
		self.inning1Score = 0
		self.inning1Result = ""
		self.inning2Score = " "
		self.balls = 0
		self.innings = 1
		self.gameHappening = True
		self.coinToss = True
		self.tossDecision = True
		self.team1 = team1
		self.team2 = team2


#load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
games = []
userTurn = 0
bowlerNumber = 0
wickets = 0
gameStarted = False


def convertBoolToInt(value):
	if (value == True):
		return 1
	else:
		return 0


def convertIntToBool(value):
	if (int(value) == 1):

		return True
	else:
		return False

def sendGameList(gameList):
	games = gameList.copy()
	dataDump = []
	for n in range(len(games)):
		specificGame = games[n]

		gameHappening = convertBoolToInt(specificGame.gameHappening)
		coinToss = convertBoolToInt(specificGame.coinToss)
		tossDecision = convertBoolToInt(specificGame.tossDecision)
		dump = [
		    specificGame.channelId, specificGame.player1, specificGame.player2,
		    specificGame.gameId, specificGame.runs, specificGame.bowlerNumber,
		    specificGame.userTurn, specificGame.currentInningWickets,
		    specificGame.inning1Score, specificGame.inning1Result,
		    specificGame.balls, specificGame.innings, gameHappening, coinToss,
		    tossDecision, specificGame.team1, specificGame.team2
		]
		dataDump.append(dump)
	return dataDump


def sendGameValues(games):

	conn = sqlite3.connect('users.db', timeout=1)
	cursor = conn.cursor()
	cursor.execute('DELETE FROM games;', )
	dataDump = []
	for n in range(len(games)):
		specificGame = games[n]

		gameHappening = convertBoolToInt(specificGame.gameHappening)
		coinToss = convertBoolToInt(specificGame.coinToss)
		tossDecision = convertBoolToInt(specificGame.tossDecision)
		cursor.execute(
		    "insert into games (channelId, player1, player2, gameId, runs, bowlerNumber, userTurn, currentInningsWickets, inning1Score, inning1Result, balls, innings, gameHappening, coinToss, tossDecision, team1, team2) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
		    (specificGame.channelId, specificGame.player1,
		     specificGame.player2, specificGame.gameId, specificGame.runs,
		     specificGame.bowlerNumber, specificGame.userTurn,
		     specificGame.currentInningWickets, specificGame.inning1Score,
		     specificGame.inning1Result, specificGame.balls,
		     specificGame.innings, gameHappening, coinToss, tossDecision,
		     specificGame.team1, specificGame.team2))
		dump = [
		    specificGame.channelId, specificGame.player1, specificGame.player2,
		    specificGame.gameId, specificGame.runs, specificGame.bowlerNumber,
		    specificGame.userTurn, specificGame.currentInningWickets,
		    specificGame.inning1Score, specificGame.inning1Result,
		    specificGame.balls, specificGame.innings, gameHappening, coinToss,
		    tossDecision, specificGame.team1, specificGame.team2
		]
		dataDump.append(dump)

		conn.commit()
	filename = "games.csv"

	# writing to csv file
	with open(filename, 'w') as csvfile:
		# creating a csv writer object
		csvwriter = csv.writer(csvfile)

		# writing the fields

		# writing the data rows
		csvwriter.writerows(dataDump)
	conn.commit()
	conn.close()


def importGameValues():
	conn = sqlite3.connect('users.db', timeout=1)
	cursor = conn.cursor()
	gameData = cursor.execute(
	    "SELECT channelId, player1, player2, gameId, runs, bowlerNumber, userTurn, currentInningsWickets, inning1Score, inning1Result, balls, innings, gameHappening, coinToss, tossDecision, team1, team2 FROM games"
	).fetchall()

	games = []
	for n in range(len(gameData)):
		currentGame = gameData[n]
		dump = Game(currentGame[0], currentGame[15], currentGame[16],
		            currentGame[1], currentGame[2], currentGame[3])
		dump.runs = currentGame[4]
		dump.bowlerNumber = currentGame[5]
		dump.userTurn = currentGame[6]
		dump.currentInningWickets = currentGame[7]
		dump.inning1Score = currentGame[8]
		dump.inning1Result = currentGame[9]
		dump.balls = currentGame[10]
		dump.innings = currentGame[11]
		dump.gameHappening = convertIntToBool(currentGame[12])

		dump.coinToss = convertIntToBool(currentGame[13])
		dump.tossDecision = convertIntToBool(currentGame[14])
		games.append(dump)
	conn.commit()
	conn.close()
	return games


def turnGamesListBack(games):
	gameData = games.copy()
	gameList = []
	for n in range(len(gameData)):
		currentGame = gameData[n]
		print (currentGame)
		dump = Game(
		    int(currentGame[0]), currentGame[15], currentGame[16],
		    int(currentGame[1]), int(currentGame[2]), int(currentGame[3]))
		dump.runs = int(currentGame[4])
		dump.bowlerNumber = int(currentGame[5])
		dump.userTurn = int(currentGame[6])
		if(currentGame[7] == ''):
			currentGame[7] = 0
		dump.currentInningWickets = int(currentGame[7])
		dump.inning1Score = int(currentGame[8])
		dump.inning1Result = currentGame[9]
		dump.balls = int(currentGame[10])
		dump.innings = int(currentGame[11])

		dump.gameHappening = convertIntToBool(currentGame[12])

		dump.coinToss = convertIntToBool(currentGame[13])
		dump.tossDecision = convertIntToBool(currentGame[14])
		gameList.append(dump)

	return gameList


@client.event
async def on_ready():

	print(f'{client.user.name} has connected to Discord!')

  

@client.event
async def on_member_join(member):
	await member.create_dm()
	await member.dm_channel.send(f'Hi {member.name}, welcome to Fake Cricket!')


@client.event
async def on_message(message):
	# we do not want the bot to reply to itself
	if message.author == client.user:
		return

	# can be cached...


@client.event
async def on_message(message):
	global gameStarted
	global userTurn
	global bowlerNumber
	games = importGameValues()
	if "duck" == message.content:
		await message.channel.send(":duck:")
		return
	if message.author == client.user:
		return
	if message.content == "kill bot":
		await client.close()
		return

	if(len(games)>0):
			channel = client.get_channel(776503505157619722)
			thingToPush = sendGameList(games)
			stringOutput = "["
			for n in range(len(thingToPush)):
				stringOutput += "["
				for g in range(len(thingToPush[n])):
					stringOutput += '"'
					stringOutput += str(thingToPush[n][g])
					stringOutput += '"'
					if g != (len(thingToPush[n])-1):
						stringOutput += ","
				stringOutput +="]"
				if n != (len(thingToPush)-1):
					stringOutput+=","
			stringOutput +="]"
			print(stringOutput)
			for n in range(int(len(stringOutput)/1000)+1):
				start = n*1000
				end = (n+1)*1000
				if(end>len(stringOutput)):
					end = len(stringOutput)
				await channel.send(stringOutput[start:end])
	if "?import game list" in message.content:
		gameData = message.content.replace("?import game list","")

		mylist = ast.literal_eval(gameData)
		print(mylist)
		games = turnGamesListBack(mylist)
		sendGameValues(games)
		await message.channel.send("Game List changed")
		return

	isMod = False
	conn = sqlite3.connect('users.db', timeout=1)
	cursor = conn.cursor()

	Database = cursor.execute("SELECT teamName, userId FROM users").fetchall()
	conn.commit()

	for n in range(len(ModIds)):
		if message.author.id == ModIds[n]:
			isMod = True
	if "Kill bot" in message.content:
		if isMod == True:
			client.logout()
	user = client.get_user(706698513710579762)
	if "delete games" in message.content:
		await message.channel.send("games deleted")
		games = []
		sendGameValues(games)
		return
	if "badoom" in message.content:
		games = [["775439156728823860","432286179195617280","701221250776825856","0","51","26","0","3","80","80/4 (9.6)","37","2","1","0","0","Carolina Cricketeers","Vienna Austrians"],["775439173057511434","534010044182822914","256431620729470976","1","88","27","0","1","92"," (92/1)","60","2","0","0","0","  Army Black Knights","  North Sydney Bears"],["775439203579986001","202273074261917697","144969605977341953","2","93","41","0","1","91","91/2 (9.6)","57","2","0","0","0","Red Star Laos","Chesire"],["775439257053429760","129120653948223488","409350943788892160","3","47","33","0","1","41","41/5 (4.6)","23","2","0","0","0","Connacht Cricket","Austin Bats"],["775439270672334848","105545186028822528","500805562376650758","4","60","19","0","5","112","112/4 (9.6)","36","2","0","0","0","Honolulu Hornets","Sydney Sixers"],["775439286245916692","237234603981537280","185900072234385408","5","69","20","0","5","87","87/4 (9.6)","35","2","0","0","0","Calcutta Curry","Tallinn Tall Estonians"],["775439300765679686","517933512171585537","306609698340339714","6","88","28","0","0","98","98/2(9.6)","60","2","0","0","0","New Delhi Superstars","Hamrun Knights"],["775439325714317363","391151653358665728","280100750523236352","7","48","25","0","5","81","81/4 (9.6)","40","2","0","0","0","San Antonio Cricket Club","Brisbane Heat"],["775439338582179841","706698513710579762","715243714003337296","8","52","37","0","5","94","94/3 (9.6)","33","2","0","0","0","Super 11","Sunrisers Hyderabad"],["775439352712790028","244161099337957376","340541260672532482","9","70","19","0","3","69","69/4 (9.6)","51","2","0","0","0"," Omaha Union"," Rotterdam Rhinos"],["775439413550514226","693027263062474782","326553566909300737","10","86","39","0","2","83","83/4 (9.6)","44","2","0","0","0","Burnt Pine Mutineers","Mornington Wombats"],["775439430361677825","501849193338503168","293778672807182336","11","74","22","0","3","0","","42","1","1","0","0","Flipping Flyers","Pakistani Falcons"],["775439441380507648","205443196401090561","473181824516882432","12","67","48","0","5","67","67/2 (9.6)","55","2","0","0","0","Thermopylae Mediterraneans","Wollongong Warriors"],["775439455687409746","352849361920851968","309625595854323712","13","68","25","0","3","66","66/5 (7.1)","44","2","0","0","0","Royal Rumblers","Tajikistan Royals"],["792392593886412800","495544574358323200","524251268437245952","16","19","16","0","0","0","","9","1","1","0","0","Sri Lanka Hurricanes","Canada"],["792392533858713612","712732591177990228","733552144505897020","15","2","50","0","0","0","","2","1","1","0","0","RCB","San Jose Nuggets"]]
		
		sendGameValues(turnGamesListBack(games))
	if "resume games" in message.content:

		for n in range(len(games)):
     
			currentGame = games[n]
	

			if (currentGame.gameHappening != True):

				break
			elif (currentGame.coinToss == True):
				channel = client.get_channel(currentGame.channelId)
				output = "<@!" + str(
				    currentGame.player1) + ">,please calls heads or tail"
				await channel.send(output)

			elif (currentGame.tossDecision == True):
				channel = client.get_channel
				(currentGame.channelId)
				output = "<@!" + str(
				    currentGame.player1) + ">,please choose to bowl or bat"
				await channel.send(output)
				return
			else:
				if currentGame.userTurn == 0:
					userId = currentGame.player2
					await client.wait_until_ready()
					user = client.get_user(int(userId))
					print(userId)
					print(user)
          
					#await user.send("Put in bowler number")
				else:
					channel = client.get_channel(currentGame.channelId)
					output = "<@!" + str(currentGame.player1) + ">, please input Swing Number"
					await channel.send(output)

	if message.author == client.user:
		return
	if "?add user" in message.content:
		if isMod == True:
			text = message.content.lower()
			text = text.replace("?add user", "")
			playerInfo = text.split(',')
			playerInfo[0] = str(playerInfo[0])
			playerInfo[1] = int(playerInfo[1])
			await message.channel.send(playerInfo)
			Database = cursor.execute(
			    "SELECT teamName, userId FROM users").fetchall()

			playerInDatabase = False
			for n in range(len(Database)):
				if playerInfo[1] == Database[n][1]:
					Database[n][0] == playerInfo
					playerInDatabase = True
					newTeamName = playerInfo[0]
					playerId = playerInfo[1]
					cursor.execute(
					    "UPDATE users SET teamName = ? WHERE userId = ?",
					    (newTeamName, playerId))
					await message.channel.send("Player Team Changed")
			if playerInDatabase == False:
				conn = sqlite3.connect('users.db', timeout=1)
				cursor = conn.cursor()
				input = "INSERT INTO users VALUES ('" + playerInfo[
				    0] + "'," + str(playerInfo[1]) + ")"
				await message.channel.send(input)
				cursor.execute(input)
				await message.channel.send("Player Added")
				conn.commit()

		return

	if "?start game," in message.content:
		print("Here")
		for n in range(len(games)):
			if games[n].channelId == message.channel.id:
				if games[n].gameHappening == True:
					await message.channel.send("Channel is in use")
					return
		text = message.content.lower()
		text = text.replace("?start game", "")
		players = text.split(',')
		team1 = ""
		team2 = ""

		print("Here")
		for n in range(len(players)):
			for x in range(len(Database)):

				player = Database[x][0].lower()
				if player in players[n]:
					if team1 == "":
						team1 = Database[x][1]
						team1Name = Database[x][0]
					else:
						team2 = Database[x][1]
						team2Name = Database[x][0]
		if team1 == "" or team2 == "":
			await message.channel.send("One of those teams doesn't exist")
			print(Database)
			return
		for n in range(len(games)):
			if (team1 == games[n].player1 or team1 == games[n].player2
			    or team2 == games[n].player1 or team2 == games[n].player2):
				if games[n].gameHappening == True:
					await message.channel.send(
					    "One of the teams is already in a game")
					return
		newGame = Game(message.channel.id, team1Name, team2Name, team1, team2,len(games))

		await message.channel.edit(name=(team1Name + " vs. " + team2Name))
		output = "<@!" + str(newGame.player1) + ">,please calls heads or tail"
		await message.channel.send(output)
		games.append(newGame)
   
		sendGameValues(games)
		return
	isInGame = False
	currentGameId5 = -1
	for n in range(len(games)):
		if (message.channel.id == games[n].channelId):
			isInGame = True
			currentGameId5 = n
	print(currentGameId5)
	print(len(games))
	if (currentGameId5 != -1):
		currentGame = games[currentGameId5]

	if isInGame == True:
		if "?waitingon" in message.content:
			if currentGame.coinToss == 1:
				output = "waiting on <@!" + str(currentGame.player1) + ">	to call heads or tails"
				await message.channel.send(output)
				return
			if currentGame.tossDecision == 1:
				output = "waiting on <@!" + str(currentGame.player1) + ">	to choose to bowl or bat"
				await message.channel.send(output)
			if currentGame.userTurn == 0:
				output = "waiting on <@!" + str(currentGame.player2) + ">	to dm bot bowler number"
				await message.channel.send(output)
			if currentGame.userTurn == 1:
				output = "waiting on <@!" + str(currentGame.player1) + "> to put swing number"
				await message.channel.send(output)
			return
	isInGame = False
	currentGameId = -1

	for n in range(len(games)):
		if (message.author.id == games[n].player1
		    or message.author.id == games[n].player2):
			isInGame = True
			currentGameId = n

	
	if currentGameId != -1:
		currentGame = games[currentGameId]
	print("hi")
	if "end game" == message.content:
		print("hi")
		if isMod == True:
			currentGame.gameHappening = False
			if(currentGameId5 == -1):
				await message.channel.send("No game in progess")
				return
			await message.channel.send("Game Ended")
			games.pop(currentGameId5)
			sendGameValues(games)
			return
	if "print game data" in message.content:
		isInGame2 = False
		currentGameId2 = -1
		print (games)
		for n in range(len(games)):
			print(n)
			print(games[n].channelId)
			if (message.channel.id == games[n].channelId):
				isInGame2 = True
				currentGameId2 = n
		if(isInGame2 == False):
				await message.channel.send("No game available")
				return
		currentGame = games[currentGameId2]
		dump = [
		    currentGame.channelId, currentGame.player1, currentGame.player2,
		    currentGame.gameId, currentGame.runs, currentGame.bowlerNumber,
		    currentGame.userTurn, currentGame.currentInningWickets,
		    currentGame.inning1Score, currentGame.inning1Result,
		    currentGame.balls, currentGame.innings, convertBoolToInt(currentGame.gameHappening), convertBoolToInt(currentGame.coinToss),
		    convertBoolToInt(currentGame.tossDecision), currentGame.team1, currentGame.team2
		]
		await message.channel.send(dump)
		return	
	if "?edit game data" in message.content:
		if isMod == True:
			isInGame2 = False
			currentGameId2 = -1

			for n in range(len(games)):
				print(n)
				print(games[n].channelId)
				if (message.channel.id == games[n].channelId):
					isInGame2 = True
					currentGameId2 = n
			if(isInGame2 == False):
					await message.channel.send("No game available")
					return
			currentGame = games[currentGameId2]
			text = message.content
			text = text.replace("?edit game data", "")
			gameDataInput = text.split(',')
			dump = Game(
	    	int(gameDataInput[0]), gameDataInput[15], gameDataInput[16],
		    int(gameDataInput[1]), int(gameDataInput[2]), int(gameDataInput[3]))
			dump.runs = int(gameDataInput[4])
			dump.bowlerNumber = int(gameDataInput[5])
			dump.userTurn = int(gameDataInput[6])
			dump.currentInningWickets = int(gameDataInput[7])	
			dump.inning1Score = int(gameDataInput[8])
			dump.inning1Result = gameDataInput[9]
			dump.balls = int(gameDataInput[10])
			dump.innings = int(gameDataInput[11])				
			dump.gameHappening = convertIntToBool(gameDataInput[12])
			dump.coinToss = convertIntToBool(gameDataInput[13])
			dump.tossDecision = convertIntToBool(gameDataInput[14])
			games[currentGameId2] = dump
			sendGameValues(games)
			await message.channel.send("Game edited")
			return
	if currentGameId != -1:
		currentGame = games[currentGameId]

	if currentGame.gameHappening == False:
		return

	if message.channel.id != currentGame.channelId and not isinstance(
	    message.channel, discord.DMChannel):
		return
	if currentGame.coinToss == True:

		if message.author.id != currentGame.player1:
			return
		if message.content.lower() == "heads" or message.content.lower(
		) == "tails":
			coinToss = random.randint(0, 1)
			calledToss = 1
			currentGame.coinToss = False
			if (message.content.lower() == "heads"):
				calledToss = 0
			if (coinToss == calledToss):
				output = "<@!" + str(
				    currentGame.player1) + ">,please choose to bowl or bat"

				await message.channel.send(output)
				sendGameValues(games)
				return
			else:
				newPlayer2 = currentGame.player1
				newPlayer1 = currentGame.player2
				currentGame.player1 = newPlayer1
				currentGame.player2 = newPlayer2
				newTeam1 = currentGame.team2
				newTeam2 = currentGame.team1
				currentGame.team1 = newTeam1
				currentGame.team2 = newTeam2
				output = "<@!" + str(
				    currentGame.player1) + ">,please choose to bowl or bat"

				await message.channel.send(output)
				sendGameValues(games)
				return

		else:
			await message.channel.send("please calls heads or tails")
			return

		return
	if currentGame.tossDecision == True:
		if (message.author.id != currentGame.player1):
			return
		if message.content.lower() == "bowl" or message.content.lower(
		) == "bat":
			currentGame.tossDecision = False
			if (message.content.lower() == "bowl"):
				newPlayer2 = currentGame.player1
				newPlayer1 = currentGame.player2
				currentGame.player1 = newPlayer1
				currentGame.player2 = newPlayer2
				newTeam1 = currentGame.team2
				newTeam2 = currentGame.team1
				currentGame.team1 = newTeam1
				currentGame.team2 = newTeam2

			user = client.get_user(currentGame.player2)
			sendGameValues(games)
			await user.send("Please input bowler number")
		else:
			await message.channel.send("please choose to bowl or bat")
			return
		return
	if currentGame.userTurn == 0 and isinstance(message.channel,discord.DMChannel):
		if message.content.isnumeric():
			if int(message.content) > 50 or int(message.content) < 1:
				await message.channel.send("Put a number 1-50")
				return
			currentGame.bowlerNumber = int(message.content)
		else:
			await message.channel.send("please input a number")
			return
		channel = client.get_channel(currentGame.channelId)
		output = "<@!" + str(
		    currentGame.player1) + ">,please input Swing Number"
		await channel.send(output)
		await message.channel.send("Your number "+ message.content+ " has been submitted")
		currentGame.userTurn = 1
		sendGameValues(games)
		return
	if currentGame.userTurn == 1 and message.channel.id == currentGame.channelId and message.author.id == currentGame.player1:

		global wickets
		if message.content.isnumeric():
			if int(message.content) > 50 or int(message.content) < 1:
				await message.channel.send("Put a number 1-50")
				return
			writeup = ""
			output = ""
			response = abs(int(message.content) - currentGame.bowlerNumber)
			if response > 25:
				response = 50 - response
			if response < 2:
				writeup = sixWriteups[random.randint(0, len(sixWriteups) - 1)]
				output = "Six!"
				currentGame.runs += 6
			elif response < 5:
				output = "Four"
				writeup = fourWriteups[random.randint(0,
				                                      len(fourWriteups) - 1)]
				currentGame.runs += 4

			elif response < 6:
				output = "Three"
				currentGame.runs += 3
				writeup = threeWriteups[random.randint(0,
				                                       len(threeWriteups) - 1)]
			elif response < 9:
				output = "Two"
				currentGame.runs += 2
				writeup = twoWriteups[random.randint(0, len(twoWriteups) - 1)]
			elif response < 15:
				output = "One"
				currentGame.runs += 1
				writeup = oneWriteups[random.randint(0, len(oneWriteups) - 1)]
			elif response < 24:
				output = "Dot"
				currentGame.runs += 0
				writeup = dotBallWriteups[random.randint(
				    0,
				    len(dotBallWriteups) - 1)]
			else:
				output = "Wicket"
				currentGame.runs += 0
				currentGame.currentInningWickets += 1
				writeup = wicketWriteups[random.randint(
				    0,
				    len(wicketWriteups) - 1)]
				# can be cached..
			currentGame.balls += 1
			overs = int((currentGame.balls - 1) / 6)
			balls = currentGame.balls % 6
			if balls == 0:
				balls = 6

			runs = currentGame.runs
			currentGame.userTurn = 0
			currentScore = writeup + "\n" + output + "\n" + "Bowler number: " + str(
			    currentGame.bowlerNumber) + "\n" + "Batter number: " + str(
			        int(message.content)) + "\n" + "Difference: " + str(
			            response) + "\n" + str(overs) + "." + str(
			                balls) + "  " + str(runs) + "/" + str(
			                    currentGame.currentInningWickets)
			currentScore += "\n" + "Run Rate:" + str(
			    round(6 * runs / currentGame.balls, 2))
			if (currentGame.innings == 2 and 60 > currentGame.balls):
				currentScore += "\n" + "Runs Needed:" + str(
				    1 + currentGame.inning1Score - runs)
				print(currentGame.balls)
				currentScore += "\n" + "Required Run Rate:" + str(
				    round(
				        6 * (1 + currentGame.inning1Score - runs)/(60 - currentGame.balls), 2))
			await message.channel.send(currentScore)

			if (currentGame.innings == 1):
				if (currentGame.balls >= 60
				    or currentGame.currentInningWickets >= 5):
					await message.channel.send("Innings is over, " +str(runs) + " runs scored")
					user = client.get_user(currentGame.player2)
					await user.send("Innings is over")
		
					currentGame.inning1Result = str(runs) + "/" + str(
					    currentGame.currentInningWickets) + " (" + str(
					        overs) + "." + str(balls) + ")"
					currentGame.innings = 2
					currentGame.inning1Score = runs
					currentGame.balls = 0
					currentGame.currentInningWickets = 0
					newPlayer2 = currentGame.player1
					newPlayer1 = currentGame.player2
					currentGame.player1 = newPlayer1
					currentGame.player2 = newPlayer2
					sendGameValues(games)
					currentGame.runs = 0
			else:
				if (currentGame.balls >= 60
				    or currentGame.currentInningWickets >= 5
				    or runs > currentGame.inning1Score):
					innings2Result = str(runs) + "/" + str(
					    currentGame.currentInningWickets) + " (" + str(
					        overs) + "." + str(balls) + ")"
					if (runs > currentGame.inning1Score):
						await message.channel.send(currentGame.team2 + " wins by" + str(5 - currentGame.currentInningWickets) +" wickets")
						user = client.get_user(currentGame.player2)
						await user.send("Innings is over")
						await message.channel.send(currentGame.team1 + ": " +
						                           currentGame.inning1Result)
						await message.channel.send(currentGame.team2 + ": " +
						                           innings2Result)

					else:
						await message.channel.send(
						    currentGame.team1 + " wins by" +
						    str(currentGame.inning1Score - runs) + " runs")
						await message.channel.send(currentGame.team1 + ": " +
						                           currentGame.inning1Result)
						await message.channel.send(currentGame.team2 + ": " +
						                           innings2Result)
					currentGame.gameHappening = False
					sendGameValues(games)
					return

			user = client.get_user(currentGame.player2)
			print(currentGame.player2)
			sendGameValues(games)
			await channel.send(output)
			output = "<@!" + str(currentGame.player2) + ">,please dm bot bowler number"
			print(user)
			print(user == "none")
		 
			await user.send(currentScore)
			await user.send("Put in bowler number")
			
			


client.run(TOKEN)
