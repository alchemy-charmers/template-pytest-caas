from charmhelpers.core import hookenv, templating
from charms import layer


class ${libclass}():
    def __init__(self):
        self.charm_config = hookenv.config()
        self.metadata = hookenv.metadata()

    def action_function(self):
        ''' An example function for calling from an action '''
        return

    def make_pod_spec(self):
        image_info = layer.docker_resource.get_info('${metadata.package}_image')
        context = {'registry_path': image_info.registry_path,
                   'image_username': image_info.username,
                   'image_password': image_info.password,
                   'name': self.metadata.get('name'),
                   }
        spec = templating.render('pod_spec.j2', None, context=context)
        return spec
