/**
 * Loads complete set on npm metadata in two steps:
 * 1.) Get npm skim
 * 2.) Get package-specific metadata for every package contained in the skim
 *
 * No further input required.
 */

var fs = require('fs')
var JSONStream = require('JSONStream')
var Transform = require('stream').Transform
var request = require('request')
var async = require('async')
var moment = require('moment')

// kick things off:
//loadRepoList()

fs.readFile('../../data/missing_names_skim.json', 'utf8', function(err, data) {
  if (err) throw err; // we'll not consider error handling for now
  var missingRepoList = JSON.parse(data)
  loadData(missingRepoList)
});


// config:
var concurrency = 25

function loadRepoList () {
  var readCount = 0
  var repoList = []

  // set up streams:
  var parser = JSONStream.parse('rows.*')
  var extractor = new Transform({objectMode: true})
  extractor._transform = function (dataObj, encoding, done) {
    readCount++
    if (readCount % 10000 === 0) console.log('%s repositories assessed...', readCount)

    repoList.push(dataObj.id)

    this.push(dataObj)
    done()
  }
  var stringifyer = JSONStream.stringify('[\n', '\n,\n', '\n]\n', '\t')
  var outputPath = '../../data/' + moment().format('YYYY-MM-DD') + '_npm_skim.json'
  var wstream = fs.createWriteStream(outputPath, {encoding: 'utf8'})

  // start streams:
  request
    .get('https://skimdb.npmjs.com/registry/_design/scratch/_view/byField')
    .pipe(parser)
    .pipe(extractor)
    .pipe(stringifyer)
    .pipe(wstream)
    .on('error', function (err) {
      console.log('Error: ' + err)
    })
    .on('finish', function () {
      console.log('loaded list of %s repositories; will consider %s in the following', readCount, repoList.length)
      console.log('written results to "%s"', outputPath)
      loadData(repoList)
    })
}

function loadData (repoList) {
  var loadCount = 0
  var successCount = 0
  var errorCount = 0
  var outputPath = '../../data/' + moment().format('YYYY-MM-DD') + '_npm_repos.txt'

  async.eachLimit(repoList, concurrency, function (id, callback) {
    if (loadCount % 1000 === 0) console.log('%s loaded...', loadCount)
    request({
      method: 'GET',
      uri: 'https://registry.npmjs.org/' + id.id,
      json: true
    }, function (err, res, body) {
      loadCount++
      if (err || res.statusCode !== 200) {
        errorCount++
        // console.log('%s ERROR LOADING %s', loadCount, id)
        callback()
      } else {
        fs.appendFile(outputPath, JSON.stringify(body) + '\n', function (err) {
          if (err) {
            // console.log('%s ERROR WRITING %s', loadCount, id)
          } else {
            successCount++
            // console.log('%s SUCCESS %s', loadCount, id)
          }
          callback()
        })
      }
    })
  }, function (err) {
    if (err) {
      console.log(err)
    } else {
      console.log('loaded %s repositories (%s successes and %s errors)',
        loadCount, successCount, errorCount)
      console.log('written results to "%s', outputPath)
    }
  })
}
