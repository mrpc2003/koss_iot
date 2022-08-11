package org.opentutorials.javatutorials.numberstring;

import java.util.Scanner;

public class question3 
{
	public static void main(String[] args) 
	{
		Scanner sc = new Scanner(System.in);
		int A = sc.nextInt(); //자연수 A
		int B = sc.nextInt(); //자연수 B
		int C = sc.nextInt(); //자연수 C
		sc.close();
		int num = A * B * C; //세 자연수의 곱
		int count[] = {0,0,0,0,0,0,0,0,0,0}; //0~9의 숫자가 몇번 사용되었는지 저장할 배열
		
		String number = String.valueOf(num); //세 자연수의 곱을 String타입으로 바꿈
		
		//문자열을 한 문자씩 자르기
		//split("") : 공백문자를 파라미터로 지정해 문자를 하나씩 자름 
		String[] strArray = number.split(""); 
		//배열을 검사하여 가져올 값이 있으면 s에 저장
		for(String s : strArray)
		{
			switch(s) //s가 각각 0~9의 숫자이면 각각 배열의 값을 1씩 증가
	//입력변수의 값과 일치하는 case 입력값(입력값1, 입력값2, ...)이 있다면 해당 case문에 속한 문장들이 실행된다. 
			{
				case "0":
				{
					++count[0];
					break;
				}
				case "1":
				{
					++count[1];
					break;
				}
				case "2":
				{
					++count[2];
					break;
				}
				case "3":
				{
					++count[3];
					break;
				}
				case "4":
				{
					++count[4];
					break;
				}
				case "5":
				{
					++count[5];
					break;
				}
				case "6":
				{
					++count[6];
					break;
				}
				case "7":
				{
					++count[7];
					break;
				}
				case "8":
				{
					++count[8];
					break;
				}
				case "9":
				{
					++count[9];
					break;
				}
			}
		}
		for(int j = 0; j<10; j++)
		{
			System.out.println(count[j]); //0~9까지 사용된 횟수 출력
		}
	}
}