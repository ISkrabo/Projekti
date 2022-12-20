package hr.fer.oop.lab4.zad2.verzijaNadjiPrazneRacune;

import java.io.IOException;
import java.nio.file.FileVisitor;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class Program {

	public static void main(String[] args) {
		
		FileVisitor<Path> visitor = new MyByteReaderEmptyBills();
		Path racuni = Paths.get("C:/Users/Vegeto/eclipse-workspace/lab4_moje/racuni/2003/1");
		
		try {
			Files.walkFileTree(racuni, visitor);
			
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
