#NFL_TEAMS = (ARZ, ATL, BAL, BUF, CAR, CHI, CIN, CLE, DAL,
# DEN, DET, GB, HOU, IND, JAC, KC, LAR, MIA, MIN, NE, NO, NYG, NYJ,
# OAK, PHI, PIT, SD, SEA, SF, TB, TEN, WAS)

games = {
    #AFC EAST
    'NE':{
        'Home':('BUF','MIA','NYJ','BAL','CIN','HOU','LAR','SEA'),
        'Away':('BUF','MIA','NYJ','CLE','PIT','DEN','ARZ','SF')
    },
    'NYJ':{
        'Home':('BUF','MIA','NE','BAL','CIN','IND','LAR','SEA'),
        'Away':('BUF','MIA','NE','CLE','PIT','KC','ARZ','SF')
    },
    'BUF':{
        'Home':('MIA','NE','NYJ','CLE','PIT','JAC','ARZ','SF'),
        'Away':('MIA','NE','NYJ','BAL','CIN','OAK','LAR','SEA')
    },
    'MIA':{
        'Home':('BUF','NE','NYJ','CLE','PIT','TEN','ARZ','SF'),
        'Away':('BUF','NE','NYJ','BAL','CIN','SD','LAR','SEA')
    },
    #AFC NORTH
    'CIN':{
        'Home':('BAL','CLE','PIT','BUF','MIA','DEN','PHI','WAS'),
        'Away':('BAL','CLE','PIT','NE','NYJ','HOU','DAL','NYG')
    },
    'PIT':{
        'Home':('BAL','CIN','CLE','NE','NYJ','KC','DAL','NYG'),
        'Away':('BAL','CIN','CLE','BUF','MIA','IND','PHI','WAS')
    },
    'BAL':{
        'Home':('CIN','CLE','PIT','BUF','MIA','OAK','PHI','WAS'),
        'Away':('CIN','CLE','PIT','NE','NYJ','JAC','DAL','NYG')
    },
    'CLE':{
        'Home':('BAL','CIN','PIT','NE','NYJ','SD','DAL','NYG'),
        'Away':('BAL','CIN','PIT','BUF','MIA','TEN','PHI','WAS')
    },
    #AFC SOUTH
    'HOU':{
        'Home':('IND','JAC','TEN','KC','SD','CIN','CHI','DET'),
        'Away':('IND','JAC','TEN','DEN','OAK','NE','GB','MIN')
    },
    'IND':{
        'Home':('HOU','JAC','TEN','KC','SD','PIT','CHI','DET'),
        'Away':('HOU','JAC','TEN','DEN','OAK','NYJ','GB','MIN')
    },
    'JAC':{
        'Home':('HOU','IND','TEN','DEN','OAK','BAL','GB','MIN'),
        'Away':('HOU','IND','TEN','KC','SD','BUF','CHI','DET')
    },
    'TEN':{
        'Home':('HOU','IND','JAC','DEN','OAK','CLE','GB','MIN'),
        'Away':('HOU','IND','JAC','KC','SD','MIA','CHI','DET')
    },
    #AFC WEST
    'DEN':{
        'Home':('KC','OAK','SD','HOU','IND','NE','ATL','CAR'),
        'Away':('KC','OAK','SD','JAC','TEN','CIN','NO','TB')
    },
    'KC':{
        'Home':('DEN','OAK','SD','JAC','TEN','NYJ','NO','TB'),
        'Away':('DEN','OAK','SD','HOU','IND','PIT','ATL','CAR')
    },
    'OAK':{
        'Home':('DEN','KC','SD','HOU','IND','BUF','ATL','CAR'),
        'Away':('DEN','KC','SD','JAC','TEN','BAL','NO','TB')
    },
    'SD':{
        'Home':('DEN','KC','OAK','JAC','TEN','MIA','NO','TB'),
        'Away':('DEN','KC','OAK','HOU','IND','CLE','ATL','CAR')
    },
    #NFC EAST
     'WAS':{
        'Home':('DAL', 'NYG', 'PHI', 'GB', 'MIN', 'CAR', 'CLE', 'PIT'),
        'Away':('DAL', 'NYG', 'PHI', 'CHI', 'DET', 'ARZ', 'BAL', 'CIN')
    },
    'PHI':{
        'Home':('DAL', 'NYG', 'WAS', 'GB', 'MIN', 'ATL', 'CLE', 'PIT'),
        'Away':('DAL', 'NYG', 'WAS', 'CHI', 'DET', 'SEA', 'BAL', 'CIN')
    },
    'NYG':{
        'Home':('DAL', 'PHI', 'WAS', 'CHI', 'DET', 'NO', 'BAL', 'CIN'),
        'Away':('DAL', 'PHI', 'WAS', 'GB', 'MIN', 'LAR', 'CLE', 'PIT')
    },
    'DAL':{
        'Home':('NYG', 'PHI', 'WAS', 'CHI', 'DET', 'TB', 'BAL', 'CIN'),
        'Away':('NYG', 'PHI', 'WAS', 'GB', 'MIN', 'SF', 'CLE', 'PIT')

    },
    #NFC NORTH
    'MIN':{
        'Home':('CHI', 'DET', 'GB', 'DAL', 'NYG', 'ARZ', 'HOU', 'IND'),
        'Away':('CHI', 'DET', 'GB', 'PHI', 'WAS', 'CAR', 'JAC', 'TEN')
    },
    'GB':{
        'Home':('CHI', 'DET', 'MIN', 'DAL', 'NYG', 'SEA', 'HOU', 'IND'),
        'Away':('CHI', 'DET', 'MIN', 'PHI', 'WAS', 'ATL', 'JAC', 'TEN')
    },
    'DET':{
        'Home':('CHI', 'GB', 'MIN', 'PHI', 'WAS', 'LAR', 'JAC', 'TEN'),
        'Away':('CHI', 'GB', 'MIN', 'DAL', 'NYG', 'NO', 'HOU', 'IND')
    },
    'CHI':{
        'Home':('DET', 'GB', 'MIN', 'PHI', 'WAS', 'SF', 'JAC', 'TEN'),
        'Away':('DET', 'GB', 'MIN', 'DAL', 'NYG', 'TB', 'HOU', 'IND')
    },
    #NFC SOUTH
    'CAR':{
        'Home':('ATL', 'NO', 'TB', 'ARZ', 'SF', 'MIN', 'KC', 'SD'),
        'Away':('ATL', 'NO', 'TB', 'LAR', 'SEA', 'WAS', 'DEN', 'OAK')
    },
    'CHI':{
        'Home':('DET', 'GB', 'MIN', 'PHI', 'WAS', 'SF', 'JAC', 'TEN'),
        'Away':('DET', 'GB', 'MIN', 'DAL', 'NYG', 'TB', 'HOU', 'IND')
    },
    'ATL':{
        'Home':('CAR', 'NO', 'TB', 'ARZ', 'SF', 'GB', 'KC', 'SD'),
        'Away':('CAR', 'NO', 'TB', 'LAR', 'SEA', 'PHI', 'DEN', 'OAK')
    },
    'NO':{
        'Home':('ATL', 'CAR', 'TB', 'LAR', 'SEA', 'DET', 'DEN', 'OAK'),
        'Away':('ATL', 'CAR', 'TB', 'ARZ', 'SF', 'NYG', 'KC', 'SD')
    },
    'TB':{
        'Home':('ATL', 'CAR', 'NO', 'LAR', 'SEA', 'CHI', 'DEN', 'OAK'),
        'Away':('ATL', 'CAR', 'NO', 'ARZ', 'SF', 'DAL', 'KC', 'SD')
    },
    # NFC WEST
    'ARZ':{
        'Home':('LAR', 'SF', 'SEA', 'NO', 'TB', 'WAS', 'NE', 'NYJ'),
        'Away':('LAR', 'SF', 'SEA', 'ATL', 'CAR', 'MIN', 'BUF', 'MIA')
    },
    'SEA':{
        'Home':('ARZ', 'SF', 'LAR', 'ATL', 'CAR', 'PHI', 'BUF', 'MIA'),
        'Away':('ARZ', 'SF', 'LAR','NO', 'TB', 'GB', 'NE', 'NYJ')
    },
    'LAR':{
        'Home':('ARZ', 'SF', 'SEA', 'ATL', 'CAR', 'NYG', 'BUF', 'MIA'),
        'Away':('ARZ', 'SF', 'SEA', 'NO', 'TB', 'DAL', 'NE', 'NYJ')
    },
    'SF':{
        'Home':('ARZ', 'LAR', 'SEA', 'NO', 'TB', 'DAL', 'NE', 'NYJ'),
        'Away':('ARZ', 'LAR', 'SEA', 'ATL', 'CAR', 'CHI', 'BUF', 'MIA')
    }
}


