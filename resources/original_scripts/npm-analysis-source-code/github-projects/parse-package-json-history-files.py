import json
import glob
import sys
import itertools

from collections import Counter

directory = sys.argv[1]

tot_repos = 0
tot_vers  = 0
tot_malf  = 0

tot_declared_deps = 0
tot_declared_dev_deps = 0

tot_errors = 0

dependency_counter = Counter({})
dev_dependency_counter = Counter({})

for path in glob.glob("%s/*.json" % directory):
    with open(path) as history_file:
        tot_repos += 1
        try:
            data = json.load(history_file)

            num_versions = len(data["time"])
            num_errors   = len(data["json_errors"])

            tot_vers += num_versions
            tot_malf += num_errors

            times = data["time"]

            local_deps = {}
            local_dev_deps = {}

            package_files = data["versions"].values()

            dependency_blocks = filter(lambda d : isinstance(d, dict),
                map(lambda p : p.get("dependencies", {}),
                    package_files))

            dev_dependency_blocks = filter(lambda d : isinstance(d, dict),
                map(lambda p : p.get("devDependencies", {}),
                    package_files))

            dependency_lists = map(lambda d : d.keys(), dependency_blocks)
            dev_dependency_lists = map(lambda d : d.keys(), dev_dependency_blocks)

            all_dependencies = set(itertools.chain.from_iterable(dependency_lists))
            all_dev_dependencies = set(itertools.chain.from_iterable(dev_dependency_lists))

            dependency_counter += Counter(all_dependencies)
            dev_dependency_counter += Counter(all_dev_dependencies)

            tot_declared_deps += len(all_dependencies)
            tot_declared_dev_deps += len(all_dev_dependencies)

        except Exception as e:
            print e 
            tot_errors += 1

valid_reps = float(tot_repos - tot_errors)

print "# of repositories    : %d" % tot_repos
print "Processing errors    : %d" % tot_errors
print "Avg. # of versions   : %f" % (float(tot_vers) / valid_reps)
print "Avg. # of json errors: %f" % (float(tot_malf) / valid_reps)
print "Avg. # deps.         : %f" % (float(tot_declared_deps) / valid_reps)
print "Avg. # devDeps.      : %f" % (float(tot_declared_dev_deps) / valid_reps)
print "Total distinct deps. : %d" % len(dependency_counter)
print "Total dist. devDeps. : %d" % len(dev_dependency_counter)

print "Top dependencies:"
for p, c in dependency_counter.most_common(10):
    print "  %7d %s" % (c, p)

print "Top devDependencies:"
for p, c in dev_dependency_counter.most_common(10):
    print "  %7d %s" % (c, p)

with open("dependencies.txt", 'w') as deps_file:
    for p, c in dependency_counter.most_common(1000000000):
        deps_file.write("  %7d %s\n" % (c, p))

with open("devDependencies.txt", 'w') as dev_deps_file:
    for p, c in dev_dependency_counter.most_common(1000000000):
        dev_deps_file.write("  %7d %s\n" % (c, p))
    

