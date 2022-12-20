package hr.fer.oop.lab4.zad1b;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.file.FileVisitResult;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.attribute.BasicFileAttributes;

public class MyByteReader extends SimpleFileVisitor<Path> {
	
	private BufferedOutputStream bos;

	public MyByteReader (OutputStream os) {
		this.bos = new BufferedOutputStream(os);
	}
	
	@Override
	public FileVisitResult visitFile (Path file, BasicFileAttributes attrs) throws IOException {
		
		System.out.println("Reading file: " + file.getFileName());
		
		if (file.toString().endsWith("txt")) {
			BufferedInputStream bis = new BufferedInputStream(
					Files.newInputStream(file)
					);
			byte[] buffer = new byte[1024];
			while(true) {
				int numOfReadBytes = bis.read(buffer);
				if (numOfReadBytes < 1) break;
				bos.write(buffer, 0, numOfReadBytes);
			}
			
			bis.close();
		}
		
		return FileVisitResult.CONTINUE;
	}
	
}
