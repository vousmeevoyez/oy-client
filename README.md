# Oy Client 

Unofficial Oy Client using Python 
https://api-docs.oyindonesia.com/

### Prerequisites
	These library only tested for python 3.7 but it should be compatible to other python version
	please create issue or contact me if you want to test it on python2

### Installing
```
	pip3 install oy-client
```
### Quick Start
```
from oy import build_client

# get balance
oy_client = build_client("https://sandbox.oyindonesia.com/staging/partner", "username", "api-key")
oy_client.get_balance()

# inquiry account
oy_client.inquiry_account("014", "1234561234")

# disburse
disburse("014", "123456789", 100000)
```

## Built With

* [Requests](https://requests.readthedocs.io/en/master/) - HTTP Library Used

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Kelvin Desman** - [Vousmeevoyez](https://github.com/vousmeevoyez/)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
