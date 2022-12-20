package zadatak_1_za_11_bodova;

public class AVL_tree {
	Node root;

	Node insert(Node node, int value) {
		// Normal tree inserting
		if (node == null)
			return (new Node(value));

		if (value < node.value)
			node.left = insert(node.left, value);
		else if (value > node.value)
			node.right = insert(node.right, value);
		else // Duplicates not allowed
			return node;

		// update height
		node.height = 1 + max(getHeight(node.left), getHeight(node.right));

		// Get balance factor to check if it needs rebalancing
		int balanceFactor = getBalanceFactor(node);

		// If this node becomes unbalanced, then there are 4 cases:

		// Right Right Case
		if (balanceFactor < -1 && value > node.right.value)
			return leftRotate(node);

		// Left Left Case
		if (balanceFactor > 1 && value < node.left.value)
			return rightRotate(node);

		// Right Left Case
		if (balanceFactor < -1 && value < node.right.value) {
			node.right = rightRotate(node.right);
			return leftRotate(node);
		}

		// Left Right Case
		if (balanceFactor > 1 && value > node.left.value) {
			node.left = leftRotate(node.left);
			return rightRotate(node);
		}

		// return unchanged node
		return node;
	}

	int getHeight(Node N) {
		if (N == null)
			return 0;

		return N.height;
	}

	int max(int a, int b) {
		return (a > b) ? a : b;
	}

	// Right rotate subtree with the base node y
	Node rightRotate(Node y) {
		Node x = y.left;
		Node T2 = x.right;

		// Perform rotation
		x.right = y;
		y.left = T2;

		// Update heights
		y.height = max(getHeight(y.left), getHeight(y.right)) + 1;
		x.height = max(getHeight(x.left), getHeight(x.right)) + 1;

		// Return new root
		return x;
	}

	// Left rotate subtree with the base node x
	Node leftRotate(Node x) {
		Node y = x.right;
		Node T2 = y.left;

		// Perform rotation
		y.left = x;
		x.right = T2;

		// Update heights
		x.height = max(getHeight(x.left), getHeight(x.right)) + 1;
		y.height = max(getHeight(y.left), getHeight(y.right)) + 1;

		// Return new root
		return y;
	}

	int getBalanceFactor(Node N) {
		if (N == null)
			return 0;
		return getHeight(N.left) - getHeight(N.right);
	}

	// Print Tree function
	void printTree(Node node) {
		for (int i = 1; i <= node.height; i++) {
			printTreeWithDepth(node, i);
			System.out.print("\n");
		}
	}

	private void printTreeWithDepth(Node node, int depth) {
		if (node != null && depth == 1) {
			System.out.print(node.value + "  ");
		} else if (node != null) {
			printTreeWithDepth(node.left, depth - 1);
			printTreeWithDepth(node.right, depth - 1);
		} else {
			System.out.print("x  ");
		}
	}
}
