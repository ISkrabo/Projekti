package hr.fer.oop.lab4.zad2.verzijaMinMaxAvg;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.FileVisitResult;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.StandardOpenOption;
import java.nio.file.attribute.BasicFileAttributes;




public class MyByteReaderMinMaxAvg extends SimpleFileVisitor<Path> {
	
	private double average;
	private double numOfArticles;
	private String minName, minPrice = "0";
	private String maxName, maxPrice = "0";
	
	public MyByteReaderMinMaxAvg() {
		super();
	}
	

	@Override
	public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
//		System.out.println("                                            reading file :"+file.toString());
		if(file.toString().endsWith("txt")){
//			Artikl a;
			BufferedReader br = new BufferedReader(new InputStreamReader(Files.newInputStream(file, StandardOpenOption.READ)));
			while(true){
				String line = br.readLine();
				line.trim();
				if(line.startsWith("UKUPNO"))break;
				else if(!line.isEmpty() && !line.startsWith("Racun br") && !line.startsWith("Kupac:") && !line.startsWith("---") && !line.endsWith("---") && !line.startsWith("Proizvod")){
					String [] parts = line.split("\\s\\s\\s+");
//					a = new Artikl(parts[0], parts[1]);
//					System.out.println(a.getNaziv() + "   " + a.getCijena());
					if (Double.parseDouble(minPrice) == 0 || Double.parseDouble(minPrice) > Double.parseDouble(parts[1])) {
						minName = parts[0];
						minPrice = parts[1];
					}
					if (Double.parseDouble(maxPrice) < Double.parseDouble(parts[1])) {
						maxName = parts[0];
						maxPrice = parts[1];
					}
					
					average += Double.parseDouble(parts[1]);
					numOfArticles++;
				}
			}
			
		}
		
		return FileVisitResult.CONTINUE;
	}
	
	public double getAverage() {
		return average/numOfArticles;
	}
	
	public String getMinName() {
		return minName;
	}
	public String getMinPrice() {
		return minPrice;
	}
	public String getMaxName() {
		return maxName;
	}
	public String getMaxPrice() {
		return maxPrice;
	}

}
