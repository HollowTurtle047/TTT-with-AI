
import gym
from gym import spaces
from gym.utils import seeding
from collections import Counter

class TTTEnv(gym.Env):
    """ 
    Observation:
        board
    
    Action:
        Type: Discrete(<=9)
    
    """
    
    def __init__(self):
        # self.BOARD = [0]*9
        self.viewer = None
        self.action_space = spaces.Discrete(9)
        self.observation_space = spaces.MultiDiscrete([3]*9+[2])
        self.n_action = self.action_space.n
        self.n_features = 10
        
    def reset(self):
        self.state = [0]*9 + [0]
        return self.state
        
    def render(self, mode='human'):
        # num2piece = {0:' ', 1:'X', -1:'O'}
        # board = [num2piece[x] if x in self.state else x for x in self.state]
        # print('')
        # print(' {} | {} | {} '.format(board[0],board[1],board[2]))
        # print('---+---+---')
        # print(' {} | {} | {} '.format(board[3],board[4],board[5]))
        # print('---+---+---')
        # print(' {} | {} | {} '.format(board[6],board[7],board[8]))
    
        screen_width = 300
        screen_height = 300
        
        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height)
            line1 = rendering.Line((0, 100), (300, 100))
            line2 = rendering.Line((0, 200), (300, 200))
            line3 = rendering.Line((100, 0), (100, 300))
            line4 = rendering.Line((200, 0), (200, 300))
            # set color
            line1.set_color(0, 0, 0)
            line2.set_color(0, 0, 0)
            line3.set_color(0, 0, 0)
            line4.set_color(0, 0, 0)
            self.viewer.add_geom(line1)
            self.viewer.add_geom(line2)
            self.viewer.add_geom(line3)
            self.viewer.add_geom(line4)
            # [i for i,x in enumerate(board) if x==piece]
            self.pieces = [None]*9
            for i in range(9):
                self.pieces[i] = rendering.make_circle(30)
                circle_transform = rendering.Transform(translation=((i%3)*100+50,(i//3)*100+50))
                self.pieces[i].add_attr(circle_transform)
                self.pieces[i].set_color(1,1,1)
                self.viewer.add_geom(self.pieces[i])
        
        board = self.state[:-1]
        for i,x in enumerate(board):
            if x==1:
                self.pieces[i].set_color(1,0,0)
            elif x==-1:
                self.pieces[i].set_color(0,0,1)
            else:
                self.pieces[i].set_color(1,1,1)
            
        return self.viewer.render(return_rgb_array=mode == 'rgb_array')
            
    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        
        board, turn = self.state[:-1], self.state[-1]
        reward = 0
        done = False
        # player_0 turn
        if turn==0:
            if board[action] == 0:
                board[action] = 1
                player_0 = [i for i,x in enumerate(board) if x==1]
                if isWin(player_0): # player_0 win
                    done = True
                    reward = 1
                elif 0 not in board: # draw
                    done = True
            else: # not valid
                done = True
                reward = -1
        # player_1 turn
        else:
            if board[action] == 0:
                board[action] = -1
                player_1 = [i for i,x in enumerate(board) if x==-1]
                if isWin(player_1): # player_1 win
                    done = True
                    reward = -1
                elif 0 not in board: # draw
                    done = True
            else: # not valid
                done = True
                reward = 1
                
        # switch turn
        turn = int (not turn)
        
        self.state = board + [turn]
        return self.state, reward, done, {}
    
    # def close(self):
    #     if self.viewer:
    #         self.viewer.close()
    #         self.viewer = None
    
def isWin(player):
    
    row = [i//3 for i in player]
    col = [i%3 for i in player]
    
    if 0 in player and 4 in player and 8 in player:
        return True
    elif 2 in player and 4 in player and 6 in player:
        return True
    elif Counter(row).most_common(1)[0][1] == 3:
        return True
    elif Counter(col).most_common(1)[0][1] == 3:
        return True
    else:
        return False