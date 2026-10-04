#include <iostream>
#include <vector>
using namespace std;

int n;
int k;

vector<int> selected;

void backtracking(int start, int sum) {

    if (selected.size() == k) {

        if (sum % 2 == 1) {

            for (int x : selected) {
                cout << x << " ";
            }

            cout << endl;
        }

        return;
    }

    for (int i = start; i <= n; i++) {

        if (selected.size() == 0 || i - selected.back() >= 3) {

            selected.push_back(i);

            backtracking(i + 1, sum + i);

            selected.pop_back();
        }
    }
}

int main() {

    cout << "Enter n: ";
    cin >> n;

    cout << "Enter k: ";
    cin >> k;

    cout << "Answer: " << endl;

    backtracking(1, 0);

    return 0;
}