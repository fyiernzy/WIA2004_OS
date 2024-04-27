from table_formatter import TableFormatter

FREE = False
IN_USE = True
THINK = 0
EAT = 1
WAIT = 2


class Action():
    def __init__(self, pid: int, action: int):
        self.pid = pid
        self.action = action

    def __repr__(self):
        action_names = {THINK: "THINK", EAT: "EAT", WAIT: "WAIT"}
        return f"Action(pid = {self.pid} , action = {action_names[self.action]})"


class ActionValidator():
    def validate(self, actions: list[Action], n: int):
        return self._are_actions_valid(actions, n) and self._is_sequence_valid(actions)

    def _are_actions_valid(self, actions: list[Action], n: int):
        return all(self._is_action_valid(action, n) for action in actions)

    def _is_sequence_valid(self, actions: list[Action]):
        pid_action_map = {}
        for action in actions:
            if pid_action_map.get(action.pid, False) == action.action:
                return False
            pid_action_map[action.pid] = action.action
        return True

    def _is_action_valid(self, action: Action, n: int):
        return 0 <= action.pid < n and action.action in [THINK, EAT]


class DiningPhilosopher():
    def __init__(self, n: int):
        self.n = n
        self._reset()

    def set_actions(self, actions: list[Action]):
        validator = ActionValidator()
        if validator.validate(actions, self.n):
            self._reset()
            self.actions = actions
        else:
            print("Invalid action sequence.")
            self.actions = []

    def simulate(self):
        if not self.actions:
            print("No actions set")
            return

        for action in self.actions:
            self._process_queue()
            self._process_actions(action)
            self._print_status(action)

    def _process_queue(self):
        while self.queue and self._are_chopsticks_free(self.queue[0].pid):
            self._handle_eating(self.queue.pop(0))

    def _process_actions(self, action):
        if action.action == THINK:
            self._handle_thinking(action)
        else:
            self._handle_eating(action)

    def _handle_thinking(self, action: Action):
        if self.philosophers[action.pid] == EAT:
            self._set_chopsticks_status(action.pid, FREE)
        self.philosophers[action.pid] = THINK

    def _handle_eating(self, action: Action):
        if self._are_chopsticks_free(action.pid):
            self._set_chopsticks_status(action.pid, IN_USE)
            self.philosophers[action.pid] = EAT
        else:
            self.philosophers[action.pid] = WAIT
            self.queue.append(action)

    def _set_chopsticks_status(self, pid: int, status: bool):
        self.chopsticks[pid] = status
        self.chopsticks[(pid + 1) % 5] = status

    def _are_chopsticks_free(self, pid: int):
        return self.chopsticks[pid] == FREE and self.chopsticks[(pid + 1) % self.n] == FREE

    def _print_status(self, action: Action):
        chopstick_statuses = ['In Use' if s else 'Free' for s in self.chopsticks]
        philosopher_statuses = ['Eating' if p == EAT else 'Thinking' if p == THINK else 'Waiting' for p in self.philosophers]
        queue_statuses = [str(a) for a in self.queue]

        headers = ["Position", "Chopstick", "Philosopher"]
        rows = [
            (i, chopstick_status, philosopher_status)
            for i, (chopstick_status, philosopher_status) in enumerate(zip(chopstick_statuses, philosopher_statuses))
        ]

        # Initialize and display table for current status
        table_formatter = TableFormatter(headers, rows)
        print(f"Current Action: {action}\n")
        table_formatter.display_table()

        if queue_statuses:
            print("Queue:")
            for status in queue_statuses:
                print(f"  {status}")
            print()

    def _reset(self):
        self.chopsticks = [FREE] * self.n
        self.philosophers = [THINK] * self.n
        self.queue = []
        self.actions = []


def main():
    actions = [Action(pid, action) for pid, action in [
        (0, EAT), (1, EAT), (2, EAT),
        (0, THINK), (3, EAT), (2, THINK),
        (4, EAT)]]

    dp = DiningPhilosopher(5)
    dp.set_actions(actions)
    dp.simulate()


if __name__ == '__main__':
    main()
