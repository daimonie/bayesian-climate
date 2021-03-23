install:
	docker run hello-world
	docker build  -f Dockerfile -t bayesian-climate .

dev:
	docker run -v $(PWD)/container/:/opt/container \
	--rm -ti --entrypoint=bash bayesian-climate:latest

pep8:
	docker run --rm -v $(PWD)/container/:/opt/container \
		--entrypoint=/usr/local/bin/python \
		bayesian-climate:latest \
		/usr/local/bin/pycodestyle /opt/container

unittest:
	docker run --rm -v $(PWD)/container/:/opt/container \
		-v $(PWD)/tests/:/opt/container/tests \
		--entrypoint=/bin/bash \
		bayesian-climate:latest \
		/opt/container/tests/test

test:
	make pep8
	make unittest