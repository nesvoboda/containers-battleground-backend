#include "benchmarks.hpp"
#include <string.h>

Timer::Timer()
{
	_start = 0;
}

Timer::~Timer()
{
}

void Timer::start()
{
	_start = std::clock();
}

std::clock_t Timer::stop()
{
	return std::clock() - _start;
}

Timer::Timer(const Timer &ref)
{
	_start = ref._start;
}

Timer &Timer::operator=(const Timer &ref)
{
	_start = ref._start;
	return (*this);
}

void benchmark_map()
{
	ft::map<int, bool> m1;

	insert_growing(500000, m1);
}

void benchmark_vector()
{
	ft::vector<int> v1;

	v_insert_growing(50000000, v1);
}

void benchmark_stack()
{

	ft::stack<int> s1;

	s_insert_growing(50000000, s1);
	
}


int main(int ac, char **av)
{
	if (ac != 2)
		return 1;
	if (!strcmp(av[1], "map"))
		benchmark_map();
	else if (!strcmp(av[1], "vector"))
		benchmark_vector();
	else if (!strcmp(av[1], "stack"))
		benchmark_stack();
	else
	{
		std::cout << av[1] << std::endl;
		std::cout << "lol" << std::endl;
	}
	return 0;
}