#pragma once
#include <filesystem>
#include <cstdio>
#include <string_view>
#include <string>
#include <shared_mutex>

#include "StringHash.hpp"

namespace N8 {
  class KVStore {
  private:
    std::FILE* m_file = nullptr;
    std::filesystem::path m_filepath;
    std::unordered_map<std::string, long, StringHash, std::equal_to<>> m_offsets;
    mutable std::shared_mutex m_mutex;
    
  public:
    KVStore(const std::filesystem::path& filepath);
    ~KVStore();
    KVStore(const KVStore&) = delete;
    KVStore(KVStore&&) noexcept;
    KVStore& operator=(const KVStore&) = delete;
    KVStore& operator=(KVStore&&) noexcept;

    const std::filesystem::path& Path() { return m_filepath; };
    void Put(std::string_view key, std::string_view value);
    std::string Get(std::string_view key);
    void Delete(std::string_view key);
    void Trim();
  };
}
