#include <iostream>
using namespace std;
#define COLS 500
int getmax(char array[][COLS], int rows, int cols);
int flipnum(char array[][COLS], int rows, int cols, int numflip, int max);
int flipcols(char array[][COLS], int rows, int cols, bool cols_to_flip[]);
char opposite(char val);
int checkmax(char array[][COLS], int rows, int cols);
int main() {
    /* Enter your code here. Read input from STDIN. Print output to STDOUT */
    int m, n;
    cin >> m >> n;
    char array[m][COLS];
    for (int i=0; i<n; i++){
        for(int j=0; j<m; j++){
            char val;
            cin >> val;
            array[j][i] = val;
        }
    }
    cout << getmax(array, m, n);
    return 0;
}

int getmax(char array[][COLS], int rows, int cols){
    //get initial max
    int max = checkmax(array, rows, cols);
    //check if can get a greater max
    //flip i number of cols
    for(int i=0; i<cols; i++){
        max = flipnum(array, rows, cols, i, max);
    }
    return max;
}

int flipnum(char array[][COLS], int rows, int cols, int numflip, int max){
    int i = 0;
    bool cols_to_flip[cols];
    
    while(i<cols){
        //reset newmax and cols to flip
        int newmax = 0;
        for(int x=0; x<cols; x++){
            cols_to_flip[x] = false;
        }
        //go through and add cols to flip starting at i
        for(int j=i; j<numflip; j++){
            cols_to_flip[j] = true;
        }
        newmax = flipcols(array, rows, cols, cols_to_flip);
        if(newmax > max)
            max = newmax;
    }
    return max;
}

//actually flips the cols and returns max
int flipcols(char array[][COLS], int rows, int cols, bool cols_to_flip[]){
    //if false then dont flip that col
    for(int i=0; i<cols; i++){
        //if true then go through rows and flip
        if (cols_to_flip[i]){
            for(int j=0; j<rows; j++){
                array[i][j] = opposite(array[i][j]);
            }
        }
    }
    
    return checkmax(array, rows, cols);
}

char opposite(char val){
    if (val == 'T')
        return 'P';
    else
        return 'T';
}

int checkmax(char array[][COLS], int rows, int cols){
    //go through all cols and increment max if all the same
    int max = 0;
    for (int i=0; i<rows; i++){
        int count=0;
        for(int j=0; j<cols; j++){
            //dont go off end
            int next = j++;
            if (next <cols){
                if (array[i][j] == array[i][next])
                    count++;
            }
        }
        if (count == cols)
            max++;
    }
    return max;
}