import time
import gym
import torch

from wrappers import *
from network import *
from agent import Agent
from torch.utils.tensorboard import SummaryWriter
import warnings
import torch
from pytorch_wrappers import make_atari, wrap_deepmind


#from pytorch_wrappers import make_atari_deepmind


warnings.filterwarnings("ignore")
torch.cuda.empty_cache()




def show(agent,episode,reward,loss):
    print(f"we are in eipisode number {episode} "
            f", we are on step number {agent.current_step} "
            f", epsilon is {agent.exploration_rate} "
            f",rewards is {reward} "
            f"loss is {loss}")
# def test(env,agent):
#     number_of_episode=10
#     for _ in range(number_of_episode):
#         done=False
#         state=env.reset()
#         while


def evaluate_model(env):
    for _ in range(10):
        done = False
        state = env.reset()
        while not done:
            action = env.action_space.sample()
            state, reward, done, _ = env.step(action)
            env.render()
            time.sleep(.03)
    env.close()


env= gym.make("BreakoutNoFrameskip-v4")
# env=lambda:make_atari_deepmind("Breakout-v0",scale_values=True,clip_rewards=True)
env = SkipFrame(env, skip=4)
env = GrayScaleObservation(env)
env = ResizeObservation(env, shape=84)
env = FrameStack(env, num_stack=4)
env=ClipRewardEnv(env)


save_dir = Path("checkpoints") / datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
# load_path=Path("checkpoints","2021-09-17T11-51-24","DDQN____2000000____0.1.chkpt")

save_dir.mkdir(parents=True)
checkpoint=None
agent=Agent(150000,32,save_dir,1,.1,1000000
            ,4,(4,84,84),
            0.9,"DDQN",0.00025,1e4,10000,4,50000)
# agent.load(load_path)
# print(agent.exploration_rate)
num_of_episodes=30000
writer = SummaryWriter()
for e in range(num_of_episodes):
    done=False
    state=env.reset()
    rewards=0
    while not done:
        action=agent.select_action(state)
        next_state, reward, done, info = env.step(action)
        agent.remember(state,next_state,reward,done,action)
        state = next_state
        q, loss = agent.learn()
        rewards += reward
        # if agent.memory_initalizing_done:
        #
        #         #writer.add_scalar("loss/Number of step", loss, agent.current_step-agent.min_exp)
        if loss != None:
            writer.add_scalar("loss/Number of step ", loss, agent.current_step - agent.min_exp)
            # env.render()
        if done:
            writer.add_scalar("Reward/episode", rewards, e)
            show(agent,e,rewards,loss)
agent.save()
    #
    #
    #
    #
    #
    #
    #
# from pytorch_wrappers import make_atari, wrap_deepmind
# import numpy as np
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
#
# # Configuration paramaters for the whole setup
# seed = 42
# gamma = 0.99  # Discount factor for past rewards
# epsilon = 1.0  # Epsilon greedy parameter
# epsilon_min = 0.1  # Minimum epsilon greedy parameter
# epsilon_max = 1.0  # Maximum epsilon greedy parameter
# epsilon_interval = (
#     epsilon_max - epsilon_min
# )  # Rate at which to reduce chance of random action being taken
# batch_size = 32  # Size of batch taken from replay buffer
# max_steps_per_episode = 10000
#
# # Use the Baseline Atari environment because of Deepmind helper functions
# env = make_atari("BreakoutNoFrameskip-v4")
# # Warp the frames, grey scale, stake four frame and scale to smaller ratio
# env = wrap_deepmind(env, frame_stack=True, scale=True)
# env.seed(seed)
#
# num_actions = 4
#
#
# def create_q_model():
#     # Network defined by the Deepmind paper
#     inputs = layers.Input(shape=(84, 84, 4,))
#
#     # Convolutions on the frames on the screen
#     layer1 = layers.Conv2D(32, 8, strides=4, activation="relu")(inputs)
#     layer2 = layers.Conv2D(64, 4, strides=2, activation="relu")(layer1)
#     layer3 = layers.Conv2D(64, 3, strides=1, activation="relu")(layer2)
#
#     layer4 = layers.Flatten()(layer3)
#
#     layer5 = layers.Dense(512, activation="relu")(layer4)
#     action = layers.Dense(num_actions, activation="linear")(layer5)
#
#     return keras.Model(inputs=inputs, outputs=action)
#
#
# # The first model makes the predictions for Q-values which are used to
# # make a action.
# model = create_q_model()
# # Build a target model for the prediction of future rewards.
# # The weights of a target model get updated every 10000 steps thus when the
# # loss between the Q-values is calculated the target Q-value is stable.
# model_target = create_q_model()
#
#
#
# # In the Deepmind paper they use RMSProp however then Adam optimizer
# # improves training time
# optimizer = keras.optimizers.Adam(learning_rate=0.00025, clipnorm=1.0)
#
# # Experience replay buffers
# action_history = []
# state_history = []
# state_next_history = []
# rewards_history = []
# done_history = []
# episode_reward_history = []
# running_reward = 0
# episode_count = 0
# frame_count = 0
# # Number of frames to take random action and observe output
# epsilon_random_frames = 50000
# # Number of frames for exploration
# epsilon_greedy_frames = 1000000.0
# # Maximum replay length
# # Note: The Deepmind paper suggests 1000000 however this causes memory issues
# max_memory_length = 100000
# # Train the model after 4 actions
# update_after_actions = 4
# # How often to update the target network
# update_target_network = 10000
# # Using huber loss for stability
# loss_function = keras.losses.Huber()
#
# while True:  # Run until solved
#     state = np.array(env.reset())
#     episode_reward = 0
#
#     for timestep in range(1, max_steps_per_episode):
#         # env.render(); Adding this line would show the attempts
#         # of the agent in a pop up window.
#         frame_count += 1
#
#         # Use epsilon-greedy for exploration
#         if frame_count < epsilon_random_frames or epsilon > np.random.rand(1)[0]:
#             # Take random action
#             action = np.random.choice(num_actions)
#         else:
#             # Predict action Q-values
#             # From environment state
#             state_tensor = tf.convert_to_tensor(state)
#             state_tensor = tf.expand_dims(state_tensor, 0)
#             action_probs = model(state_tensor, training=False)
#             # Take best action
#             action = tf.argmax(action_probs[0]).numpy()
#
#         # Decay probability of taking random action
#         epsilon -= epsilon_interval / epsilon_greedy_frames
#         epsilon = max(epsilon, epsilon_min)
#
#         # Apply the sampled action in our environment
#         state_next, reward, done, _ = env.step(action)
#         state_next = np.array(state_next)
#
#         episode_reward += reward
#
#         # Save actions and states in replay buffer
#         action_history.append(action)
#         state_history.append(state)
#         state_next_history.append(state_next)
#         done_history.append(done)
#         rewards_history.append(reward)
#         state = state_next
#
#         # Update every fourth frame and once batch size is over 32
#         if frame_count % update_after_actions == 0 and len(done_history) > batch_size:
#
#             # Get indices of samples for replay buffers
#             indices = np.random.choice(range(len(done_history)), size=batch_size)
#
#             # Using list comprehension to sample from replay buffer
#             state_sample = np.array([state_history[i] for i in indices])
#             state_next_sample = np.array([state_next_history[i] for i in indices])
#             rewards_sample = [rewards_history[i] for i in indices]
#             action_sample = [action_history[i] for i in indices]
#             done_sample = tf.convert_to_tensor(
#                 [float(done_history[i]) for i in indices]
#             )
#
#             # Build the updated Q-values for the sampled future states
#             # Use the target model for stability
#             future_rewards = model_target.predict(state_next_sample)
#             # Q value = reward + discount factor * expected future reward
#             updated_q_values = rewards_sample + gamma * tf.reduce_max(
#                 future_rewards, axis=1
#             )
#
#             # If final frame set the last value to -1
#             updated_q_values = updated_q_values * (1 - done_sample) - done_sample
#
#             # Create a mask so we only calculate loss on the updated Q-values
#             masks = tf.one_hot(action_sample, num_actions)
#
#             with tf.GradientTape() as tape:
#                 # Train the model on the states and updated Q-values
#                 q_values = model(state_sample)
#
#                 # Apply the masks to the Q-values to get the Q-value for action taken
#                 q_action = tf.reduce_sum(tf.multiply(q_values, masks), axis=1)
#                 # Calculate loss between new Q-value and old Q-value
#                 loss = loss_function(updated_q_values, q_action)
#
#             # Backpropagation
#             grads = tape.gradient(loss, model.trainable_variables)
#             optimizer.apply_gradients(zip(grads, model.trainable_variables))
#
#         if frame_count % update_target_network == 0:
#             # update the the target network with new weights
#             model_target.set_weights(model.get_weights())
#             # Log details
#             template = "running reward: {:.2f} at episode {}, frame count {}"
#             print(template.format(running_reward, episode_count, frame_count))
#
#         # Limit the state and reward history
#         if len(rewards_history) > max_memory_length:
#             del rewards_history[:1]
#             del state_history[:1]
#             del state_next_history[:1]
#             del action_history[:1]
#             del done_history[:1]
#
#         if done:
#             break
#
#     # Update running reward to check condition for solving
#     episode_reward_history.append(episode_reward)
#     print(f"episode rewards is {episode_reward}")
#     if len(episode_reward_history) > 100:
#         del episode_reward_history[:1]
#     running_reward = np.mean(episode_reward_history)
#
#     episode_count += 1
#
#     if running_reward > 40:  # Condition to consider the task solved
#         print("Solved at episode {}!".format(episode_count))
#         break
