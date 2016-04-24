from gurobipy import *
import sqlite3

# TODO
# Update constraintNames at end of each addConstr procedure -- right now it is just calling the constraint name
# we are writing to the optimize.lp file. Sometimes warning message popping up like Warning: constraints 1029 and 1030 have the same name "10_First_Week_MNF_1"

# TODO
# 1) Change constraint in six to commented code and adjust if needed
# 2) Check that home_games[t] vs away_games[t] is correct in constraint six
# 3) Once Dr.C sends his comments, update/fix what is needed


dbName = "hw_9.db"
myConnection = sqlite3.connect(dbName)
myCursor = myConnection.cursor()

teams = ('NE', 'NYJ', 'BUF', 'MIA', 'CIN', 'PIT', 'BAL', 'CLE', 'HOU', 'IND', 'JAC',
         'TEN', 'DEN', 'KC', 'OAK', 'SD', 'WAS', 'PHI', 'NYG', 'DAL', 'MIN', 'GB', 'DET', 'CHI', 'CAR', 'ATL', 'NO',
         'TB', 'ARZ', 'SEA', 'LAR', 'SF')

westCoast = ('SD', 'SF', 'SEA', 'OAK', 'LAR')
mtnTeams = ('DEN', 'ARZ')
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
             'MON_2_ESPN', 'THU_N_NBC'],
         2: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_N_CBS'],
         3: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_N_CBS'],
         4: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_N_CBS'],
         5: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_N_CBS'],
         6: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_N_CBS'],
         7: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_N_CBS'],
         8: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_N_CBS'],
         9: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_N_CBS'],
         10: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
              'THU_N_NFL'],
         11: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
              'THU_N_NFL'],
         12: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
              'THU_E_CBS', 'THU_L_FOX', 'THU_N_NBC'],
         13: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
              'THU_N_NFL'],
         14: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
              'THU_N_NFL'],
         15: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
              'THU_N_NFL', 'SAT_E_NFL', 'SAT_L_NFL'],
         16: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
              'THU_N_NFL'],
         17: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX']}


# Create model
nflModel = Model()
nflModel.modelSense = GRB.MINIMIZE
nflModel.update()

myGames = {}

# myGames [hometeam, away team, scheduling slot, week number]

# Every game/week/slot combination
for h in teams:  # home team
    print 'Home team ' + str(h)
    for a in home_games[h]:  # away games
        for w in range(1, 18):  # week game is ocurring
            for s in slots[w]:
                myGames[h, a, s, w] = nflModel.addVar(obj=1,
                                                      vtype=GRB.BINARY,
                                                      name='game_%s_%s_%s_%s' % (h, a, s, w))
nflModel.update()

# A bye week for every team for every week in season
for t in teams:
    for w in range(1, 18):
        myGames[t, "BYE", 'Sun_BYE_NFL', w] = nflModel.addVar(obj=1,
                                                              vtype=GRB.BINARY,
                                                              name='game_%s_BYE_Sun_Bye_NFL_%s' % (t, w))
nflModel.update()

# First constraint?
myConstr = {}
for t in teams:
    for a in home_games[t]:
        constrName = '01_game_once_%s_%s' % (t, a)
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, s, w]
                                                           for w in range(1, 18)
                                                           for s in slots[w]) == 1,
                                                  name='1_game_once_%s_%s' % (t, a))
nflModel.update()

# TODO
# Investigate second quicksum should we be looping over home_games[t] or away games?
# Second Constraint everyone plays once per week
for t in teams:
    for w in [1,2,3,12,13,14,15,16,17]:
        constrName = '02_no_Bye_not_In_bye_week_%s_team_%s' % (w,t)
        myConstr[constrName] = myGames[t,'BYE','Sun_BYE_NFL', w].setAttr('ub',0)

    for w in range(1, 18):
        constrName = '02_one_game_per_week_%s_for_team_%s' % (w, t)
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, s, w]
                                                           for a in home_games[t]
                                                           for s in slots[w]) + quicksum(myGames[h, t, s, w]
                                                                                         for h in away_games[t]
                                                                                         for s in slots[w]) + myGames[
                                                      t, "BYE", 'Sun_BYE_NFL', w]== 1,
                                                  name=constrName)
nflModel.update()
# for t in teams:
#     constrName = '02_one_Game_per_week_for_team_%s' % (t)
#     myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t,a,s,w]
#                                                        for a in home_games[t]
#                                                        for w in range(1,18)
#                                                        for s in slots[w])+quicksum(myGames[h,t,s,w]
#                                                                                    for h in away_games[t]
#                                                                                    for w in range(1,18)
#                                                                                    for s in slots[w]) + quicksum(myGames[t, "BYE", 'Sun_BYE_NFL', w]
#                                                                                                                  for w in range(4,12)) <= 3,
#                                               name = constrName)
nflModel.update()

# Third constraint?
# What constraint is this
# Constraining bye weeks to 4-11
for t in teams:
    constrName = '03_bye_game_%s' % (t)
    myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, 'BYE', 'Sun_BYE_NFL', w]
                                                       for w in range(4, 12)) == 1,
                                              name=constrName)
nflModel.update()

# Fourth Constraint
# No more than six bye games per week
for w in range(4, 12):
    constrName = '04_six_byes_per_week_%s' % (w)
    myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, 'BYE', 'Sun_BYE_NFL', w] for t in teams) <= 6,
                                              name=constrName)
nflModel.update()

# Fifth Constraint
# NE and TEN cant have week 4 as bye week

constrName = "05_NE_TEN_NO_BYE_%s" % (w)

myConstr[constrName] = nflModel.addConstr(
    myGames['NE', "BYE", "Sun_BYE_NFL", 4] + myGames["TEN", "BYE", "Sun_BYE_NFL", 4] == 0,
    name=constrName)
nflModel.update()


# Sixth Constraint
# One thursday night game per week

# THU_L_CBS THU_L_NFL   THU_L_NBC
# TODO
# Verify that this constraint is working properly
# Confirm that Thursday Late CBS Games are played in weeks 2-9 (for k in range(2,10)

constrName = '06_One_Thurs_Night_Game'
for w in range(1,17):
    myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t,a,s,w]
                                                       for t in teams
                                                       for a in home_games[t]
                                                       for s in slots[w] if s[:5] == 'THU_N') ==1,
                                              name = constrName)
nflModel.update()

# for w in range(1, 17):
#     for s in slots[w]:
#         constrName = '06_thurs_night_%s_%s' % (s, w)
#         myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, s, w]
#                                                            for s in slots[w] if s[:5] == 'THU_L'
#                                                            for t in teams
#                                                            for a in home_games[t]) + quicksum(
#             myGames[t, a, s, w]
#             for s in slots[w] if s[:5] == 'THU_L'
#             for t in teams
#             for a in home_games[t]) + quicksum(myGames[t, a, s, w]
#                                                for s in slots[w] if s[:5] == 'THU_L'
#                                                for t in teams
#                                                for a in home_games[t]) == 1,
#                                                   name=constrName)
# nflModel.update()

# for w in range(1, 18):
#     for s in slots[w]:
#         constrName = '06_thurs_night_%s_%s' % (s, w)
#         myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, "THU_L_CBS", k]
#                                                            for k in range(2, 10)
#                                                            for t in teams
#                                                            for a in home_games[t]) + quicksum(
#             myGames[t, a, "THU_L_NFL", k]
#             for k in [10, 11, 13, 14, 15, 16]
#             for t in teams
#             for a in home_games[t]) + quicksum(myGames[t, a, "THU_L_NBC", k]
#                                                for k in [1, 12]
#                                                for t in teams
#                                                for a in home_games[t]) == 1,
#                                                   name=constrName)
# nflModel.update()

# for w in range(1, 17):
#     constrName = '06_thurs_night_%s_%s' % (s, w)
#     # add if statements to check?
#     myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, s, w]
#                                                        for t in teams
#                                                        for a in home_games[t]
#                                                        for s in slots[w] if s[:5] == 'THU_L') + quicksum(
#         myGames[t, a, s, w]
#         for t in teams
#         for a in home_games[t]
#         for s in slots[w] if s[:5] == 'THU_L') + quicksum(myGames[t, a, s, w]
#                                                           for t in teams
#                                                           for a in home_games[t]
#                                                           for s in slots[w] if s[:5] == 'THU_L') == 1,
#                                               name=constrName)
# nflModel.update()

# Seventh Constraint
# Two Saturday Night games in week 15 (Saturday early and saturday late)
# Adding two SAT_L_NFL games instead of one early/one late

constrName = '07_One_Sat_Early_Game_%s' % (w)
myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, 'SAT_E_NFL', 15]
                                                   for t in teams
                                                   for a in home_games[t]) == 1,
                                          name=constrName)

constrName = '07_One_Late_Sat_Night_Game_%s' % (w)
myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, 'SAT_L_NFL', 15]
                                                   for t in teams
                                                   for a in home_games[t]) == 1,
                                          name=constrName)

nflModel.update()


# Eighth Constraint
# only one double header game in weeks 1-16 and two in week 17
for w in range(1, 17):
    constrName = 'Limit_Double_Headers_%s' % (w)
    myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, s, w]
                                                       for t in teams
                                                       for a in home_games[t]
                                                       for s in slots[w] if s[:5] == 'SUN_D') == 1,
                                              name='08_limit_double_header_%s' % (w))

constrName = 'Two_DoubleHeaders_Week17_18'
myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t,a,s,17]
                                                   for t in teams
                                                   for a in home_games[t]
                                                   for s in slots[w] if s == 'SUN_D_CBS') == 1,
                                          name = '08_two_double_headers_CBS_17')

myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t,a,s,17]
                                                   for t in teams
                                                   for a in home_games[t]
                                                   for s in slots[w] if s == 'SUN_D_FOX') == 1,
                                          name = '08_two_double_headers_FOX_17')

nflModel.update()

# Ninth Constraint
# Only One sunday night game in weeks 1-16, no Sunday night game in week 17
for w in range(1, 17):
    constrName = '09_Limit_Sunday_Night_Games_%s' % (w)
    myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, 'SUN_N_NBC', w]
                                                       for t in teams
                                                       for a in home_games[t]) == 1,
                                              name=constrName)
nflModel.update()

# Tenth Constraint
# Multiple rules for  Monday Night Games
# Two Monday Night games in week 1 -- late game must be hosted by a west coast team
# Only one monday night game in weeks 2-16. No mon night game in week 17


for w in range(1, 17):
    if w == 1:
        constrName = '10_First_Week_MNF_%s' % (w)

        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, 'MON_1_ESPN', w]
                                                           for t in teams
                                                           for a in home_games[t]) == 1,
                                                  name=constrName)

        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, 'MON_2_ESPN', w]
                                                           for t in westCoast
                                                           for a in home_games[t]) == 1,
                                                  name=constrName)
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, 'MON_2_ESPN', w]
                                                           for t in teams if t not in westCoast
                                                           for a in home_games[t]) == 0,
                                                  name=constrName)
    else:
        constrName = '10_Regular_Season_MNF_%s' % (w)

        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, 'MON_1_ESPN', w]
                                                           for t in teams
                                                           for a in home_games[t]) == 1,
                                                  name=constrName)

nflModel.update()

# Eleventh Constraint
# West coast and Mountain Teams cannot play at home during sunday early timeslot
for w in range(1, 18):
    for t in westCoast + mtnTeams:
        constrName = '11_No_LeftCoast_Early_Teams_%s_%s' % (t, w)
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, 'Sun_E_CBS', w]
                                                           for a in home_games[t]) + quicksum(
            myGames[t, a, 'Sun_E_FOX', w]
            for a in home_games[t]) == 0,
                                                  name=constrName)
nflModel.update()


# Twelfth
# No team plays 4 consecutive home/away games (BYE game counts as away)

for t in teams:
    constrName = '12_Four_Consecutive_HomeAway_Games_%s' % (t)
    for i in range(1,15):
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t,a,s,w]
                                                           for a in home_games[t]
                                                           for w in range(i,i+4)
                                                           for s in slots[w]) <= 3,
                                                  name = constrName)

        # TODO
        # Check if this below constraint needs its own i in range loop
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[h,t,s,w]
                                                           for h in away_games[t]
                                                           for w in range(i,i+4)
                                                           for s in slots[w]) <= 3,
                                                  name = constrName)
nflModel.update()

# 13th constraint
# No team plays 3 consecutive home/away games during weeks 1-5 and 15-17
constr13Weeks = [1,2,3,4,5,15,16,17]
constrThirtIter = [1,2,3,15]
for t in teams:
    constrName = '13_3_Consecutive_CertainWeeks_forTeam_%s' % (t)
    for i in constrThirtIter:
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t,a,s,w]
                                                           for a in home_games[t]
                                                           for w in range(i,i+3)
                                                           for s in slots[w]) <= 2,
                                                  name = constrName)

        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[h,t,s,w]
                                                           for h in away_games[t]
                                                           for w in range (i,i+3)
                                                           for s in slots[w]) <= 2,
                                                  name = constrName)
nflModel.update()




# 14th constraint
# Each team must play at least 2 home/away games every 6 weeks

for t in teams:
    for i in range(1, 13):
        constrName = '14_2_homeAway_games_every6weeks_%s' % (t)
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, s, w]
                                                           for a in home_games[t]
                                                           for w in range(i, i+6)
                                                           for s in slots[w]) >= 2,
                                                  name = constrName)
nflModel.update()

for t in teams:
    for i in range(1,13):
        constrName = '14_2_away_gaems_6_weeks_%s_week_%s' % (t,i)
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[h,t,s,w]
                                                           for h in away_games[t]
                                                           for w in range(i,i+6)
                                                           for s in slots[w]) >=2,
                                                  name = constrName)
nflModel.update()


# 15th Constraint
# Each team must play at least 4 home/away games every 10 weeks

for t in teams:
    for i in range(1,9):
        constrName = '15_4_home_everyTenWeeks_%s' % (t)
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t,a,s,w]
                                                   for a in home_games[t]
                                                   for w in range(i,i+10)
                                                   for s in slots[w]) >= 4,
                                          name = constrName)

nflModel.update()

for t in teams:
    for i in range(1,9):
        constrName = '15_4_Away_everyTenWeeks_%s' % (t)
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[h,t,s,w]
                                                   for h in away_games[t]
                                                   for w in range(i,i+10)
                                                   for s in slots[w]) >= 4,
                                          name = constrName)

nflModel.update()


# 16th Constraint
# Previous year superbowl champion opens season at home on thursday night
champ = ['DEN']
for t in champ:
    constrName = '16_SuperBowlChamp_%s_Opens_At_Home' % champ
    myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, 'THU_N_NBC', 1]
                                           for a in home_games[t]) == 1,
                                  name = constrName)
nflModel.update()

# 17th Constraint
# DAL & DET play at home on Thanksgiving (Week 12)
# Dallas = myGames['DAL',home_games['DAL'],'THU_L_FOX',12]
# Detroit = myGames['DET',home_games['DET'],'THU_E_CBS',12]

constrName = '17_Thanksgiving_games_for_team_DAL'
myConstr[constrName] = nflModel.addConstr(quicksum(myGames['DAL', a, 'THU_L_FOX', 12]
                                           for a in home_games['DAL']) == 1,
                                  name = constrName)
nflModel.update()

constrName = '17_Thanksgiving_games_for_team_DET'
myConstr[constrName] = nflModel.addConstr(quicksum(myGames['DET', a, 'THU_E_CBS', 12]
                                           for a in home_games['DET']) == 1,
                                  name=constrName)
nflModel.update()

# Prevent other teams from playing at home THU_E_CBS
for t in teams:
    if t != 'DET':
        constrName = '17_no_other_home_teams_Thanksgiving_%s' % t
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, 'THU_E_CBS', 12]
                                                   for a in home_games[t]) == 0,
                                          name=constrName)
nflModel.update()

# Prevent other teams from playing at home THU_L_FOX
for t in teams:
    if t != 'DAL':
        constrName = '17_no_other_home_teams_Thanksgiving_%s' % t
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, 'THU_L_FOX', 12]
                                                   for a in home_games[t]) == 0,
                                          name=constrName)
nflModel.update()

# TODO 18th constraint
# NBC Gets Thursday Night Games week 1 & 12
# Scheduling dictionary has been set up to account for this already (also reduces number of variables created by gurobi)
# Is constraint necessary???

# NBC only getting game week 1

constrName = '18_nbc_thurs_night_week_1'
myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, 'THU_N_NBC', 1]
                                          for t in teams
                                          for a in home_games[t]) == 1,
                                          name = constrName)
nflModel.update()

constrName = '18_nbc_thurs_night_week_12'
myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, 'THU_N_NBC', 12]
                                          for t in teams
                                          for a in home_games[t]) == 1,
                                          name = constrName)
nflModel.update()


# constraint 19
# CBS gets Thursday Night Games week 2-9
# Same as above

# Currently working as expected due to dictionary

# constraint 20
# NFL gets Thursday Night Games Weeks 10, 11, 13-16 (and Saturday night games)
# Same as 18th constraint..dict accounts for this to reduce number of variables created.
# Constraint still necessary?

# Currently working as expected due to dictionary

# TODO 21st Constraint
# Fox/CBS Get at least 3 early games on Sundays

# Sun_E_CBS games
# for t in teams:
#     for a in home_games[t]:
#         constrName = '21_at_least_3_early_games_SUN_E_CBS'
#         myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, 'Sun_E_CBS', w]
#                                                        for w in range(1, 18)) <= 18,
#                                               name=constrName)
#
#
# nflModel.update()

# constrName = '21_at_least_3_early_games_SUN_E_CBS'
# myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t,a,s,w]
#                                                    for t in teams
#                                                    for a in home_games[t]
#                                                    for w in range(1,18)
#                                                    for s in slots[w]) >= 3,
#                                           name = constrName)
# nflModel.update()
#
# constrName = '21_at_least_3_early_games_SUN_E_CBS'
# myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t,a,s,w]
#                                                    for t in teams
#                                                    for a in home_games[t]
#                                                    for w in range(1,18)
#                                                    for s in slots[w]) <= 17,
#                                           name = constrName)
# nflModel.update()

# for t in teams:
#     for a in home_games[t]:
#         constrName = '21_at_least_3_early_games_SUN_E_CBS'
#         myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, 'Sun_E_CBS', w]
#                                                        for w in range(1, 18)) >= 3,
#                                               name=constrName)
# nflModel.update()
# #
# for t in teams:
#     constrName = '21_at_least_3_early_games_SUN_E_FOX'
#     myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, s, w]
#                                                        for a in home_games[t]
#                                                        for w in range(1,18)
#                                                        for s in slots[w] if s == 'SUN_E_FOX') >= 3,
#                                               name = constrName)
#
# for w in range(1, 18):
#     for t in teams:
#         constrName = '21_at_least_3_early_games_SUN_E_FOX'
#         myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, s, w]
#                                                for a in home_games[t]
#                                                for s in slots[w] if s == 'Sun_E_FOX') >= 3,
#                                       name=constrName)
#
# nflModel.update()


# TODO 22nd constraint
# Fox/CBS each get at least 5 games on sundays
# Same as 21st/15th constraint?
# for w in range(1, 18):
#     for t in teams:
#         constrName = '22_at_least_5_sun_games_SUN_CBS'
#         myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, 'Sun_E_CBS', w]
#                                                            for a in home_games[t]) + quicksum(
#             myGames[t, a, 'SUN_L_CBS', w]
#             for a in home_games[t]) +
#                                                   quicksum(myGames[t, a, 'SUN_D_CBS', w]
#                                                            for a in home_games[t]) >= 5,
#                                                   name=constrName)
# nflModel.update()

# for t in teams:
#     for w in range(1, 18):
#         constrName = '22_at_least_5_sun_games_SUN_E_FOX'
#         myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, 'Sun_E_FOX', w]
#                                                for a in home_games[t]) + quicksum(myGames[t, a, 'SUN_L_FOX', w]
#                                                                              for a in home_games[t]) +
#                                       quicksum(myGames[t, a, 'SUN_D_FOX', w]
#                                                for a in home_games[t]) >= 5,
#                                      name = constrName)
#nflModel.update()

# TODO 23rd Constraint
# Fox/CBS each get 8 double headers total for weeks 1 - 16
# use iterator


# for t in teams:
#     constrName = '23_eight_double_headers_FOX'
#     myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, 'SUN_D_FOX', w]
#                                                        for a in home_games[t]
#                                                        for w in range(1, 17)) >= 8,
#                                               name=constrName)
# nflModel.update()
#
# for t in teams:
#     constrName = '23_eight_double_headers_CBS'
#     myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, 'SUN_D_CBS', w]
#                                                        for a in home_games[t]
#                                                        for w in range(1, 17)) >= 8,
#                                               name=constrName)
# nflModel.update()


# for w in range(1, 17):
#     for t in teams:
#         constrName = '23a_eight_double_headers_CBS'
#         myConstr = nflModel.addConstr(quicksum(myGames[t, a, s, w]
#                                                for a in home_games[t]
#                                                for s in slots[w] if s == 'Sun_D_CBS') == 8,
#                                       name=constrName)
# nflModel.update()


# TODO 24th constraint
# FOX/CBS each get a double header in week 17
# Scheduling dictionary already accounts for this
constrName = '24_fox_doubleHeader'
myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, 'SUN_D_FOX', 17]
                                       for t in teams
                                       for a in home_games[t]) == 1,
                              name = constrName)
nflModel.update()

constrName = '24_cbs_doubleheader'
myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, 'SUN_D_CBS', 17]
                                       for t in teams
                                       for a in home_games[t]) == 1,
                              name = constrName)
nflModel.update()

# TODO 25th constraint
# FOX/CBS cannot have more than 2 double headers in a row  -- not working

for t in teams:
    constrName = '25cbs_Max_two_DH_%s' % t
    for i in range(1,17):
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, s, w]
                                                           for a in home_games[t]
                                                           for w in range(i, i+1)
                                                           for s in slots[w] if s == 'SUN_D_CBS') <= 2,
                                                  name = constrName)
nflModel.update()

for t in teams:
    constrName = '25fox_Max_two_DH_%s' % t
    for i in range(1,17):
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t, a, s, w]
                                                           for a in home_games[t]
                                                           for w in range(i,i+1)
                                                           for s in slots[w] if s == 'SUN_D_FOX') <= 2,
                                                  name = constrName)
nflModel.update()

# TODO 26th constraint
# No team can have more than 5 prime time games in a season (Thanksgiving day games do not count as primetime)
# Primetime games = MON_1_ESPN, MON_2_ESPN, SUN_D_CBS, SUN_D_FOX, SUN_N_NBC, THU_L_CBS, THU_N_NBC,

# TODO 27th Constraint
# No more than 4 games on NBC in a season
# Already happening due to dictionary?
for t in teams:
    for a in home_games[t]:
        constrName = '27_no_more_than_4_nbc_%s_%s' % (t,a)
        myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t,a,s,w]
                                                           for w in range(1,18)
                                                           for s in slots[w] if s[6:]=='NBC') <= 4,
                                                  name = constrName)

# TODO 28th Constraint- what is the international game time slot??
# Teams playing an international game will have a home game the week before their international game


# TODO 29th Constraint
# Teams playing an international game will have their BYE game the week following the international game


# TODO 30th Constraint
# Two teams cannot play back to back games against each other or play against each other the week before and after a BYE
# for t in teams:
#     for a in home_games[t]:
#         for w in range(1,17):
#             nextWeek = w+1
#             constrName = '30_no_back_to_back_teams_%s_%s' % (t,a)
#             myConstr[constrName] = nflModel.addConstr(quicksum(myGames[t,a,s,w]
#                                                                for s in slots[w]) + quicksum(myGames[home,a,s,nextWeek]
#                                                                                              for home in away_games[a]
#
#                                                                                              for s in slots[nextWeek]) == 0,
#             name = constrName)
#
# nflModel.update()


# TODO #31st Constraint
# No team plays more than 2 road games against teams coming off a BYE


# TODO 32nd Constraint
# All teams playing away on Thursday night are home the week before

# TODO 33rd Constraint
# Week 17 will consist of games between division opponents only


nflModel.setParam('MIPFocus', 1)
nflModel.write('optimize.lp')
nflModel.optimize()


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
