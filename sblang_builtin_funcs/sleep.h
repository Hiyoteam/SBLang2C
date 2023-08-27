#include <chrono>
#include <thread>

void sleep(long long int milliseconds) {
    std::chrono::milliseconds duration(milliseconds);
    std::this_thread::sleep_for(duration);
}
