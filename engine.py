import epicbox
from statistics import mean

PROFILES = {
    'gcc_clone': {
        'docker_image': 'bg',
        'user': 'root',
        'network_disabled': False,
    },
    'gcc_compile': {
        'docker_image': 'bg',
        'user': 'root',
    },
    'gcc_run': {
        'docker_image': 'bg',
        # It's safer to run untrusted code as a non-root user (even in a container)
        'user': 'sandbox',
        'read_only': True,
        'network_disabled': False,
    },
}
epicbox.configure(profiles=PROFILES)

def run_container(epicbox, workdir, container):
    acc = []
    for i in range(3):
        res = epicbox.run('gcc_run', f'./main {container}',
                limits={'cputime': 2, 'memory': 512},
                workdir=workdir)
        print(res)
        if res['exit_code'] != 0 or res['timeout'] != False or res['oom_killed'] != False:
            return -1.0
        acc.append(res['duration'])
    return mean(acc)

def test_solution(github_link):

    # A working directory allows to preserve files created in a one-time container
    # and access them from another one. Internally it is a temporary Docker volume.
    with epicbox.working_directory() as workdir:

        res = epicbox.run('gcc_clone', f'git clone {github_link} tested_code',
                    limits={'cputime': 5, 'memory': 64},
                    workdir=workdir)
        
        # compilation
        res = None
        with open("./benchmarks.cpp", mode="rb") as bcpp, open("./benchmarks.hpp", mode="rb") as bhpp:
            res = epicbox.run('gcc_compile', 'g++ -O2 -static -o main benchmarks.cpp',
                        files=[
                            {'name': 'benchmarks.cpp', 'content': bcpp.read()},
                            {'name': 'benchmarks.hpp', 'content': bhpp.read()},
                            ],
                            limits={'cputime': 2, 'memory': 128},
                        workdir=workdir)
            print(f"Comp: {res}")

        return {
            'vector': run_container(epicbox, workdir, 'vector'),
            'map': run_container(epicbox, workdir, 'map'),
            'stack': run_container(epicbox, workdir, 'stack'),
        }
    