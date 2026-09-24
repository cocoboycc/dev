#include <iostream>
#include <algorithm>
#include <vector>
#include <random>
#include <chrono>
#include <cassert>
#include <climits>
void merge(std::vector<double> &vec, unsigned int l, unsigned int m, unsigned int r){
    unsigned int curr_left= l; 
    unsigned int curr_right=m+1; 
    std::vector<double> copy; 
    while(curr_left<=m && curr_right<=r){
        if (vec[curr_left]<=vec[curr_right]){
            copy.push_back(vec[curr_left]); 
            ++curr_left; 
        }else{
            copy.push_back(vec[curr_right]); 
            ++curr_right; 
        }
    }
    if (curr_left<=m){
        while (curr_left<=m){
            copy.push_back(vec[curr_left]);
            ++curr_left; 
        }
    }else if (curr_right<=r){
        while (curr_right<=r){
            copy.push_back(vec[curr_right]); 
            ++curr_right; 
        }
    }
    unsigned int iterator=0; 
    for (unsigned int i=l; i<=r; ++i){
        vec[i]= copy[iterator]; 
        ++iterator; 
    }
}

void merge_sort(std::vector<double> &vector){
    unsigned int n = vector.size();

    bool merged;

    do {
        merged=false; 
        unsigned int r = 0;

        while (r < n) {
            unsigned int l = r;
            unsigned int m = l;

            while (m < n-1 && vector[m+1] >= vector[m]) {
                ++m;
            }

            if (m < n-1) {
                r = m + 1;

                while (r < n-1 && vector[r+1] >= vector[r]) {
                    ++r;
                }

                merge(vector, l, m, r);
                merged = true;
                ++r;
            } else {
                r = n;
            }
        }

    } while (merged);
}

void quicksort(std::vector<int> &vec, int l, int r){
    if (r-l<1){
        return; 
    }
    int pivot= vec[l]; 
    int i= l+1; 
    int j=r-1; 
    while (i<=j){
        while (i<=j && vec[i]<=pivot){
            ++i; 
        } 
        while (i<=j && vec[j]>pivot){
            --j; 
        }
        if (i<j){
            std::swap(vec[i], vec[j]);
        }
    }
    std::swap(vec[l],vec[j]);
    quicksort(vec,l,j-1);
    quicksort(vec,j+1,r); 
}

char bit_checker(const std::string& A, int bit) {
    return A[bit];
}

// insertion of strings with binary 0 or 1
void radix_sort(std::vector<std::string>& vec, int left, int right, int bit) {

    if (left >= right || bit < 0) {
        return;
    }

    assert(static_cast<size_t>(bit) < vec[0].size());

    int i = left-1;
    int j = right+1;

    do {
        do {
            ++i;
        } while (i < j && bit_checker(vec[i], bit) == '0');

        do {
            --j;
        } while (i < j && bit_checker(vec[j], bit) == '1');

        if (i < j) {
            std::swap(vec[i], vec[j]);
        }

    } while (i < j);

    radix_sort(vec, left, i - 1, bit + 1);
    radix_sort(vec, i, right, bit + 1);
}

void dp_largest_inc_subs(const std::vector<int> vec){
    int n = vec.size();

    std::vector<int> T(n + 1, INT_MAX);
    T[0] = INT_MIN;

    std::vector<int> V(n, INT_MAX);

    for (int k = 0; k < n; ++k){
        for (int l = 0; l < n; ++l){
            if (vec[k] > T[l] && vec[k] < T[l + 1]){
                T[l + 1] = vec[k]; 
                V[k] = T[l]; 
            }
        } 
    }

    // searching the largest index in T with T[i] < INT_MAX
    int largest_index = 0;

    for (int l = 1; l <= n; ++l){
        if (T[l] < INT_MAX){
            largest_index = l; 
        }
    }

    int e = T[largest_index];

    while (e != INT_MIN){

        for (int i = 0; i < n; ++i){

            if (vec[i] == e){

                std::cout << e << " "; 
                e = V[i];
                break;
            }
        }
    }
}


int knapsack(int W, std::vector<int> &val, std::vector<int> &wt) {
    int n = wt.size();
    std::vector<std::vector<int>> dp(n + 1, std::vector<int>(W + 1));

    for (int i = 0; i <= n; i++) {
        for (int j = 0; j <= W; j++) {
            
            // If there is no item or the knapsack's capacity is 0
            if (i == 0 || j == 0)
                dp[i][j] = 0;
            else {
                int pick = 0;
                
                // Pick ith item if it does not exceed the capacity of knapsack
                if(wt[i - 1] <= j)
                    pick = val[i - 1] + dp[i - 1][j - wt[i - 1]];
                    
                // Don't pick the ith item
                int notPick = dp[i - 1][j];
                
                dp[i][j] = std::max(pick, notPick);
            }
        }
    }
    return dp[n][W];
}



int main(){
unsigned int n = 100000000;
std::vector<double> vec(n);

std::random_device rd;
std::mt19937 gen(rd());
std::uniform_real_distribution<double> dist(0.0, 100000.0);

for (unsigned int i = 0; i < n; ++i) {
    vec[i] = dist(gen);
}
auto start= std::chrono::high_resolution_clock::now(); 
merge_sort(vec);
auto stop= std::chrono::high_resolution_clock::now(); 
auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);

std::cout << duration.count() << " s\n";
}

