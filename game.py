class Game:
    def __init__(self,id):
        self.p1Went=False
        self.p2Went=False
        self.ready=False
        self.id=id
        self.moves=[None,None]
        self.wins=[0,0]
        self.ties=0

    def get_player_moves(self):
        return self.moves
    
    def play(self,player,move):
        self.moves[player]=move
        if player==0:
            self.p1Went=True
        else:
            self.p2Went=True

    def is_connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):
        # The Following Dictionary is in such format that 
        # Key Beats Value
        winDict={"R":"S","S":"P","P":"R"}
        p1_move=self.moves[0].upper()[0]
        p2_move=self.moves[1].upper()[0]
        w=-1
        if winDict[p1_move]==p2_move:
            # P1 Wins
            w=0
        elif winDict[p2_move]==p1_move:
            w=1
        return w
    def resetWent(self):
        self.p1Went=False
        self.p2Went=False