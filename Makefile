clean: 
	find . -name \*.pyc -delete
	rm -rf build dist oy_client.egg-info

publish-staging:
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/* --verbose

publish:
	python3 -m twine upload dist/* --verbose

check-cc:
	radon cc oy --total-average -s 

check-mi:
	radon mi oy -s

check-raw:
	radon raw oy -s

check-hal:
	radon hal oy -f
