from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.data import load_yaml
from nornir.plugins.tasks.text import template_file
from nornir.plugins.tasks.networking import netmiko_send_command

nr = InitNornir(config_file="config.yaml")

def load_vars(task):
    data = task.run(task=load_yaml, file=f'./host_vars/{task.host}.yaml')
    task.host["facts"] = data.result
    config_bgp(task)

def config_bgp(task):
    bgp_template = task.run(task=template_file, name="Buildling BGP Configuration", template="bgp.j2", path="./templates")
    bgp_output = bgp_template.result
    bgp_split = bgp_output.splitlines()
    for cmds in bgp_split:
        task.run(task=netmiko_send_command, name="AUTOMATING BGP", command_string=cmds)

result=nr.run(task=load_vars)
print_result(result)
