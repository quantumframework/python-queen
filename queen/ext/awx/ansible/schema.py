from .base import BaseAnsibleTowerModule


class SchemaModule(BaseAnsibleTowerModule):
    module_args = {
        'api_url': {'type': 'str', 'required': False},
        'api_user': {'type': 'str', 'required': False},
        'api_password': {'type': 'str', 'required': False, 'no_log': True},
        'validate_certs': {'type': 'bool', 'required': False, 'default': False},
        'state': {'type': 'str', 'required': False, 'default': 'present'},
        'job_template_id': {'type': 'int', 'required': True},
        'name': {'type': 'str', 'required': True},
        'rrule': {'type': 'str', 'required': True},
        'description': {'type': 'str', 'required': False, 'default': ''},
        'enabled': {'type': 'bool', 'required': False, 'default': True},
    }

    @property
    def job_template_id(self):
        return self.params['job_template_id']

    def dtofromparams(self):
        dto = {
            'name': self.params['name'],
            'description': str.strip(self.params['description']),
            'enabled': self.params['enabled'],
            'rrule': self.params['rrule']
        }
        if self.resource:
            dto['unified_job_template'] = self.resource['unified_job_template']
        return dto

    def getsubjectresource(self):
        return self.client.list('job_templates',
            self.job_template_id, 'schedules',
            params={'name': self.params['name']})

    def getcreateurlparts(self):
        return ['POST', 'job_templates', self.job_template_id,
            'schedules']

    def getupdateurlparts(self):
        return ['PUT', 'schedules', self.resource['id']]

    def getdeleteurlparts(self):
        return ['DELETE', 'schedules', self.resource['id']]
