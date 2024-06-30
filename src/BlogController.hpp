#pragma once
#include <string_view>

namespace N8 {
  class KVStore;
};

namespace N8::Controller {
  class Blog
  {
    KVStore& m_kvStore;
  public:
    Blog(KVStore& kvStore);
    void CreateOrUpdate(std::string_view name, std::string_view content);
    std::string Get(std::string_view name);
  };
}
