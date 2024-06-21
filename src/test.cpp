#include "KVStore.hpp"
#include <iostream>
using namespace N8;
using namespace std;
int main(int argc, char* argv[]) {
  KVStore store("db");
  store.Put("abc", "12345");
  store.Put("cdef", "9999");
  store.Put("123125lksdf", "19824uskdf");
  const auto value = store.Get("cdef");

  cout << value << endl;
  return 0;
}
