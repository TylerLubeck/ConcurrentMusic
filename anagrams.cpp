#include <iostream>
using namespace std;
bool sort(string word1, string word2);
bool compare(int word1[], int word2[], int len);
int main() {
    /* Enter your code here. Read input from STDIN. Print output to STDOUT */
    string word1, word2;
    cin >> word1 >> word2;
    cout << word1<< endl;
    cout << word2 << endl;
    if (sort(word1, word2))
        cout << "Anagrams!";
    else
        cout << "Not anagrams!";
    return 0;
}

bool sort(string word1, string word2){
    if (word1.length() == word2.length()){
        if (word1.length() == 0)
            return true;
        int array1[400];
        int array2[400];
        for(int i=0; i<400; i++){
            array1[i]=0;
            array2[i]=0;
        }
        int len = word1.length();
        for(int i=0; i<len; i++){
            array1[int(word1[i])]++;
            array2[int(word2[i])]++;
        }
        return compare(array1, array2, 400);
    }
    return false;
}

bool compare(int word1[], int word2[], int len){
    for(int i=0; i<len; i++){
        if (word1[i] != word2[i])
            return false;
    }
    return true;
}