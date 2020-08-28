from dockerfile_parse import DockerfileParser
import guestfs
import subprocess

class BuildImage():

    def parseDockerfile(dockerfile):
        dfp = DockerfileParser()
        dfp.content = dockerfile
        dfp.content = request.get_data()
        response = dfp.json
        return dfp.structure

    def create_tar():
        cli = APIClient(base_url='unix://var/run/docker.sock')
        container = 'nginx:latest'
        id_sha = cli.images(container, quiet=True)
        print (id_sha[0])
        id = (id_sha[0]).strip("sha256:")
        print (id)
        resp = cli.export(container=id)
        f = open('nginx-latest.tar', 'wb')
        for chunk in resp:
            f.write(chunk)
        f.close()
        return

    def create_base_image(self, tarfile):
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