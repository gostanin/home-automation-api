docker_up:
	docker-compose -p home-automation-api up -d --build --remove-orphans --force-recreate

docker_stop:
	docker-compose -p home-automation-api stop

docker_down:
	docker-compose -p home-automation-api down -v