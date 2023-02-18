init:
	pip install -r requirements.txt
	pip install pipreqs

reqs:
	pipreqs . --force

requirements: reqs

driver:
	@if [ -f "lib/chromedriver/chromedriver-bundle.zip" ]; then \
		echo "chromedriver bundle already exists"; \
	else \
		mkdir -p lib/chromedriver &&\
		cd lib/chromedriver &&\
		echo "[X] Downloading chromedriver" &&\
		curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip &&\
		unzip chromedriver.zip &&\
		rm chromedriver.zip &&\
		echo "[X] Downloading headless chromium" &&\
		curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-41/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip &&\
		unzip headless-chromium.zip &&\
		rm headless-chromium.zip; \
	fi

serverless-init:
	npm install

deploy:
	sls deploy
