#include <iostream>
#include <omp.h>

using namespace std;

void factorial(int n)
{
    int res = 1, i;
    for (i = 2; i <= n; i++)
        res *= i;

    cout<<"Factorial for "<<n<<" : "<<res;
}

int main(){
    int nthreads, tid;
    #pragma omp parallel
    {
 
        factorial(12345);

    }

    return 0;
}