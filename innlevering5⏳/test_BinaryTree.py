import unittest
from BinaryTree import BinaryTree
from BinaryTreeNode import BinaryTreeNode
from collections import namedtuple
import pandas as pd
import numpy as numpy
from collections import namedtuple
from BinaryTree import BinaryTree


class globalVar:
    #lightweight objs
    Person = namedtuple('Person','etternavn fornavn adresse postnr area')
    p1 = Person('KRISTIANSEN','MORTEN KRISTIAN', 'LEINAHYTTA 36', '7224', 'MELHUS')
    p2 = Person('STAVANG', 'ELISABETH', 'ESPENES 116', '4684', 'BYGLAND')
    p3 = Person('SYVERSEN', 'HARISHANKAR', 'SISIKVEIEN 84', '1390', 'VOLLEN')
    p4 = Person('TYRIBERGET', 'EDWARD J.', 'HALLAND JOHAN 66', '5649', 'EIKELANDSOSEN')
    p5 = Person('AASE','TRINE', 'LEINAHYTTA 360', '7200', 'ROGNE')
    p6 = Person('AAASE','MÅSE', 'LEINAHYTTA 311', '100', 'BERGEN')


class BinaryTreeTest(unittest.TestCase):

    def test_insert(self):    
        var = globalVar() #Contains variables for tree insertion 
        bTree = BinaryTree()
        bTree.insert(value= var.p1)
        self.assertEqual(bTree._root.value, var.p1)
        bTree.insert(value=var.p2)
        self.assertEqual(bTree.findRightMost(bTree._root).value, var.p2)
        bTree.insert(value=var.p5)
        self.assertEqual(bTree.findLeftMost(bTree._root).value, var.p5 )


    def test_root(self):
        var = globalVar() #Contains variables for tree insertion 
        bTree = BinaryTree()
        bTree.insert(value= var.p1)
        bTree.insert(value= var.p2)
        bTree.insert(value= var.p3)
        self.assertEqual(bTree._root.value,  var.p1)
        
        bTree2 = BinaryTree()
        bTree2.insert(value= var.p4)
        bTree2.insert(value= var.p5)
        self.assertEqual(bTree2._root.value,  var.p4)
    

    def test_not_accepting_duplicates(self):
        var = globalVar() #Contains variables for tree insertion 
        bTree = BinaryTree()
        bTree.insert(value= var.p1)
        self.assertTrue(bTree.insert(value= var.p2)) 
        with self.assertRaises(Exception): #Insert for second time, expect an exception
            bTree.insert(value= var.p1)
    
    def test_findLeftMost(self):
        var = globalVar() #Contains variables for tree insertion 
        bTree = BinaryTree()
        bTree.insert(value= var.p1)
        bTree.insert(value= var.p2)
        bTree.insert(value= var.p5)
        bTree.insert(value= var.p4)
        self.assertEqual(bTree.findLeftMost(bTree._root).value, var.p5) #The smallest value, ('AASE')
        bTree.insert(value= var.p6)
        bTree.insert(value= var.p3)
        self.assertEqual(bTree.findLeftMost(bTree._root).value, var.p6)

    def test_findRightMost(self):
        var = globalVar() #Contains variables for tree insertion 
        bTree = BinaryTree()
        bTree.insert(value= var.p1)
        bTree.insert(value= var.p2)
        self.assertEqual(bTree.findRightMost(bTree._root).value, var.p2)
        bTree.insert(value= var.p5)
        bTree.insert(value= var.p4)
        self.assertEqual(bTree.findRightMost(bTree._root).value, var.p4) 
    
    def test_findMax(self):
        var = globalVar() #Contains variables for tree insertion 
        bTree = BinaryTree()
        bTree.insert(value= var.p1)
        bTree.insert(value= var.p2)
        self.assertEqual(bTree.findMax().value, var.p2)
        bTree.insert(value= var.p3)
        bTree.insert(value= var.p5)
        bTree.insert(value= var.p4)
        self.assertEqual(bTree.findMax().value, var.p4)
        bTree.insert(value= var.p6)

    def test_findMin(self):
        var = globalVar() #Contains variables for tree insertion 
        bTree = BinaryTree()
        bTree.insert(value= var.p1)
        bTree.insert(value= var.p2)
        self.assertEqual(bTree.findMin().value, var.p1)
        bTree.insert(value= var.p5)
        self.assertEqual(bTree.findMin().value, var.p5)

    def test_find(self):
        var = globalVar() #Contains variables for tree insertion 
        bTree = BinaryTree()
        bTree.insert(value= var.p1)
        bTree.insert(value= var.p2)
        bTree.insert(value= var.p3)
        bTree.insert(value= var.p5)
        bTree.insert(value= var.p4)
        self.assertEqual(bTree.find(var.p1).value, var.p1)
        self.assertEqual(bTree.find(var.p4).value, var.p4)


    def test_deleteMin(self):
        var = globalVar() #Contains variables for tree insertion 
        bTree = BinaryTree()
        bTree.insert(value= var.p1)
        bTree.insert(value= var.p2)
        bTree.insert(value= var.p5)
        self.assertEqual(bTree.find(var.p5).value, var.p5)
        bTree.deleteMin()
        with self.assertRaises(Exception): 
            bTree.find(var.p5).value #Looking for deleted element

    def test_deleteMax(self):
        var = globalVar() #Contains variables for tree insertion 
        bTree = BinaryTree()
        bTree.insert(value= var.p1)
        bTree.insert(value= var.p2)
        bTree.insert(value= var.p5)
        bTree.insert(value= var.p6)
        bTree.insert(value= var.p4)
        self.assertEqual(bTree.find(var.p4).value, var.p4)
        bTree.deleteMax()
        with self.assertRaises(Exception): 
            bTree.find(var.p4).value #Looking for deleted element


    #Funker ikke
    def test_delete(self):
        var = globalVar() #Contains variables for tree insertion 
        bTree = BinaryTree()
        bTree.insert(value= var.p1)
        bTree.insert(value= var.p2)
        bTree.insert(value= var.p3)
        self.assertEqual(bTree.find(var.p3).value, var.p3)
        bTree.delete(var.p3)
        with self.assertRaises(Exception): 
            bTree.find(var.p3).value#Looking for deleted element

    def test_deleteRecursive(self):
        #data input
        df = pd.read_fwf('Personer.dta', )
        df = df.applymap(str)
        df.columns = ["name"]
        df[['First', 'Last', 'Address', 'Nr', 'City']] = df.name.str.split(';', expand=True)
        df = df.drop(columns=["name"])
        Personer = namedtuple('Personer', ['First', 'Last', 'Address', 'Nr', 'City'])
        list_df = list(df.itertuples(name='Person', index=False))
        binaryTree = BinaryTree()
        for data in list_df:
            binaryTree.insert(value=data)
        
        #Test starts
        p_test1 = list_df[10]
        p_test2 = list_df[88888]

        p1 = list_df[1000]
        p2 = list_df[10000]
        values_to_delete = [p1, p2]

        for i in values_to_delete:
            binaryTree.deleteRecursive(key=i)

        self.assertEqual(binaryTree.find(p_test1).value, p_test1)
        self.assertEqual(binaryTree.find(p_test2).value, p_test2)
        with self.assertRaises(Exception): 
            binaryTree.find(p1).value#Looking for deleted element
            binaryTree.find(p2).value#Looking for deleted element

        