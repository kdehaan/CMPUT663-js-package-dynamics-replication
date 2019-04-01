package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"sync"
)

var wg = &sync.WaitGroup{}
var sem = make(chan int, 100)

// Our datastructures for JSON unmarshalling
type Data struct {
	Objects []PackageObj `json:"objects"`
}

type PackageObj struct {
	Package struct {
		Name string `json:"name"`
	} `json:"package"`
}

func get_package_names(stable bool, offset int) {
	defer wg.Done()

	stability := ""
	if stable {
		stability = "stable"
	} else {
		stability = "unstable"
	}

	// do an http GET
	urlstr := fmt.Sprintf("https://registry.npmjs.org/-/v1/search?text=is:%s&size=250&from=%d", stability, offset)
	resp, err := http.Get(urlstr)
	if err != nil {
		fmt.Println(err)
	}

	defer resp.Body.Close()

	// read the response from the http request
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println(err)
	}

	// Handle the unjsonifying data
	data := Data{}
	json.Unmarshal(body, &data)

	// create the file to write to
	f, err := os.OpenFile(fmt.Sprintf("/Volumes/RFSH-Ext/663-Names/%s-%d.txt", stability, offset), os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Println(err)
	}

	defer f.Close()

	// print all the names to our file
	for _, p := range data.Objects {
		fmt.Fprintf(f, "%s\n", p.Package.Name)
	}

	<-sem
}

func main() {
	/*
	 These are magic numbers of how many packages there are with stable/unstable
	 we use a search that does text=is:{stable/unstable} to get all packages,
	 since it's not obvious that we can actually get all.
	 Queries are split into chunks of 250 packages since npm registry has that as it's
	 maximum search query size
	*/
	for i := 0; i < 4197; i += 250 {
		sem <- 1
		wg.Add(1)
		go get_package_names(false, i)
	}
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
