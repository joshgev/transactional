# transactional
## Introduction
An experiment with transactional data structures.  By transactional data structures, I do not refer to the concepts introduced
in [this paper](http://webee.technion.ac.il/~idish/ftp/TransactionalLibrariesPLDI16.pdf), which uses the concept 
of transactions to implement atomic data structure operations for concurrent systems.  Instead, this is a much simpler experiment.

# Motivation

I got curious about this idea when I was implementing a simulation that involved making random, complex changes to a polygon 
mesh and, occasionally having to undo those complex changes.  To make things more concrete, here is an example of what an
iteration might look like in my simulation:

* Select polygon randomly
* Split the polygon into two or more polygons
* Test the change to see if I like it
* Undo change if the change is not suitable

There are two obvious ways to implement this system.  First, I could just copy my polygon mesh, make the change, and
revert to the copy if the change is not to be kept.  The issue with this approach is that, if the mesh is very large,
copying and the mesh each iteration will take more time and memory than I am willing to devote to the process.

The second way is to basically implement the "undo" key in the mesh.  The obvious way to do that is to keep track of
all the changes made to the mesh during some operation (which vertices are added, which are removed, which edges are added,
etc.).  To undo, you just go backwards in your list of atomic operations and invert each of them.  

The latter approach is what I chose to do; I augmented my mesh class to make atomic operations transactional.  After 
implementing this system, I realized that there was a more general way to solve this problem; a way that would allow
me to port this "undo key" to any program for which I needed this functionality.  The realization was my polygon mesh
was just a composite structure that boiled down to a bunch of lists, sets, and dicts.  Given that, why not just
write analogous data structures that were as close to Python's built-in structures as possible, but transactional as well.

I wrote a prototype and reimplemented the polygon mesh to use it, instead of its own custom transaction system.

# Installation

Just use pip:
```
pip install git+git://github.com/joshgev/transactional
```

# Use

Using the package is pretty easy.  There are three data structures that are already implemented: List, Dict, and Set.

Here is the system in action:

```python
from transactional.structures import List, Dict, Set
from transactional.core import Transaction

# We initialize some data structures
l = List([0, 1, 2, 3])  # The list contains 0, 1, 2, 3
d = Dict([("a", 0), ("b", 1)])  # {"a": 0, "b": 1}
s = Set([0, 1, 2, 2])  # {0, 1, 2}

# Now let's make some changes we might want to undo
with Transaction() as t:
  l.append(4) # [0, 1, 2, 3, 4]
  d["a"] = 100 # {"a": 100, "b": 1}
  s.add(-1) # {0, 1, 2, -1}

assert l == List(range(5))
assert d == Dict((("a", 100), ("b", 1)))
assert s == Set([0, 1, 2, -1])

# Now we can undo the changes:

t.undo()

assert l == List(range(4))
assert d == Dict((("a", 0), ("b", 1)))
assert s == Set([0, 1, 2])
```

There is one more tool that is implemented: Variable.  The inspiration for Variable is that one might want to make
member variables on their classes also transactional.  So let's say we have a simple class that has only one member, x.
Here is how we might use Variable:

```python
from transactional.core import Transaction, Variable

class MyClass(object):
  def __init__(self, val):
    self.x = Variable(val)

c =  MyClass(1)

# To access x, we call it like a function:
assert c.x() == 1

# Now let's change the value so we can undo it later
with Transaction() as t:
  c.x(2)
  
assert c.x() == 2

# Now let's undo it
t.undo()

assert c.x() == 1
```

## Data structure API

The API for Set, List, and Dict are similar to those of Python's set, list, and dict.  The code for the data structures 
is simple enough that their API can be fully understood after a cursory glance.  Further, the test folder contains 
more detailed use of each of these structures.
