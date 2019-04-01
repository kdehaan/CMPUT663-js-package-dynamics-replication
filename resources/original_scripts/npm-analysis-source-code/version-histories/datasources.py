class DataSources:
    # The expected format is a JSON array, where each entry is a record
    # with at least the following field: r["value"]["name"].
    #
    # Expected size is ~300M
    npm_packages = "../data/2015-09-22_npm_skim.json"

    # The expected format is a text file where each line contains a JSON object.
    # Each object is expected to have the following fields:
    #   - obj["name"]
    #   - obj["time"]
    # Expected size is ~2G if full of ~300M if "curated"
    # npm_full = "../data/just_express.txt"
    npm_full = "../data/2015-09-22_npm_repos_curated.txt"

    # The expected format is a directory containing many JSON files.
    project_history_dir = "../github-projects/histories"
