# NoC Test Scraping

Script to scrape publications from the websites of the [NoC (Network of Centers)](https://networkofcenters.net/) centers.
Currently it can scrape:
* [Berkman Klein Center for Internet and Society](https://cyber.harvard.edu/)
* [Nexa Center for Internet and Society](https://nexa.polito.it/)
* [Institute of Network Cultures](http://cyberlaw.stanford.edu/)
* [Center for Internet and Society](http://networkcultures.org/)
* [Information Society Project](https://law.yale.edu/isp)

## Getting Started

Browse to the project folder then type

```
scrapy crawl nexa
```
or
```
scrapy crawl nexa -L WARNING
```
to suppress debug messages

### Prerequisites

You'll need [Scrapy v1.5.0](https://scrapy.org/) and [Python 3](https://www.python.org/download/releases/3.0/) to run the spider.

## Built With

* [Scrapy](https://scrapy.org/) - The scraping framework used

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details.
