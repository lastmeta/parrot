import os
from functools import partial
from boxset.aid import root, get, put, env, var


root = partial(root, os.path.abspath(__file__))
get = partial(get, root=root)
put = partial(put, root=root)
env = partial(env, get=get, root=root)
