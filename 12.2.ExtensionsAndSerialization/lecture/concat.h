#include <string>

class EmptyArgumentException : public std::runtime_error {
    using std::runtime_error::runtime_error;
};

std::string cpp_concat(const std::string& l, const std::string& r) {
    if (l.empty() || r.empty()) {
        throw EmptyArgumentException{"Empty argument passed"};
    }
    return l + r;
}
