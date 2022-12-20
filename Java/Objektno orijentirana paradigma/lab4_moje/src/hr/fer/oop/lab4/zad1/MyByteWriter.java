package hr.fer.oop.lab4.zad1;

import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;

public class MyByteWriter {
	
	//FileInputStream, BufferedInputStream, FileVisitor.
	
	protected BufferedInputStream buf;
	protected Path destination;
	
	public MyByteWriter(InputStream in, Path path) {
		this.buf = new BufferedInputStream(in);
		this.destination = path;
	}
	
	public void run() throws IOException {
		if (Files.notExists(this.destination)) {
			Files.createFile(destination);
		}
		
		OutputStream os = Files.newOutputStream(this.destination);
		byte[] buffer = new byte[1024];
		while (true) {
			int numOfReadBytes = buf.read(buffer);
			if (numOfReadBytes < 1) break;
			os.write(buffer, 0, numOfReadBytes);
		}
		buf.close();
		os.close();
	}

}
