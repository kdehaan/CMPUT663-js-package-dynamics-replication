/**
 * Script that reads version queries and candidates in JSON from standard input
 * and produces the best version for the query as output.
 *
 * Input looks like this (one JSON object per line):
 * { "vq" : "~0.8.0", "vs" : [ "0.0.1", "0.1.1", "0.8.0", "0.8.1" ] }
 *
 * Output looks like this (one string per line):
 * 0.8.1
 *
 * Note: requires 'semver' package, as specified in the package.json (use 'npm install')
 */
var readline = require('readline')
var semver = require('semver')

var rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
})

rl.on('line', function (line) {
  var data = JSON.parse(line)
  var query = data.vq
  var candidates = data.vs

  var maxSatisfying = semver.maxSatisfying(candidates, query)

  // console.log('Query=%s, Candidates=%s, maxSatisfying=%s', query, candidates.join(', '), maxSatisfying)
  console.log(maxSatisfying)
})
