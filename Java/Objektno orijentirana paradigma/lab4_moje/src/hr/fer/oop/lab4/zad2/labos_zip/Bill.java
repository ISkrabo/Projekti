package hr.fer.oop.lab4.zad2.labos_zip;

import java.nio.file.Path;

public class Bill implements Comparable<Bill> {

	private String brRacuna;
	private String ukupno;
	private Path path;
	
	public Bill(String brRacuna, String ukupno, Path path) {
		this.brRacuna = brRacuna;
		this.ukupno = ukupno;
		this.path = path;
	}
	
	public String getBrRacuna() {
		return brRacuna;
	}
	public Path getPath() {
		return path;
	}
	public String getUkupno() {
		return ukupno;
	}
	
	@Override
	public boolean equals(Object naziv) {
		return this.brRacuna.equals(naziv);
	}
	
	@Override
	public int hashCode() {
		return this.brRacuna.hashCode();
	}
	
	public int compareTo(Bill a) {
		return this.brRacuna.compareTo(a.getBrRacuna());
	}
	
}
