init:
	pip install -r requirements.txt
	pip install pipreqs

reqs:
	pipreqs . --force

requirements: reqs

serverless-init:
	npm install

deploy:
	sls deploy
