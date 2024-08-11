# username - lotenberg
# id1      - 2131475752
# name1    - Yuval Lotenberg
# id2      - 322290750
# name2    - Alon Balassiano

import random


"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type value: str
    @param value: data of your node
    """

    def __init__(self, value):
        self.value: str = value
        self.left: AVLNode = None
        self.right: AVLNode = None
        self.parent: AVLNode = None
        self.height: int = -1  # Balance factor

        self.size = 0

    """innit new non-virtual node
    @type value: str
    @param value: data of your node
    
    @rtype: AVLNode
    @return: the new node
    """

    @staticmethod
    def newNode(value: str):
        node = AVLNode(value)
        node.height = 0
        node.size = 1
        node.left = AVLNode("")
        node.right = AVLNode("")

        node.right.parent = node.left.parent = node

        return node

    """copy this node without relations
    
    @rtype: AVLNode
    @returns: copied node
    """
    def copy(self):
        return AVLNode.newNode(self.value)

    """returns the left child
    @rtype: AVLNode
    @returns: the left child of self, None if there is no left child
    """

    def getLeft(self):
        return self.left

    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child
    """

    def getRight(self):
        return self.right

    """returns the parent 

    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    """

    def getParent(self):
        return self.parent

    """return the value

    @rtype: str
    @returns: the value of self, None if the node is virtual
    """

    def getValue(self):
        return self.value

    """returns the height

    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    """

    def getHeight(self):
        return self.height

    """returns the size

   @rtype: int
   @returns: size of subtree
   """

    def getSize(self):
        return self.size

    """sets left child

    @type node: AVLNode
    @param node: a node
    """

    def setLeft(self, node):
        self.left = node

    """sets right child

    @type node: AVLNode
    @param node: a node
    """

    def setRight(self, node):
        self.right = node
        return None

    """sets parent

    @type node: AVLNode
    @param node: a node
    """

    def setParent(self, node):
        self.parent = node
        return None

    """sets value

    @type value: str
    @param value: data
    """

    def setValue(self, value):
        self.value = value
        return None

    """sets size

    @type value: int
    @param value: size
    """

    def setSize(self, value):
        self.size = value
        return None

    """sets the balance factor of the node

    @type h: int
    @param h: the height
    """

    def setHeight(self, h):
        self.height = h
        return None

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def isRealNode(self):
        return self.height != -1

    """returns whether self is a virtual node 

    @rtype: bool
    @returns: True if self is a virtual node, False otherwise.
    """

    def isVir(self):
        return self.height == -1

    """returns the balance factor 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def balanceFactor(self):
        if self.isRealNode():
            return self.left.height - self.right.height
        return 0

    """return the minimum in the subtree
    
    @rtype: AVLNode
    @returns: the min 
    
    @complexity: O(log n)
    """

    def min(self):
        curr = self
        while curr.left.isRealNode():
            curr = curr.left
        return curr

    """return the maximum in the subtree

    @rtype: AVLNode
    @returns: the max 

    @complexity: O(log n)
    """

    def max(self):
        curr = self
        while curr.right.isRealNode():
            curr = curr.right
        return curr

    """successor
    
    @rtype: AVLNode
    @returns: the successor node
    
    @complexity: O(log n)
                 at worst we have one travel up and one travel down, O(2h) = O(log n)
    """

    def succ(self):
        # right subtree non-empty -> minimum in the right subtree
        if self.right.isRealNode():
            return self.right.min()

        # else travel until you're a left child
        node = self
        parent = node.parent
        while parent != None and node == parent.right:
            node = parent
            parent = node.parent
        return parent

    """predecessor

    @rtype: AVLNode
    @returns: the predecessor node

    @complexity: O(log n)
                 at worst we have one travel up and one travel down, O(2h) = O(log n)
    """

    def pred(self):
        # left subtree non-empty -> maximum in left subtree
        if self.left.isRealNode():
            return self.left.max()

        # else travel up until you're right child
        node = self
        parent = node.parent
        while parent != None and node == parent.left:
            node = parent
            parent = node.parent
        return parent

    """return the ith element in the inorder sacn
    
    @rtype: AVLNode
    @returns: the ith node in the inordered list
    
    @complexity: O(log n)
                 we saw this algorithm in class
                 each step we move one down in depth, and thus we have O(h) = O(log n)
    """

    def select(self, i):
        if not self.isRealNode():
            # print(f"on {i} i got virtual")
            return None

        node = self
        index = i

        while node.isRealNode():
            # print(f"searching for {index} in tree {node}")

            # if the left subtree is exactly the size of the index we are looking for,
            # we found the ith item
            if node.left.size == index:
                return node

            # if the size is bigger, the ith item is in the left subtree
            elif node.left.size > index:
                node = node.left

            # else the ith item is in the right subtree, and it is exactly
            # the (i - size(left) - 1)th item in that tree
            # because by moving right we are skipping size(left) + 1 items
            else:
                index -= node.left.size + 1
                node = node.right

    """add after a node (in the inorder scan)
    
    @type value: str
    @param value: data
    
    @rtype: AVLNode
    @returns: the new (leaf) node added
    
    @complexity: O(log n)
                 (at most) travel from the root to a leaf
    """

    def addAfter(self, value):
        # to add a node exactly after self we have to place it in the successor position of self

        # if the right subtree is non-empty, the successor will be the minimum of the right subtree
        # thus, add it in the minimum position, all the way left
        if self.right.isRealNode():
            new_node = self.right.addMin(value)

        # if the right subtree is empty, add it as a new node there
        # now it is the minimum of the non-empty right subtree, and thus in the correct position
        else:
            new_node = AVLNode.newNode(value)  # create new node
            self.right = new_node
            new_node.parent = self

        # IMPORTANT: in both cases the new_node was added as a leaf, just as if we
        # had added keys to the whole tree, and then inserted the node with a key
        # that is exactly between self.key and self.successor.key (or +∞ if succ is None),
        # which was our goal with this function

        # return the new leaf, for balancing the trip from this leaf to the root later
        return new_node

    """add a node as a new minimum
    
    @type value: str
    @param value: data

    @rtype: AVLNode
    @returns: the new (leaf) node added
    
    @complexity: O(log n)
                 (at most) travel from the root to a leaf (in min method)
    """

    def addMin(self, value):
        # find the min, and add it to the left of it, all the way down-left
        minn = self.min()
        new_node = AVLNode.newNode(value)

        new_node.parent = minn
        minn.left = new_node

        # return the new leaf, for balancing the trip from this leaf to the root later
        return new_node

    """update the size and height based on children 
    
    @pre: not virtual
    @pre everything (strictly) below self is correct, in particular the children of self
    
    @post: the whole subtree of self is correct
    
    @complexity: O(1)
    """

    def update(self):
        if self.isRealNode():
            self.height = 1 + max(self.left.height, self.right.height)  # height formula
            self.size = 1 + self.left.size + self.right.size  # size formula

        # this is unnecessary, but it is useful conceptually
        else:
            self.height = -1
            self.size = 0

    """balance the AVL tree
    
    @rtype: (int, AVLNode)
    @return: number of rotations needed to balance and new root
    
    @complexity: O(log n)
                 travel all the way up, doing constant operations at each level
    """

    def balance(self):
        # we chose an iterative approach to balancing
        # as seen in class, with the addition of maintaining the
        # fields size and height, and thus travelling all the way to the root

        curr = self
        rot = 0

        root = self

        # print("before balance:", curr)

        while curr:
            root = curr
            curr.update()
            # print(f"{curr}  \t height: {curr.height} \t size: {curr.size}")
            if abs(curr.balanceFactor()) < 2:
                curr = curr.parent
                continue

            # print(f"decided I'm balancing {curr}, with BF {curr.balanceFactor()}")

            if curr.balanceFactor() == -2:
                if curr.right.balanceFactor() in [-1, 0]:
                    # L rotation
                    curr.leftRot()
                    curr = curr.parent
                    rot += 1
                elif curr.right.balanceFactor() == 1:
                    # RL rotation
                    curr.right.rightRot()
                    curr.leftRot()
                    curr = curr.parent
                    rot += 1
                else:
                    raise Exception("shouldn't happen")
            elif curr.balanceFactor() == 2:
                if curr.left.balanceFactor() in [0, 1]:
                    # R rotation
                    curr.rightRot()
                    curr = curr.parent
                    rot += 1
                elif curr.left.balanceFactor() == -1:
                    # LR rotation
                    curr.left.leftRot()
                    curr.rightRot()
                    curr = curr.parent
                    rot += 1
                else:
                    raise Exception("shouldn't happen")
            else:
                raise Exception(f"this shouldn't happen, balance of {self.balanceFactor()}")

        # print("after balance:", root)
        return rot, root

    """
    perform right rotation
        
            u                         v
         /     \                   /     \ 
       v         C     --R-->     A        u
     /   \                               /   \ 
    A     B                            B     C

    @rtype: AVLNode
    @returns: the new 'root'
    
    @complexity: O(1)
    """

    def rightRot(self):
        u = self
        v = self.left
        A = v.left
        B = v.right
        C = self.right
        parent = self.parent
        isLeft = parent != None and self == parent.left

        # assert u.isRealNode() and v.isRealNode()
        # assert A and B and C

        v.parent = parent
        if parent != None:
            if isLeft:
                parent.left = v
            else:
                parent.right = v

        v.left = A
        if A: A.parent = v

        v.right = u
        u.parent = v

        u.left = B
        if B: B.parent = u

        u.right = C
        if C: C.parent = u

        u.update()
        v.update()

        return v

    """
    perform left rotation
    
            u                         v
         /     \                   /     \ 
       v         C     <--L--     A        u
     /   \                               /   \ 
    A     B                             B     C
    
    @rtype: AVLNode
    @returns: the new 'root'
    
    @complexity: O(1)
    """

    def leftRot(self):

        # print(f"about to left rot {self}")

        v = self
        u = self.right
        A = v.left
        B = u.left
        C = u.right
        parent = self.parent
        isLeft = parent != None and self == parent.left

        # assert u.isRealNode() and v.isRealNode()
        # assert A and B and C

        u.parent = parent
        if parent != None:
            if isLeft:
                parent.left = u
            else:
                parent.right = u

        u.right = C
        if C: C.parent = u

        u.left = v
        v.parent = u

        v.left = A
        if A: A.parent = v

        v.right = B
        if B: B.parent = v

        v.update()
        u.update()

        return u

    """find the first subtree above self with size greater than i

    @type i: int
    @param i: size we want
    """
    def findFirstSubtree(self, i):
        curr = self

        while curr.size <= i and curr.parent is not None:
            curr = curr.parent

        return curr

    """find the first subtree above self with height greater than h

        @type h: int
        @param h: size we want
        """

    def findFirstSubtreeHeight(self, h):
        curr = self

        while curr.height < h and curr.parent is not None:
            curr = curr.parent

        return curr

    """delete this node from the tree, and then return the node up from which balancing is required
    
    @rtype: AVLNode
    @returns: node that requires balancing
    """
    def delete(self):

        if self.left.isVir():

            movedUp = self.right
            movedUp.parent = self.parent

            # parent update
            if self.parent is not None:
                if self == self.parent.left:
                    self.parent.left = movedUp
                else:
                    self.parent.right = movedUp

            return movedUp

        elif self.right.isVir():
            movedUp = self.left
            movedUp.parent = self.parent

            if self.parent is not None:
                if self == self.parent.left:
                    self.parent.left = movedUp
                else:
                    self.parent.right = movedUp

            return movedUp

        else:
            succ = self.succ()
            balancing_needed = succ.delete()

            succ.parent = self.parent

            succ.left = self.left
            succ.right = self.right

            if self.parent is not None:
                if self == self.parent.left:
                    self.parent.left = succ
                else:
                    self.parent.right = succ

            succ.left.parent = succ
            succ.right.parent = succ

            return balancing_needed




    """insert into the tree by lexicographical order
    
    @type node: AVLNode
    @param node: new node added
    
    @pre: node is real    
    """
    def addLexicographical(self, node):
        node: AVLNode
        curr = self
        while curr.isRealNode():
            if node.value <= curr.value:
                curr = curr.left
            else:
                curr = curr.right

        node.parent = curr.parent
        if curr == curr.parent.left:
            curr.parent.left = node
        else:
            curr.parent.right = node

        return node


    """return string in lisp format
    
    value (left) (right)
    
    @rtype: str
    """

    def __str__(self):
        if self.isRealNode():
            return f"{self.value} ({self.left}) ({self.right})"
        else:
            return "VIR"

    def __repr__(self):
        if self.isRealNode():
            return f"({self.left}){self.value}({self.right})"
        else:
            return "VIRTUAL"

    """inorder scan of the list
    
    @type lst: List
    @param lst: a list to add the inorder items to
    @type index: int
    @param index: the index in the list
    
    @rtype: int
    @returns: new index in the list
    """

    def inOrder(self, lst, index):
        if self.isRealNode():
            index = self.left.inOrder(lst, index)
            lst[index] = self.value
            return self.right.inOrder(lst, index + 1)
        return index

    """inorder scan of the list
    
    @rtype: List[str]
    @returns: list represented by subtree of the node self
    """

    def inOrderNoLst(self):
        lst = [""] * self.size
        self.inOrder(lst, 0)
        return lst

    """helper function to print the tree
    
    @type tabs: str
    @param tabs: a prefix for the nice printing of the tree
    """

    def easyToRead(self, tabs=""):
        if self.isRealNode():
            print(tabs + f"{self.value}   height:{self.height}   size:{self.size}")
            self.left.easyToRead(tabs + "\t")
            self.right.easyToRead(tabs + "\t")
        else:
            print(tabs + "VIR")

    """helper function to assert correctness of the tree
    
    @rtype: bool
    @returns: if the tree is correct
    """

    def assertRight(self):
        if not self.isRealNode():
            return
        self.left.assertRight()
        self.right.assertRight()

        if self.size != self.left.size + self.right.size + 1:
            print(f"ERROR IN {self}")
            assert False
        if self.height != 1 + max(self.left.height, self.right.height):
            print(f"ERROR IN {self}")
            assert False
        if self.right.parent != self:
            print(f"ERROR IN {self}")
            assert False
        if self.left.parent != self:
            print(f"ERROR IN {self}")
            assert False
        if abs(self.balanceFactor()) >= 2:
            print(f"ERROR IN {self}")
            assert False

    """deepcopy the whole tree
    
    @rtype: AVLNode
    @returns: copied versoin of the whole tree
    """
    def deepcopy(self):
        if self.isVir():
            return AVLNode("")

        right = self.right.deepcopy()
        left = self.left.deepcopy()
        new_self = self.copy()

        new_self.left = left
        new_self.right = right
        left.parent = right.parent = new_self

        new_self.size = self.size
        new_self.height = self.height


"""
A class implementing the ADT list, using an AVL tree.
"""


class AVLTreeList(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.size: int = 0
        self.root: AVLNode = None

        self.min: AVLNode = None
        self.max: AVLNode = None

    """returns whether the list is empty

    @rtype: bool
    @returns: True if the list is empty, False otherwise
    """

    def empty(self):
        return self.size == 0

    """pre-retrieves the node of the i'th item in the list

        @type i: int
        @pre: 0 <= i < self.length()
        @param i: index in the list
        @rtype: AVLNode
        @returns: the the node of the i'th item in the list

        @complexity: O(log i)
        """

    def preRetrieve(self, i):
        # print(f"about to retrieve the {i}th item from {self.root.inOrderNoLst()}")
        if i > self.size or i < 0:
            return None
        # print(f"returned with {self.root.select(i)}")

        # print(self.size)

        # finding the first subtree of appropriate size, O(log i)
        subtree = self.min.findFirstSubtree(i)
        # print(f"looking for {i}th in tree {self.root}, using {subtree}")

        # select as seen in class, O(log size(subtree)) = O(log i), and we saw size(subtree) = O(i^2)
        return subtree.select(i)

    """retrieves the value of the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: index in the list
    @rtype: str
    @returns: the the value of the i'th item in the list
    
    @complexity: O(log i)
    """

    def retrieve(self, i):
        return self.preRetrieve(i).value

    """inserts val at position i in the list

    @type i: int
    @pre: 0 <= i <= self.length()
    @param i: The intended index in the list to which we insert val
    @type val: str
    @param val: the value we inserts
    @rtype: list
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def insert(self, i, val):

        # we did the same algorithm as was suggested in the tirgul. but we did it reversed
        # i.e., if added first, place in the min position
        # else, place after the item in the i-1 position

        self.size += 1
        newlyAdded = None
        if self.root is None:
            self.root = AVLNode.newNode(val)
            newlyAdded = self.root
        elif i == 0:
            newlyAdded = self.root.addMin(val)
        else:
            node = self.preRetrieve(i - 1)
            # print(node.value)
            newlyAdded = node.addAfter(val)

        if i == 0:
            self.min = newlyAdded
        if i == self.size - 1:
            self.max = newlyAdded

        (rot, root) = newlyAdded.balance()
        self.root = root

        return rot

    """deletes the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list to be deleted
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, i):
        if i < 0 or i >= self.size:
            return -1

        self.size -= 1
        if self.size == 0:
            self.root = self.min = self.max = None
            return

        node = self.preRetrieve(i)
        print(f"found this node: {node}, going to delete it!")
        balance_needed = node.delete()

        (rot, root) = balance_needed.balance()
        self.root = root

        self.min = self.root.min()
        self.max = self.root.max()

        return rot

    """returns the value of the first item in the list

    @rtype: str
    @returns: the value of the first item, None if the list is empty
    """

    def first(self):
        return self.min.value

    """returns the value of the last item in the list

    @rtype: str
    @returns: the value of the last item, None if the list is empty
    """

    def last(self):
        return self.max.value

    """returns an array representing list 

    @rtype: list
    @returns: a list of strings representing the data structure
    """

    def listToArray(self):
        if self.size > 0:
            return self.root.inOrderNoLst()
        return []

    """returns the size of the list 

    @rtype: int
    @returns: the size of the list
    """

    def length(self):
        return self.size

    """sort the info values of the list

    @rtype: list
    @returns: an AVLTreeList where the values are sorted by the info of the original list.
    """

    def sort(self):
        if self.size == 0:
            return AVLTreeList()

        new_root = self.min.copy()
        curr = self.min.succ()
        while curr is not None:
            current_in_sorted = new_root.addLexicographical(curr.copy())
            (rot, new_root) = current_in_sorted.balance()
            curr = curr.succ()

        new_list = AVLTreeList()
        new_list.root = new_root
        new_list.min = new_root.min()
        new_list.max = new_root.max()
        new_list.size = new_root.size

        return new_list

    """permute the info values of the list 

    @rtype: list
    @returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
    """

    def permutation(self):

        permuted = AVLTreeList()

        curr = self.min
        while curr is not None:
            i = random.randint(0, permuted.size)
            permuted.insert(i, curr.value)
            curr = curr.succ()

        return permuted

    """concatenates lst to self

    @type lst: AVLTreeList
    @param lst: a list to be concatenated after self
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def concat(self, lst):
        old_size = self.size

        self.size += lst.size
        hdif = self.getHeight() - lst.getHeight()

        if lst.size == 0:
            pass
        elif old_size == 0:
            self.root = lst.root
            self.min = lst.min
            self.max = lst.max
        elif abs(hdif) <= 1:
            # add a fictive node

            self.size += 1
            fictive = AVLNode.newNode("FICTIVE")

            fictive.left = self.root
            fictive.right = lst.root

            fictive.update()

            self.root.parent = lst.root.parent = fictive

            self.root = fictive
            self.max = lst.max

            self.delete(old_size)

        elif hdif >= 2:  # self.height > other.height
            # necessary nodes for addition
            first = self.max.findFirstSubtreeHeight(lst.getHeight())
            second = lst.root
            fictive = AVLNode.newNode("FICTIVE")
            first_par = first.parent

            # add a fictive node
            self.size += 1
            fictive.left, fictive.right = first, second
            first.parent = second.parent = fictive
            fictive.parent = first_par
            first_par.right = fictive
            fictive.update()
            (_, self.root) = fictive.balance()

            # print(f"going to delete in {old_size} position, in {self.listToArray()}, that is {self.retrieve(old_size)}")
            # self.root.easyToRead()

            self.delete(old_size)
            # print(f"after deletion, {self.listToArray()}")

        else:  # self.height < other.height
            # necessary nodes for addition
            first = self.root
            second = lst.min.findFirstSubtreeHeight(self.getHeight())
            fictive = AVLNode.newNode("FICTIVE")  # name for debugging reasons
            sec_par = second.parent

            # add a fictive node
            self.size += 1
            fictive.left, fictive.right = first, second
            first.parent = second.parent = fictive
            fictive.parent = sec_par
            sec_par.left = fictive
            fictive.update()
            (_, self.root) = fictive.balance()

            # print(f"going to delete in {old_size} position, in {self.listToArray()}, that is {self.retrieve(old_size)}")
            # self.root.easyToRead()

            self.delete(old_size)

        return abs(hdif)



    """searches for a *value* in the list

    @type val: str
    @param val: a value to be searched
    @rtype: int
    @returns: the first index that contains val, -1 if not found.
    """

    def search(self, val):
        curr = self.min
        count = 0

        while curr != None:
            if curr.value == val:
                return count
            curr = curr.succ()
            count += 1

        return -1

    """returns the root of the tree representing the list

    @rtype: AVLNode
    @returns: the root, None if the list is empty
    """

    def getRoot(self):
        return self.root

    """returns the height of the tree representing the list

    @rtype: int
    @returns: the height, -1 if the list is empty
    """

    def getHeight(self):
        return -1 if self.size == 0 else self.root.height

    """deep-copy the whole list

    @rtype: AVLTreeList
    @returns: copied version of the whole list
    """
    def deepcopy(self):
        new = AVLTreeList()
        new.root = None if self.root is None else self.root.deepcopy()
        new.min = new.root.min()
        new.max = new.root.max()
        new.size = self.size
