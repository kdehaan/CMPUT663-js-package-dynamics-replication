/**
 * Loads npm download data per package in two steps:
 * 1.) Get npm skim
 * 2.) Get, per package found in the skim, the package download metadata
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
loadRepoList()

// config:
var concurrency = 40

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
  var outputPath = '../../data/' + moment().format('YYYY-MM-DD') + '_npm_downloads-2010_01_01-2015_10_31.txt'

  async.eachLimit(repoList, concurrency, function (id, callback) {
    if (loadCount % 1000 === 0) console.log('%s loaded...', loadCount)
    request({
      method: 'GET',
      uri: 'https://api.npmjs.org/downloads/range/2010-01-01:2015-10-31/' + id,
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
