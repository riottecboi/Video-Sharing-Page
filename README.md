
# Youtube-Video-Sharing

This project is allowing user can share Youtube's link video to the website where everyone can see their activity.

At this stage, every users can login or register automatically if the account is not exist in the database

https://raw.githubusercontent.com/riottecboi/Video-Sharing-Page/master/demo/main.png

https://raw.githubusercontent.com/riottecboi/Video-Sharing-Page/master/demo/share.png


## Stages

We can run this project by two ways:

- Command line 

- Docker (docker composer)

### Command line

For the enviroment, please be sure running the project with python3.7+ and set up a settings.cfg file or enviroment variables:

```
  SECRET_KEY = "supersecretkey"
  MYSQL_HOST = "xxx"
  MYSQL_USER = "xxx"
  MYSQL_PASSWORD = "xxx"
  MYSQL_DB = "xxx"
```

Install pip for suitable python3 version

```
  sudo apt update
  sudo apt install python3-pip
```
Install a requirement packages

```
  pip install -r requirement.txt
```
Run a code

```
  python3 main.py
```
### Docker (docker composer)

Please build your own docker image and replace your image tag to the `image` in `docker/docker-compose.yaml`

Run docker compose at the level of directory which having the `docker-compose.yaml` file

```
  docker-compose up
```

or

```
  docker compose up
```

## Demo

https://github.com/riottecboi/Video-Sharing-Page/blob/cbb0e1c964f203e3f57cf82394a6c6cb7f265d8b/demo/demo.mp4
