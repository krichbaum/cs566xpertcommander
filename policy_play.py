import torch
from training.instantiate import instantiate
from training.utils import ParamDict
from utils import plot_learning_curve, plot_testing
from cs566xpertcommander.the_game import Env
from training.duel_dqn import DuelDQN
from training.policy import Policy

import warnings
warnings.filterwarnings("ignore")

# hyperparameters
policy_params = ParamDict(
    policy_class=Policy,   # Policy class to use (replaced later)
    hidden_dim=128,         # dimension of the hidden state in actor network
    learning_rate=1e-3,    # learning rate of policy update
    batch_size=1024,       # batch size for policy update
    policy_epochs=25,       # number of epochs per policy update
    entropy_coef=0.001    # hyperparameter to vary the contribution of entropy loss
)
params = ParamDict(
    policy_params=policy_params,
    rollout_size=5000,     # number of collected rollout steps per policy update
    num_updates=100,       # number of training policy iterations
    discount=0.999,        # discount factor
    plotting_iters=50,    # interval for logging graphs and policy rollouts
    # env_name=Env(),  # we are using a tiny environment here for testing
)
rollouts, policy = instantiate(params)
policy.actor.load_state_dict(torch.load('./models/multi_policy1.pt'))

# rollouts, policy2 = instantiate(params)
# policy2.actor.load_state_dict(torch.load('./models/policy_single.pt'))
#
# rollouts, policy3 = instantiate(params)
# policy3.actor.load_state_dict(torch.load('./models/policy_single.pt'))
#
# rollouts, policy4 = instantiate(params)
# policy4.actor.load_state_dict(torch.load('./models/policy_single.pt'))

NUM_OF_PLAYERS = 1
config = {
    'num_players': NUM_OF_PLAYERS,
    'log_filename': './logs/policy_agent.log',
    'static_drawpile': False,
}
env = Env(config)

evaluations = []
num_iter = 50
for i in range(num_iter):  # lets play 50 games
    # env.run_agents([policy, policy2, policy3, policy4])
    env.run_agents([policy])
    evaluations.append(env.get_num_cards_in_drawpile())
print('GAME OVER!')

plot_testing(evaluations, num_iter)