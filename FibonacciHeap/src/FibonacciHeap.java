/**
 * FibonacciHeap
 *
 * An implementation of a Fibonacci Heap over integers.
 * 
 * username - lotenberg
 * id1      - 2131475752
 * name1    - Yuval Lotenberg
 * id2      - 322290750
 * name2    - Alon Balassiano
 * 
 * 
 */
public class FibonacciHeap
{
	
	private HeapNode first;    // left most tree
	private HeapNode last;     // right most tree
	private HeapNode minimum;  // tree with minimal root
	
	private int size = 0;         // total number of nodes
	private int numOfTrees = 0;    // size of forest, number of roots
	private int numOfMarked = 0;  // number of marked nodes
	
	
	private static int CUTS = 0;   // number of cuts throughout program
	private static int LINKS = 0;  // number of links throughout program
	
   /**
    * public boolean isEmpty()
    *
    * Returns true if and only if the heap is empty.
    * 
    * Time complexity: O(1) 
    *   
    */
    public boolean isEmpty()
    {
    	return size == 0;
    }
		
   /**
    * public HeapNode insert(int key)
    *
    * Creates a node (of type HeapNode) which contains the given key, and inserts it into the heap.
    * The added key is assumed not to already belong to the heap.  
    * 
    * Returns the newly created node.
    * 
    * Time complexity: O(1) 
    *                  we insert it in the beginning as a new root
    */
    public HeapNode insert(int key)
    {    
    	HeapNode node = new HeapNode(key);
    	
    	size++;
    	numOfTrees++;
    	
    	// insert to an empty tree
    	if (this.first == null) {
    		this.first = node;
    		this.last = node;
    		this.minimum = node;
    	}
    	
    	// insert to a non-empty tree, just add a new tree of degree 0
    	else {
    		node.next = this.first;
    		this.first.prev = node;
    		this.first = node;
    	}
    	
    	// update the minimum if needed
    	if (node.key < this.minimum.key)
    		this.minimum = node;
    	
    	return node; // should be replaced by student code
    }

   /**
    * public void deleteMin()
    *
    * Deletes the node containing the minimum key.
    * 
    * Time complexity: W.C.       O(n) 
    *                  Amortized  O(log n)
    *
    */
    public void deleteMin()
    {
    	// remove the root
     	this.deleteRoot(minimum);
     	
     	// "un-lazify" the heap
     	this.consolidate();
    }

   /**
    * public HeapNode findMin()
    *
    * Returns the node of the heap whose key is minimal, or null if the heap is empty.
    *
    * Time complexity: O(1) 
    *
    */
    public HeapNode findMin()
    {
    	return this.minimum; 
    } 
    
   /**
    * public void meld (FibonacciHeap heap2)
    *
    * Melds heap2 with the current heap.
    * 
    * Time complexity: O(1) 
    *
    */
    public void meld (FibonacciHeap heap2)
    {
		
    	// heap3 empty
    	if (heap2 == null || heap2.isEmpty())
    		return;
    	
    	// update statistics fields
    	this.size += heap2.size;
    	this.numOfTrees += heap2.numOfTrees;
    	this.numOfMarked += heap2.numOfMarked;
    	
    	// link the forest of heap2 to this forest
    	if (this.isEmpty()) {
    		this.first = heap2.first;
    		this.last = heap2.last;
    		this.minimum = heap2.minimum;
    	}
    	
    	else {
	    	this.last.next = heap2.first;
	    	heap2.first.prev = this.last;
	    	// the minimum in the new heap should be the minimum of this and heap2
	    	this.minimum = (this.minimum.key < heap2.minimum.key) ? this.minimum : heap2.minimum;
	    	this.last = heap2.last;
	    }
    }

   /**
    * public int size()
    *
    * Returns the number of elements in the heap.
    * 
    * Time complexity: O(1) 
    *   
    */
    public int size()
    {
    	return this.size; // should be replaced by student code
    }
    	
    /**
    * public int[] countersRep()
    *
    * Return an array of counters. The i-th entry contains the number of trees of order i in the heap.
    * (Note: The size of of the array depends on the maximum order of a tree.)  
    * 
    * Time complexity: O(this.numOfTrees) = O(n) 
    * 
    */
    public int[] countersRep()
    {
    	int maxDegree = 0;
    	
    	HeapNode curr = this.first;
    	while (curr != null) {
    		maxDegree = Math.max(maxDegree, curr.degree);
    		curr = curr.next;
    	}
    	
    	int[] arr = new int[maxDegree + 1];
    	curr = this.first;
    	while (curr != null) {
    		arr[curr.degree]++;
    		curr = curr.next;
    	}
    	
    	return arr;
    }
	
   /**
    * public void delete(HeapNode x)
    *
    * Deletes the node x from the heap.
	* It is assumed that x indeed belongs to the heap.
	* 
	* Time complexity: W.C.       O(n)
	*                  Amoritzed  O(log n)
    *
    */
    public void delete(HeapNode x) 
    {    
    	/* we avoided the usual implementation:
    	 * 		decreaseKey(x, -inf)
    	 * 		deleteMin()
    	 * 
    	 * so that it would be possible to insert to the heap Integer.MIN_VALUE
    	 * 
    	 * instead of decreasing its key, we "manually" decrease the key, 
    	 * which would cause it to be cut, then removed as a root and then 
    	 * consolidate the tree (in the same manner removeMin would operate)
    	 */
    	cut(x);
    	deleteRoot(x);
    	this.consolidate();
    }

   /**
    * public void decreaseKey(HeapNode x, int delta)
    *
    * Decreases the key of the node x by a non-negative value delta. The structure of the heap should be updated
    * to reflect this change (for example, the cascading cuts procedure should be applied if needed).
    * 
    * Time complexity: W.C.       O(log n)
	*                  Amoritzed  O(1)
    * 
    */
    public void decreaseKey(HeapNode x, int delta)
    {    
    	x.key -= delta;
    	if (x.key < this.minimum.key)
    		this.minimum = x;
    	
    	if (x.parent == null || x.parent.key <= x.key)
    		return;
    	
    	// if it is greater than its parent, cut it
    	cut(x);
    	
    }

   /**
    * public int nonMarked() 
    *
    * This function returns the current number of non-marked items in the heap
    * 
    * Time Complexity: O(1)
    * 
    */
    public int nonMarked() 
    {    
        return this.size - this.numOfMarked;
    }

   /**
    * public int potential() 
    *
    * This function returns the current potential of the heap, which is:
    * Potential = #trees + 2*#marked
    * 
    * In words: The potential equals to the number of trees in the heap
    * plus twice the number of marked nodes in the heap. 
    * 
    * Time Complexity: O(1)
    * 
    */
    public int potential() 
    {    
        return this.numOfTrees + 2 * this.numOfMarked; 
    }

   /**
    * public static int totalLinks() 
    *
    * This static function returns the total number of link operations made during the
    * run-time of the program. A link operation is the operation which gets as input two
    * trees of the same rank, and generates a tree of rank bigger by one, by hanging the
    * tree which has larger value in its root under the other tree.
    * 
    * Time Complexity: O(1)
    * 
    */
    public static int totalLinks()
    {    
    	return LINKS; 
    }

   /**
    * public static int totalCuts() 
    *
    * This static function returns the total number of cut operations made during the
    * run-time of the program. A cut operation is the operation which disconnects a subtree
    * from its parent (during decreaseKey/delete methods). 
    * 
    * Time Complexity: O(1)
    * 
    */
    public static int totalCuts()
    {    
    	return CUTS; 
    }

     /**
    * public static int[] kMin(FibonacciHeap H, int k) 
    *
    * This static function returns the k smallest elements in a Fibonacci heap that contains a single tree.
    * The function should run in O(k*deg(H)). (deg(H) is the degree of the only tree in H.)
    *  
    * ###CRITICAL### : you are NOT allowed to change H. 
    * 
    * Time Complexity: O(k log n)
    */
    public static int[] kMin(FibonacciHeap H, int k)
    {    
    	// idea: use a heap with elements in H 
    	// start with the minimum and whenever you remove a node, add its children
    	// problem: when removing the minimum, how do we know where it is in H?
    	// solution: use the linkToOccurenceInOtherHeap 
    	// pointer in HeapNode for this purpose.
        
    	int[] arr = new int[k];
        
        FibonacciHeap newHeap = new FibonacciHeap();
        
        HeapNode root = newHeap.insert(H.first.key);
        root.linkToOccurenceInOtherHeap = H.first;
        
        for (int i = 0; i < k; i++) {
        	// newHeap.printItems();
        	
        	HeapNode extractedMin = newHeap.findMin();
        	newHeap.deleteMin();
        	
        	HeapNode curr = extractedMin.linkToOccurenceInOtherHeap.leftChild;
        	while (curr != null) {
        		HeapNode currInNewHeap = newHeap.insert(curr.key);
        		currInNewHeap.linkToOccurenceInOtherHeap = curr;
        		curr = curr.next;
        	}
        	arr[i] = extractedMin.key;
        }
        return arr;
    }
    
        
   /**
	* public void deleteRoot(HeapNode x)
	* 
	* remove x (assuming it's a root of a tree) and adds its children to the heap
	* 
	* Time Complexity: O(x.degree) <= O(log n)
	*/
    private void deleteRoot(HeapNode x) {
    	
    	HeapNode previous = x.prev, xRight = x.next, curr = x.leftChild;
    	
    	// we delete one node, so the size goes down by 1
    	this.size -= 1;
    	if (this.size == 0) {
    		// the tree is now empty
    		first = null; last = null; this.minimum = null;
    		numOfTrees = 0; numOfMarked = 0;
    		return;
    	}
    	
    	// we add all the children of x, but remove x itself
    	this.numOfTrees += x.degree - 1;
    	
    	// go over and add the children
    	while (curr != null) {
    		if (previous != null)
    			previous.next = curr;
    		else {
    			// this should only happen if x is the left most node
    			this.first = curr;
    		}
    		
    		curr.prev = previous;
    		
    		curr.parent = null;
    		
    		// we make curr a root so we need to unmark it if it is marked
    		if (curr.marked) {
    			curr.marked = false;
    			this.numOfMarked -= 1;
    		}
    		
    		// move the pointers for next iteration
    		previous = curr;
    		curr = curr.next;
    	}
    	
    	// the last child we added to the root layer, needs to point to the (previous) next of x
    	if (previous != null)
    		previous.next = xRight;
    	else {
    		// delete this.first, and this.first has no children
    		this.first = this.first.next;
    		this.first.prev = null;
    	}
    	
    	if (xRight != null) {
    		xRight.prev = previous;
    	}
    	else {
    		// this should only happen if x is the last
    		this.last = previous;
    	}
    	
    }
    
    
    /**
	* public void cut(HeapNode x)
	* 
	* cut x from its parent, add to children to the heap
	* 
	* Time Complexity: W.C.       O(log n)
	* 				   Amortized  O(1)
	*/
    private void cut(HeapNode x) {
    	// we cannot cut roots
    	if (x.parent == null)
    		return;
    	
    	// cut happening
    	CUTS++;
    	
    	HeapNode oldParent = x.parent;
    	oldParent.degree--;
    	
    	// connect the left and right neighbors of x
    	if (x.prev != null)
    		x.prev.next = x.next;
    	else {
    		// if x is the leftmost child, need to update the parent
    		oldParent.leftChild = x.next;
    	}
    	
    	if (x.next != null)
    		x.next.prev = x.prev;
    	
    	x.parent = null;
    	
    	// unmark x, roots cannot be marked
    	if (x.marked) {
    		this.numOfMarked -= 1;
    		x.marked = false;
    	}
    	
    	// add x to the linked list of roots
    	this.first.prev = x;
    	x.next = this.first;
    	x.prev = null;
    	this.first = x;
    	numOfTrees += 1;
  
    	
    	// cascading cuts
    	if (oldParent.marked) {
    		cut(oldParent);
    	}
    	else if (oldParent.parent != null) {
    		oldParent.marked = true;
    		this.numOfMarked += 1;
    	}
    }
    
    
    /**
	* private void consolidate()
	* 
	* "un-lazify" the heap, so that each degree may only appear once
	* 
	* Time Complexity: W.C.       O(n)
	* 				   Amortized  O(log n)
	*/
    private void consolidate() {
    	
    	// this.easyToRead();
    	
    	if (this.size == 0) {
    		this.first = null; this.last = null; this.minimum = null;
        	this.numOfTrees = 0; numOfMarked = 0;
        	return;
    	}
    	
    	// we use the theorem: max degree with n items is log(phi, n) <= 2.1 ln(n)
    	int maxDegreeAfter = (int)(2.1 * Math.log(this.size)) + 1;
    			
    	// make the buckets, using the knowledge of the size of each one from counterRep
    	HeapNode[] buckets = new HeapNode[maxDegreeAfter + 1];
    	
    	// collect the roots into buckets
    	HeapNode curr = this.first;
    	while (curr != null) {
    
    		HeapNode nxt = curr.next;
    		successiveLink(curr, buckets);
    		
    		curr = nxt;
    	}

    	
    	
    	this.first = null; this.last = null; this.minimum = null;
    	this.numOfTrees = 0;
    	
    	for (int degree = 0; degree < buckets.length; degree++) {
    		
    		// if after all linking still have this degree, add it to the final list
    		if (buckets[degree] != null) {
    			this.numOfTrees++;
    			
    			HeapNode needsToBeAdded = buckets[degree];
    			
    			needsToBeAdded.next = null;
    			needsToBeAdded.prev = null;
    			needsToBeAdded.parent = null;
    			
    			if (this.first == null) {
    				this.first = needsToBeAdded;
    				this.last = this.first;
    				this.minimum = this.first;
    			}
    			
    			else {
    				this.last.next = needsToBeAdded;
    				needsToBeAdded.prev = this.last;
    				this.last = needsToBeAdded;
    				this.minimum = (this.minimum.key < this.last.key) ? this.minimum : this.last;
    			}
    			
    		}
    	}
    }
    
    
    /** private static HeapNode link(HeapNode x, HeapNode y)
     * 
     * link x and y and return the new node
     * 
     * Time Complexity: O(1)
     */
    private static HeapNode link(HeapNode x, HeapNode y) {
    	
    	HeapNode oldLeftChild = x.leftChild;
    	
    	if (x.key > y.key) {
    		return link(y, x);
    	}
    	
    	LINKS++;
    	
    	x.leftChild = y;
    	y.parent = x;
    	y.next = oldLeftChild;
    	if (oldLeftChild != null)
    		oldLeftChild.prev = y;
    	
    	y.prev = null;
    	
    	x.degree += 1;
    	
    	return x;
    }
    
    
    
    /** private static void successiveLink(HeapNode x, HeapNode[] buckets)
     * 
     * add x to the buckets, doing successive links until bucket is empty.
     * 
     * Time Complexity: O(1)
     */
    private static void successiveLink(HeapNode x, HeapNode[] buckets) {
    	while (buckets[x.degree] != null) {
    		x = link(x, buckets[x.degree]);
    		buckets[x.degree - 1] = null;
    	}
    	buckets[x.degree] = x;
    }
    
    
    
   /**
    * public class HeapNode
    * 
    * If you wish to implement classes other than FibonacciHeap
    * (for example HeapNode), do it in this file, not in another file. 
    *  
    */
    public static class HeapNode{

    	public int key;
    	public int degree;
    	
    	public HeapNode parent = null;
    	public HeapNode prev = null;
    	public HeapNode next = null;
    	public HeapNode leftChild = null;
    	
    	// this is only for kMin, to link this cell to its position in another heap
    	// because in that method we build a heap made of heap nodes
    	public HeapNode linkToOccurenceInOtherHeap = null;

    	public boolean marked = false;
    	
    	public HeapNode(int key) {
    		this.key = key;
    	}

    	public int getKey() {
    		return this.key;
    	}
    
    }
    
    
}
