import pickle
import pprint

data1 = {'a': [1, 2.0, 3, 4+6j],
         'b': ('string', u'Unicode string'),
         'c': None}

selfref_list = [1, 2, 3]
selfref_list.append(selfref_list)
print ' id ', hex(id(data1))

testfile = '/tmp/data.pkl'
output = open(testfile, 'wb')

# Pickle dictionary using protocol 0.
pickle.dump(data1, output)
#print pickle.dumps(data1)

# Pickle the list using the highest protocol available.
pickle.dump(selfref_list, output, -1)
#print pickle.dumps(selfref_list)

output.close()

#------------------#

pkl_file = open(testfile, 'rb')

data1 = pickle.load(pkl_file)
pprint.pprint(data1)
print type(data1)

data2 = pickle.load(pkl_file)
pprint.pprint(data2)
print ' id ', hex(id(data2)), 'ele ', hex(id(data2[-1]))
print type(data2)

try:
    data3 = pickle.load(pkl_file)
    print data3
except EOFError as e:
    print e.message

pkl_file.close()

#------------------#

from collections import defaultdict

colours = (
    ('Yasoob', 'Yellow'),
    ('Ali', 'Blue'),
    ('Arham', 'Green'),
    ('Ali', 'Black'),
    ('Yasoob', 'Red'),
    ('Ahmed', 'Silver'),
)

favourite_colours = defaultdict(list)

for name, colour in colours:
    favourite_colours[name].append(colour)

print(favourite_colours)

from collections import Counter

favs = Counter(name for name, colour in colours)
print(favs)

from collections import deque
d = deque()
d.append('1')
d.append('2')
d.append('3')
print(len(d))
print(d[0])
print(d[-1])

d = deque(range(5))
print(len(d))
d.popleft()
d.pop()
print(d)

d = deque([1,2,3,4,5])
d.extendleft([0])
d.extend([6,7,8])
print(d)

#------------------#

import itertools
# Uses 'yield'

letters = ['a', 'b', 'c', 'd', 'e', 'f']
booleans = [1, 0, 1, 0, 0, 1]
numbers = [23, 20, 44, 32, 7, 12]
decimals = [0.1, 0.7, 0.4, 0.4, 0.5]

print list(itertools.chain(letters, letters[3:]))

for i in itertools.count(10, 0.25):
    if i < 20: print i,
    else: 
        print
        break

print list(itertools.compress(letters, booleans))
print list(itertools.imap(lambda x,y: x*y, numbers, decimals))
print list(itertools.imap(None, numbers, decimals))

#------------------#

from functools import partial
def power(base, exponent): return base ** exponent
square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print square(2)
print cube(2)

#------------------#

