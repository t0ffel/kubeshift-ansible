# kubeshift-ansible
ansible modules for openshift/kubernetes based on kubeshift library

# Goals

idempotent deployment of complex applications without inventing anything really
new, which is to be accomplished via Ansible.
'Complex' - means apps that require:
* secrets
* configmaps
* SCCs
* serviceaccounts
* persistent storage
* deployment in a certain order.

# Example

Please see the playbook for deploying fluentd: [fluentd](playbooks/fluentd.yaml)
