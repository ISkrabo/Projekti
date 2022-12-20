package hr.fer.oop.lab4.zad2.verzija10MostArticles;

public class Artikl implements Comparable<Artikl> {

	private String naziv;
	private String cijena;
	
	public Artikl(String naziv, String cijena) {
		this.naziv = naziv;
		this.cijena = cijena;
	}
	
	public String getNaziv() {
		return naziv;
	}
	public String getCijena() {
		return cijena;
	}
	
	@Override
	public boolean equals(Object naziv) {
		return this.naziv.equals(naziv);
	}
	
	@Override
	public int hashCode() {
		return this.naziv.hashCode();
	}
	
	public int compareTo(Artikl a) {
		return this.naziv.compareTo(a.getNaziv());
	}
	
}
