var moment = require('moment')
require('moment-range')
var graphSnapshot = require('./graph-snapshot')
var async = require('async')
var fs = require('fs')

;(function () {
  function getDateRange (start, end) {
    var results = []
    var startDate = moment(start, 'YYYY-MM-DD')
    var endDate = moment(end, 'YYYY-MM-DD')
    // var range = date.range('month')
    var range = moment.range(startDate, endDate)
    range.by('months', function (moment) {
      results.push(moment.format('YYYY-MM-DD'))
    })
    return results
  }

  if (!module.parent) {
    if (typeof process.argv[2] !== 'undefined' ||
      typeof process.argv[3] !== 'undefined' ||
      typeof process.argv[4] !== 'undefined' ||
      typeof process.argv[5] !== 'undefined') {
      // get params:
      var inputPath = process.argv[2]
      var start = process.argv[3]
      var end = process.argv[4]
      var simple = (process.argv[5] === 'true')

      var range = getDateRange(start, end)
      console.log(range)

      var results = []
      async.eachSeries(range, function (date, callback) {
        var outputPath = '../../data/json-graphs-versioned/' + date + '_npm_graph_versioned.json'
        if (simple) {
          outputPath = '../../data/json-graphs/' + date + '_npm_graph.json'
        }
        graphSnapshot.createSnapshot(inputPath, outputPath, date, simple, function (err, result) {
          if (err) {
            callback(err)
          } else {
            results.push(result)
            callback()
          }
        })
      }, function done () {
        console.log('Finished')
        var outputFile = '../../data/report_' + start + '_' + end + '_versioned.json'
        if (simple) {
          outputFile = '../../data/report_' + start + '_' + end + '.json'
        }
        fs.writeFile(outputFile, JSON.stringify(results, null, 2), function (err) {
          if (err) {
            console.log(err)
          } else {
            console.log('saved results to %s', outputFile)
          }
        })
      })
    } else {
      console.log('usage: node %s <input-path> <start-date> <end-date> <simple?>', process.argv[1])
    }
  }
})()
