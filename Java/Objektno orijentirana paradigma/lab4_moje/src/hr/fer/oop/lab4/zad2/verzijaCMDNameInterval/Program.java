package hr.fer.oop.lab4.zad2.verzijaCMDNameInterval;

import java.io.IOException;
import java.nio.file.FileVisitor;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.TreeSet;

public class Program {

	public static void main(String[] args) {
		// moji argumenti su: abel 250 300 , dobivam 18 artikala.

		if (args.length != 3) {
			System.out.println("Predaj mi kao argumente dio naziva + interval cijene (2 broja; od do)");
			return;
		}

		FileVisitor<Path> visitor = new MyByteReaderNamePricerange(args[0], args[1], args[2]);
		Path racuni = Paths.get("C:/Users/Vegeto/eclipse-workspace/lab4_moje/racuni");

		try {
			Files.walkFileTree(racuni, visitor);
			TreeSet<Artikl> artikli = ((MyByteReaderNamePricerange) visitor).getArticles();
			for (Artikl a : artikli) {
				System.out.println("Artikl " + a.getNaziv() + " sa cijenom " + a.getCijena());
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
