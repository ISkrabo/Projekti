package hr.fer.oop.lab4.zad2.labos_zip;

import java.io.File;
import java.io.FileNotFoundException;
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

	public static void main(String[] args) throws FileNotFoundException {
		
		if (args.length != 1) {
			System.out.println("Netočan broj argumenata predan. Očekujem iznos za kojeg tražim račune čije ukupno je manje od predanog iznosa.");
			return;
		}
		
		FileVisitor<Path> visitor = new MyByteReaderBillsSmallerThan(args[0]);
		Path racuni = Paths.get("C:/Users/Vegeto/eclipse-workspace/lab4_moje/racuni");
		
		String zipout = "C:/Users/Vegeto/eclipse-workspace/lab4_moje/NoviRacuni/";
		zipout += "manjiod" + args[0] + ".zip";
		ZipOutputStream zipOutput = new ZipOutputStream(new FileOutputStream(new File(zipout)));
		
		try {
			Files.walkFileTree(racuni, visitor);
			TreeSet<Bill> bills = ((MyByteReaderBillsSmallerThan) visitor).getBills();
			
			for (Bill a : bills) {
				String zipEntry = 
						a.getPath().getName(a.getPath().getNameCount() - 3).toString() +		//godina
						"_" + a.getPath().getName(a.getPath().getNameCount() - 2).toString() + 	//mjesec
						"_" + a.getPath().getFileName().toString();								//racun
				ZipEntry e = new ZipEntry(zipEntry);
				zipOutput.putNextEntry(e);
				
				byte[] data = (a.getBrRacuna() + "   " + a.getPath()).getBytes();
				zipOutput.write(data, 0, data.length);
				zipOutput.closeEntry();
			}
			System.out.println("Stvorio sam zip.");
			zipOutput.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
