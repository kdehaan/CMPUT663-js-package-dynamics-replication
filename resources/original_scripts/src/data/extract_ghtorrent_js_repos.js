/**
 * Finds JavaScript repositories in GHTorrent data.
 *
 * Input: <path-to-ghtorrent-repo-data>
 */

var fs = require('fs')
var byline = require('byline')

function extractJSRepos (inputPath, outputPath) {
  console.log('extract repos from %s', inputPath)

  var repos = []

  var lineCount = 0
  var repoCount = 0
  var noLanguage = 0

  var stream = fs.createReadStream(inputPath)
  stream = byline.createStream(stream, { encoding: 'utf8' })

  stream.on('data', function (line) {
    lineCount++
    if (lineCount % 50000 === 0) console.log(' %s repos checked...', lineCount)

    line = line.replace(/"_id" : ObjectId\( "[^"]*" \),/g, '')

    try {
      var repo = JSON.parse(line)
      if (repo.full_name === 'request/request' || repo.full_name === 'caolan/async' || repo.full_name === 'facebook/react') {
        console.log('       %s %s', repo.full_name, repo.language)
      }
      if (!repo.language) {
        noLanguage++
      } else if (repo.language && repo.language.toLowerCase() === 'javascript') {
        repoCount++
        repos.push({
          full_name: repo.full_name,
          fork: repo.fork
        })
      }
    } catch (err) {
      console.log(err)
    }
  })

  stream.on('finish', function () {
    console.log('done processing %s repos - %s JavaScript repos found - %s have no language', lineCount, repoCount, noLanguage)
    storeRepos(repos, outputPath)
  })
}

function storeRepos (repos, outputPath) {
  fs.writeFile(outputPath, JSON.stringify(repos, null, 2), function (err) {
    if (err) {
      console.log(err)
    } else {
      console.log('repos saved to %s', outputPath)
    }
  })
}

if (!module.parent) {
  if (typeof process.argv[2] === 'undefined' ||
    typeof process.argv[3] === 'undefined') {
    console.log('usage: node %s <path-to-ghtorrent-repo-data> <output-path>', process.argv[1])
  } else {
    extractJSRepos(process.argv[2], process.argv[3])
  }
}
