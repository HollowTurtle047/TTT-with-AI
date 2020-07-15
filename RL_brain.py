
import numpy as np
import tensorflow as tf
from tensorflow.keras import models, layers
import os
np.random.seed(1)
tf.random.set_seed(1)


class DeepQNetwork:
    
    def _build_net(self):
        #build net
        self.q_target = models.Sequential([
            layers.Dense(200, input_shape = (10,), activation='relu'),
            layers.Dense(100, activation='relu'),
            layers.Dense(9, activation='softmax'),
        ])
        self.q_eval = models.Sequential([
            layers.Dense(200, input_shape = (10,) , activation='relu'),
            layers.Dense(100, activation='relu'),
            layers.Dense(9, activation='softmax'),
        ])
        self.q_target.compile(
            optimizer='adam',
            loss='mean_squared_error',
            metrics=['accuracy']
        )
        self.q_eval.compile(
            optimizer='adam',
            loss='mean_squared_error',
            metrics=['accuracy']
        )
        if not os.path.isdir('models/'):
            os.makedirs('models/')
        self.q_target.save(self.target_path)
        self.q_eval.save(self.evalue_path)
        
    def __init__(
        self,
        n_actions,
        n_features,
        name,
        op_name,
        learning_rate=0.01,
        reward_decay=0.9,
        e_greedy=0.9,
        replace_target_iter=300,
        memory_size=500,
        batch_size=32,
        e_greedy_increment=None,
        # output_graph=False,
    ):
        self.n_actions = n_actions
        self.n_features = n_features
        self.name = name
        self.op_name = op_name
        self.target_path = 'models/'+self.name+'_target.h5'
        self.evalue_path = 'models/'+self.name+'_evalue.h5'
        self.op_target_path = 'models/'+self.op_name+'_target.h5'
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon_max = e_greedy
        self.replace_target_iter = replace_target_iter
        self.memory_size = memory_size
        self.batch_size = batch_size
        self.epsilon_increment = e_greedy_increment
        self.epsilon = 0 if e_greedy_increment is not None else self.epsilon_max
        
        # total learning step
        self.learn_step_counter = 0

        # initialize zero memory [s, a, r, s_]
        self.memory = np.zeros((self.memory_size, n_features * 2 + 2))

        # consist of [target_net, evaluate_net]
        if os.path.isfile(self.target_path) and os.path.isfile(self.evalue_path):
            # for i in range(100):
            self.q_target = models.load_model(self.target_path)
            self.q_eval = models.load_model(self.evalue_path)
        else :
            self._build_net()
        self.q_op_target = models.load_model(self.op_target_path)
            
        # self.cost_his = []
        
    def choose_action(self, observation):
        board, turn = observation[:-1], observation[-1]
        blocks = [i for i,x in enumerate(board) if x==0]
        input_data = np.array(board + [turn])[np.newaxis, :]
        if np.random.uniform() < self.epsilon:
            # print('predict')
            actions_value = self.q_eval.predict(input_data)[0]
            actions_list = np.argsort(actions_value)[::-1]
            
            # shuffle same value
            left = 0
            right = 1
            for i in range(actions_list.size-1):
                if actions_value[actions_list[i]] != actions_value[actions_list[i+1]]:
                    np.random.shuffle(actions_list[left:right])
                    left = right
                right += 1
            np.random.shuffle(actions_list[left:right]) # shuffle last sequence
        else:
            # print('random')
            actions_list = list(range(self.n_actions))
            np.random.shuffle(actions_list)
        # print('action list:'+str(actions_list))
        
        for action in actions_list:
            if action in blocks:
                return int(action)
            
    def store_transition(self, s, a, r, s_):
        if not hasattr(self, 'memory_counter'):
            self.memory_counter = 0
        transition = np.hstack((s, [a, r], s_))
        # replace the old memory with new memory
        index = self.memory_counter % self.memory_size
        self.memory[index, :] = transition
        self.memory_counter += 1
        
    def learn(self):
        # check to replace target parameters
        if self.learn_step_counter % self.replace_target_iter == 0:
            self.q_eval.save(self.target_path)
            self.q_op_target = models.load_model(self.op_target_path)
            print('\ntarget_params_replaced\n')

        # sample batch memory from all memory
        if self.memory_counter > self.memory_size:
            sample_index = np.random.choice(self.memory_size, size=self.batch_size)
        else:
            sample_index = np.random.choice(self.memory_counter, size=self.batch_size)
        batch_memory = self.memory[sample_index, :]
        
        s = batch_memory[:, :self.n_features]
        a = batch_memory[:, self.n_features]
        r = batch_memory[:, self.n_features+1]
        s_op = batch_memory[:, -self.n_features:]
        
        q_eval = self.q_eval.predict(s)
        q_op = self.q_op_target.predict(s_op)
        # h_range = 9 # horizontal range of opponent predict
        s_ = np.tile(s_op, (1, 9))
        s_.resize(s_.size//10, 10)
        for i,x in enumerate(s_):
            if x[9]==0:
                x[i%9] = 1
                x[9] = 1
            else:
                x[i%9] = -1
                x[9] = 0
        q_next = self.q_target.predict(s_)
        q_next = np.max(q_next, axis=1)
        q_next.resize(q_next.size//(self.n_features-1), self.n_features-1)
        
        q_target = q_eval.copy()
        batch_index = np.arange(self.batch_size, dtype=np.int32)
        eval_act_index = a.astype(int)
        q_target[batch_index, eval_act_index] = r + self.gamma * np.sum(q_next * q_op, axis=1)
        
        # with tf.device('/cpu:0'):
        self.q_eval.fit(s, q_target)
        
        # increasing epsilon
        self.epsilon = self.epsilon + self.epsilon_increment if self.epsilon < self.epsilon_max else self.epsilon_max
        self.learn_step_counter += 1

if __name__ == '__main__':
    DQN = DeepQNetwork(9,10,'test_0','test_1')
    print(DQN.choose_action(([0]*9+[0])))
        