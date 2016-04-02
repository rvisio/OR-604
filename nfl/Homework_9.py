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
    }
}
