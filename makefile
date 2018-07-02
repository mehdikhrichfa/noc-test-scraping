tests:
	cd ./main && python3 -m unittest tests.py

test_sanity:
	cd ./main/test_pages/ && sh test_sanity.sh

sync_test:
	cd ./main/test_pages/ && sh test_sanity.sh --sync
