#!/usr/bin/env python

"""
oneline tree with simple search and add function

ref: https://gist.github.com/hrldcpr/2012250

Date: 2013/4/18

"""

from collections import defaultdict
from pprint import pprint

# one-line tree definition
tree = lambda: defaultdict(tree)

# converts to normal dicts
dicts = lambda t: {k: dicts(t[k]) for k in t}

# pretty print the tree
print_tree = lambda t: pprint(dicts(t))

# determine if node is leaf
is_leaf = lambda n: n == {}

# search node in the tree
# returns the node if found, None otherwise.
def tree_search_node(t, key):
    # empty tree
    if is_leaf(t): return None
    for node in t:
        if key == node: return t[node]
        found = tree_search_node(t[node], key)
        if found is not None: return found
    return None

# add a node in the tree under a parent node
# returns True if added successfully, False otherwise.
def tree_add_node(t, parent, node):
    p_node = tree_search_node(t, parent)
    if p_node is None: return False
    # add node
    p_node[node]
    return True

# add a distinct node in the tree under a parent node.
# The node must not be existent in the tree. 
# returns True if the node is distinct and added successfully
def tree_add_node_distinct(t, parent, node):
    found = tree_search_node(t, node)
    if found is None:
        return tree_add_node(t, parent, node)
    return False

# ===============================

import unittest

class OnelineTreeTestCase(unittest.TestCase):
    def setUp(self):
        self.tree = tree()
        self.tree['top']['hello']
        self.tree['top']['test']['now']

        self.tree2 = tree()
        self.tree2['top']

        self.tree3 = tree()

    def tearDown(self):
        self.tree = None
        self.tree2 = None
        self.tree3 = None

    def test_is_leaf_tree1(self):
        self.assertFalse(is_leaf(self.tree))
        self.assertFalse(is_leaf(self.tree['top']))
        self.assertTrue(is_leaf(self.tree['top']['hello']))
        self.assertFalse(is_leaf(self.tree['top']['test']))
        self.assertTrue(is_leaf(self.tree['top']['test']['now']))

    def test_is_leaf_tree2(self):
        self.assertFalse(is_leaf(self.tree2))
        self.assertTrue(is_leaf(self.tree2['top']))

    def test_is_leaf_tree3(self):
        self.assertTrue(is_leaf(self.tree3))

    def test_tree_search_node(self):
        # searching nodes
        r = tree_search_node(self.tree, 'hello')
        self.assertTrue(r != None)
        r = tree_search_node(self.tree, 'now')
        self.assertTrue(r != None)
        r = tree_search_node(self.tree, 'top')
        self.assertTrue(r != None)
        r = tree_search_node(self.tree, 'test')
        self.assertTrue(r != None)
        r = tree_search_node(self.tree, 'not exist')
        self.assertEqual(r, None)
        r = tree_search_node(self.tree2, 'any')
        self.assertEqual(r, None)

    def test_tree_add_node(self):
       # adding nodes
        r = tree_add_node(self.tree, 'hello', 'new')
        self.assertTrue(r)
        r = tree_add_node(self.tree, 'hello', 'new2')
        self.assertTrue(r)
        r = tree_search_node(self.tree, 'new')
        self.assertTrue(r != None)
        r = tree_search_node(self.tree, 'new2')
        self.assertTrue(r != None)
        r = tree_search_node(self.tree, 'new3')
        self.assertEqual(r, None)
        r = tree_add_node(self.tree, 'now', 'and then')
        self.assertTrue(r)
        r = tree_add_node(self.tree, 'not_exist', 'okok')
        self.assertFalse(r)
        print_tree(self.tree)

    def test_random_create(self):
        # create another tree by random ints
        import random
        b = tree()
        b[0] # top node
        for i in range(10): # add first level nodes
            tree_add_node_distinct(b, 0, random.randint(1,100))
        for i in range(1000): # randomly adds some nodes
            tree_add_node_distinct(b, random.randint(1,100), random.randint(1,100))
        r = tree_search_node(b, 1024)
        self.assertTrue(r == None)
        r = tree_search_node(b, 3)
        self.assertTrue(r != None)
        r = tree_search_node(b, 8)
        self.assertTrue(r != None)
        print_tree(b)
 
if __name__ == '__main__':
    unittest.main()
