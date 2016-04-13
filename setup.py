try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A PageRank-style node-centrality algorithm for \
    ranking vertices (nodes) in an arbitrary weighted digraph.',
    'author': 'Arthur Tilley',
    'url': 'https://github.com/aetilley/pyrron',
    'author_email': 'aetilley@gmail.com',
    'version': '0.1',
    'install requires': [] #['nose'],
    'packages': ['pyrron'],
    'scripts': [],
    'name': 'pyrron'
}

setup(**config)
