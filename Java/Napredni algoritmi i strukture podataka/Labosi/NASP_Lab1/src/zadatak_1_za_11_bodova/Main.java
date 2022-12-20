package zadatak_1_za_11_bodova;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Scanner;

public class Main {

	public static void main(String[] args) {

		AVL_tree tree = new AVL_tree();

		// file reading - getting file path + name
		String filePath = "C:/Users/Vegeto/eclipse-workspace/NASP_Lab1/Tree_ASCII_files/";

		System.out.println(
				"Type in the name of the txt file from which to create the AVL tree. Available txt files are:\ntree1");
		Scanner in = new Scanner(System.in);
		String s = in.nextLine();

		filePath += s + ".txt";

		// file reading
		String[] numbersFromFile = null;
		try (BufferedReader is = new BufferedReader(new FileReader(filePath))) {
			String line = null;
			while ((line = is.readLine()) != null) {
				numbersFromFile = line.split("\\s+");
			}
		} catch (IOException e) {
			e.printStackTrace();
		}

		// Create tree from the numbers given in the file
		// Duplicates will be ignored
		for (int i = 0; i < numbersFromFile.length; i++) {
			tree.root = tree.insert(tree.root, Integer.parseInt(numbersFromFile[i]));
		}

		System.out.println("\nResulting AVL tree:");
		tree.printTree(tree.root);

		// New numbers to add
		System.out.println("\nWhich number do you want inserted into the tree? (Write a negative number to end)");

		s = in.nextLine();
		int valueToAdd = Integer.parseInt(s);
		while (valueToAdd >= 0) {
			tree.root = tree.insert(tree.root, valueToAdd);
			System.out.println("Printing current tree.");
			tree.printTree(tree.root);
			System.out.println();
			s = in.nextLine();
			valueToAdd = Integer.parseInt(s);
		}

		in.close();
	}

}
