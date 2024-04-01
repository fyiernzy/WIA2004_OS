import threading
import random
import time

class Philosopher:
    def __init__(self, id):
        self.id = id
        self.left_fork = id
        self.right_fork = (id + 1) % num_philosophers

    def think(self):
        print(f"Philosopher {self.id} is thinking and waiting.")
        time.sleep(1)

    def eat(self):
        self.pick_up_forks()
        print(f"Philosopher {self.id} has started eating with forks {self.left_fork} and {self.right_fork}.")
        print(f"State: {self.get_state()}")
        print("----------------------------------------------------------------------------------------")
        print()
        print()

        # Simulate eating for some time
        time.sleep(random.randint(1, 3))

        self.put_down_forks()
        print(f"Philosopher {self.id} has finished eating and released forks {self.left_fork} and {self.right_fork}.")
        print(f"State: {self.get_state()}")
        print("----------------------------------------------------------------------------------------")
        print()
        print()

    def pick_up_forks(self):
        forks[self.left_fork].acquire()
        forks[self.right_fork].acquire()

    def put_down_forks(self):
        forks[self.left_fork].release()
        forks[self.right_fork].release()

    def get_state(self):
        return f"Forks: {[fork.locked() for fork in forks]}"

def print_initial_state():
    print("Initial State:")
    print(f"Forks: {[fork.locked() for fork in forks]}")
    print("----------------------------------------------------------------------------------------")
    print()
    print()

def print_final_state():
    print("Final State:")
    print(f"Forks: {[fork.locked() for fork in forks]}")
    print("----------------------------------------------------------------------------------------")
    print()

# Main program

num_philosophers = int(input("Enter the number of philosophers: "))
forks = [threading.Lock() for _ in range(num_philosophers)]

philosophers = [Philosopher(i) for i in range(num_philosophers)]

print_initial_state()

threads = []
for philosopher in philosophers:
    thread = threading.Thread(target=philosopher.eat)
    thread.start()
    threads.append(thread)

time.sleep(10)  # Run the simulation for 10 seconds
print_final_state()

# Wait for all threads to finish
for thread in threads:
    thread.join()