#include <crow.h>
#include <sstream>
#include "KVStore.hpp"
using namespace crow;
using namespace std;
using namespace N8;

int main(int argc, char* argv[]) {
  SimpleApp app;
  KVStore store("webiste.db");
  
  CROW_ROUTE(app, "/<string>").methods(HTTPMethod::POST)
    ([&store](const request& req, std::string key) {
      store.Put(key, req.body);

      stringstream ss;
      ss << "Stored " << key << ": " << req.body;
      return ss.str();
    });

  CROW_ROUTE(app, "/<string>").methods(HTTPMethod::GET)
    ([&store](std::string key) {
      return store.Get(key);
    });

  app.port(18080).multithreaded().run();
  return 0;
}
