var readline = require('readline')
var semver = require('semver')

var rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
})

var processed = 0

rl.on('line', function (line) {
    var data = JSON.parse(line);
    var query = data.vq;
    var candidates = data.vs;

    if (query == "latest") {
        query = "*";
    }

    try {
        var validCandidates = candidates.filter(function (c) {
            return semver.valid(c) != null;
        });

        var maxSatisfying = semver.maxSatisfying(validCandidates, query);
        data["vr"] = maxSatisfying;
    } catch (e) {
        data["vr"] = null;
    }

    delete data.vs;

    console.log(JSON.stringify(data));

    processed += 1;
    if(processed % 1000 == 0) {
        process.stderr.write(".");
    }
})
