package org.opentutorials.javatutorials.numberstring;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.Collections;

public class question1 {

	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		ArrayList<Integer> numList = new ArrayList<Integer>();
		numList.add(sc.nextInt());
		numList.add(sc.nextInt());
		numList.add(sc.nextInt());
		numList.add(sc.nextInt());
		numList.add(sc.nextInt());
		numList.add(sc.nextInt());
		sc.close();
		int sum = 0;
		for(int i:numList)
		{
			sum += i;
		}
		System.out.println("합계: " + sum + ", 최대: " + Collections.max(numList) + ", 최소: " + Collections.min(numList) + ", 평균: " + (double)sum / numList.size());
	}

}
