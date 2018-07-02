# NoC Test Scraping

Script to scrape publications from the websites of the [NoC (Network of Centers)](https://networkofcenters.net/) centers.
Currently it can scrape:
* [Berkman Klein Center for Internet and Society](https://cyber.harvard.edu/)
* [Nexa Center for Internet and Society](https://nexa.polito.it/)
* [Institute of Network Cultures](http://cyberlaw.stanford.edu/)
* [Center for Internet and Society](http://networkcultures.org/)
* [Information Society Project](https://law.yale.edu/isp)

## Getting Started

Browse to the project folder then, to run the script, type

```
scrapy crawl <center>
```
where <b>&lt;center&gt;</b> can be replaced by:
* nexa
* bkc
* inc
* cis
* isp

### Options
```
-L WARNING                              #run the script with no debug messages

-a print_only=true                      #print the URLs without downloading the files

-s FILES_STORE="/path/to/valid/dir"     #choose the folder to store the downloded pdf files
```

### Testing

To test the scripts, browse to the main folder, then type

```
make tests
```


### Prerequisites

You'll need [Scrapy v1.5.0](https://scrapy.org/) and [Python 3](https://www.python.org/download/releases/3.0/) to run the spider.
[Colorama](https://pypi.org/project/colorama/) is used for the output.
[jq](https://stedolan.github.io/jq/) is used in tests.

` pip3 install --user scrapy colorama `

## Built With

* [Scrapy](https://scrapy.org/) - The scraping framework used

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details.
