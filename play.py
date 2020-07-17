
from TTT import TTTEnv
from RL_brain import DeepQNetwork
import time

def play():
    for i in range(10):
        observation = env.reset()
        
        while True:
            # 刷新环境
            env.render()

            if observation[9] == 0:
                # DQN 根据观测值选择行为
                action = RL_0.choose_action(observation)
                print('AI_0 action:'+str(action+1))
                # 环境根据行为给出下一个 state, reward, 是否终止
                observation_, reward, done, _ = env.step(action)

            else:
                action = RL_1.choose_action(observation)
                print('AI_1 action:'+str(action+1))
                # action = int(input('')) - 1
                observation_, reward, done, _ = env.step(action)

            # # 将下一个 state_ 变为 下次循环的 state
            observation = observation_
            # 如果终止, 就跳出循环
            if done:
                print('Reward:'+str(reward))
                env.render()
                input('Press Enter to continue')
                break
            
            time.sleep(0.5)
        
if __name__ == '__main__':
    env = TTTEnv()
    RL_0 = DeepQNetwork(
        env.n_action, env.n_features,
        'player_0', 'player_1',
        e_greedy = 1,
    )
    RL_1 = DeepQNetwork(
        env.n_action, env.n_features,
        'player_1', 'player_0',
        e_greedy = 1,
    )
    play()
    