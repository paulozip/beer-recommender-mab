import numpy as np

class Bandit(object):
    '''
    Base Bandit Class
    '''
    def __init__(self, total_arms):
        self._total_arms   = total_arms
        self._arms_rewards = { key: [0.0] for key in range(self._total_arms) }
    
    def act(self):
        pass
    
    def update(self, arm, reward):
        if arm in self._arms_rewards:
            self._arms_rewards[arm].append(reward)
        else:
            self._arms_rewards[arm] = [reward]
    
    def reduction_rewards(self, func=np.mean):
        return np.array([func(self._arms_rewards[i]) for i in range(self._total_arms)])

class EpsilonGreedy(Bandit):
    def __init__(self, total_arms, epsilon=0.3):
        super().__init__(total_arms)
        self._total_arms = total_arms
        self._epsilon = epsilon

    def pull(self):
        '''
        Pull an arm
        '''
        if np.random.choice([True, False], p=[self._epsilon, 1.0 - self._epsilon]):
            # Exploration
            action = np.random.choice(range(self._total_arms))
            return action, 'exploration', self._arms_rewards[action]
        else:
            # Exploitation
            action = np.argmax(self.reduction_rewards())
            return action, 'exploitation', self._arms_rewards[action]