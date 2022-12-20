package hr.fer.oop.lab4.zad2;

import java.io.BufferedOutputStream;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Set;

public class Program {

	public static void main(String[] args) {
		
		MySecondByteReader visitor = new MySecondByteReader();
		Path racuni = Paths.get("C:/Users/Vegeto/eclipse-workspace/lab4_moje/racuni");
		
		try {
			Files.walkFileTree(racuni, visitor);
			Set<Artikl> artikli = visitor.getArticles();
			Writer bw = new BufferedWriter(new OutputStreamWriter(new BufferedOutputStream(new FileOutputStream("C:/Users/Vegeto/eclipse-workspace/lab4_moje/NoviRacuni/cjenik.88592.txt")), "ISO-8859-2"));
			Writer bw2 = new BufferedWriter(new OutputStreamWriter(new BufferedOutputStream(new FileOutputStream("C:/Users/Vegeto/eclipse-workspace/lab4_moje/NoviRacuni/cjenik.UTF.txt")), "UTF-8"));
			
			for (Artikl a : artikli) {
				System.out.println(a.getNaziv() + ";" + a.getCijena());
				bw.write(a.getNaziv()+"\t"+a.getCijena()+"\n");
				bw2.write(a.getNaziv()+"\t"+a.getCijena()+"\n");
			}
			
			bw.close();
			bw2.close();
			
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
