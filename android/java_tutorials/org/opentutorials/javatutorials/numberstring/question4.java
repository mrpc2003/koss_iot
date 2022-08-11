package org.opentutorials.javatutorials.numberstring;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;
public class question4 {

	public static void main(String[] args) {

		Scanner sc = new Scanner(System.in);
		int A = sc.nextInt(); //자연수 A
		int B = sc.nextInt(); //자연수 B
		int C = sc.nextInt(); //자연수 C
		sc.close();
		ArrayList<Integer> numList = new ArrayList<Integer>();
		numList.add(A);
		numList.add(B);
		numList.add(C);
		
		if(numList.get(0) == numList.get(1) && numList.get(1)== numList.get(2)){
			int result = 10000+ A*1000;
			System.out.println(result);
					
		}else if(A == numList.get(1) || A == numList.get(2)) {
			int result =  1000 + A * 100;
			System.out.println(result);

		}else if(B == numList.get(2)) {
			int result = 1000 + B * 100;
			System.out.println(result);

		}else {
			int result = Collections.max(numList)*100;
			System.out.println(result);

		}
		
	}

}
