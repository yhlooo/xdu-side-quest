#include<stdio.h>
#include<windows.h>
void status(void);
char cell1[27][27]={{0}}, cell2[27][27]={{0}};

int main()
{

	int i, j, k=1, n;
	freopen(".\\data.txt", "r", stdin);
	printf("       5    10   15   20   25\n");
	for(i=1;i<26;i++){
		printf("%-2d ", i);
		for(j=1;j<26;j++){
			cell1[i][j] = getchar()-48;
		}
		getchar();
	}
	while(1){
		n=0;
		for(i=1;i<26;i++){
			for(j=1;j<26;j++){
				if(cell1[i][j]==1)
					n++;
			}
		}
		if(n==0){
			system("cls");
			printf("                 第%d代居民数为%d\n", k, n);
			printf("0          5         10        15        20        25\n");
			for(i=1;i<13;i++)
				printf("%-2d \n", i);
			printf("13            你世界的居民繁衍了%d代\n", k-1);
			printf("14         他们由于人口过少覆灭啦，哈哈哈！\n");
			for(i=15;i<26;i++)
				printf("%-2d \n", i);
			break;
		}
		system("cls");
		printf("              第%d代居民数为%d\n", k, n);
		printf("0          5         10        15        20        25\n");
		for(i=1;i<26;i++){
			printf("%-2d ", i);
			for(j=1;j<26;j++){
				if(cell1[i][j]==1)
					printf("O ");
				else
					printf("  ");
			}
			printf("\n");
		}
		status();
		k++;
		Sleep(500);
	}
	return 0;
}

void status(void)
{
	int n, i, j;
	for(i=1;i<26;i++){
		for(j=1;j<26;j++){
			n = cell1[i-1][j-1]+cell1[i-1][j]+cell1[i-1][j+1];
			n += cell1[i][j-1]+cell1[i][j+1];
			n += cell1[i+1][j-1]+cell1[i+1][j]+cell1[i+1][j+1];
			if(cell1[i][j]==1){
				if(n>3 || n<2)
					cell2[i][j] = 0;
				else
					cell2[i][j] = 1;
			}
			else{
				if(n==3)
					cell2[i][j] = 1;
				else
					cell2[i][j] = 0;
			}
		}
	}
	for(i=1;i<26;i++){
		for(j=1;j<26;j++){
			cell1[i][j]=cell2[i][j];
		}
	}
}
