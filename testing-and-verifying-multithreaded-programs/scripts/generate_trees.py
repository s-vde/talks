
import ntpath
import os
import sys


def get_nr_executions(statistics_file):
    file = open(statistics_file, 'r')
    lines = file.readlines()
    return int(lines[0].split("\t")[1])


def iterate_with_increasing_bound(mode_exe, program, compiler_options,
                                  max_nr_explorations):
    output_dirs = []
    bound = 0
    previous_nr_executions = 0

    while bound < 2:
        output_dir = os.path.join("generated_trees",
                                  ntpath.basename(program),
                                  "bounded_search",
                                  str(bound))

        explore = "%s --i %s --max %d --o %s --bound %d %s" \
            % (mode_exe, program, max_nr_explorations, output_dir, bound,
               compiler_options)

        if not os.path.exists(output_dir):
            os.system(explore)

        output_dirs.append(output_dir)

        nr_executions = get_nr_executions(os.path.join(output_dir,
                                                       "statistics.txt"))
        if nr_executions <= previous_nr_executions:
            break
        bound = bound + 1
        previous_nr_executions = nr_executions

    return output_dirs


# ------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------

def main(argv):
    sse_src = "./demos/state-space-explorer"
    sse_build = "./build/demos/state-space-explorer"

    search_tree = os.path.join(sse_src, "tools/search_tree.py")

    test_programs = "./build/demos/programs"

    programs = {
                # # filesystem
                # os.path.join(programs, "filesystem.c"):
                # (["inode", "busy", "locki", "lockb", "START"],
                #  "",
                #  ["dpor"]),
                # # dining_philosophers (deadlock)
                # os.path.join(programs, "dining_philosophers.cpp"):
                # (["forks", "nr_meals", "START"],
                #  "--c -std=c++14"),
                # work_stealing_queue
                # os.path.join(programs, "work_stealing_queue.cpp"):
                # (["queue", "START"],
                #  "--opt 3 --c -std=c++14",
                #  ["dpor"]),
                # readers_nonpreemptive
                # "%s/tests/test_programs/benchmarks/readers_nonpreemptive.c" \
                # % sse_src:
                # (["x", "START"],
                #  "",
                #  ["bounded_search"]),
                # background_thread
                os.path.join(test_programs, "background_thread.cpp"):
                (["m"],                         # 0: name_filter
                 "--opt 3 --c -std=c++14",      # 1: command line options
                 ["dpor", "bounded_search"],    # 2: exploration modes
                 10,                            # 3: max nr exploration
                 5)                             # 4: nodesep
               }

    for program, properties in programs.items():
        for mode in properties[2]:
            mode_exe = os.path.join(sse_build, mode)

            print("\n----------------------------------------")
            print("Generating trees for %s using %s"
                  % (ntpath.basename(program), mode))

            if mode == "bounded_search":
                output_dirs = iterate_with_increasing_bound(mode_exe,
                                                            program,
                                                            properties[1],
                                                            properties[3])
            else:
                output_dir = os.path.join("generated_trees",
                                          ntpath.basename(program),
                                          mode)
                explore = "%s --i %s --max %d --o %s %s" % (mode_exe,
                                                            program,
                                                            properties[3],
                                                            output_dir,
                                                            properties[1])

                if not os.path.exists(output_dir):
                    os.system(explore)

                output_dirs = [output_dir]

            for output_dir in output_dirs:
                generate = "python3 %s -i %s -o %s -f \'[%s]\' -s %d" \
                    % (search_tree,
                       output_dir,
                       os.path.join(output_dir, "trees"),
                       ",".join(list(map(lambda variable: "\"%s\"" % variable,
                                     properties[0]))),
                       properties[4])
                print (generate)
                os.system(generate)

# ------------------------------------------------------------------------------

if __name__ == "__main__":
    main(sys.argv[1:])
