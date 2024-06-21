#pragma once
#include <filesystem>
#include <cstdio>
#include <string_view>
#include <string>
#include <shared_mutex>

namespace N8 {
  class KVStore {
  private:
    std::FILE* m_file = nullptr;
    std::filesystem::path m_filepath;
    std::unordered_map<std::string, uint64_t> m_offsets;
    mutable std::shared_mutex m_mutex;
    
  public:
    KVStore(std::filesystem::path filepath);
    ~KVStore();
    KVStore(const KVStore&) = delete;
    KVStore(KVStore&&) noexcept;
    KVStore& operator=(const KVStore&) = delete;
    KVStore& operator=(KVStore&&) noexcept;

    void Put(std::string_view key, std::string_view value);
    std::string Get(std::string_view key);
  };
}
