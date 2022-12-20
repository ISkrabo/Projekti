package hr.fer.oop.lab4.zad2;

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



public class MySecondByteReader extends SimpleFileVisitor<Path> {

	protected TreeSet<Artikl> articles;
	
	public MySecondByteReader() {
		articles = new TreeSet<Artikl>();
	}
	
	public TreeSet<Artikl> getArticles() {
		return articles;
	}
	
	@Override
	public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
		System.out.println("reading file :"+file.toString());
		if(file.toString().endsWith("txt")){
			Artikl a;
			BufferedReader br = new BufferedReader(new InputStreamReader(Files.newInputStream(file, StandardOpenOption.READ)));
			while(true){
				String line = br.readLine();
				line.trim();
				if(line.startsWith("UKUPNO"))break;
				else if(!line.isEmpty() && !line.startsWith("Racun br") && !line.startsWith("Kupac:") && !line.startsWith("---") && !line.endsWith("---") && !line.startsWith("Proizvod")){
					String [] parts = line.split("\\s\\s+");
					a = new Artikl(parts[0], parts[1]);
					this.articles.add(a);
				}
			}
		}
		return FileVisitResult.CONTINUE;
	}
	
}
