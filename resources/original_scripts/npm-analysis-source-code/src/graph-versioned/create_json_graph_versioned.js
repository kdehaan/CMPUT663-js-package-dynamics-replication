var fs = require('fs')
var byline = require('byline')
var moment = require('moment')
var semver = require('semver')

var inputData

;(function () {
  function createSnapshot (inputPath, outputPath, dateString, simple, callback) {
    console.log('create snapshot from %s at date %s. simple: %s', inputPath, dateString, simple)

    var date = moment(dateString, 'YYYY-MM-DD')
    var graph = {}

    var lineCount = 0
    var nodeCount = 0
    var start = new Date().getTime()

    if (!inputData) {
      console.log('read input data from file...')
      var stream = fs.createReadStream(inputPath)
      stream = byline.createStream(stream)
      inputData = []

      stream.on('data', function (line) {
        lineCount++
        if (lineCount % 10000 === 0) console.log('%s lines...', lineCount)
        try {
          inputData.push(line)
          var repo = JSON.parse(line)
          var oldVersions
          if (simple) {
            oldVersions = getOldVersionsSimple(repo, date)
          } else {
            oldVersions = getOldVersions(repo, date)
          }
          if (oldVersions) {
            nodeCount++
            graph[repo.name] = oldVersions
          }
        } catch (err) {
          console.log(err)
        }
      })

      stream.on('finish', function () {
        var end = new Date().getTime()
        var time = (end - start) / 1000
        console.log('created %s nodes from %s lines', nodeCount, lineCount)
        console.log(' - %s seconds to create nodes', time)
        concretizeDependencies(graph, outputPath, date, simple, callback)
      })
    } else {
      console.log('use input data from memory...')
      for (var i = inputData.length - 1; i >= 0; i--) {
        lineCount++
        if (lineCount % 10000 === 0) console.log('%s lines...', lineCount)
        var repo = JSON.parse(inputData[i])
        var oldVersions
        if (simple) {
          oldVersions = getOldVersionsSimple(repo, date)
        } else {
          oldVersions = getOldVersions(repo, date)
        }
        if (oldVersions) {
          nodeCount++
          graph[repo.name] = oldVersions
        }
      }
      var end = new Date().getTime()
      var time = (end - start) / 1000
      console.log('created %s nodes from %s lines', nodeCount, lineCount)
      console.log(' - %s seconds to create nodes', time)
      concretizeDependencies(graph, outputPath, date, simple, callback)
    }
  }

  function concretizeDependencies (graph, outputPath, date, simple, callback) {
    var start = new Date().getTime()
    var nodeCount = 0
    var edgeCount = 0
    var errorCount = 0

    for (var repoKey in graph) {
      // output progress:
      nodeCount++
      if (nodeCount % 1000 === 0) console.log('%s edges for %s nodes...', edgeCount, nodeCount)

      var repo = graph[repoKey]
      for (var repoVersionKey in repo) {
        var dependencies = repo[repoVersionKey].dependencies // object: key = dependent repository, value = version string
        if (isNonEmptyObject(dependencies)) {
          for (var depKey in dependencies) {
            if (isNonEmptyObject(graph[depKey])) { // check if there is an entry for the repo in the graph
              // in the simple case, just put dependency to fake version 1:
              if (simple) {
                edgeCount++
                dependencies[depKey] = 1
                continue
              }

              var depReq = dependencies[depKey]
              var candidates = Object.keys(graph[depKey])
              var concreteReq = getConcreteVersion(depKey, depReq, candidates)
              // console.log(' "%s" (%s) requires "%s" (%s). Candidates: [%s] => %s',
              //   repoKey, repoVersionKey, depKey, depReq, candidates, concreteReq)
              if (concreteReq) {
                // console.log(' resolved dependency %s %s to %s', depKey, depReq, concreteReq)
                edgeCount++
                dependencies[depKey] = concreteReq
              } else {
                // console.log(' could not resolve dependency %s %s', depKey, depReq)
                delete dependencies[depKey]
                errorCount++
              }
            } else {
              // console.log(' "%s" is not contained in the graph', depKey)
              delete dependencies[depKey]
              errorCount++
            }
          }
        }

        var devDependencies = repo[repoVersionKey].devDependencies // object: key = dependent repository, value = version string
        if (isNonEmptyObject(devDependencies)) {
          for (var devDepKey in devDependencies) {
            if (isNonEmptyObject(graph[devDepKey])) { // check if there is an entry for the repo in the graph
              // in the simple case, just put dependency to fake version 1:
              if (simple) {
                edgeCount++
                devDependencies[devDepKey] = 1
                continue
              }

              var devDepReq = devDependencies[devDepKey]
              var devCandidates = Object.keys(graph[devDepKey])
              var concreteDevReq = getConcreteVersion(devDepKey, devDepReq, devCandidates)
              // console.log(' "%s" (%s) dev-requires "%s" (%s). Candidates: [%s] => %s',
              //   repoKey, repoVersionKey, devDepKey, devDepReq, devCandidates, concreteDevReq)
              if (concreteDevReq) {
                // console.log(' resolved devDependency %s %s to %s', devDepKey, devDepReq, concreteDevReq)
                edgeCount++
                devDependencies[devDepKey] = concreteDevReq
              } else {
                // console.log(' could not resolve devDependency %s %s', devDepKey, devDepReq)
                delete devDependencies[devDepKey]
                errorCount++
              }
            } else {
              // console.log(' "%s" is not contained in the graph', devDepKey)
              delete devDependencies[devDepKey]
              errorCount++
            }
          }
        }
      }
    }
    var end = new Date().getTime()
    var time = (end - start) / 1000
    console.log('created graph with %s nodes and %s edges', nodeCount, edgeCount)
    console.log(' - %s dependencies could not be resolved (%s percent)', errorCount, (100 * errorCount / (errorCount + edgeCount)))
    console.log(' - %s seconds to concretize dependencies', time)

    var results = {
      date: date.format('YYYY-MM-DD'),
      num_repositories: nodeCount,
      num_resolved_dependencies: edgeCount,
      num_unresolved_dependencies: errorCount
    }

    storeGraph(graph, outputPath, results, callback)
  }

  function isNonEmptyObject (cand) {
    return cand !== null &&
      typeof cand !== 'undefined' &&
      typeof cand === 'object' &&
      Object.keys(cand).length > 0
  }

  var seenVersions = {}
  function getConcreteVersion (devKey, depReq, candidates) {
    devKey = devKey.replace(' ', '')
    var seenKey = devKey + '_' + depReq
    if (seenVersions.hasOwnProperty(seenKey)) {
      return seenVersions[seenKey]
    } else {
      var concreteReq = semver.maxSatisfying(candidates, depReq)
      if (concreteReq) {
        seenVersions[seenKey] = concreteReq
        return concreteReq
      } else {
        return null
      }
    }
  }

  function storeGraph (graph, outputPath, results, callback) {
    fs.writeFile(outputPath, JSON.stringify(graph, null, 2), function (err) {
      if (err) {
        console.log(err)
        return callback(err)
      }
      console.log('graph saved to "%s"', outputPath)
      callback(null, results)
    })
  }

  function getOldVersions (repo, inputDate) {
    var oldVersions = {}

    // check for availability of 'time' data:
    if (typeof repo.time === 'undefined') {
      return null
    }

    // check for availability of 'versions' data:
    if (typeof repo.versions === 'undefined') {
      return null
    }

    var createdDate = moment(repo.time.created)

    // eliminate repositories that are too now:
    if (inputDate.diff(createdDate) < 0) {
      // console.log('%s was created AFTER the input date...', repo.name)
      return null
    }

    for (var version in repo.time) {
      if (typeof repo.versions[version] === 'undefined') {
        continue
      }
      if (version === 'created' || version === 'modified') {
        continue
      }
      var versionDate = moment(repo.time[version])

      // store version, if its old enough:
      if (inputDate.diff(versionDate) > 0) {
        oldVersions[version] = {
          dependencies: repo.versions[version].dependencies,
          devDependencies: repo.versions[version].devDependencies
        }
      }
    }
    return oldVersions
  }

  /**
   * returns the latest version available at inputDate. Every version is made '1'.
   * @param  {Object} repo      Object representation of repository
   * @param  {String} inputDate The date until which versions are considered
   * @return {Object}           The latest version of the repository at the input date
   */
  function getOldVersionsSimple (repo, inputDate) {
    var oldVersions = {}

    // check for availability of 'time' data:
    if (typeof repo.time === 'undefined') {
      return null
    }

    // check for availability of 'versions' data:
    if (typeof repo.versions === 'undefined') {
      return null
    }

    var createdDate = moment(repo.time.created)

    // eliminate too new repositories:
    if (inputDate.diff(createdDate) < 0) {
      // console.log('%s was created AFTER the input date...', repo.name)
      return null
    }

    // collect all versions available until inputDate:
    var versions = []
    for (var version in repo.time) {
      if (typeof repo.versions[version] === 'undefined') {
        continue
      }
      if (version === 'created' || version === 'modified') {
        continue
      }
      var versionDate = moment(repo.time[version])

      // store version, if its old enough:
      if (inputDate.diff(versionDate) > 0) {
        versions.push(version)
      }
    }
    if (versions.length === 0) {
      return null
    }

    // determine which of these versions is the latest:
    var latestVersion = '0.0.0'
    for (var key in versions) {
      if (semver.gte(versions[key], latestVersion)) {
        latestVersion = versions[key]
      }
    }
    // console.log('latest version for %s is: %s', repo.name, latestVersion)

    if (typeof repo.versions[latestVersion] === 'undefined') {
      return null
    }

    // return the latest version as version '1':
    oldVersions[1] = {
      dependencies: repo.versions[latestVersion].dependencies,
      devDependencies: repo.versions[latestVersion].devDependencies
    }
    return oldVersions
  }

  // define exports:
  exports.createSnapshot = createSnapshot

  if (!module.parent) {
    // user input:
    //
    //        node graph-snapshot.js <path-to-data> <date>
    //
    if (typeof process.argv[2] === 'undefined' ||
      typeof process.argv[3] === 'undefined' ||
      typeof process.argv[4] === 'undefined') {
      console.log('usage: node %s <path-to-data> <date> <simple?>', process.argv[1])
    } else {
      var date = process.argv[3]
      var simple = (process.argv[4] === 'true')
      if (!moment(date).isValid()) {
        console.log('invalid date %s', date)
      } else {
        var inputPath = process.argv[2]
        var outputPath = '../../data/json-graphs-versioned/' + date + '_npm_graph_versioned.json'
        if (simple) {
          outputPath = '../../data/json-graphs/' + date + '_npm_graph.json'
        }
        createSnapshot(inputPath, outputPath, date, simple, function (err, data) {
          if (err) {
            console.log(err)
          }
          console.log('done.')
        })
        // getGraphSnapshot(inputPath, outputPath, date)
      }
    }
  }
})()
