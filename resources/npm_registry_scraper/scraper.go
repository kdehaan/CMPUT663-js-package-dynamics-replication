package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"sync"
)

var ES_BASE_URL = "http://localhost:9200/packages/_package/"
var REGISTRY_BASE_URL = "https://registry.npmjs.org/"

var wg = &sync.WaitGroup{}
var sem = make(chan int, 100)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func get_package_info(name string) {
	// We want to pull from registry
	resp, err := http.Get(REGISTRY_BASE_URL + name)
	check(err)
	defer resp.Body.Close()

	// send to our ES server
	contents, err := ioutil.ReadAll(resp.Body)

	werr := ioutil.WriteFile("/Volumes/RFSH-Ext/ESData"+name, contents, 0644)
	check(werr)
	//<-sem
}

func main() {
	/*
	 These are magic numbers of how many packages there are with stable/unstable
	 we use a search that does text=is:{stable/unstable} to get all packages,
	 since it's not obvious that we can actually get all.
	 Queries are split into chunks of 250 packages since npm registry has that as it's
	 maximum search query size
	*/
	get_package_info("isnum")
	//for i := 0; i < 419727; i += 250 {
	//sem <- 1
	//wg.Add(1)
	//go get_package_names(false, i)
	//}
	//for i := 0; i < 913617; i += 250 {
	//sem <- 1
	//wg.Add(1)
	//go get_package_names(true, i)
	//}
	wg.Wait()
	fmt.Println("we done")
}
