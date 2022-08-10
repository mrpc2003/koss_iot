package org.opentutorials.javatutorials.numberstring;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.Collections;

public class question3 {

	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		ArrayList<Integer> numList = new ArrayList<Integer>();
		numList.add(sc.nextInt());
		numList.add(sc.nextInt());
		numList.add(sc.nextInt());

		int sum = 1;
		for(int i:numList)
		{
			sum *= i;
		}
		String str = String.valueOf(sum);
		char[] array_number = new char[str.length()];
		for(int i = 0; i<numList.size();i++) {
			array_number[i] = (str.charAt(i));
		}
		System.out.println(array_number);
	}

}
