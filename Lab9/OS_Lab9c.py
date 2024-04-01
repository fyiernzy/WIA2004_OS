import threading
import time

room = threading.Semaphore(4)
forks = [threading.Semaphore(1) for _ in range(5)]


def philosopher(num):
    # wait to be signalled and hungry...
    room.acquire()
    # print the philosopher which is hungry
    print(f"Philosopher {num} is hungry")

    # lock the semaphore - right fork
    forks[num].acquire()

    # lock the semaphore - left fork
    forks[(num + 1) % 5].acquire()

    # print the philosopher that gets forks 
    print(f"Philosopher {num} gets forks {num} and {(num + 1) % 5}")

    # only when both left and right forks are available...
    eat(num)

    # wait for the current thread for 2 seconds...
    time.sleep(2)

    # print the philosopher which finished eating and release the forks
    print(f"Philosopher {num} has finished eating")
    print(f"Philosopher {num} puts down forks {num} and {(num + 1) % 5}")

    # release the semaphore (forks)...
    forks[(num + 1) % 5].release()
    forks[num].release()
    room.release()

# method for philosopher to eat 
def eat(num):
    print(f"Philosopher {num} is eating")

# driver code 
if __name__ == "__main__":

    # initialize philosophers array 
    philosophers = []

    # append the philosophers array 
    for i in range(5):
        philosophers.append(threading.Thread(target=philosopher, args=(i,)))
        philosophers[-1].start()

    for philosopher_thread in philosophers:
        philosopher_thread.join()

    print("\nAll Philosophers have finished eating...")