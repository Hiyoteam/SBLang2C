#include <nlohmann/json.hpp>
using json = nlohmann::json;
using namespace std;
string get_json_value(string json_text,string key){
    return json::parse(json_text)[key].get<std::string>();
}
string json_to_string(json object){
    return object.dump();
}