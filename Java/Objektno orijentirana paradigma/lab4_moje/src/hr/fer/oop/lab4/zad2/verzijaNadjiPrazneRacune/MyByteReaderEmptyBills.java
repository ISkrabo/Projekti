package hr.fer.oop.lab4.zad2.verzijaNadjiPrazneRacune;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.FileVisitResult;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.StandardOpenOption;
import java.nio.file.attribute.BasicFileAttributes;

public class MyByteReaderEmptyBills extends SimpleFileVisitor<Path> {

	public MyByteReaderEmptyBills() {
	}

	@Override
	public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
		if (file.toString().endsWith("txt")) {
			BufferedReader br = new BufferedReader(
					new InputStreamReader(Files.newInputStream(file, StandardOpenOption.READ)));
			int i = 0;
			while (true) {
				String line = br.readLine();
				line.trim();
				if (line.startsWith("UKUPNO"))
					break;
				else if (!line.isEmpty() && !line.startsWith("Racun br") && !line.startsWith("Kupac:")
						&& !line.startsWith("---") && !line.endsWith("---") && !line.startsWith("Proizvod")) {
					i++;
				}
			}
			if (i == 0) {
				System.out.println("Stvaram.");
				String izlaz = Paths.get("C:/Users/Vegeto/eclipse-workspace/lab4_moje/NoviRacuni").toString() + "\\"
						+ file.getName((file.getNameCount() - 3)) + "-" + file.getName((file.getNameCount() - 2)) + "-"
						+ file.getFileName().toString().substring(0, file.getFileName().toString().length() - 4);
				System.out.println(izlaz);

				if (!Files.exists(Paths.get(izlaz))) {
					Files.createDirectory(Paths.get(izlaz));
					Files.createFile(Paths.get(izlaz + "\\" + file.getFileName()));
				}
			}
		}
		return FileVisitResult.CONTINUE;
	}

}
