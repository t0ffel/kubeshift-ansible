#!/usr/bin/python
DOCUMENTATION = '''
---
module: k8s_contains
short_description:
description:
version_added: "2.2"
author: "Anton Sherkhonov, @t0ffel"
notes:
requirements:
options:
    resource_desc:
        default: None
        description:
            - JSON/YAML description of the resource
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
            target_resource=dict(required=True, type='dict'),
            patch=dict(required=True, type='dict'),
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
        )
    )
    if not HAS_KUBESHIFT:
        module.fail_json(msg='kubeshift required for this module')

    # Client configuration
    user = getpass.getuser()
    config = kubeshift.Config.from_file("/home/%s/.kube/config" % user)
    client = kubeshift.OpenshiftClient(config)

    state = module.params.get('state')

    k8s_object = module.params.get('target_resource')
    patch = module.params.get('patch')

    try:
        if state == 'present':
            res = client.ensure_patched(k8s_object, patch)
        else:
            res = client.ensure_absent(k8s_object)
    except KubeRequestError as err:
        module.fail_json(msg=err.message)

    module.exit_json(**res)

# import module snippets
from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
