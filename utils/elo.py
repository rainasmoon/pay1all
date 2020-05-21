# -*- coding: UTF-8 -*- 
'''
Created on 2019-10-23

@author: Administrator
'''


class Elorating:
    ELO_RESULT_WIN = 1
    ELO_RESULT_LOSS = -1
    ELO_RESULT_TIE = 0

    ELO_RATING_DEFAULT = 1500

    ascores = 0
    bscores = 0
    awinratio = 0
    bwinratio = 0
    score_adjust = 0

    def __init__(self, ascores=ELO_RATING_DEFAULT, bscores=ELO_RATING_DEFAULT):

        def compute_win_ratio(score1, score2):
            ratio = 1 / (1 + pow(10, (score2 - score1) / 400))
            return round(ratio, 2)

        self.ascores = ascores
        self.bscores = bscores        
        self.awinratio = compute_win_ratio(self.ascores, self.bscores)
        self.bwinratio = compute_win_ratio(self.bscores, self.ascores)

    def win(self):        
        self.score_adjust = 1  
        self.caculate_scores()      
           
    def lose(self):
        self.score_adjust = 0
        self.caculate_scores()
        
    def tie(self):
        self.score_adjust = 0.5
        self.caculate_scores()
        
    def caculate_scores(self):

        def computeK(rating):
            if rating >= 2400:
                return 16
            elif rating >= 2100:
                return 24
            else:
                return 36

        self.ascores = self.ascores + computeK(self.ascores) * (self.score_adjust - self.awinratio)
        self.bscores = self.bscores + computeK(self.bscores) * (1 - self.score_adjust - self.bwinratio)

    def __str__(self):
        return '[{0}:{1}:{2}:{3}]'.format(self.ascores, self.bscores, self.awinratio, self.bwinratio) 


if __name__ == '__main__':
    a = Elorating(ascores=1500, bscores=1500)
    print(a)
    a.win()
    print(a)
    
    a = Elorating(ascores=1500, bscores=1500)
    print(a)
    a.lose()
    print(a)
    
    a = Elorating(ascores=1500, bscores=1500)
    print(a)
    a.tie()
    print(a)
    
    a = Elorating(ascores=1500, bscores=1600)
    print(a)
    a.tie()
    print(a)
    
    a = Elorating(ascores=1600, bscores=1500)
    print(a)
    a.tie()
    print(a)
    
    a = Elorating(ascores=1500, bscores=1900)
    a.win()
    print(a)
    a = Elorating(ascores=1900, bscores=1500)
    a.win()
    print(a)
