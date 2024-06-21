#include "KVStore.hpp"
#include <format>
#include <system_error>
#include <cerrno>
#include <vector>
#include <string.h>

using namespace std;

struct RecordHeader {
  uint64_t KeySize;
  uint64_t ValueSize;
};

namespace N8 {
  KVStore::KVStore(filesystem::path filepath) {
    m_file = fopen(filepath.c_str(), "ab+");
    if (m_file == nullptr) {
      throw std::system_error(make_error_code(errc(errno)), "unable to open file");
    }
  }

  KVStore::~KVStore() {
    if (m_file != nullptr) {
      fclose(m_file);
    }
  }

  KVStore::KVStore(KVStore&& other) noexcept
    : m_file(exchange(other.m_file, nullptr)) {
  }
  
  KVStore& KVStore::operator=(KVStore&& other) noexcept {
    swap(m_file, other.m_file);
    return *this;
  }

  void KVStore::Put(std::span<uint8_t> key, std::span<uint8_t> value) {
    vector<uint8_t> buffer;
    buffer.resize(sizeof(RecordHeader), key.size() + value.size());
    RecordHeader header {
      .KeySize = key.size(),
      .ValueSize = value.size(),
    };

    memcpy(buffer.data(), &header, sizeof(header));
    copy(key.begin(),
	 key.end(),
	 buffer.begin() + sizeof(header));
    copy(value.begin(),
	 value.end(),
	 buffer.begin() + sizeof(header) + header.KeySize);
    fwrite(buffer.data(), buffer.size(), 1, m_file);
  }
}
