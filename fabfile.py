from fabric.api import local, settings, run, env

# Lista servera
env.hosts = ["pass.sedamcvrkuta.com"] # SSH korisnik
env.user = "root"

# Varijable servisa
name = "seventweets"
port = 8000
repository = "spiderkv/seventweets"
network = "seventweets"


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
        {}{}
    """.format(name, network, port, port, repository, tag))


def stop():
    local("docker stop {}".format(name))
    local("docker rm {}".format(name))


def restart():
    stop()
    start()


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
            {}{}
        """.format(name, network, port, port, repository, tag))
