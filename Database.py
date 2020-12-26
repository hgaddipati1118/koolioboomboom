"""
Created on Sat Oct 31 15:59:56 2020

@author: Harsha Gaddipati
"""
import sqlite3

def makeTables():
  
  conn = sqlite3.connect('users.db')
  cursor = conn.cursor()
  Database = cursor.execute("SELECT teamName, userId FROM users").fetchall()
 
  if(len(Database)<2):
    cursor.execute('DELETE FROM games;',);
    conn.commit()
    conn.close()
    return
 
  cursor.execute('DELETE FROM users;',);
  #cursor.execute("CREATE TABLE users (teamName TEXT, userId INTEGER)")
 # cursor.execute("CREATE TABLE games (channelId INTEGER, player1 INTEGER, player2 INTEGER, gameId INTEGER, runs INTEGER, bowlerNumber INTEGER, userTurn INTEGER, currentInningsWickets INTEGER, inning1Score INTEGER, inning1Result TEXT, balls INTEGER, innings INTEGER, gameHappening INTEGER, coinToss INTEGER, tossDecision INTEGER, team1 TEXT, team2 TEXT )")
 
 # START CUT AND PAST HERE
  cursor.execute("INSERT INTO users VALUES ('Sunrisers Hyderabad',706698513710579762)")
  cursor.execute("INSERT INTO users VALUES ('Omaha Union',340541260672532482)")
  cursor.execute("INSERT INTO users VALUES ('Carolina Cricketeers',701221250776825856)")
  cursor.execute("INSERT INTO users VALUES ('Lake Frozen',612494299120140295)")
  cursor.execute("INSERT INTO users VALUES ('Chesire',202273074261917697)")
  cursor.execute("INSERT INTO users VALUES ('Arizona Scorpions',477216596667006996)")
  cursor.execute("INSERT INTO users VALUES ('Army Black Knights',534010044182822914)")

  cursor.execute("INSERT INTO users VALUES ('Super 11',715243714003337296)")
  cursor.execute("INSERT INTO users VALUES ('Chincinnati Nega Chins',652016781690404884)")
  cursor.execute("INSERT INTO users VALUES ('Columbus Cricket Club',404782639824764951)")
  cursor.execute("INSERT INTO users VALUES ('Superzakers',740781497048629270)")
  cursor.execute("INSERT INTO users VALUES ('DELHI DAREDEVILS',756157157501567118)")
  cursor.execute("INSERT INTO users VALUES ('Canadian Cricket Cowboys',636749752683200523)")
  cursor.execute("INSERT INTO users VALUES ('Pakistani Falcons',293778672807182336)")
  cursor.execute("INSERT INTO users VALUES ('Tallinn Tall Estonians',237234603981537280)")
  cursor.execute("INSERT INTO users VALUES ('C0ldspark',195544830481268736)")
  cursor.execute("INSERT INTO users VALUES ('Calypso Kings',716465822020665405)")
  cursor.execute("INSERT INTO users VALUES ('New Delhi Superstars',306609698340339714)")
  cursor.execute("INSERT INTO users VALUES ('KBK Stallions',670980759275962378)")
  cursor.execute("INSERT INTO users VALUES ('schizo d dharms',532472438718464001)")
  cursor.execute("INSERT INTO users VALUES ('Sydney Sixers',105545186028822528)")
  cursor.execute("INSERT INTO users VALUES ('Tajikistan Royals',352849361920851968)")
  cursor.execute("INSERT INTO users VALUES ('Red Star Laos',144969605977341953)")
  cursor.execute("INSERT INTO users VALUES ('Connacht Cricket',409350943788892160)")
  cursor.execute("INSERT INTO users VALUES ('Moonrisers',456899475278135300)")
  cursor.execute("INSERT INTO users VALUES ('Mumbai Dragons',200681587472334848)")
  cursor.execute("INSERT INTO users VALUES ('Mornington Wombats',693027263062474782)")
  cursor.execute("INSERT INTO users VALUES ('Sri Lanka Hurricanes',495544574358323200)")
  cursor.execute("INSERT INTO users VALUES ('Boxo CC',211051381228961792)")
  cursor.execute("INSERT INTO users VALUES ('Wik XI',747379104126468129)")
  cursor.execute("INSERT INTO users VALUES ('Pondy Punters',294442863138439168)")
  cursor.execute("INSERT INTO users VALUES ('Brisbane Heat',391151653358665728)")
  cursor.execute("INSERT INTO users VALUES ('San Antonio Cricket Club',280100750523236352)")
  cursor.execute("INSERT INTO users VALUES ('Detroit Rouge',257956618015211522)")
  cursor.execute("INSERT INTO users VALUES ('Jiminy Cricket Team',140944286282678273)")
  cursor.execute("INSERT INTO users VALUES ('Dallas Thunder',327486880394510356)")
  cursor.execute("INSERT INTO users VALUES ('Calcutta Curry',185900072234385408)")
  cursor.execute("INSERT INTO users VALUES ('Flipping Flyers',501849193338503168)")
  cursor.execute("INSERT INTO users VALUES ('North Sydney Bears',256431620729470976)")
  cursor.execute("INSERT INTO users VALUES ('Honolulu Hornets',500805562376650758)")
  cursor.execute("INSERT INTO users VALUES ('Blazing Razors',733695195358560286)")
  cursor.execute("INSERT INTO users VALUES ('Eastern Ents',398339792930340884)")
  cursor.execute("INSERT INTO users VALUES ('Royal Rumblers',309625595854323712)")
  cursor.execute("INSERT INTO users VALUES ('Chicago Dawgs',560918273546518530)")
  cursor.execute("INSERT INTO users VALUES ('Cricket Kings',767625867807031317)")
  cursor.execute("INSERT INTO users VALUES ('Vienna Austrians',432286179195617280)")
  cursor.execute("INSERT INTO users VALUES ('The Truth Commission',538504544988954652)")
  cursor.execute("INSERT INTO users VALUES ('Senators Dream',463321629078847529)")
  cursor.execute("INSERT INTO users VALUES ('Hamrun Knights',517933512171585537)")
  cursor.execute("INSERT INTO users VALUES ('Thermopylae Mediterraneans',473181824516882432)")
  cursor.execute("INSERT INTO users VALUES ('Washington Cricket Team',560918273546518530)")
  cursor.execute("INSERT INTO users VALUES ('Austin Bats',129120653948223488)")
  cursor.execute("INSERT INTO users VALUES ('Rotterdam Rhinos',244161099337957376)")
  cursor.execute("INSERT INTO users VALUES ('Tikka Bomb Indians',530072906353344542)")
  cursor.execute("INSERT INTO users VALUES ('Cyber Pearls Hyderabad',616784046734835752)")
  cursor.execute("INSERT INTO users VALUES ('CricBuzzers',668763710046732289)")
  cursor.execute("INSERT INTO users VALUES ('Daredevils',747500674325151845)")
  cursor.execute("INSERT INTO users VALUES ('Wollongong Warriors',205443196401090561)")
  cursor.execute("INSERT INTO users VALUES ('Canada',524251268437245952)")
  cursor.execute("INSERT INTO users VALUES ('Depressed Wankers',670890203707211808)")
  cursor.execute("INSERT INTO users VALUES ('RCB',712732591177990228)")
  cursor.execute("INSERT INTO users VALUES ('Fightbackers',413995263192203265)")
  cursor.execute("INSERT INTO users VALUES ('Chasing Mavericks',467236639253463062)")
  cursor.execute("INSERT INTO users VALUES ('Saitama 11',743033969552916510)")
  cursor.execute("INSERT INTO users VALUES ('Mangudai',531823613758668800)")
  cursor.execute("INSERT INTO users VALUES ('Bruno The GSD Sports',705771752730394635)")
  cursor.execute("INSERT INTO users VALUES ('Team Solid',604254595593666582)")
  cursor.execute("INSERT INTO users VALUES ('Rockstar Champions',686558605998161951)")
  cursor.execute("INSERT INTO users VALUES ('San Jose Nuggets',733552144505897020)")
  # END CUT AND PASTE HERE
  Database = cursor.execute("SELECT teamName, userId FROM users").fetchall()
  print(len(Database))
  conn.commit()
  conn.close()
 

ModIds = [391151653358665728,409350943788892160,256431620729470976,202273074261917697,534010044182822914,706698513710579762,477216596667006996,340541260672532482,715243714003337296,473181824516882432]
