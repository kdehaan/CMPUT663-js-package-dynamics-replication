
/**
 * Creates a JSON graph from input data, in which every line
 * is a stringified JSON object describing an npm package,
 * as available at http://registry.npmjs.org/<name>
 */

var fs = require('fs')
var byline = require('byline')
var moment = require('moment')
var semver = require('semver')

;(function () {
  function createSnapshotFromSingleFile (inputPath, outputPath, callback) {
    console.log('create FULL snapshot from file %s.', inputPath)

    var graph = {}

    var lineCount = 0
    var numNodes = 0
    var numDeps = 0
    var numLostDeps = 0
    var numReDeps = 0
    var start = new Date().getTime()

    console.log('read input data from file...')
    var stream = fs.createReadStream(inputPath)
    stream = byline.createStream(stream)

    stream.on('data', function (line) {
      lineCount++
      if (lineCount % 10000 === 0) console.log('%s lines...', lineCount)
      var repo = JSON.parse(line)
      var formattedVersions = getFormattedVersions(repo, 1500000000000, true)
      if (formattedVersions) {
        numNodes++
        graph[repo.name] = formattedVersions.deps
        numDeps += formattedVersions.numDeps
        numLostDeps += formattedVersions.numLostDeps
        numReDeps += formattedVersions.numReDeps
      }
    })

    stream.on('finish', function () {
      var end = new Date().getTime()
      var time = (end - start) / 1000
      console.log('Created graph from %s lines', lineCount)
      console.log(' - %s nodes', numNodes)
      console.log(' - %s edges (%s lost deps, %s recreated deps)', numDeps, numLostDeps, numReDeps)
      console.log(' - %s seconds to create nodes', time)
      var results = {
        numNodes: numNodes,
        numDeps: numDeps,
        numLostDeps: numLostDeps,
        numReDeps: numReDeps
      }
      storeGraph(graph, outputPath, results, callback)
    })
  }

  function createSnapshotFromMultipleFiles (inputPath, outputPath, callback) {
    console.log('create FULL snapshot from folder %s.', inputPath)

    // remove possibly existing file:
    try {
      if (fs.existsSync(outputPath)) {
        fs.unlinkSync(outputPath)
        console.log('removed file %s', outputPath)
      } else {
        console.log('file %s does not exist yet', outputPath)
      }
    } catch (e) {
      console.log('file %s does not yet exist...', outputPath)
    }

    var lineCount = 0
    var numNodes = 0
    var numFailedNodes = 0
    var numDeps = 0
    var numLostDeps = 0
    var numReDeps = 0
    var start = new Date().getTime()

    fs.appendFileSync(outputPath, '{')

    var fileList = fs.readdirSync(inputPath)
    console.log('process %s repos', fileList.length)
    var repo
    for (var i in fileList) {
      repo = JSON.parse(fs.readFileSync(inputPath + fileList[i]))
      if (typeof repo.name === 'undefined' && typeof repo._id !== 'undefined') {
        repo.name = repo._id
      }
      var formattedVersions = getFormattedVersions(repo, 1500000000000, false)
      if (formattedVersions) {
        var prefix = '"' + repo.name + '": '
        if (numNodes > 0) {
          prefix = ', ' + prefix
        }
        prefix = '\n' + prefix
        fs.appendFileSync(outputPath, prefix + JSON.stringify(formattedVersions.deps))

        numDeps += formattedVersions.numDeps
        numLostDeps += formattedVersions.numLostDeps
        numReDeps += formattedVersions.numReDeps

        numNodes++
      } else {
        console.log('formattedVersions of %s are: %s', repo.name, formattedVersions)
        numFailedNodes++
      }
      lineCount++
      if (lineCount % 10000 === 0) console.log('%s lines...', lineCount)
    }

    fs.appendFileSync(outputPath, '\n}')

    var end = new Date().getTime()
    var time = (end - start) / 1000
    console.log('Created graph from %s lines', lineCount)
    console.log(' - %s nodes (%s failed)', numNodes, numFailedNodes)
    console.log(' - %s edges (%s lost deps, %s recreated deps)', numDeps, numLostDeps, numReDeps)
    console.log(' - %s seconds to create nodes', time)
    var results = {
      numNodes: numNodes,
      numDeps: numDeps,
      numLostDeps: numLostDeps,
      numReDeps: numReDeps
    }
    callback(results)
    // storeGraph(graph, outputPath, results, callback)
  }

  function getFormattedVersions (repo, closeDate, doFilter) {
    // console.log('')

    // check for availability of 'time' data:
    if (typeof repo.time === 'undefined') {
      console.log('%s has not "time" property', repo.name)
      return null
    }

    // check for availability of 'versions' data:
    if (typeof repo.versions === 'undefined') {
      console.log('%s has not "versions" property', repo.name)
      return null
    }

    var depDict = {}
    depDict.deps = {}
    var creationDate = 0

    var numDeps = 0
    var numLostDeps = 0
    var numReDeps = 0

    // 1st order of business: sort versions by time.
    var sortedVersions = []
    for (var v in repo.time) {
      if (v === 'created') {
        creationDate = moment(repo.time[v]).valueOf()
        continue
      } else {
        sortedVersions.push({
          version: v,
          date: moment(repo.time[v]).valueOf()
        })
      }
    }
    sortedVersions = sortedVersions.sort(function (a, b) {
      return a.date - b.date
    })

    // 2nd order of business: filter unwanted versions
    var filteredVersions = sortedVersions
    if (doFilter) {
      var lastVersion = '0.0.0'
      filteredVersions = sortedVersions.filter(function (e) {
        var v = e.version
        if (!semver.valid(v)) {
          // console.log('INVALID: %s', v)
          return false
        } else if (!v.match(/[0-9]+\.[0-9]+\.[0-9]+$/)) {
          // console.log('INVALID - not only numbers: %s', v)
          return false
        } else if (semver.lt(v, lastVersion)) {
          // console.log('INVALID - too small: %s', v)
          return false
        } else {
          lastVersion = v
          // console.log('VALID: %s', v)
          return true
        }
      })
    }
    // console.log(sortedVersions.length, filteredVersions.length)

    // 3rd order of business: lets iterate
    for (var e in filteredVersions) {
      var version = filteredVersions[e].version
      if (typeof repo.versions[version] === 'undefined') {
        continue
      }
      if (version === 'modified' || version === 'created') {
        continue
      }

      var versionDate = moment(repo.time[version]).valueOf()

      // store dependencies:
      var depKeys = [] // stores dependencies contained in the current version!
      var dependencies = repo.versions[version].dependencies
      for (var depKey in dependencies) {
        depKeys.push(depKey)
        if (typeof depDict.deps[depKey] === 'undefined') {
          // console.log('"%s" depends on "%s" for the first time in version %s', repo.name, depKey, version)
          numDeps++
          depDict.deps[depKey] = []
          depDict.deps[depKey].push({from: versionDate})
        } else if (typeof depDict.deps[depKey][depDict.deps[depKey].length - 1].to !== 'undefined') {
          // console.log('"%s" depends on "%s" AGAIN in version %s', repo.name, depKey, version)
          numDeps++
          numReDeps++
          depDict.deps[depKey].push({from: versionDate})
        }
      }

      // store devDependencies:
      var devDependencies = repo.versions[version].devDependencies
      for (var devDepKey in devDependencies) {
        depKeys.push(devDepKey)
        if (typeof depDict.deps[devDepKey] === 'undefined') {
          // console.log('"%s" depends on "%s" for the first time in version %s', repo.name, devDepKey, version)
          numDeps++
          depDict.deps[devDepKey] = []
          depDict.deps[devDepKey].push({from: versionDate})
        } else if (typeof depDict.deps[devDepKey][depDict.deps[devDepKey].length - 1].to !== 'undefined') {
          // console.log('"%s" depends on "%s" AGAIN in version %s', repo.name, devDepKey, version)
          numDeps++
          numReDeps++
          depDict.deps[devDepKey].push({from: versionDate})
        }
      }

      // end version dependency by specifying 'to':
      for (var depKey2 in depDict.deps) {
        if (depKeys.indexOf(depKey2) === -1 &&
          typeof depDict.deps[depKey2][depDict.deps[depKey2].length - 1].to === 'undefined') {
          // console.log('"%s" depends NO MORE on "%s" in version %s', repo.name, depKey2, version)
          numLostDeps++
          depDict.deps[depKey2][depDict.deps[depKey2].length - 1].to = versionDate
        }
      }
    }

    // close down all open 'to's:
    for (var depKey3 in depDict.deps) {
      if (typeof depDict.deps[depKey3][depDict.deps[depKey3].length - 1].to === 'undefined') {
        // console.log('"%s" depends on "%s" until the bitter end.', repo.name, depKey3)
        depDict.deps[depKey3][depDict.deps[depKey3].length - 1].to = closeDate
      }
    }

    if (creationDate === 0 && filteredVersions.length > 0) {
      depDict.creationDate = filteredVersions[0].date
    } else {
      depDict.creationDate = creationDate
    }

    return {
      deps: depDict,
      numDeps: numDeps,
      numLostDeps: numLostDeps,
      numReDeps: numReDeps
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

  // define exports:
  exports.createSnapshotFromSingleFile = createSnapshotFromSingleFile
  exports.createSnapshotFromMultipleFiles = createSnapshotFromMultipleFiles

  if (!module.parent) {
    // user input:
    //
    //        node graph-snapshot.js <path-to-data>
    //
    if (typeof process.argv[2] === 'undefined' ||
        typeof process.argv[3] === 'undefined') {
      console.log('usage: node %s <path-to-data> <output-path, e.g. ../npm_graph_deps.json>', process.argv[1])
    } else {
      var inputPath = process.argv[2]
      var outputPath = process.argv[3]

      if (fs.lstatSync(inputPath).isFile()) {
        createSnapshotFromSingleFile(inputPath, outputPath, function (err, data) {
          if (err) {
            console.log(err)
          }
          console.log('done.')
          console.log(JSON.stringify(data, null, 2))
        })
      } else if (fs.lstatSync(inputPath).isDirectory()) {
        createSnapshotFromMultipleFiles(inputPath, outputPath, function (err, data) {
          if (err) {
            console.log(err)
          }
          console.log('done.')
        })
      } else {
        console.log('provided input-path is neither file nor folder')
      }
    }
  }
})()
