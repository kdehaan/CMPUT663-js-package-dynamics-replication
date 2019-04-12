import sys
import codecs
import re
import requests

REPO_LIST = sys.argv[1]


with open(REPO_LIST) as repo_file:
    with open("404s.txt", "a") as fourofours:
        with open("200s.txt", "a") as twohundreds:
            ln = 0

            for line in repo_file:
                ln = ln + 1
                m = re.match("""^([^/]*)/([^/]*)$""", line.strip())

                if m is None:
                    sys.stderr.write("Cannot parse line %d: %s\n" % (ln, line.strip()))
                else:
                    gh_user = m.group(1)
                    gh_repo = m.group(2)

                    print (gh_user, gh_repo)

                    url = "https://raw.githubusercontent.com/%s/%s/master/package.json" % (gh_user, gh_repo)

                    r = requests.get(url)

                    if r.status_code == 200:
                        twohundreds.write("%s/%s\n" % (gh_user, gh_repo))
                        of = codecs.open("./package-files/%s--%s--package.json" % (gh_user, gh_repo), "w", "utf-8")
                        of.write(r.text)
                        of.close()
                    elif r.status_code == 404:
                        fourofours.write("%s/%s\n" % (gh_user, gh_repo))
                    else:
                        sys.stderr.write("Unexpected response code: %d.\n" % r.status_code)
                         
