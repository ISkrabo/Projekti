package hr.fer.oop.lab4.zad2.verzijaMinMaxAvg;

import java.io.IOException;
import java.nio.file.FileVisitor;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class Program {

	public static void main(String[] args) {
		
		Path racuni = Paths.get("C:/Users/Vegeto/eclipse-workspace/lab4_moje/racuni");
		FileVisitor<Path> visitor = new MyByteReaderMinMaxAvg();
		
		try {
			Files.walkFileTree(racuni, visitor);
			
			System.out.println("\n\nNajmanji artikl je " + ((MyByteReaderMinMaxAvg) visitor).getMinName()
					+ " sa cijenom " + ((MyByteReaderMinMaxAvg) visitor).getMinPrice()
					+ "\nDok je najskuplji artikl " + ((MyByteReaderMinMaxAvg)visitor).getMaxName()
					+ " sa cijenom " + ((MyByteReaderMinMaxAvg) visitor).getMaxPrice()
					);
			
			System.out.printf("\n\nAverage je %.2f", ((MyByteReaderMinMaxAvg) visitor).getAverage());
			
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}
}
