import os
import pytest
import subprocess
import stat

from charmhelpers.core import hookenv

os.environ['JUJU_CHARM_DIR'] = '.'
metadata = hookenv.metadata()

# Treat all tests as coroutines
pytestmark = pytest.mark.asyncio

juju_repository = os.getenv("JUJU_REPOSITORY", ".").rstrip("/")
images = [
# Tuple: (name, image:tag)
    ("xenial", pytest.param("ubuntu:16.04")),
    ("bionic", pytest.param("ubuntu:18.04")),
    ("latest", pytest.param("ubuntu:latest", marks=pytest.mark.xfail(reason="canary"))),
]
sources = [
    ("local", "{}/builds/{}".format(juju_repository, metadata.get('name'))),
    # ('jujucharms', 'cs:...'),
]


# Custom fixtures
@pytest.fixture(params=images, ids=[i[0] for i in images])
def image(request):
    return request.param


@pytest.fixture(params=sources, ids=[s[0] for s in sources])
def source(request):
    return request.param


@pytest.fixture
async def app(model, image, source):
    app_name = "{}-{}-{}".format(metadata.get('name'),
                                 image[0],
                                 source[0],
                                 )
    return await model._wait_for_new("application", app_name)


@pytest.mark.deploy
async def test_${fixture}_deploy(model, image, source, request):
    # Starts a deploy for each series
    # Using subprocess b/c libjuju fails with JAAS
    # https://github.com/juju/python-libjuju/issues/221
    application_name = '{}-{}-{}'.format(metadata.get('name'),
                                         image[0],
                                         source[0])
    cmd = ['juju',
           'deploy',
           source[1],
           '-m',
           model.info.name,
           application_name,
           '--resource',
           '{}_image={}'.format(metadata.get('name'), image[1].values[0])]
    subprocess.check_call(cmd)


@pytest.mark.deploy
@pytest.mark.timeout(300)
async def test_charm_upgrade(model, app):
    if app.name.endswith("local"):
        pytest.skip("No need to upgrade the local deploy")
    unit = app.units[0]
    await model.block_until(lambda: unit.agent_status == "idle")
    subprocess.check_call(
        [
            "juju",
            "upgrade-charm",
            "--switch={}".format(sources[0][1]),
            "-m",
            model.info.name,
            app.name,
        ]
    )
    await model.block_until(lambda: unit.agent_status == "executing")


@pytest.mark.deploy
@pytest.mark.timeout(300)
async def test_${fixture}_status(model, app):
    # Verifies status for all deployed series of the charm
    await model.block_until(lambda: app.status == 'active')
    unit = app.units[0]
    await model.block_until(lambda: unit.agent_status == 'idle')


# Tests
# async def test_example_action(app):
#     unit = app.units[0]
#     action = await unit.run_action("example-action")
#     action = await action.wait()
#     assert action.status == "completed"


async def test_run_command(app, jujutools):
    unit = app.units[0]
    cmd = "hostname --all-ip-addresses"
    results = await jujutools.run_command(cmd, unit)
    assert results["Code"] == "0"
    assert unit.public_address in results["Stdout"]


async def test_file_stat(app, jujutools):
    unit = app.units[0]
    path = "/var/lib/juju/agents/unit-{}/charm/metadata.yaml".format(
        unit.entity_id.replace("/", "-")
    )
    fstat = await jujutools.file_stat(path, unit)
    assert stat.filemode(fstat.st_mode) == "-rw-r--r--"
    assert fstat.st_uid == 0
    assert fstat.st_gid == 0
