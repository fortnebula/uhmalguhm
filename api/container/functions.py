from docker import APIClient
import guestfs
import subprocess
from tempfile import mkstemp
from os import unlink


def create_tarball(docker_image=None, docker_tag=None):
    d = APIClient(base_url='unix://var/run/docker.sock')
    d.pull(docker_image, docker_tag)
    container = d.create_container(docker_image)
    resp = d.export(container=container['Id'])
    tarfd, tarball = mkstemp(prefix='/tmp/', suffix='.tar')
    f = open(tarball, 'wb')
    for chunk in resp:
        f.write(chunk)
    f.close()
    d.remove_container(container['Id'])
    return tarball


def create_image(tarball=None, image_format=None):
    diskfd, diskpath = mkstemp(prefix='/tmp/', suffix='.img')
    g = guestfs.GuestFS(python_return_dict=True)
    g.disk_create(diskpath, image_format, 512 * 1024 * 1024)
    g.set_trace(1)
    g.add_drive_opts(diskpath, format=image_format, readonly=0)
    g.launch()
    devices = g.list_devices()
    assert(len(devices) == 1)
    g.part_disk(devices[0], "gpt")
    partitions = g.list_partitions()
    assert(len(partitions) == 1)
    g.mkfs("ext4", partitions[0])
    g.mount(partitions[0], "/")
    g.tar_in(tarfile=tarball, directory="/")
    g.shutdown()
    g.close()
    unlink(tarball)
    print ('Deleted Tarball')
    return diskpath


def create_boot(diskpath=None):
    package = "systemd,linux-image-kvm"
    subprocess.run(["/usr/bin/virt-customize", "-a", diskpath,
                    "--install", str(package), "--delete",
                    "/usr/sbin/policy-rc.d", "--delete",
                    "/sbin/initctl", "--link",
                    "/lib/systemd/systemd:/sbin/init"])
    unlink(diskpath)
    print ('Deleted Image')
