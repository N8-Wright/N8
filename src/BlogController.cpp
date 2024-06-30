#include <sstream>
#include <md4c-html.h>

#include "BlogController.hpp"
#include "KVStore.hpp"

using namespace std;
namespace N8::Controller {
  Blog::Blog(KVStore& kvStore)
    : m_kvStore(kvStore) {
  }

  void Blog::CreateOrUpdate(string_view name, string_view content) {
    string renderedContent;
    md_html(content.data(),
	    content.size(),
	    [](const MD_CHAR* content, MD_SIZE size, void* data) {
	      auto* render = static_cast<string*>(data);
	      render->append(string_view(content, size));
	    },
	    &renderedContent, 0, 0);

    m_kvStore.Put(name, renderedContent);
  }

  string Blog::Get(std::string_view name) {
    stringstream blogPost;
    blogPost << "<!DOCTYPE html><html><body>";
    blogPost << m_kvStore.Get(name);
    blogPost << "</body></html>";
    return blogPost.str();
  }
}
