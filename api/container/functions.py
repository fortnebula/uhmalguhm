from dockerfile_parse import DockerfileParser


def parseDockerfile(dockerfile):
    dfp = DockerfileParser()
    dfp.content = dockerfile
    return dfp.structure
