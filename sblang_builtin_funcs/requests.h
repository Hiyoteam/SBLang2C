#ifndef REQUESTS_H
#define REQUESTS_H

#include <string>
#include <vector>
#include <curl/curl.h>
struct HttpResponse {
    long status_code;
    std::vector<std::string> headers;
    std::string text;
};

size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* response) {
    size_t total_size = size * nmemb;
    response->append(static_cast<char*>(contents), total_size);
    return total_size;
}
namespace std{
HttpResponse web_get(const std::string& url) {
    HttpResponse response;

    CURL* curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

        std::string header_string;
        std::string body_string;

        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &body_string);
        curl_easy_setopt(curl, CURLOPT_HEADERDATA, &header_string);

        CURLcode res = curl_easy_perform(curl);
        if (res == CURLE_OK) {
            curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response.status_code);

            // 解析响应头
            std::string header_line;
            size_t header_start = 0;
            size_t header_end = header_string.find("\r\n");
            while (header_end != std::string::npos) {
                header_line = header_string.substr(header_start, header_end - header_start);
                response.headers.push_back(header_line);
                header_start = header_end + 2;
                header_end = header_string.find("\r\n", header_start);
            }

            // 解析响应正文
            response.text = std::move(body_string);
        }

        curl_easy_cleanup(curl);
    }

    return response;
}
}
#endif  // REQUESTS_H