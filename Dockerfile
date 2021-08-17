FROM stepik/epicbox-gcc:6.3.0

RUN apt-get update && apt-get install -y git python3 clang
# Clone the benchmark
RUN git clone https://github.com/nesvoboda/containers-benchmark
# Compile inputs for tests
RUN cd containers-benchmark ; ./setup.sh
