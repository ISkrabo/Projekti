package hr.fer.oop.lab4.zad2.verzijaCMDNameInterval;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.FileVisitResult;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.StandardOpenOption;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.TreeSet;

public class MyByteReaderNamePricerange extends SimpleFileVisitor<Path> {

	private String substring;
	private double min, max;

	protected TreeSet<Artikl> articles;

	public MyByteReaderNamePricerange(String s1, String s2, String s3) {
		this.substring = s1;
		this.min = Double.parseDouble(s2);
		this.max = Double.parseDouble(s3);
		this.articles = new TreeSet<Artikl>();
	}

	public TreeSet<Artikl> getArticles() {
		return articles;
	}

	@Override
	public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
		// System.out.println(" reading file :"+file.toString());
		if (file.toString().endsWith("txt")) {
			Artikl a;
			BufferedReader br = new BufferedReader(
					new InputStreamReader(Files.newInputStream(file, StandardOpenOption.READ)));
			while (true) {
				String line = br.readLine();
				line.trim();
				if (line.startsWith("UKUPNO"))
					break;
				else if (!line.isEmpty() && !line.startsWith("Racun br") && !line.startsWith("Kupac:")
						&& !line.startsWith("---") && !line.endsWith("---") && !line.startsWith("Proizvod")) {
					String[] parts = line.split("\\s\\s\\s+");
					a = new Artikl(parts[0], parts[1]);
//					System.out.println("IME ARTIKLA JE " + parts[0] + " TE MU JE CIJENA (krivo dana) " + parts[1]);
					if (a.getNaziv().contains(substring)
							&& (Double.parseDouble(a.getCijena()) > min && Double.parseDouble(a.getCijena()) < max)) {
						articles.add(a);
					}
				}
			}
		}
		return FileVisitResult.CONTINUE;
	}
}
