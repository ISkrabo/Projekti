package hr.fer.oop.lab4.zad2.verzija10MostArticles;

import java.io.BufferedOutputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.FileVisitor;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class Program {

	public static void main(String[] args) {
		
		FileVisitor<Path> visitor = new MyByteReader10MostArticles();
		Path racuni = Paths.get("C:/Users/Vegeto/eclipse-workspace/lab4_moje/racuni/2003/10");
		Path output = Paths.get("C:/Users/Vegeto/eclipse-workspace/lab4_moje/NoviRacuni/najprodavaniji.txt");
		
		
		try {
			Files.walkFileTree(racuni, visitor);
			
			double[] exp = ((MyByteReader10MostArticles) visitor).getExpensive();
			double[] sold = ((MyByteReader10MostArticles)visitor).getMostSold();
			
			if (!Files.exists(output)) {
				Files.createFile(output);
			}
			BufferedOutputStream out = new BufferedOutputStream(new FileOutputStream(output.toFile()));
			
			String convert;
			
			for (int i = 0; i < 10; i++) {
				convert = String.valueOf(exp[i]) + " " + String.valueOf(sold[i]) + "\n";
				out.write(convert.getBytes());
			}
			convert = "\n" + String.format("%.2f", ((MyByteReader10MostArticles) visitor).averageNumOfArticlesSold());

			out.write(convert.getBytes());
			System.out.println("Napisao sam.");
			out.close();
			
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
