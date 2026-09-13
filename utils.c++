#include <iostream>
#include <algorithm>
#include <vector>
#include <random>
#include <chrono>
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