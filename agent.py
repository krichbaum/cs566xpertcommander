import torch
from training.policy import Policy
from training.AC_policy import ACPolicy
from training.PPO import PPO
from training.instantiate import instantiate
import sys
import logging
from training.utils import ParamDict
from training.training import Trainer
from utils import plot_learning_curve, plot_testing
from matplotlib import pyplot as plt
import numpy as np
import warnings
import torch
warnings.filterwarnings("ignore")
import pickle

sys.path.append('../')
from cs566xpertcommander.the_game import Env


# hyperparameters
policy_params = ParamDict(
    policy_class=PPO,   # Policy class to use (replaced later)
    hidden_dim=128,         # dimension of the hidden state in actor network
    learning_rate=1e-3,    # learning rate of policy update
    batch_size=1024,       # batch size for policy update
    policy_epochs=25,       # number of epochs per policy update
    entropy_coef=0.002    # hyperparameter to vary the contribution of entropy loss
)
params = ParamDict(
    policy_params=policy_params,
    rollout_size=5000,     # number of collected rollout steps per policy update
    num_updates=200,       # number of training policy iterations
    discount=0.99,        # discount factor
    plotting_iters=100,    # interval for logging graphs and policy rollouts
    # env_name=Env(),  # we are using a tiny environment here for testing
)

NUM_OF_PLAYERS = 1

config = {
    'num_players': NUM_OF_PLAYERS,
    'log_filename': './logs/policy_agent.log',
    'static_drawpile': False,
}
logging.basicConfig(filename=config['log_filename'], filemode='w', level=logging.INFO)
env = Env(config)

rollouts, policy = instantiate(params)
trainer = Trainer()
rewards, deck_ends = trainer.train(env, rollouts, policy, params)

my_dict = {'single_agent': deck_ends}
with open('pickle_files/single_agent.pickle', 'wb') as f:
    pickle.dump(my_dict, f)
    
print("Training completed!")

torch.save(policy.actor.state_dict(), './models/policy.pt')

evaluations = []
num_iter = 50
for i in range(num_iter):  # lets play 50 games
    env.run_PG(policy)
    evaluations.append(env.get_num_cards_in_drawpile())
print('GAME OVER!')

bins = np.linspace(0, 100, 11)
plt.hist(evaluations, bins=bins) 
plt.title('Histogram of played games')
plt.xlabel('drawpile size')
plt.ylabel('no of games')
plt.ylim([0, 50])
plt.show()

plot_testing(evaluations, num_iter)