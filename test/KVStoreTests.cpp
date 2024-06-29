#include <gtest/gtest.h>
#include <iostream>
#include <random>
#include "KVStore.hpp"
using namespace std;
using namespace N8;

string GenerateFileName(string_view prefix) {
  random_device rd;
  mt19937 gen(rd()); 
  uniform_int_distribution<> dis(0, numeric_limits<int>::max());
  const auto randomNum = dis(gen);
  
  stringstream ss;
  ss << prefix << "." << randomNum;
  return ss.str();
}

class KVStoreTests : public testing::Test {
protected:
  void SetUp() override {
    m_kvStore = std::make_unique<KVStore>(GenerateFileName("KVStoreTests"));
    m_path = m_kvStore->Path();
  }

  void TearDown() override {
    m_kvStore.reset();
    filesystem::remove(m_path);
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

TEST_F(KVStoreTests, PutThenGet_Restart_ReturnsExpectedValue) {
  // Arrange
  m_kvStore->Put("abc", "123");

  // Act
  m_kvStore.reset();
  m_kvStore = std::make_unique<KVStore>(m_path);

  // Assert
  const auto value = m_kvStore->Get("abc");
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
  m_kvStore = std::make_unique<KVStore>(m_path);

  // Assert
  const auto value = m_kvStore->Get("abc");
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
