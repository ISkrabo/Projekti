package hr.fer.oop.lab4.zad2.verzijaCMDBrRacunaManjiOd;

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

public class MyByteReaderBillSmallerThan extends SimpleFileVisitor<Path> {

	private double maximum;

	protected TreeSet<Artikl> articles;

	public MyByteReaderBillSmallerThan(String s1) {
		this.maximum = Double.parseDouble(s1);
		articles = new TreeSet<Artikl>();
	}

	public TreeSet<Artikl> getArticles() {
		return articles;
	}

	@Override
	public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
		// System.out.println(" reading file :"+file.toString());
		if (file.toString().endsWith("txt")) {
			Artikl a;
			String brRacuna = "0", ukupno = "0";
			BufferedReader br = new BufferedReader(
					new InputStreamReader(Files.newInputStream(file, StandardOpenOption.READ)));
			while (true) {
				String line = br.readLine();
				line.trim();

				if (line.startsWith("Racun")) {
					String[] parts = line.split("\\s+");
					// System.out.println("racun " + parts[2]);
					brRacuna = parts[2];
				}
				if (line.startsWith("UKUPNO")) {
					String[] parts = line.split("\\s+");
					// System.out.println("cijena " + parts[1]);
					ukupno = parts[1];
					break;
				}
			}
			if (!ukupno.equals("0") && Double.parseDouble(ukupno) < maximum) {
				// System.out.println("pronasao " + brRacuna + " " + ukupno);
				a = new Artikl(brRacuna, ukupno, file);
				articles.add(a);
			}

		}

		return FileVisitResult.CONTINUE;
	}

}
