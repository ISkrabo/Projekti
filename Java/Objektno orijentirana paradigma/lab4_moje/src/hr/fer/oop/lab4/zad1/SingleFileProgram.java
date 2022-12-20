package hr.fer.oop.lab4.zad1;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;

public class SingleFileProgram {
	
	//C:\Users\Vegeto\eclipse-workspace\lab4_moje

	
	public static void main(String[] args) {
		
		Path fileToRead = Paths.get("C:/Users/Vegeto/eclipse-workspace/lab4_moje/racuni/2003/1/Racun_0.txt");
		Path result = Paths.get("C:/Users/Vegeto/eclipse-workspace/lab4_moje/NoviRacuni/new-racun0.txt");
		
		try (InputStream is = Files.newInputStream(fileToRead)) {
			MyByteWriter rewriter = new MyByteWriter(is, result);
			rewriter.run();
			System.out.println(filesEquals(fileToRead, result));
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public static boolean filesEquals(Path f1, Path f2) throws IOException {
        return Arrays.equals(Files.readAllBytes(f1), Files.readAllBytes(f2));
	}
}
