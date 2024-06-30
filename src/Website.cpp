#include <crow.h>
using namespace crow;

int main(int argc, char* argv[]) {
  SimpleApp app;
  
  CROW_ROUTE(app, "/")([]() {
    return "Hello world";
  });

  app.port(18080).multithreaded().run();
  return 0;
}
