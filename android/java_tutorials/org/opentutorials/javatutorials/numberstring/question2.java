package org.opentutorials.javatutorials.numberstring;
import java.util.Scanner;

public class question2 {

	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		int i = sc.nextInt();
		for(int j=1;j<i;j++) {
			System.out.println(" ".repeat(i-j-1)+"*".repeat((2*j)-1));
//			System.out.println("k:"+(i-j));
//			System.out.println("j:"+j);
//		
			
		}
	}

}
