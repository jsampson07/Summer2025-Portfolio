#This is to test bst.py
from bst import BST
def test():
    test_bst = BST()
    test_bst.insert(30)
    test_bst.insert(15)
    test_bst.insert(22)
    test_bst.insert(90)
    test_bst.insert(100)
    test_bst.insert(36)
    test_bst.insert(10)
    test_bst.insert(91)
    print(test_bst.height())
    print(test_bst)
    test_bst.remove(30)
    test_bst.remove(22)
    test_bst.remove(100)
    print(test_bst)
    print(test_bst.height())
    print(test_bst.search(30))
    print(test_bst.contains(90))
    print(test_bst.contains(100))

    print(test_bst.preorder())
    print(test_bst.postorder())
    print(test_bst.inorder())

    print(test_bst.getSize())

if __name__ == "__main__":
    test()