package main;

import java.io. *;

public class Main {

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		String chaine = "script.py";
		Runtime rt = Runtime.getRuntime ();
		try {
			Process pr = rt.exec ("mkdir " + chaine);
			pr.waitFor ();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
