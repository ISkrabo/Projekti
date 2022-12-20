package hr.fer.oop.lab4.zad1b;

import java.io.IOException;
import java.io.OutputStream;
import java.nio.file.FileVisitor;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class MultiFileProgram {
	
	public static void main(String[] args) {
		Path racuni = Paths.get("C:/Users/Vegeto/eclipse-workspace/lab4_moje/racuni");
		Path outputFile = Paths.get("C:/Users/Vegeto/eclipse-workspace/lab4_moje/NoviRacuni/sviRacuni.txt");
		
		if (Files.notExists(outputFile)) {
			try {
				Files.createFile(outputFile);
			} catch (IOException e) {
				e.printStackTrace();
			};
		}
		
		try {
			OutputStream os = Files.newOutputStream(outputFile);
			FileVisitor<Path> visitor = new MyByteReader(os);
			Files.walkFileTree(racuni, visitor);
			os.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

}
