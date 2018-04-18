from fabric.api import cd
from fabric.api import env
from fabric.api import local
from fabric.api import task
from patchwork.files import append
from patchwork.files import contains
from patchwork.files import directory
from patchwork.files import rm
from patchwork.files import rmdir
from patchwork.transfers import rsync

env.use_ssh_config = True


@task
def test_rsync_file():

    # setup
    d = 'test_rsync'
    remote_f = 'remote\ file.txt'
    local_f = 'local_file.txt'
    directory(d)
    with cd(d):
        rm(remote_f)
        append(remote_f, 'Hello world')

    # download file
    src = '%s/%s' % (d, remote_f)
    rsync(
        remote_dir=src,
        local_dir=local_f,
        upload=False
    )
    assert contains(local_f, 'Hello world', runner=local) is True

    # append to and upload file
    append(local_f, 'Hello from local', runner=local)
    rsync(
        remote_dir=src,
        local_dir=local_f,
    )
    # check uploaded file
    with cd(d):
        assert contains(remote_f, 'Hello from local') is True

    # cleanup
    rm(local_f, runner=local)
    rmdir(d)
