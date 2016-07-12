from pythonds.basic.stack import Stack
from pythonds.trees.binaryTree import BinaryTree
from pythonds.trees.binaryTree import pd


def build_parse_tree(fpexp):
    fplist = fpexp.split()
    for i in fplist:
        if i.__contains__('(') and i != '(':
            index = fplist.index(i)
            i_l = i.split('(')
            fplist[index] = i_l[-1]
            for j in range(len(i_l)-1):
                fplist.insert(index, '(')
        if i.__contains__(')') and i != ')':
            index = fplist.index(i)
            i_l = i.split(')')
            fplist[index] = i.split(')')[0]
            for j in range(len(i_l)-1):
                fplist.insert(index+1, ')')
    pstack = Stack()
    current_tree = BinaryTree('')
    current_tree.insertLeft('')
    pstack.push(current_tree)
    current_tree = current_tree.getLeftChild()
    for i in fplist:
        if i == '(':
            current_tree.insertLeft('')
            pstack.push(current_tree)
            current_tree = current_tree.getLeftChild()
        elif i not in ['and', 'or', ')']:
            current_tree.setRootVal(i)
            parent = pstack.pop()
            current_tree = parent

        elif i in ['and', 'or']:
            if current_tree.getRootVal() != "":
                pstack.push(current_tree)
                current_tree = BinaryTree('')
                current_tree.leftChild = pstack.pop()
            current_tree.setRootVal(i)
            current_tree.insertRight('')
            pstack.push(current_tree)
            current_tree = current_tree.getRightChild()
        elif i == ')':
            current_tree = pstack.pop()
        else:
            raise ValueError
    return current_tree


pt = build_parse_tree("a=2 and b=3 ")
pt.postorder()
print(pd)
