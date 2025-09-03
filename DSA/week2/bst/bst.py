#Implementation of a BST and some BST operations
from bst_node import BSTNode

class BST:
    def __init__(self):
        self.root = None
        self.size = 0
    def insert(self, data):
        #With traversing, return the child's value on each recursive iteration
            #assign the ret. val to an EXISTING ptr
        self.root = self._insert(self.root, data)
    def _insert(self, curr, data):
        if curr is None:
            self.size+=1
            return BSTNode(data)
        if data < curr.data: #recurse to the left
            curr.left = self._insert(curr.left, data)
        elif data > curr.data:
            curr.right = self._insert(curr.right, data)
        return curr
    def search(self, data):
        data_from_tree = BSTNode()
        self._search(self.root, data, data_from_tree)
        if data_from_tree.data is None:
            return "Data could not be found"
        return data_from_tree.data
    def _search(self, curr, data, tree_data):
        if curr is None:
            return None
        if data < curr.data:
            self._search(curr.left, data, tree_data)
        elif data > curr.data:
            self._search(curr.right, data, tree_data)
        else: #equal case
            tree_data.data = curr.data
    def remove(self, data):
        if self.root is None:
            raise Exception("Cannot remove from empty tree")
        node_removed = BSTNode()
        root = self._remove(self.root, data, node_removed)
        return node_removed.data
    def _remove(self, curr, data, node_removed):
        if curr is None: #then we have not found a matching Node
            raise Exception("Node does not exist to remove")
        if data < curr.data:
            curr.left = self._remove(curr.left, data, node_removed)
        elif data > curr.data:
            curr.right = self._remove(curr.right, data, node_removed)
        else:
            node_removed.data = data
            self.size-=1
            if (curr.left is None) and (curr.right is None): #zero-child case
                return None
            elif (curr.left is None and curr.right is not None) or (curr.right is None and curr.left is not None): #one-child case
                if curr.right is None and curr.left is not None:#if left child
                    return curr.left
                else: #right child
                    return curr.right
            else: #two-child case
                #find predecessor
                predecessor = BSTNode()
                curr.left = self._removePredecessor(curr.left, predecessor)
                curr.data = predecessor.data
        return curr
    def _removePredecessor(self, curr, predecessor):
        if curr.right is None: #we have found the predecessor
            predecessor.data = curr.data
            return curr.left #if no child = None, if child, must be left, keep structure and return the entire left subtree to reconstruct tree correctly
        curr.right = self._removePredecessor(curr.right, predecessor)
        return curr
    def contains(self, data):
        return self._contains(self.root, data)
    def _contains(self, curr, data):
        if curr is None:
            return False
        if data < curr.data:
            return self._contains(curr.left, data)
        elif data > curr.data:
            return self._contains(curr.right, data)
        else:
            #We have found the data
            return True
    def preorder(self) -> list: #useful for situations where wish to create an exact copy of BST ==> add all data in the order presented to new BST
        preorder_list = []
        self._preorder(self.root, preorder_list)
        return preorder_list
    def _preorder(self, curr, pre_list):
        if curr is not None:
            pre_list.append(curr.data)
            self._preorder(curr.left, pre_list)
            self._preorder(curr.right, pre_list)
    def inorder(self):
        inorder_list = []
        self._inorder(self.root, inorder_list)
        return inorder_list
    def _inorder(self, curr, in_list):
        if curr is not None:
            self._inorder(curr.left, in_list)
            in_list.append(curr.data)
            self._inorder(curr.right, in_list)
    def postorder(self): #used for situations where removing data
        postorder_list = []
        self._postorder(self.root, postorder_list)
        return postorder_list
    def _postorder(self, curr, post_list):
        if curr is not None:
            self._postorder(curr.left, post_list)
            self._postorder(curr.right, post_list)
            post_list.append(curr.data)
    def height(self):
        return self._height(self.root)
    def _height(self, curr):
        if curr is None:
            return -1
        return max(self._height(curr.left), self._height(curr.right)) + 1
    def clear(self):
        self.root = None
        self.size = 0
    def getSize(self):
        return self.size
    def __str__(self):
        return f"{self.inorder()}"