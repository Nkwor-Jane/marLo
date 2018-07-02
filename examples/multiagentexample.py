import argparse
import gym
import marlo
from gym.envs.registration import register

import time
from marlo.multiagent import start_agents


def main():
    """Running Malmo gym env for multiple agents."""

    parser = argparse.ArgumentParser(description='Multi-agent example')
    parser.add_argument('--rollouts', type=int, default=1, help='number of rollouts')
    # Example missions: 'pig_chase.xml' or 'bb_mission_1.xml' or 'th_mission_1.xml'
    parser.add_argument('--mission_file', type=str, default="basic.xml", help='the mission xml')
    parser.add_argument('--turn_based', action='store_true')
    args = parser.parse_args()

    turn_based = args.turn_based
    print("turn based " + str(turn_based))

    number_of_rollouts = args.rollouts

    # Register the multi-agent environment.
    env_name = 'malmo-multi-agent-v0'

    register(
        id=env_name,
        entry_point='marlo.envs:MinecraftEnv',
        # Make sure mission xml is in the marlo/assets directory.
        kwargs={'mission_file': args.mission_file}
    )

    # Create one env to obtain the mission xml.
    env = gym.make(env_name)

    resolution = [800, 600]
    config = {'allowDiscreteMovement': ["move", "turn"], 'videoResolution': resolution, 'turn_based': turn_based}

    join_agents = start_agents(env, env_name, config, number_of_rollouts)

    env.init(**config)

    for i in range(number_of_rollouts):
        print("reset for new game " + str(i + 1))
        env.reset()

        done = False
        while not done:
            env.render("rgb_array")

            # TODO your agent here.
            action = env.action_space.sample()

            obs, reward, done, info = env.step(action)
            print(reward)
            print(obs)

    env.close()
    join_agents()


if __name__ == "__main__":
    main()
