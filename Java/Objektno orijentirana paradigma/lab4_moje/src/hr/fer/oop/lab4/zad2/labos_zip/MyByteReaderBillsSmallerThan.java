package hr.fer.oop.lab4.zad2.labos_zip;

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

public class MyByteReaderBillsSmallerThan extends SimpleFileVisitor<Path> {
	
	private double maximum;
	protected TreeSet<Bill> bills;

	public MyByteReaderBillsSmallerThan(String max) {
		this.maximum = Double.parseDouble(max);
		bills = new TreeSet<Bill>();
	}
	
	public TreeSet<Bill> getBills() {
		return bills;
	}

	@Override
	public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
		
		if (file.toString().endsWith("txt")) {
			BufferedReader br = new BufferedReader(
					new InputStreamReader(Files.newInputStream(file, StandardOpenOption.READ)));
			Bill a;
			String brRacuna = "0", ukupno = "0";
			
			while (true) {
				String line = br.readLine();
				line.trim();
				if (line.startsWith("Racun")) {
					String[] parts = line.split("\\s+");
					brRacuna = parts[2];
				} 
				if (line.startsWith("UKUPNO")) {
					String[] parts = line.split("\\s+");
					ukupno = parts[1];
					break;
				}
			}
			
			if (!ukupno.equals("0") && Double.parseDouble(ukupno) < maximum) {
				a = new Bill(brRacuna, ukupno, file);
				bills.add(a);
			}
		}
		return FileVisitResult.CONTINUE;
	}

}
