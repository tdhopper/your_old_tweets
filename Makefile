all: deploy

.PHONY: deploy
deploy:
	STATIC_DEPS=true pip3 install -U "python-twitter<4" "python-dateutil"
	rm -rf concurrent/futures
	serverless deploy

.PHONY: clean
clean:
	git clean -fd
