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

    m_filepath = std::move(filepath);
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

  void KVStore::Put(std::string_view key, std::string_view value) {
    vector<uint8_t> buffer;

    m_offsets[std::string(key)] = ftell(m_file);
    
    buffer.resize(sizeof(RecordHeader) + key.size() + value.size());
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
    fflush(m_file);
  }

  string KVStore::Get(string_view key) {
    const auto offset = m_offsets.find(key.data());
    if (offset == m_offsets.end()) {
      return "";
    }

    auto handle = fopen(m_filepath.c_str(), "rb");
    if (handle == nullptr) {
      return "";
    }

    if (fseek(handle, offset->second, SEEK_SET) != 0) {
      fclose(handle);
      throw std::system_error(make_error_code(errc(errno)), "unable to seek");
    }

    RecordHeader header;
    if (fread(&header, sizeof(header), 1, handle) != 1) {
      fclose(handle);      
      throw system_error(make_error_code(errc(errno)), "unable to read header");
    }

    if (fseek(handle, header.KeySize, SEEK_CUR) != 0) {
      fclose(handle);      
      throw std::system_error(make_error_code(errc(errno)), "unable to seek");
    }

    string value;
    value.resize(header.ValueSize);
    if (fread(value.data(), header.ValueSize, 1, handle) != 1) {
      fclose(handle);      
      throw system_error(make_error_code(errc(errno)), "unable to read value");      
    }

    fclose(handle);
    return value;
  }
}
