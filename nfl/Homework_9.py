from gurobipy import *
import sqlite3

dbName = "hw_9.db"
myConnection = sqlite3.connect(dbName)
myCursor = myConnection.cursor()

teams = ('NE', 'NYJ', 'BUF', 'MIA', 'CIN', 'PIT', 'BAL', 'CLE', 'HOU', 'IND', 'JAC',
         'TEN', 'DEN', 'KC', 'OAK', 'SD', 'WAS', 'PHI', 'NYG', 'DAL', 'MIN', 'GB', 'DET', 'CHI', 'CAR', 'ATL', 'NO',
         'TB', 'ARZ', 'SEA', 'LAR', 'SF')

westCoast = ('SD','SF','SEA','OAK','LAR')
mtnTeams = ('DEN','ARZ')
# Home Games Dictionary - Lists all 8 home games for each of 32 each
home_games = {
    'WAS': ('DAL', 'NYG', 'PHI', 'GB', 'MIN', 'CAR', 'CLE', 'PIT'),
    'PHI': ('DAL', 'NYG', 'WAS', 'GB', 'MIN', 'ATL', 'CLE', 'PIT'),
    'NYG': ('DAL', 'PHI', 'WAS', 'CHI', 'DET', 'NO', 'BAL', 'CIN'),
    'DAL': ('NYG', 'PHI', 'WAS', 'CHI', 'DET', 'TB', 'BAL', 'CIN'),
    'MIN': ('CHI', 'DET', 'GB', 'DAL', 'NYG', 'ARZ', 'HOU', 'IND'),
    'GB': ('CHI', 'DET', 'MIN', 'DAL', 'NYG', 'SEA', 'HOU', 'IND'),
    'DET': ('CHI', 'GB', 'MIN', 'PHI', 'WAS', 'LAR', 'JAC', 'TEN'),
    'CHI': ('DET', 'GB', 'MIN', 'PHI', 'WAS', 'SF', 'JAC', 'TEN'),
    'CAR': ('ATL', 'NO', 'TB', 'ARZ', 'SF', 'MIN', 'KC', 'SD'),
    'ATL': ('CAR', 'NO', 'TB', 'ARZ', 'SF', 'GB', 'KC', 'SD'),
    'NO': ('ATL', 'CAR', 'TB', 'LAR', 'SEA', 'DET', 'DEN', 'OAK'),
    'TB': ('ATL', 'CAR', 'NO', 'LAR', 'SEA', 'CHI', 'DEN', 'OAK'),
    'ARZ': ('LAR', 'SF', 'SEA', 'NO', 'TB', 'WAS', 'NE', 'NYJ'),
    'SEA': ('ARZ', 'SF', 'LAR', 'ATL', 'CAR', 'PHI', 'BUF', 'MIA'),
    'LAR': ('ARZ', 'SF', 'SEA', 'ATL', 'CAR', 'NYG', 'BUF', 'MIA'),
    'SF': ('ARZ', 'LAR', 'SEA', 'NO', 'TB', 'DAL', 'NE', 'NYJ'),
    'NE': ('BUF', 'MIA', 'NYJ', 'BAL', 'CIN', 'HOU', 'LAR', 'SEA'),
    'NYJ': ('BUF', 'MIA', 'NE', 'BAL', 'CIN', 'IND', 'LAR', 'SEA'),
    'BUF': ('MIA', 'NE', 'NYJ', 'CLE', 'PIT', 'JAC', 'ARZ', 'SF'),
    'MIA': ('BUF', 'NE', 'NYJ', 'CLE', 'PIT', 'TEN', 'ARZ', 'SF'),
    'CIN': ('BAL', 'CLE', 'PIT', 'BUF', 'MIA', 'DEN', 'PHI', 'WAS'),
    'PIT': ('BAL', 'CIN', 'CLE', 'NE', 'NYJ', 'KC', 'DAL', 'NYG'),
    'BAL': ('CIN', 'CLE', 'PIT', 'BUF', 'MIA', 'OAK', 'PHI', 'WAS'),
    'CLE': ('BAL', 'CIN', 'PIT', 'NE', 'NYJ', 'SD', 'DAL', 'NYG'),
    'HOU': ('IND', 'JAC', 'TEN', 'KC', 'SD', 'CIN', 'CHI', 'DET'),
    'IND': ('HOU', 'JAC', 'TEN', 'KC', 'SD', 'PIT', 'CHI', 'DET'),
    'JAC': ('HOU', 'IND', 'TEN', 'DEN', 'OAK', 'BAL', 'GB', 'MIN'),
    'TEN': ('HOU', 'IND', 'JAC', 'DEN', 'OAK', 'CLE', 'GB', 'MIN'),
    'DEN': ('KC', 'OAK', 'SD', 'HOU', 'IND', 'NE', 'ATL', 'CAR'),
    'KC': ('DEN', 'OAK', 'SD', 'JAC', 'TEN', 'NYJ', 'NO', 'TB'),
    'OAK': ('DEN', 'KC', 'SD', 'HOU', 'IND', 'BUF', 'ATL', 'CAR'),
    'SD': ('DEN', 'KC', 'OAK', 'JAC', 'TEN', 'MIA', 'NO', 'TB')
}
# Away Games Dictionary - Lists all 8 away games for each of 32 teams
away_games = {
    'WAS': ('DAL', 'NYG', 'PHI', 'CHI', 'DET', 'ARZ', 'BAL', 'CIN'),
    'PHI': ('DAL', 'NYG', 'WAS', 'CHI', 'DET', 'SEA', 'BAL', 'CIN'),
    'NYG': ('DAL', 'PHI', 'WAS', 'GB', 'MIN', 'LAR', 'CLE', 'PIT'),
    'DAL': ('NYG', 'PHI', 'WAS', 'GB', 'MIN', 'SF', 'CLE', 'PIT'),
    'MIN': ('CHI', 'DET', 'GB', 'PHI', 'WAS', 'CAR', 'JAC', 'TEN'),
    'GB': ('CHI', 'DET', 'MIN', 'PHI', 'WAS', 'ATL', 'JAC', 'TEN'),
    'DET': ('CHI', 'GB', 'MIN', 'DAL', 'NYG', 'NO', 'HOU', 'IND'),
    'CHI': ('DET', 'GB', 'MIN', 'DAL', 'NYG', 'TB', 'HOU', 'IND'),
    'CAR': ('ATL', 'NO', 'TB', 'LAR', 'SEA', 'WAS', 'DEN', 'OAK'),
    'ATL': ('CAR', 'NO', 'TB', 'LAR', 'SEA', 'PHI', 'DEN', 'OAK'),
    'NO': ('ATL', 'CAR', 'TB', 'ARZ', 'SF', 'NYG', 'KC', 'SD'),
    'TB': ('ATL', 'CAR', 'NO', 'ARZ', 'SF', 'DAL', 'KC', 'SD'),
    'ARZ': ('LAR', 'SF', 'SEA', 'ATL', 'CAR', 'MIN', 'BUF', 'MIA'),
    'SEA': ('ARZ', 'SF', 'LAR', 'NO', 'TB', 'GB', 'NE', 'NYJ'),
    'LAR': ('ARZ', 'SF', 'SEA', 'NO', 'TB', 'DET', 'NE', 'NYJ'),
    'SF': ('ARZ', 'LAR', 'SEA', 'ATL', 'CAR', 'CHI', 'BUF', 'MIA'),
    'NE': ('BUF', 'MIA', 'NYJ', 'CLE', 'PIT', 'DEN', 'ARZ', 'SF'),
    'NYJ': ('BUF', 'MIA', 'NE', 'CLE', 'PIT', 'KC', 'ARZ', 'SF'),
    'BUF': ('MIA', 'NE', 'NYJ', 'BAL', 'CIN', 'OAK', 'LAR', 'SEA'),
    'MIA': ('BUF', 'NE', 'NYJ', 'BAL', 'CIN', 'SD', 'LAR', 'SEA'),
    'CIN': ('BAL', 'CLE', 'PIT', 'NE', 'NYJ', 'HOU', 'DAL', 'NYG'),
    'PIT': ('BAL', 'CIN', 'CLE', 'BUF', 'MIA', 'IND', 'PHI', 'WAS'),
    'BAL': ('CIN', 'CLE', 'PIT', 'NE', 'NYJ', 'JAC', 'DAL', 'NYG'),
    'CLE': ('BAL', 'CIN', 'PIT', 'BUF', 'MIA', 'TEN', 'PHI', 'WAS'),
    'HOU': ('IND', 'JAC', 'TEN', 'DEN', 'OAK', 'NE', 'GB', 'MIN'),
    'IND': ('HOU', 'JAC', 'TEN', 'DEN', 'OAK', 'NYJ', 'GB', 'MIN'),
    'JAC': ('HOU', 'IND', 'TEN', 'KC', 'SD', 'BUF', 'CHI', 'DET'),
    'TEN': ('HOU', 'IND', 'JAC', 'KC', 'SD', 'MIA', 'CHI', 'DET'),
    'DEN': ('KC', 'OAK', 'SD', 'JAC', 'TEN', 'CIN', 'NO', 'TB'),
    'KC': ('DEN', 'OAK', 'SD', 'HOU', 'IND', 'PIT', 'ATL', 'CAR'),
    'OAK': ('DEN', 'KC', 'SD', 'JAC', 'TEN', 'BAL', 'NO', 'TB'),
    'SD': ('DEN', 'KC', 'OAK', 'HOU', 'IND', 'CLE', 'ATL', 'CAR')
}

# Conference Dictionary - Lists all 16 teams in each of two conferences
conference = {
    'AFC': ('NE', 'NYJ', 'BUF', 'MIA', 'CIN', 'PIT', 'BAL', 'CLE', 'HOU', 'IND', 'JAC',
            'TEN', 'DEN', 'KC', 'OAK', 'SD'),
    'NFC': ('WAS', 'PHI', 'NYG', 'DAL', 'MIN', 'GB', 'DET', 'CHI', 'CAR', 'ATL', 'NO',
            'TB', 'ARZ', 'SEA', 'LAR', 'SF')
}
# Division Dict - lists all 4 teams in each of 8 divisions
division = {
    'AFC': {
        'EAST': {'NE', 'NYJ', 'BUF', 'MIA'},
        'WEST': {'DEN', 'KC', 'OAK', 'SD'},
        'SOUTH': {'HOU', 'IND', 'JAC', 'TEN'},
        'NORTH': {'CIN', 'PIT', 'BAL', 'CLE'}
    },
    'NFC': {
        'EAST': {'WAS', 'PHI', 'NYG''DAL'},
        'WEST': {'ARZ', 'SEA', 'LAR', 'SF'},
        'SOUTH': {'CAR', 'ATL', 'NO', 'TB'},
        'NORTH': {'MIN', 'GB', 'DET', 'CHI'}
    }

}

# Time Slot Dictionary - Lists all network timeslots available each week
slots = {1: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'MON_2_ESPN', 'THU_L_NBC'],
         2: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_L_CBS'],
         3: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_L_CBS'],
         4: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_L_CBS', "Sun_BYE_NFL"],
         5: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_L_CBS', "Sun_BYE_NFL"],
         6: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_L_CBS', "Sun_BYE_NFL"],
         7: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_L_CBS', "Sun_BYE_NFL"],
         8: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_L_CBS', "Sun_BYE_NFL"],
         9: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_L_CBS', "Sun_BYE_NFL"],
         10: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
              'THU_L_NFL', "Sun_BYE_NFL"],
         11: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
              'THU_L_NFL', "Sun_BYE_NFL"],
         12: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
              'THU_E_CBS', 'THU_L_FOX', 'THU_L_NBC'],
         13: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
              'THU_L_NFL'],
         14: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
              'THU_L_NFL'],
         15: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
              'THU_L_NFL', 'SAT_E_NFL', 'SAT_L_NFL'],
         16: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
              'THU_L_NFL'],
         17: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
              'THU_L_NFL']}

# Create model
nflModel = Model()
nflModel.modelSense = GRB.MINIMIZE
nflModel.update()

myGames = {}

# myGames [hometeam, away team, scheduling slot, week number]

# Every game/week/slot combination
for h in teams:  # home team
    print 'Home team ' + str(h)
    for a in away_games[h]:  # away games
        for w in range(1, 18):  # week game is ocurring
            for s in slots[w]:
                myGames[h, a, s, w] = nflModel.addVar(obj=1,
                                                      vtype=GRB.BINARY,
                                                      name='game_%s_%s_%s_%s' % (h, a, s, w))
nflModel.update()

# A bye week for every team for every week in season
for t in teams:
    for w in range(1,18):
        myGames[t,"BYE",'Sun_BYE_NFL',w] = nflModel.addVar(obj=1,
                                                          vtype=GRB.BINARY,
                                                          name = 'game_%s_BYE_Sun_Bye_NFL_%s' %(t,w))
nflModel.update()

# First constraint?
myConstr = {}
for t in teams:
    for a in away_games[t]:
        constrName = '01_game_once_%s_%s' % (t, a)
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, s, w]
                                                           for w in range(1, 18)
                                                           for s in slots[w]) == 1,
                                                  name='1_game_once_%s_%s' % (t, a))
nflModel.update()

#TODO
# Investigate second quicksum should we be looping over home_games[t] or away games?
# Second Constraint everyone plays once per week
for t in teams:
    for w in range(1,18):
        constrName ='02_one_game_per_week_%s_for_team_%s' % (w,t)
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t,a,s,w]
                                                           for a in away_games[t]
                                                           for s in slots[w]) + quicksum(myGames[h,t,s,w]
                                                                                         for h in home_games[t]
                                                                                         for s in slots[w]) + myGames[t,"BYE",'Sun_BYE_NFL',w] == 1,
        name = constrName)
nflModel.update()

# Third constraint?
# What constraint is this
# Constraining bye weeks to 4-11
for t in teams:
    constrName = '03_bye_game_%s' %(t)
    myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t,'BYE','Sun_BYE_NFL',w] for w in range(4,12)) == 1,
    name = constrName)
nflModel.update()

# Fourth Constraint
# No more than six bye games per week
for w in range(4,12):
    constrName = '04_six_byes_per_week_%s' %(w)
    myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, 'BYE','Sun_BYE_NFL',w] for t in teams)<=6,
                                              name = constrName)
nflModel.update()

# Fifth Constraint
# NE and TEN cant have week 4 as bye week
for w in range(4,12):
    constrName = "05_NE_TEN_NO_BYE_%s" % (w)
    myConstr[constrName] = nflModel.addConstr(myGames['NE',"BYE","Sun_BYE_NFL",4] + myGames["TEN","BYE","Sun_BYE_NFL",4] == 0,
                                                  name = constrName)
nflModel.update()

# Sixth Constraint
# One thursday night game per week

# THU_L_CBS THU_L_NFL   THU_L_NBC
# TODO
# FIX -- THIS CONSTRAINT IS NOT FUNCTIONING PROPERLY
# Confirm that Thursday Late CBS Games are played in weeks 2-9 (for k in range(2,10)

for w in range(1,18):
    for s in slots[w]:
        constrName = '06_thurs_night_%s_%s' % (s,w)
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t,a,"THU_L_CBS",k]
                                                           for k in range(2,10)
                                                           for t in teams
                                                           for a in away_games[t])+ quicksum(myGames[t,a,"THU_L_NFL",k]
                                                                                             for k in [10,11,13,14,15,16]
                                                                                             for t in teams
                                                                                             for a in away_games[t])+ quicksum(myGames[t,a,"THU_L_NBC",k]
                                                                                                                               for k in [1,12]
                                                                                                                               for t in teams
                                                                                                                               for a in away_games[t]) == 1,
                                                  name = constrName)
nflModel.update()

# Seventh Constraint
# Two Saturday Night games in week 15 (Saturday early and saturday late)
#TODO
# Adding two SAT_L_NFL games instead of one early/one late
for w in [15]:
    constrName = '07_Two_Sat_Night_%s' %(w)
    myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t,a,'SAT_E_NFL',w]
                                              for t in teams
                                              for a in away_games[t]) + quicksum(myGames[t,a,'SAT_L_NFL',w]
                                                                                 for t in teams
                                                                                 for a in away_games[t]) == 2,
                                              name = constrName)
nflModel.update()

# TODO
# Eighth Constraint
# only one double header game in weeks 1-16 and two in week 17

# Ninth Constraint
# Only One sunday night game in weeks 1-16, no Sunday night game in week 17
for w in range(1,18):
    constrName = '09_Limit_Sunday_Night_Games_%s' % (w)
    if w != 17:
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t,a,'SUN_N_NBC',w]
                                                           for t in teams
                                                           for a in away_games[t]) == 1,
                                                  name = constrName)
    else:
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t,a,'SUN_N_NBC', w]
                                                           for t in teams
                                                           for a in away_games[t]) == 0,
                                                  name = constrName)
nflModel.update()

# Tenth Constraint
# Multiple rules for  Monday Night Games
# Two Monday Night games in week 1 -- late game must be hosted by a west coast team
# Only one monday night game in weeks 2-16. No mon night game in week 17

#TODO
# Fix week 1 of monday night games. currently three games being scheduled (2 mon_1_espn and 1 mon_2_espn (west coast team not even hosting somehow))

for w in range(1,18):
    constrName = '10_Monday_Night_Constraints_%s' % (w)
    if w == 1:
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t,a,'MON_1_ESPN',w]
                                                           for t in teams
                                                           for a in away_games[t]) + quicksum(myGames[t,a,'MON_2_ESPN',w]
                                                                                             for t in westCoast
                                                                                             for a in away_games[t]) == 2,
                                                  name = constrName)
    elif w != 17:
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t,a,'MON_1_ESPN',w]
                                                           for t in teams
                                                           for a in away_games[t]) == 1,
                                                  name = constrName)
    else:
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t,a,'MON_1_ESPN',w]
                                                           for t in teams
                                                           for a in away_games[t]) == 0,
                                                  name = constrName)
nflModel.update()


# Eleventh Constraint
# West coast and Mountain Teams cannot play at home during sunday early timeslot
for w in range(1,18):
    for t in westCoast + mtnTeams:
        constrName = '11_No_LeftCoast_Early_Teams_%s_%s' % (t,w)
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t,a,'Sun_E_CBS',w]
                                                           for a in away_games[t]) + quicksum(myGames[t,a,'Sun_E_FOX',w]
                                                                                              for a in away_games[t]) == 0,
                                                  name = constrName)
nflModel.update()

# TODO
# Twelfth
# No team plays 4 consecutive home/away games (BYE game counts as away)

# TODO
# 13th constraint
# No team plays 3 consecutive home/away games during weeks 1-5 and 15-17

# TODO
# 14th constraint
# Each team must play at least 2 home/away games every 6 weeks

# TODO
# 15th Constraint
# Each team must play at least 4 home/away games every 10 weeks
# n
nflModel.write('optimize.lp')
nflModel.optimize()

#
DROPTABLESQL = """DROP TABLE IF EXISTS Answer"""
myCursor.execute(DROPTABLESQL)
myConnection.commit()

SQLSTRING = """CREATE TABLE IF NOT EXISTS Answer (Home TEXT, Away TEXT, Network TEXT, Week INTEGER)"""
myCursor.execute(SQLSTRING)
myConnection.commit()
tempList = []
if nflModel.Status == GRB.OPTIMAL:
    for e in myGames:
        if myGames[e].x > 0:
            print e, myGames[e].x
            val = (str(e[0]), str(e[1]), str(e[2]), int(e[3]))
            tempList.append(val)

myCursor.executemany('INSERT INTO Answer VALUES(?,?,?,?);', tempList)
myConnection.commit()
myCursor.close()
