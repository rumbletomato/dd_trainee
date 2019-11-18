## Run in first time
1. `docker-compose up db -d` 
2. Create database 'simple_crud'
3. `docker-compose up web -d`
4. `docker-compose run web python migrate`

## Run in other times
1. `docker-compose up -d`

## Stop all
1. `docker-compose down --remove-orphans`