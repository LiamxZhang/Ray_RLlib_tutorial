import ray

# Initiate ray environment
ray.init()
# By adding the `@ray.remote` decorator, a regular Python function
# becomes a Ray remote function.
@ray.remote
def f(x):
    return x * x

# Concurrently run the remote functions
futures = [f.remote(i) for i in range(4)] # i = 0,1,2,3
print(ray.get(futures)) # [0, 1, 4, 9]


@ray.remote
class Counter(object):
    def __init__(self):
        self.n = 0

    def increment(self):
        self.n += 1

    def read(self):
        return self.n


RAY_DEDUP_LOGS=0
counters = [Counter.remote() for i in range(4)] # parallelised class id
[c.increment.remote() for c in counters] # call function increment()
futures = [c.read.remote() for c in counters] # call function read()
print(ray.get(futures)) # [1, 1, 1, 1] 

ray.shutdown()