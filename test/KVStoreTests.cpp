#include <gtest/gtest.h>
#include "KVStore.hpp"
using namespace std;
using namespace N8;
class KVStoreTests : public testing::Test {
protected:
  KVStoreTests() : m_kvStore(std::make_unique<KVStore>([] {
    srand(time(NULL));
    std::stringstream ss;
    ss << "KVStoreTests." << rand();
    return ss.str();
  }())), m_path(m_kvStore->Path()) {
  }

  ~KVStoreTests() {
    filesystem::remove(m_path);
    m_kvStore.reset();
  }

  std::unique_ptr<KVStore> m_kvStore;
  filesystem::path m_path;
};

TEST_F(KVStoreTests, PutThenGet_ReturnsExpectedValue) {
  // Arrange
  m_kvStore->Put("abc", "123");

  // Act
  const auto value = m_kvStore->Get("abc");

  // Assert
  EXPECT_EQ(value, "123");
}

TEST_F(KVStoreTests, PutTwiceSameKeyThenGet_ReturnsExpectedValue) {
  // Arrange
  m_kvStore->Put("abc", "123");
  m_kvStore->Put("abc", "456789");

  // Act
  const auto value = m_kvStore->Get("abc");

  // Assert
  EXPECT_EQ(value, "456789");
}


TEST_F(KVStoreTests, PutTwiceSameKeyThenGet_Restart_ReturnsExpectedValue) {
  // Arrange
  m_kvStore->Put("abc", "123");
  m_kvStore->Put("abc", "456789");

  // Act
  m_kvStore.reset();
  KVStore restarted(m_path);

  // Assert
  const auto value = restarted.Get("abc");
  EXPECT_EQ(value, "456789");
}

TEST_F(KVStoreTests, DeleteKey_ReturnsEmptyValue) {
  // Arrange
  const auto key = "sldfjasdkjflkdjfa";
  m_kvStore->Put(key, "qwieriuqweruqweuruiqweriu");

  // Act
  m_kvStore->Delete(key);

  // Assert
  const auto value = m_kvStore->Get(key);
  EXPECT_EQ(value, "");
}

TEST_F(KVStoreTests, DeleteKey_Restart_ReturnsEmptyValue) {
  // Arrange
  const auto key = "sldfjasdkjflkdjfa";
  m_kvStore->Put(key, "qwieriuqweruqweuruiqweriu");
  m_kvStore->Delete(key);

  // Act
  m_kvStore.reset();
  KVStore restarted(m_path);

  // Assert
  const auto value = restarted.Get(key);
  EXPECT_EQ(value, "");
}
