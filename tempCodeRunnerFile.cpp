#include<iostream>
using namespace std;
bool is_prime(int num){

        if(num<=1) return false;
        if(num==2) return true;
        for(int i=2;i*i<=num;i++)
                if(num%i==0) return false;
        return true;
}
int zigzag_sum(int**matrix,int n){
int sum = 0;
int start,count;

for(int d=0;d<2*n-1;d++){
        if(d<n){
        start=0;
         count=d+1;
        }
        else{
        start=d-n+1;
        count=2*n-d-1;
        }
for(int i=0;i<count;i++){
        if(d%2==0){
        int row=d-1;
        int col=i;
        }
        else{
        int row=start+1;
        int col = d-row;
        int val = *(*(matrix + row) + col);
            sum += is_prime(val) ? -val : val;
        }



}
return sum;
}


int main(){
   int n = 3;

    int input[3][3] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };
      int** mat = new int*[n];
    for (int i = 0; i < n; ++i) {
        mat[i] = new int[n];
        for (int j = 0; j < n; ++j)
            mat[i][j] = input[i][j];
    }

    int res = zigzag_sum(mat, n);
    cout << "Zigzag sum = " << res << endl;

    for (int i = 0; i < n; ++i)
        delete[] mat[i];
    delete[] mat;
return 0;
}