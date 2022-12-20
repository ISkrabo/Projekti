package hr.fer.oop.lab4.zad2.verzijaCMDBrRacunaManjiOd;

import java.nio.file.Path;

public class Artikl implements Comparable<Artikl> {

	private String brRacuna;
	private String ukupno;
	private Path path;
	
	public Artikl(String br, String uk, Path path) {
		this.brRacuna = br;
		this.ukupno = uk;
		this.path = path;
	}
	
	public String getBrRacuna() {
		return brRacuna;
	}
	public String getUkupno() {
		return ukupno;
	}
	public Path getPath() {
		return path;
	}
	
	@Override
	public boolean equals(Object naziv) {
		return this.brRacuna.equals(naziv);
	}
	
	@Override
	public int hashCode() {
		return this.brRacuna.hashCode();
	}
	
	public int compareTo(Artikl a) {
		return this.brRacuna.compareTo(a.getBrRacuna());
	}
	
}
