# 1) Import the random function and generate both a random number between 0 and 1 as well as a random number between 1 and 10.

# 2) Use the datetime library together with the random number to generate a random, unique value.

from random import random, randint
from datetime import datetime

# 1
# 0-1
print(random())
print(random())
print(random())

# 1-10
print(randint(1, 10))
print(randint(1, 10))
print(randint(1, 10))

# 2
print(str(random()) + str(datetime.now()))
print(str(random()) + str(datetime.now()))
print(str(random()) + str(datetime.now()))
