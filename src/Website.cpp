#include <crow.h>
#include <sstream>
#include "KVStore.hpp"
#include "BlogController.hpp"

using namespace crow;
using namespace std;
using namespace N8;

int main(int argc, char* argv[]) {
  SimpleApp app;
  KVStore store("webiste.db");

  CROW_ROUTE(app, "/<string>").methods(HTTPMethod::POST)
    ([&store](const request& req, std::string key) {
      Controller::Blog blogController(store);
      blogController.CreateOrUpdate(key, req.body);
      return response(202);
    });

  CROW_ROUTE(app, "/<string>").methods(HTTPMethod::GET)
    ([&store](std::string key) {
      Controller::Blog blogController(store);
      return blogController.Get(key);
    });

  app.port(18080).multithreaded().run();
  return 0;
}
