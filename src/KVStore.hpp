#pragma once
#include <span>
#include <filesystem>
#include <cstdio>

namespace N8 {
  class KVStore {
  private:
    std::FILE* m_file = nullptr;
  public:
    KVStore(std::filesystem::path filepath);
    ~KVStore();
    KVStore(const KVStore&) = delete;
    KVStore(KVStore&&) noexcept;
    KVStore& operator=(const KVStore&) = delete;
    KVStore& operator=(KVStore&&) noexcept;

    void Put(std::span<uint8_t> key, std::span<uint8_t> value);
  };
}
