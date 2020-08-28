from dockerfile_parse import DockerfileParser


def parseDockerfile(dockerfile):
    dfp = DockerfileParser()
    dfp.content = dockerfile
    dfp.content = request.get_data()
    response = dfp.json
    return dfp.structure
