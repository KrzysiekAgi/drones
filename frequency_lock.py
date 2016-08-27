import time


class frequency_lock():
    def __init__(self, period):
        self.last_action = time.time()
        self.period = period

    def can_act(self):
        current = time.time()
        s_since_last = abs(self.last_action - current)
        if s_since_last > self.period:
            self.last_action = current
            return True
        else:
            return False
