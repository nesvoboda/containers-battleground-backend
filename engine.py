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
    },
}
epicbox.configure(profiles=PROFILES)

def run_container(epicbox, workdir, container):
    acc = []
    for i in range(3):
        res = epicbox.run('gcc_run', f'./benchmark_{container}.sh',
                limits={'cputime': 10, 'memory': 512},
                workdir=workdir)
        print(res)
        if res['exit_code'] != 0 or res['timeout'] != False or res['oom_killed'] != False:
            return -1.0

        diff_res = epicbox.run('gcc_run', f'diff test_output_{container} std_output_{container}',
                limits={'cputime': 10, 'memory': 1024},
                workdir=workdir)
        if diff_res['exit_code'] != 0 or diff_res['timeout'] != False or diff_res['oom_killed'] != False:
            return -1.0
        acc.append(res['duration'])
    return mean(acc)

def test_solution(github_link):

    # A working directory allows to preserve files created in a one-time container
    # and access them from another one. Internally it is a temporary Docker volume.
    with epicbox.working_directory() as workdir:

        res = epicbox.run('gcc_clone', f'cp /containers-benchmark/* .',
                    limits={'cputime': 5, 'memory': 64}, 
                    workdir=workdir)

        res = epicbox.run('gcc_clone', f'git clone {github_link} tested_code',
                    limits={'cputime': 5, 'memory': 64},
                    workdir=workdir)
        
        # compilation
        res = epicbox.run('gcc_compile', './compile_all_benchmarks.sh',
                            limits={'cputime': 2, 'memory': 128},
                            workdir=workdir)

        res = epicbox.run('gcc_compile', 'touch test_output_stack test_output_vector test_output_map',
                            limits={'cputime': 2, 'memory': 128},
                            workdir=workdir)

        res = epicbox.run('gcc_compile', 'chmod 777 test_output_map test_output_vector test_output_stack',
                            limits={'cputime': 2, 'memory': 128},
                            workdir=workdir)
        print(f"Comp: {res}")

        res = epicbox.run('gcc_compile', './compile_all_benchmarks.sh',
                            limits={'cputime': 2, 'memory': 128},
                            workdir=workdir)
        print(f"Comp_b: {res}")


        # return True
        return {
            'vector': run_container(epicbox, workdir, 'vector'),
            'map': run_container(epicbox, workdir, 'map'),
            'stack': run_container(epicbox, workdir, 'stack'),
        }
