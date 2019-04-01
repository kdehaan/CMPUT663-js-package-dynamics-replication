/**
 * Script to extract the creation dates of versions.
 * Produces data in the form:
 * [
 *   {
 *     name: 'rep_name',
 *     verisons: {
 *       'created': '2011-01-02:...',
 *       '0.0.1': '2012-01-02:...',
 *     }
 *   }
 * ]
 *
 * Input is "npm_repos-09_22-15.txt" (Who named that file???)
 */

var fs = require('fs')
var byline = require('byline')

;(function () {
  function extractVersionDates (inputPath) {
    var results = []

    var stream = fs.createReadStream(inputPath)
    stream = byline.createStream(stream)

    stream.on('data', function (line) {
      try {
        var repo = JSON.parse(line)
        var result = getVersionDate(repo)
        // console.log(JSON.stringify(result, null, 2))
        results.push(result)
      } catch (err) {
        console.log(err)
      }
    })

    stream.on('finish', function () {
      console.log(JSON.stringify(results, null, 2))
    })
  }

  function getVersionDate (repo) {
    var result = {}
    result.name = repo.name
    // result.versions = repo.versions
    result.time = repo.time
    return result
  }

  if (!module.parent) {
    // user input:
    //
    //        node graph-snapshot.js <path-to-data> <date>
    //
    if (typeof process.argv[2] === 'undefined') {
      console.log('usage: node %s <path-to-data>', process.argv[1])
    } else {
      var inputPath = process.argv[2]
      extractVersionDates(inputPath)
    }
  }
})()
