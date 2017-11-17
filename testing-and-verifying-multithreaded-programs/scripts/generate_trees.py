
import ntpath
import os
import sys


def get_nr_executions(statistics_file):
    file = open(statistics_file, 'r')
    lines = file.readlines()
    return int(lines[0].split("\t")[1])


def iterate_with_increasing_bound(mode_exe, program, compiler_options,
                                  max_bound, max_nr_explorations):
    output_dirs = []
    bound = 0
    previous_nr_executions = 0

    while bound <= max_bound:
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


def run_with_bounds(mode_exe, program, compiler_options, bounds,
                    max_nr_explorations, argv):
    output_dirs = []

    for bound in bounds:
        output_dir = os.path.join("generated_trees",
                                  ntpath.basename(program),
                                  "bounded_search",
                                  str(bound[0]))

        explore = "%s --i %s --max %d --o %s --bound %d %s" \
            % (mode_exe, program, max_nr_explorations, output_dir, bound[0],
               compiler_options)

        if not os.path.exists(output_dir) or argv[0] == "--force-explore":
            os.system(explore)

        output_dirs.append(output_dir)

    return output_dirs


# ------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------


def main(argv):
    sse_src = "./demos/state-space-explorer"
    sse_build = "./build/demos/state-space-explorer"

    search_tree = os.path.join(sse_src, "tools/search_tree.py")

    test_programs = "./examples"

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
                # ----- DOESN'T WORK WITH --opt 3
                # os.path.join(test_programs, "readers_nonpreemptive.c"):
                # (["x"],                         # 0: name_filter
                #  "--opt 0",                     # 1: command line options
                #  ["dpor", "bounded_search"],    # 2: exploration modes
                #  [0],                           # 3: bounds
                #  1000,                          # 4: max nr explorations
                #  "true",                        # 5: generate animation
                #  10),                           # 6: nodesep
                # ----- DOESN'T WORK WITH --opt 3
                # os.path.join(test_programs, "filesystem.c"):
                # (["inode", "busy", "locki", "lockb"],   # 0: name_filter
                #  "--opt 3",                     # 1: command line options
                #  ["dpor", "bounded_search"],    # 2: exploration modes
                #  [0],                           # 3: bounds
                #  1000,                          # 4: max nr explorations
                #  "true",                        # 5: generate animation
                #  10),                           # 6: nodesep
                # -----
                # NOTE: Just to generate the instrumented.txt
                # os.path.join(test_programs, "data_race_fixed_pthread.cpp"):
                # # 0: name_filter
                # (["x", "value", "mutex"],
                #  # 1: command line options
                #  "--opt 3 --c -std=c++14",
                #  # 2: exploration modes
                #  ["depth_first_search", "bounded_search"],
                #  # 3: bounds
                #  [(0, "Until:2")],
                #  # 4: max nr explorations
                #  1,
                #  # 5: nodesep
                #  10),
                # -----
                # NOTE: Just to generate the instrumented.txt
                # os.path.join(test_programs, "data_race.cpp"):
                # # 0: name_filter
                # ([],
                #  # 1: command line options
                #  "--opt 3 --c -std=c++14",
                #  # 2: exploration modes
                #  ["depth_first_search"],
                #  # 3: bounds
                #  [],
                #  # 4: max nr explorations
                #  1000,
                #  # 5: nodesep
                #  10),
                # # -----
                # # NOTE: Just to generate full_schedules.png
                # os.path.join(test_programs, "deadlock_pthread.cpp"):
                # # 0: name_filter
                # ([],
                #  # 1: command line options
                #  "--opt 3 --c -std=c++14",
                #  # 2: exploration modes
                #  ["dpor"],
                #  # 3: bounds
                #  [],
                #  # 4: max nr explorations
                #  1,
                #  # 5: nodesep
                #  10),
                # # -----
                # os.path.join(test_programs, "background_thread.cpp"):
                # # 0: name_filter
                # (["m"],
                #  # 1: command line options
                #  "--opt 3 --c -std=c++14",
                #  # 2: exploration modes
                #  ["dpor", "bounded_search"],
                #  # 3: bounds
                #  [(0, "True"), (1, "False"), (2, "False")],
                #  # 4: max nr explorations
                #  1000,
                #  # 5: nodesep
                #  10),
                # -----
                # os.path.join(test_programs, "bank_account.cpp"):
                # # 0: name_filter
                # (["from", "to"],
                #  # 1: command line options
                #  "--opt 3 --c -std=c++14",
                #  # 2: exploration modes
                #  ["dpor", "bounded_search", "depth_first_search"],
                #  # 3: bounds
                #  [(0, "True"), (1, "Until:3")],
                #  # 4: max nr explorations
                #  1000,
                #  # 5: nodesep
                #  10)
                # -----
                # NOTE: This is used in the presentation: there are 4 executions, 
                # but the last one should not be there
                # os.path.join(test_programs, "background_thread.cpp"):
                # # 0: name_filter
                # (["m"],
                #  # 1: command line options
                #  "--opt 3 --c -std=c++14",
                #  # 2: exploration modes
                #  ["dpor"],
                #  # 3: bounds
                #  [],
                #  # 4: max nr explorations
                #  3,
                #  # 5: nodesep
                #  10),
                # -----
                # # NOTE: To be generated with penwidth=8 and ranksep=3
                # os.path.join(test_programs, "background_thread.cpp"):
                # # 0: name_filter
                # (["m"],
                #  # 1: command line options
                #  "--opt 3 --c -std=c++14",
                #  # 2: exploration modes
                #  ["depth_first_search"],
                #  # 3: bounds
                #  [],
                #  # 4: max nr explorations
                #  1000,
                #  # 5: nodesep
                #  10)
                # NOTE: To be generated with penwidth=8 and ranksep=3
                os.path.join(test_programs, "lock_free_queue_datarace.cpp"):
                # 0: name_filter
                (["this"],
                 # 1: command line options
                 "--opt 1 --c -std=c++14",
                 # 2: exploration modes
                 ["dpor"],
                 # 3: bounds
                 [],
                 # 4: max nr explorations
                 10,
                 # 5: nodesep
                 10),
                # NOTE: To be generated with penwidth=8 and ranksep=3
                # os.path.join(test_programs, "lock_free_queue_two_steals.cpp"):
                # # 0: name_filter
                # (["this"],
                #  # 1: command line options
                #  "--opt 1 --c -std=c++14",
                #  # 2: exploration modes
                #  ["dpor"],
                #  # 3: bounds
                #  [],
                #  # 4: max nr explorations
                #  10,
                #  # 5: nodesep
                #  10)
               }

    for program, properties in programs.items():
        for mode in properties[2]:
            mode_exe = os.path.join(sse_build, mode)

            print("\n----------------------------------------")
            print("Generating trees for %s using %s"
                  % (ntpath.basename(program), mode))

            if mode == "bounded_search":
                print (properties[3])
                output_dirs = run_with_bounds(mode_exe,
                                              program,
                                              properties[1],
                                              properties[3],
                                              properties[4],
                                              argv)
            else:
                output_dir = os.path.join("generated_trees",
                                          ntpath.basename(program),
                                          mode)
                explore = "%s --i %s --max %d --o %s %s" % (mode_exe,
                                                            program,
                                                            properties[4],
                                                            output_dir,
                                                            properties[1])

                if not os.path.exists(output_dir) or argv[0] == "--force-explore":
                    os.system(explore)

                output_dirs = [output_dir]

            for index in range(0, len(output_dirs)):
                output_dir = output_dirs[index]
                trees_dir = os.path.join(output_dir, "trees")

                if not os.path.exists(trees_dir) or argv[0] == "--force-generate":

                    # determine whether to generate animations
                    generate_animation = "True"

                    if mode == "depth_first_search":
                        # generate_animation = "Until:5"
                        generate_animation = "False"

                    if mode == "bounded_search":
                        generate_animation = properties[3][index][1]

                    generate = \
                        "python3 %s -i %s -o %s -f \'[%s]\' -a %s -s %d" \
                        % (search_tree,
                           output_dir,
                           trees_dir,
                           ",".join(list(map(lambda variable:
                                             "\"%s\"" % variable,
                                         properties[0]))),
                           generate_animation,
                           properties[5])
                    os.system(generate)

# ------------------------------------------------------------------------------

if __name__ == "__main__":
    main(sys.argv[1:])
