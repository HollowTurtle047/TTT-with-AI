
from TTT import TTTEnv
from RL_brain import DeepQNetwork
import time

def train():
    step = 0
    for episode in range(400):
        observation = env.reset()
        first_step = True
        
        while True:
            # 刷新环境
            env.render()

            # 控制学习起始时间和频率 (先累积一些记忆再开始学习)
            if (step > 100) and (step % 10 == 0):
                print('Step:{}'.format(step))
                RL_0.learn()
                RL_1.learn()
            
            if observation[9] == 0:
                # DQN 根据观测值选择行为
                action = RL_0.choose_action(observation)
                
                # 环境根据行为给出下一个 state, reward, 是否终止
                observation_new, reward, done, _ = env.step(action)
                
                 # DQN 存储记忆
                if done:
                    RL_0.store_transition(observation, action, 1, observation_new)
                    RL_1.store_transition(observation_old, action_old, -0.2, observation)
                    break
                elif first_step:
                    first_step = False
                else:
                    RL_1.store_transition(observation_old, action_old, 0, observation)
                
            else:
                # DQN 根据观测值选择行为
                action = RL_1.choose_action(observation)
                
                # 环境根据行为给出下一个 state, reward, 是否终止
                observation_new, reward, done, _ = env.step(action)
                
                if done:
                    RL_1.store_transition(observation, action, 1, observation_new) # reward -1 means it wins
                    RL_0.store_transition(observation_old, action_old, -0.2, observation)
                    break
                else:
                    RL_0.store_transition(observation_old, action_old, 0, observation) # reward_old always 0
            
            # 将下一个 state_ 变为 下次循环的 state, 保存上一个state
            observation_old, observation = observation, observation_new
            action_old = action
            
            step += 1
            
def load_DQN(
    epsilon_start=0.5
):
    global RL_0
    global RL_1
    try:
        RL_1 = DeepQNetwork(
            env.n_action, env.n_features,
            'player_1', 'player_0',
            # replace_target_iter = 200,
            memory_size = 4000,
            batch_size = 500,
            epsilon_start=epsilon_start,
            e_greedy_increment=0.01
        )
    except:
        RL_0 = DeepQNetwork(
            env.n_action, env.n_features,
            'player_0', 'player_1',
            # replace_target_iter = 200,
            memory_size = 4000,
            batch_size = 500,
            epsilon_start=epsilon_start,
            e_greedy_increment=0.01
        )
        RL_1 = DeepQNetwork(
            env.n_action, env.n_features,
            'player_1', 'player_0',
            # replace_target_iter = 200,
            memory_size = 4000,
            batch_size = 500,
            epsilon_start=epsilon_start,
            e_greedy_increment=0.01
        )
    else:
        RL_0 = DeepQNetwork(
            env.n_action, env.n_features,
            'player_0', 'player_1',
            # replace_target_iter = 200,
            memory_size = 4000,
            batch_size = 500,
            epsilon_start=epsilon_start,
            e_greedy_increment=0.01
        )
        
if __name__ == '__main__':
    
    env = TTTEnv()
    for i in range(3):
        load_DQN(epsilon_start=i/20+0.7)
        train()
        
    print(i)
    