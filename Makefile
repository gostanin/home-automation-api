docker_up:
	docker-compose -p home-automation-api up -d --build --remove-orphans --force-recreate

docker_test:
	docker-compose -p home-automation-api exec -T api python -B -m pytest

docker_stop:
	docker-compose -p home-automation-api stop

docker_down:
	docker-compose -p home-automation-api down -v