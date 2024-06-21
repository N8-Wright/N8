#include "KVStore.hpp"
#include <iostream>
using namespace N8;
using namespace std;
int main(int argc, char* argv[]) {
  KVStore store("db");
  
#if 0
  store.Put("abc", "12345");

  auto store2 = std::move(store);
  store2.Put("cdef", "9999");
  store2.Put("123125lksdf", "19824uskdf");
  const auto value = store2.Get("cdef");

  cout << value << endl;

  store2.Delete("cdef");
  const auto value2 = store2.Get("cdef");
  cout << value2 << endl;
#else
  const auto value = store.Get("cdef");
  cout << value << endl;
#endif
  return 0;
}
