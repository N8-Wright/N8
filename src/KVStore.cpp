#include "KVStore.hpp"
#include <system_error>
#include <cerrno>
#include <vector>
#include <cstring>
#include <utility>
#include <sstream>
#include <mutex>
using namespace std;

uint32_t CurrentFormat = 1;
struct RecordHeader {
  RecordHeader(uint64_t keySize, uint64_t valueSize)
    : Format(CurrentFormat), Reserved(0),
      KeySize(keySize), ValueSize(valueSize) {
  }

  RecordHeader() {};
  uint32_t Format;
  uint32_t Reserved;
  uint64_t KeySize;
  uint64_t ValueSize;
};

namespace N8 {
  KVStore::KVStore(const filesystem::path& filepath) {
    m_file = fopen((const char*)filepath.c_str(), "ab+");
    if (m_file == nullptr) {
      throw system_error(make_error_code(errc(errno)), "unable to open file");
    }

    m_filepath = filepath;

    // Because we've open the file as append, we are already placed at
    // the end of it.
    if (fseek(m_file, 0, SEEK_END) != 0) {
      fclose(m_file);
      throw system_error(make_error_code(errc(errno)), "unable to seek to end of file");
    }
    
    const auto fileSize = ftell(m_file);
    if (fileSize != 0) {
      long offset = 0;

      // Start at the beginning of the file.
      if (fseek(m_file, 0, SEEK_SET) != 0) {
	  fclose(m_file);
	  throw system_error(make_error_code(errc(errno)), "unable to seek");
      }

      while (offset < fileSize) {
	RecordHeader header;
	if (fread(&header, sizeof(header), 1, m_file) != 1) {
	  fclose(m_file);
	  throw system_error(make_error_code(errc(errno)), "unable to read header");
	}

	string key;
	key.resize(header.KeySize);
	if (fread(key.data(), header.KeySize, 1, m_file) != 1) {
	  fclose(m_file);
	  throw system_error(make_error_code(errc(errno)), "unable to read key");
	}

	if (header.ValueSize == 0) {
	  // A zero valued header indicates a tombstone.
	  m_offsets.erase(key);
	}
	else {
	  m_offsets[key] = offset;
	  // We've read the header and key, now skip the value
	  if (fseek(m_file, (long)header.ValueSize, SEEK_CUR) != 0) {
	    fclose(m_file);
	    throw system_error(make_error_code(errc(errno)), "unable to seek");
	  }
	}

	offset = ftell(m_file);
      }
    }
  }

  KVStore::~KVStore() {
    if (m_file != nullptr) {
      // TODO: Make more robust.
      fclose(m_file);
    }
  }

  KVStore::KVStore(KVStore&& other) noexcept
    : m_file(exchange(other.m_file, nullptr)),
      m_filepath(move(other.m_filepath)),
      m_offsets(move(other.m_offsets)) {
  }

  KVStore& KVStore::operator=(KVStore&& other) noexcept {
    swap(m_file, other.m_file);
    swap(m_filepath, other.m_filepath);
    swap(m_offsets, other.m_offsets);
    return *this;
  }

  void KVStore::Put(string_view key, string_view value) {
    unique_lock lock(m_mutex);
    vector<uint8_t> buffer;

    m_offsets[string(key)] = ftell(m_file);

    buffer.resize(sizeof(RecordHeader) + key.size() + value.size());
    RecordHeader header(key.size(), value.size());
    memcpy(buffer.data(), &header, sizeof(header));
    copy(key.begin(),
	 key.end(),
	 buffer.begin() + sizeof(header));

    const auto offset = sizeof(header) + header.KeySize;
    copy(value.begin(),
	 value.end(),
	 buffer.begin() + static_cast<long>(offset));
    fwrite(buffer.data(), buffer.size(), 1, m_file);
    fflush(m_file);
  }

  string KVStore::Get(string_view key) {
    shared_lock lock(m_mutex);
    const auto offset = m_offsets.find(key);
    if (offset == m_offsets.end()) {
      return "";
    }

    auto handle = fopen((const char*)m_filepath.c_str(), "rb");
    if (handle == nullptr) {
      return "";
    }

    if (fseek(handle, (long)offset->second, SEEK_SET) != 0) {
      fclose(handle);
      throw system_error(make_error_code(errc(errno)), "unable to seek");
    }

    RecordHeader header;
    if (fread(&header, sizeof(header), 1, handle) != 1) {
      fclose(handle);
      throw system_error(make_error_code(errc(errno)), "unable to read header");
    }

    // Skip over the key array. We don't need it right now.
    if (fseek(handle, (long)header.KeySize, SEEK_CUR) != 0) {
      fclose(handle);
      throw system_error(make_error_code(errc(errno)), "unable to seek");
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

  void KVStore::Delete(string_view key) {
    unique_lock lock(m_mutex);
    const auto result = m_offsets.find(key);
    if (result != m_offsets.end()) {
      m_offsets.erase(result);
      vector<uint8_t> buffer;
      buffer.resize(sizeof(RecordHeader) + key.size());

      RecordHeader header(key.size(), 0);
      memcpy(buffer.data(), &header, sizeof(header));
      copy(key.begin(),
	   key.end(),
	   buffer.begin() + sizeof(header));
      fwrite(buffer.data(), buffer.size(), 1, m_file);
      fflush(m_file);
    }
  }

  void KVStore::Trim() {

  }
}
