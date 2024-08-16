website: .PHONY
	source env.sh; \
	cd website; \
	pipenv run uvicorn website:app --reload --host 0.0.0.0 --port 8080 --proxy-headers

.PHONY: all
