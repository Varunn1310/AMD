#include <iostream>
#include <omp.h>

using namespace std;

int main(){
    int nthreads, tid;
    #pragma omp parallel
    {
 
        cout<<"Hello World... from thread = "<<omp_get_thread_num()<<"\n";

    }

    return 0;
}