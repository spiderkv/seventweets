from fabric.api import local, settings, run, env

# server list
env.hosts = ["pass.sedamcvrkuta.com"]

# SSH user
env.user = "root"

# service vars
name = "seventweets"
port = 8000
repository = "spiderkv/seventweets"
network = "seventweets"

# db vars
pg_host = 'seventweets-postgres'
pg_port = 5432
pg_volume = 'seventwets-postgres-data'
pg_user = 'workshop'
pg_pass = 'p4ss'
pg_version = '9.6.2'


def build(tag=""):
    if tag is not "":
        tag = ":" + tag
    local("docker build -t {}{} .".format(repository, tag))


def push(tag=""):
    local("docker push {}{}".format(repository, tag))


def create_network():
    local("docker network create {}".format(network))


def start(tag=""):
    local("""
        docker run -d \
            --name {} \
            --net {} \
            -p {}:{} \
            -e ST_DB_USER={} \
            -e ST_DB_PASS={} \
            -e ST_DB_HOST={} \
            {}{}
        """.format(name, network, port, port, pg_user, pg_pass, pg_host, repository, tag))


def stop():
    local("docker stop {}".format(name))
    local("docker rm {}".format(name))


def restart():
    stop()
    start()


def db_start():
    with settings(warn_only=True):
        local("docker volume create {}".format(pg_volume))
        local("""
            docker run -d \
                --name {} \
                --net {} \
                --restart unless-stopped \
                -e POSTGRES_USER={} \
                -e POSTGRES_PASSWORD={} \
                -v {}:/var/lib/postgresql/data \
                -p localhost:5432:5432 \
                postgres:{}
            """.format(pg_host, network, pg_user, pg_pass, pg_volume, pg_version))


def db_stop():
    local("docker stop seventweets-postgres")
    local("docker rm seventweets-postgres")


def deploy_db():
    with settings(warn_only=True):
        run("docker volume create {}".format(pg_volume))
        run("docker network create {}".format(network))
    run("""
        docker run -d \
            --name {} \
            --net {} \
            --restart unless-stopped \
            -p {}:{} \
            -e POSTGRES_USER={} \
            -e POSTGRES_PASSWORD={} \
            -v {}:/var/lib/postgresql/data \
            postgres:{}
        """.format(pg_host, network, pg_port, pg_port, pg_user, pg_pass, pg_volume, pg_version))


def deploy(tag=""):
    build(tag)
    push(tag)
    with settings(warn_only=True):
        run("docker stop {}".format(name))
        run("docker rm {}".format(name))
        run("docker network create {}".format(name))
        run("""
            docker run -d \
            --name {} \
            --net {} \
            -p {}:{} \
            -e ST_DB_USER={} \
            -e ST_DB_PASS={} \
            -e ST_DB_HOST={} \
            {}{}
        """.format(name, network, port, port, pg_user, pg_pass, pg_host, repository, tag))
