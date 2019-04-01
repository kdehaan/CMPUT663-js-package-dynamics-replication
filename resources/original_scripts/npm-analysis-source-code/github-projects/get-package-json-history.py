import datetime
import dateutil.parser
import json
import shutil
import subprocess
import sys
import tempfile

def clone_from_github(group_id, repo_id):
    clone_dir = tempfile.mkdtemp(prefix="github-clone-%s-%s-" % (group_id, repo_id))
    github_url = "https://github.com/%s/%s.git" % (group_id, repo_id)
    subprocess.call([ 'git', 'clone', github_url, clone_dir ])
    return clone_dir

def commits_for_path(clone_dir, path):
    # How to get the list of commits where a file is changed:
    # git -C REPO --no-pager log --pretty=oneline -- PATH | cut -d ' ' -f 1
    git_log = subprocess.Popen([
        'git', '-C', clone_dir, '--no-pager', 'log', '--pretty=oneline', '--', path
    ], stdout=subprocess.PIPE)

    for line in git_log.stdout:
        # SHA1 hashes are 40 chars
        commit_hash = line[:40]
        yield commit_hash

def commit_date(clone_dir, commit):
    # How to get the commit date:
    # git -C REPO --no-pager log -1 --pretty=tformat:%ci HASH
    git_log = subprocess.Popen([
        'git', '-C', clone_dir, '--no-pager', 'log', '-1', '--pretty=tformat:%ci', commit
    ], stdout=subprocess.PIPE)

    for line in git_log.stdout:
        # there should be only one...
        date = dateutil.parser.parse(line.strip())

    return date

def json_contents_for_commit(clone_dir, path, commit):
    git_show = subprocess.Popen([
        'git', '-C', clone_dir, '--no-pager', 'show', "%s:%s" % (commit, path)
    ], stdout=subprocess.PIPE)

    try:
        return json.load(git_show.stdout)
    except:
        sys.stderr.write("Failed to read JSON contents of file: %s at commit %s.\n" % (path, commit))
        return None

if __name__ == "__main__":
    if len(sys.argv) == 2:
        GIT_USER = "local"
        GIT_REPO = sys.argv[1]
        REPO = sys.argv[1]
        delete_on_exit = False
    elif len(sys.argv) == 3:
        GIT_USER = sys.argv[1]
        GIT_REPO = sys.argv[2]
        REPO = clone_from_github(GIT_USER, GIT_REPO)
        delete_on_exit = True
    else:
        print "Usage: %s github_user repo" % sys.argv[0]
        print ""
        print "   ex: %s strongloop express" % sys.argv[0]
        print ""
        print "If you have already checked out a repo, just run:"
        print "  %s repo_dir" % sys.argv[0]
        print "...but make sure the meta-data is correct afterwards."
        sys.exit(1)
    
    PATH = "package.json"

    commits = {}
    history = {}
    json_errors = []

    for commit in commits_for_path(REPO, PATH):
        when = commit_date(REPO, commit)
        date = str(when.isoformat())
    
        obj = json_contents_for_commit(REPO, PATH, commit)

        if obj is not None:
            commits[commit] = date
            history[commit] = obj
        else:
            json_errors.append(commit)

    full = {
        "_id" : "github:%s:%s" % (GIT_USER, GIT_REPO),
        "creation_time" : str(datetime.datetime.now().isoformat()),
        "time" : commits,
        "versions" : history,
        "json_errors" : json_errors,
        "repository" : {
            "type" : "git",
            "url" : "https://github.com/%s/%s.git" % (GIT_USER, GIT_REPO)
        }
    }

    output_file = "%s-%s.json" % (GIT_USER, GIT_REPO)

    json.dump(full, open(output_file, "w"), indent=2)

    print "Found %d version(s) of package.json." % len(full["versions"])

    if delete_on_exit:
        print "Deleting temp directory %s..." % REPO
        shutil.rmtree(REPO, ignore_errors=True)

    print "Output written to %s." % output_file
