from celery.signals import task_postrun
from celery.utils.log import get_task_logger
from db.database import db_session as db
from db.models import Container
from extensions import celery
from docker import APIClient
import guestfs
import subprocess
from tempfile import mkstemp
from os import unlink

logger = get_task_logger(__name__)


@celery.task
def create_image(uuid=None, docker_image=None, docker_tag=None):
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
    diskfd, diskpath = mkstemp(prefix='/tmp/', suffix='.img')
    g = guestfs.GuestFS(python_return_dict=True)
    g.disk_create(diskpath, "raw", 512 * 1024 * 1024)
    g.set_trace(1)
    g.add_drive_opts(diskpath, format="raw", readonly=0)
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
    package = "systemd,linux-image-kvm"
    subprocess.run(["/usr/bin/virt-customize", "-a", diskpath,
                    "--install", str(package), "--delete",
                    "/usr/sbin/policy-rc.d", "--delete",
                    "/sbin/initctl", "--link",
                    "/lib/systemd/systemd:/sbin/init"])
    status = 'complete'
    Container.query.filter_by(uuid=uuid).update(dict(status=status))
    db.commit()
    unlink(diskpath)
    return (status, diskpath)


@celery.task
def log(message):
    logger.debug(message)
    logger.info(message)
    logger.warning(message)
    logger.error(message)
    logger.critical(message)


@celery.task
def reverse_messages():
    """Reverse all messages in DB."""
    for message in Message.query.all():
        words = message.text.split()
        message.text = " ".join(reversed(words))
        db.commit()


@task_postrun.connect
def close_session(*args, **kwargs):
    # Flask SQLAlchemy will automatically create new sessions for you from
    # a scoped session factory, given that we are maintaining the same app
    # context, this ensures tasks have a fresh session (e.g. session errors
    # won't propagate across tasks)
    db.remove()
