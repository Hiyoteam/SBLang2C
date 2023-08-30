bool is_integer(const std::string& input) {
    std::istringstream iss(input);
    int num;
    return (iss >> num) && iss.eof();
}