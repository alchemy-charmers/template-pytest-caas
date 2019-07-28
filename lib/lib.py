from charmhelpers.core import hookenv, templating
from charms import layer


class ${libclass}():
    def __init__(self):
        self.charm_config = hookenv.config()

    def action_function(self):
        ''' An example function for calling from an action '''
        return

    def make_pod_spec():
        image_info = layer.docker_resource.get_info('${metadata.package}_image')
        context = image_info
        context['name'] = '${metadata.package}'
        spec = templating.render('pod_spec.j2', None, context=context)
        return spec
