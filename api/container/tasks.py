from celery.signals import task_postrun
from celery.utils.log import get_task_logger
from db.database import db_session as db
from db.models import Container
from extensions import celery
from .functions import create_tarball, create_image, create_boot

logger = get_task_logger(__name__)


@celery.task
def build_image(uuid=None, docker_image=None, docker_tag=None,
                image_format=None):
    status = 'tarballing'
    tarball = create_tarball(docker_image, docker_tag)
    status = 'imagebuild'
    disk_image = create_image(tarball, image_format)
    status = 'patching'
    create_boot(disk_image)
    status = 'complete'
    Container.query.filter_by(uuid=uuid).update(dict(status=status))
    db.commit()
    return (status, disk_image)


@celery.task
def log(message):
    logger.debug(message)
    logger.info(message)
    logger.warning(message)
    logger.error(message)
    logger.critical(message)


@task_postrun.connect
def close_session(*args, **kwargs):
    # Flask SQLAlchemy will automatically create new sessions for you from
    # a scoped session factory, given that we are maintaining the same app
    # context, this ensures tasks have a fresh session (e.g. session errors
    # won't propagate across tasks)
    db.remove()
