package hr.fer.oop.lab4.zad2.verzijaCMDBrRacunaManjiOd;

import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.FileVisitor;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.TreeSet;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;


public class Program {

	public static void main(String[] args) {
		//Moj argument je 10000. Hardkodirao sam ime zip-a.
		
		if (args.length != 1) {
			System.out.println("Predaj mi kao minimalna ukupna cijena");
			return;
		}
		
		FileVisitor<Path> visitor = new MyByteReaderBillSmallerThan(args[0]);
		Path racuni = Paths.get("C:/Users/Vegeto/eclipse-workspace/lab4_moje/racuni");
		Path zipOutput = Paths.get("C:/Users/Vegeto/eclipse-workspace/lab4_moje/NoviRacuni/manjiod10000.zip");
		
		try {
			Files.walkFileTree(racuni, visitor);
			TreeSet<Artikl> artikli = ((MyByteReaderBillSmallerThan) visitor).getArticles();
			
			ZipOutputStream out = new ZipOutputStream(new FileOutputStream(zipOutput.toFile()));
			
			for (Artikl a : artikli) {
//				System.out.println("Račun " + a.getBrRacuna() + " sa ukupnim iznosom " + a.getUkupno());
				
				String zipEntry = a.getPath().getName(a.getPath().getNameCount() - 3).toString() +	//godina
						"_" + a.getPath().getName(a.getPath().getNameCount() - 2).toString() + 		//mjesec
						"_" + a.getPath().getFileName().toString();
				
				ZipEntry e = new ZipEntry(zipEntry);
				out.putNextEntry(e);
				
				byte[] data = a.getBrRacuna().getBytes();
				out.write(data, 0, data.length);
				out.closeEntry();
			}
			System.out.println("Stvorio sam.");
			out.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
