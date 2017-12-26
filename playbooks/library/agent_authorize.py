#!/usr/bin/python

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
import os


def register(params):
    has_changed = False
    url = params["tc_url"]
    headers = {'Accept': 'application/json'}

    t_url = url + "/app/rest/agents?includeUnauthorized=true"
    req = open_url(t_url, method="GET", url_username=params["tc_user"], headers=headers, url_password=params["tc_password"])
    resp_json = json.loads(req.read())

    command = ""
    for i in range(0, len(resp_json['agent'])):
        id = resp_json['agent'][i]['id']
        t_url = url + "/app/rest/agents/id:" + str(id) + "/authorized"
        command = "curl -u " + params["tc_user"] + ":" + params["tc_password"] + " --request PUT --data true --header \"Content-Type: text/plain\" " + t_url

        os.system(command)
        has_changed = True

    meta = {"params:": command}
    return (has_changed, meta)


def main():

    fields = {
        "hosts": {"required": True, "type": "str"},
        "tc_url": {"required": True, "type": "str"},
        "tc_user": {"required": True, "type": "str"},
        "tc_password": {"required": False, "type": "str"},
    }

    module = AnsibleModule(argument_spec=fields)
    has_changed, result = register(module.params)
    module.exit_json(changed=has_changed, meta=result)


if __name__ == '__main__':
    main()