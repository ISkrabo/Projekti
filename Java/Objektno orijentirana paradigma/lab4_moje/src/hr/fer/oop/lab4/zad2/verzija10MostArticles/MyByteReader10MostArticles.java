package hr.fer.oop.lab4.zad2.verzija10MostArticles;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.FileVisitResult;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.StandardOpenOption;
import java.nio.file.attribute.BasicFileAttributes;

public class MyByteReader10MostArticles extends SimpleFileVisitor<Path> {

	private double[] expensive;
	private double[] mostSold;

	private double numOfArticles;
	private double numOfReceits;

	public MyByteReader10MostArticles() {
		this.expensive = new double[10];
		this.mostSold = new double[10];
	}

	@Override
	public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
		if (file.toString().endsWith("txt")) {
			BufferedReader br = new BufferedReader(
					new InputStreamReader(Files.newInputStream(file, StandardOpenOption.READ)));
			int i = 0;
//			System.out.println("Čitam file " + file);
			while (true) {
				String line = br.readLine();
				line.trim();
				
//				System.out.println("Čitam line " + line);
				if (line.startsWith("UKUPNO"))
					break;
				else if (!line.isEmpty() && !line.startsWith("Racun br") && !line.startsWith("Kupac:")
						&& !line.startsWith("---") && !line.endsWith("---") && !line.startsWith("Proizvod")) {
					i++;
					String[] parts = line.split("\\s\\s+");
					for (int j = 0; j < 10; j++) {
						if (expensive[j] == 0 || expensive[j] < Double.parseDouble(parts[1])) {
							expensive[j] = Double.parseDouble(parts[1]);
							break;
						}
					}
					for (int j = 0; j < 10; j++) {
						if (mostSold[j] == 0 || mostSold[j] < Double.parseDouble(parts[2])) {
							mostSold[j] = Double.parseDouble(parts[2]);
							break;
						}
					}
				}
				numOfReceits++;
				numOfArticles += i;
			}
		}
		return FileVisitResult.CONTINUE;
	}

	public double averageNumOfArticlesSold() {
		return numOfArticles / numOfReceits;
	}

	public double[] getExpensive() {
		return expensive;
	}

	public double[] getMostSold() {
		return mostSold;
	}

}
