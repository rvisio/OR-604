
week = range(1,18)
# Home Games Dictionary - Lists all 8 home games for each of 32 each

# Away Games Dictionary - Lists all 8 away games for each of 32 teams

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
Slots = {1: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'MON_2_ESPN', 'THU_L_NBC'],
         2: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_L_CBS'],
         3: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_L_CBS'],
         4: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_L_CBS'],
         5: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_L_CBS'],
         6: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_L_CBS'],
         7: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_L_CBS'],
         8: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_L_CBS'],
         9: ['SUN_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
             'THU_L_CBS'],
         10: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
              'THU_L_NFL'],
         11: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
              'THU_L_NFL'],
         12: ['Sun_E_CBS', 'Sun_E_FOX', 'SUN_L_CBS', 'SUN_L_FOX', 'SUN_D_CBS', 'SUN_D_FOX', 'SUN_N_NBC', 'MON_1_ESPN',
              'THU_E_CBS', 'THU_L_FOX'],
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
