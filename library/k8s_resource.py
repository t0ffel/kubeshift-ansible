#!/usr/bin/python
DOCUMENTATION = '''
---
module: k8s_resource
short_description:
description:
version_added: "2.2"
author: "Anton Sherkhonov, @t0ffel"
notes:
requirements:
options:
    name:
        required: true
        description:
            - Name of the pod.
    state:
        required: false
        default: "present"
        choices: [ present, absent ]
        description:
            -  Whether the pod should exist or not.
    api_version:
        required: false
        default: "v1"
        choices: [ v1 ]
        descriptoin:
            - The API version to use.
    api_endpoint:
        required: false
        default: None
        description:
            - The api endpoint to use.
    username:
        required: false
        default: None
        description:
            - The username to use to authenticate to the api_endpoint.
    password:
        required: false
        default: None
        description:
            - The password to use to authenticate to the api_endpoint.
    client_cert:
        required: false
        default: None
        description:
            - The client certificate to use to authenticate to the api_endpoint.
    client_key:
        required: false
        default: None
        description:
            - The client key to use to authenticate to the api_endpoint.
    token:
        required: false
        default: None
        description:
            - The token to use to authenticate to the api_endpoint.
    certificate_authority:
        required: false
        default: None
        description:
            - The certificate authority for the server certificate.
    insecure_skip_tls_verify:
        required: false
        default: "no"
        choices: [ "yes", "no" ]
            - Whether to skip tls verification.
    labels:
        required: false
        default: None
        description:
            - A dictionary of the labels to apply to this pod.
    annotations:
        required: false
        default: None
        description:
            - A dictionary of the annotations to apply to this pod.
'''
EXAMPLES = '''
'''
import getpass

try:
    import kubeshift
    from kubeshift.exceptions import (KubeConnectionError, KubeRequestError,
                                      KubeShiftError)
    HAS_KUBESHIFT = True
except ImportError:
    HAS_KUBESHIFT = False


def main():
    module = AnsibleModule(
        argument_spec=dict(
            namespace=dict(default=None, type='str'),
            state=dict(default='present', choices=[
                       'present', 'absent'], type='str'),
            api_endpoint=dict(default=None, type='str'),
            username=dict(default=None, type='str'),
            password=dict(default=None, type='str'),
            client_cert=dict(default=None, type='str'),
            client_key=dict(default=None, type='str'),
            token=dict(default=None, type='str'),
            certificate_authority=dict(default=None, type='str'),
            insecure_skip_tls_verify=dict(default='no', type='bool'),
            resource_desc=dict(default=None, type='dict'),
        )
    )
    if not HAS_KUBESHIFT:
        module.fail_json(msg='kubeshift required for this module')

    # Client configuration
    user = getpass.getuser()
    config = kubeshift.Config.from_file("/home/%s/.kube/config" % user)
    client = kubeshift.KubernetesClient(config)

    name = module.params.get('name')
    kind = module.params.get('kind')
    api_version = module.params.get('api_version')
    state = module.params.get('state')
    # rules = module.params.get('rules')

    k8s_object = module.params.get('resource_desc')
    # {
    #     "apiVersion": api_version,
    #     "kind": kind,
    #     "metadata": {
    #         "name": name
    #     },
    #     'rules': rules
    # }

    try:
        if state == 'present':
            response = client.create(k8s_object)
        else:
            response = client.delete(k8s_object)
    except KubeRequestError as err:
        module.fail_json(msg=err.message)

    result = {
        'response': response,
        'changed': True}
    module.exit_json(**result)

# import module snippets
from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
