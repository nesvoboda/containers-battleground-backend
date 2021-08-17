#ifndef BENCHMARKS_HPP

#	include "tested_code/map.hpp"
#	include "tested_code/stack.hpp"
#	include "tested_code/vector.hpp"
#	include <iostream>
#	include <map>
#	include <stack>
#	include <vector>

// mapType must be a map to int, bool.
template <typename MapType>
void insert_growing(size_t times, MapType map)
{
	for (size_t i = 0; i < times; i++)
	{
		map[i] = true; // insert a constantly growing range of integers
		// which is a worst-case scenario for an unbalanced map.
		map.find(i);
	}
}

// Vector benchmark
// Vector must be a vector of ints
template <typename VectorType>
void v_insert_growing(size_t times, VectorType vector)
{
	int tmp = 0;

	for (size_t i = 0; i < times; i++)
	{
		vector.push_back(i); // insert a constantly growing range of integers
		tmp = vector[i];
	}
}

// Stack benchmark
// Stack must be a vector of ints
template <typename StackType>
void s_insert_growing(size_t times, StackType stack)
{
	int tmp = 0;

	for (size_t i = 0; i < times; i++)
	{
		stack.push(i); // insert a constantly growing range of integers
	}

	for (size_t i = 0; i < times; i++)
	{
		tmp = stack.top();
		stack.pop();
	}
}

void benchmark_map();

#endif // !BENCHMARKS_HPP