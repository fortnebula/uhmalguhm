from dockerfile_parse import DockerfileParser
from docker import APIClient
import guestfs
import subprocess

class BuildImage():

    def parseDockerfile(dockerfile):
        dfp = DockerfileParser()
        dfp.content = dockerfile
        return dfp.json

    def create_tar(docker_image=None, docker_tag=None):
        d = APIClient(base_url='unix://var/run/docker.sock')
        d.pull(docker_image, docker_tag)
        container = d.create_container(docker_image)
        resp = d.export(container=container['Id'])
        tarball = docker_image + docker_tag
        f = open(str(tarball) + '.tar', 'wb')
        for chunk in resp:
            f.write(chunk)
        f.close()
        d.remove_container(container['Id'])
        return (str(tarball) + '.tar')

    def create_base_image(tarfile):
        disk_image = "disk.img"
        g = guestfs.GuestFS(python_return_dict=True)
        g.disk_create(disk_image, "raw", 512 * 1024 * 1024)
        g.set_trace(1)
        g.add_drive_opts(disk_image, format="raw", readonly=0)
        g.launch()
        devices = g.list_devices()
        assert(len(devices) == 1)
        g.part_disk(devices[0], "gpt")
        partitions = g.list_partitions()
        assert(len(partitions) == 1)
        g.mkfs("ext4", partitions[0])
        g.mount(partitions[0], "/")
        g.tar_in(tarfile=tarfile, directory="/")
        g.shutdown()
        g.close()
        return disk_image

    def install_init(disk_image=None, package=None):
        package = "systemd"
        subprocess.run(["/usr/bin/virt-customize", "-a", disk_image,
                        "--install", package, "--delete",
                        "/usr/sbin/policy-rc.d", "--delete",
                        "/sbin/initctl", "--link",
                        "/lib/systemd/systemd:/sbin/init"])
