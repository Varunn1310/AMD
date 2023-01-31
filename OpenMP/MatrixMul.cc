#include <iostream>
#include <omp.h>
#include<cstring>

using namespace std;

#define mx 1002

int a[mx][mx];
int b[mx][mx];
int c[mx][mx];
int d[mx][mx];
void generate_matrix(int n)
{
	int i,j;
	for(i=0;i<n;i++)
	{
		for(j=0;j<n;j++)
		{
			a[i][j]=rand()%100;
			b[i][j]=rand()%100;
			
		}
	}
}

void matrix_mult(int n)
{
	int i,j,k;
	double st=omp_get_wtime();
	for(i=0;i<n;i++)
	{
		for(j=0;j<n;j++)
		{
			for(k=0;k<n;k++)
			{
				c[i][j]+=a[i][k]*b[k][j];
			}
		}
	}
	double en=omp_get_wtime();
	cout<<"Normal: "<<en-st<<"\n";
}

void matrix_mult_parallel(int n)
{
	//Static Scheduler
	memset(d,0,sizeof d);
	int i,j,k;
	double st=omp_get_wtime();
	#pragma omp parallel for schedule(static,50) collapse(2) private(i,j,k)shared(a,b,c)
        for(i=0;i<n;i++)
        {
            for(j=0;j<n;j++)
            {
                for(k=0;k<n;k++)
                {
                    d[i][j]+=a[i][k]*b[k][j];
                }
            }
        }
	double en=omp_get_wtime();
	cout<<"Parallel: "<<en-st<<"\n";
}

int main(){
	int n=500;
	generate_matrix(n);
	matrix_mult(n);
	
	matrix_mult_parallel(n);

    return 0;
}