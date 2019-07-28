from ${libfile} import ${libclass}
from charmhelpers.core import hookenv
from charms.reactive import set_flag, when_not, when
from charms import layer

helper = ${libclass}()


@when_not('layer.docker-resource.${metadata.package}_image.fetched')
def fetch_image():
    layer.docker_resource.fetch('${metadata.package}_image')

@when('${metadata.package}.configured')
def ${safe_package}_active():
    hookenv.status_set('active','')

@when('layer.docker-resource.${metadata.package}_image.fetched')
@when_not('${metadata.package}.configured')
def ${safe_package}_configure():
    hookenv.status_set('maitenance', 'Configuring ${metadata.package} container')
    spec = helper.make_pod_spec()
    hookenv.log('Setting pod spec:\n{}'.format(spec))
    if layer.caas_base.pod_spec_set(spec):
        hookenv.set_flag('${metadata.package}.configured')
    else:
        hookenv.log('Failed to set spec', 'ERROR')
