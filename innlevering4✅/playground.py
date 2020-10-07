from binarytree import BinaryTree
from collections import namedtuple

Person = namedtuple('Person','etternavn fornavn adresse postnr area')
p1 = Person('KRISTIANSEN','MORTEN KRISTIAN', 'LEINAHYTTA 36', '7224', 'MELHUS')
p2 = Person('STAVANG', 'ELISABETH', 'ESPENES 116', '4684', 'BYGLAND')
p3 = Person('SYVERSEN', 'HARISHANKAR', 'SISIKVEIEN 84', '1390', 'VOLLEN')
p4 = Person('TYRIBERGET', 'EDWARD J.', 'HALLAND JOHAN 66', '5649', 'EIKELANDSOSEN')
p5 = Person('AASE','TRINE', 'LEINAHYTTA 360', '7200', 'ROGNE')

bTree = BinaryTree()
bTree.insert(value=p1)
bTree.insert(value=p2)
bTree.insert(value=p3)
bTree.insert(value=p4)
bTree.insert(value=p5)
print(bTree.delete(Person('KRISTIANSEN')).value)
#print(bTree.find(p2).value)
#print(bTree.find(p2).value)
#print(bTree.findMin().value)
#print(bTree._root.value)
#print(bTree.find(p1).value)

