import threading
import random
import time


class Fork(threading.Semaphore):
    def __init__(self, id: int):
        super().__init__(1)
        self.id = id

    def acquire(self):
        super().acquire()

    def release(self):
        super().release()

    def __repr__(self):
        return f"Fork (id: {self.id}, status: {self._value})"


NUM = 5
FORKS = [Fork(i) for i in range(NUM)]


class Philosopher():
    def __init__(self, id: int):
        self.id = id
        self.left_fork = id
        self.right_fork = (id + 1) % NUM

    def eat(self):
        print(f"Philosopher {self.id} >>> starts eating")
        self.pick_up_forks()

        time.sleep(random.randint(1, 3))

        print(f"Philosopher {self.id} >>> finishes eating")
        self.put_down_forks()

    def pick_up_forks(self):
        self._handle_forks(lambda fork: fork.acquire())

    def put_down_forks(self):
        self._handle_forks(lambda fork: fork.release())

    def _handle_forks(self, operation):
        operation(FORKS[self.left_fork])
        operation(FORKS[self.right_fork])
        print(FORKS)


def main():
    PHILOSOPHERS = [Philosopher(i) for i in range(NUM)]
    threads = []

    for philosopher in PHILOSOPHERS:
        thread = threading.Thread(target=philosopher.eat)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("\nAll Philosophers have finished eating...")


if __name__ == "__main__":
    main()
