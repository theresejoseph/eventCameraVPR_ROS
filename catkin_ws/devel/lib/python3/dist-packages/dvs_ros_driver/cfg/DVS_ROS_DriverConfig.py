## *********************************************************
##
## File autogenerated for the dvs_ros_driver package
## by the dynamic_reconfigure package.
## Please do not edit.
##
## ********************************************************/

from dynamic_reconfigure.encoding import extract_params

inf = float('inf')

config_description = {'name': 'Default', 'type': '', 'state': True, 'cstate': 'true', 'id': 0, 'parent': 0, 'parameters': [{'name': 'streaming_rate', 'type': 'int', 'default': 30, 'level': 0, 'description': 'integration time', 'min': 1, 'max': 10000, 'srcline': 291, 'srcfile': '/opt/ros/noetic/lib/python3/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'edit_method': '', 'ctype': 'int', 'cconsttype': 'const int'}, {'name': 'cas', 'type': 'int', 'default': 1992, 'level': 0, 'description': 'cas (Photoreceptor cascode)', 'min': 0, 'max': 16777215, 'srcline': 291, 'srcfile': '/opt/ros/noetic/lib/python3/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'edit_method': '', 'ctype': 'int', 'cconsttype': 'const int'}, {'name': 'injGnd', 'type': 'int', 'default': 1108364, 'level': 0, 'description': 'injGnd (Differentiator switch level, higher to turn on more)', 'min': 0, 'max': 16777215, 'srcline': 291, 'srcfile': '/opt/ros/noetic/lib/python3/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'edit_method': '', 'ctype': 'int', 'cconsttype': 'const int'}, {'name': 'reqPd', 'type': 'int', 'default': 16777215, 'level': 0, 'description': 'reqPd (AER request pulldown)', 'min': 0, 'max': 16777215, 'srcline': 291, 'srcfile': '/opt/ros/noetic/lib/python3/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'edit_method': '', 'ctype': 'int', 'cconsttype': 'const int'}, {'name': 'puX', 'type': 'int', 'default': 8159221, 'level': 0, 'description': 'puX (2nd dimension AER static pullup)', 'min': 0, 'max': 16777215, 'srcline': 291, 'srcfile': '/opt/ros/noetic/lib/python3/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'edit_method': '', 'ctype': 'int', 'cconsttype': 'const int'}, {'name': 'diffOff', 'type': 'int', 'default': 132, 'level': 0, 'description': 'diffOff (OFF threshold, lower to raise threshold)', 'min': 0, 'max': 16777215, 'srcline': 291, 'srcfile': '/opt/ros/noetic/lib/python3/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'edit_method': '', 'ctype': 'int', 'cconsttype': 'const int'}, {'name': 'req', 'type': 'int', 'default': 309590, 'level': 0, 'description': 'req (OFF request inverter bias)', 'min': 0, 'max': 16777215, 'srcline': 291, 'srcfile': '/opt/ros/noetic/lib/python3/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'edit_method': '', 'ctype': 'int', 'cconsttype': 'const int'}, {'name': 'refr', 'type': 'int', 'default': 969, 'level': 0, 'description': 'refr (Refractory period)', 'min': 0, 'max': 16777215, 'srcline': 291, 'srcfile': '/opt/ros/noetic/lib/python3/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'edit_method': '', 'ctype': 'int', 'cconsttype': 'const int'}, {'name': 'puY', 'type': 'int', 'default': 16777215, 'level': 0, 'description': 'puY (1st dimension AER static pullup)', 'min': 0, 'max': 16777215, 'srcline': 291, 'srcfile': '/opt/ros/noetic/lib/python3/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'edit_method': '', 'ctype': 'int', 'cconsttype': 'const int'}, {'name': 'diffOn', 'type': 'int', 'default': 209996, 'level': 0, 'description': 'diffOn (ON threshold - higher to raise threshold)', 'min': 0, 'max': 16777215, 'srcline': 291, 'srcfile': '/opt/ros/noetic/lib/python3/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'edit_method': '', 'ctype': 'int', 'cconsttype': 'const int'}, {'name': 'diff', 'type': 'int', 'default': 13125, 'level': 0, 'description': 'diff (Differentiator)', 'min': 0, 'max': 16777215, 'srcline': 291, 'srcfile': '/opt/ros/noetic/lib/python3/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'edit_method': '', 'ctype': 'int', 'cconsttype': 'const int'}, {'name': 'foll', 'type': 'int', 'default': 271, 'level': 0, 'description': 'foll (Src follower buffer between photoreceptor and differentiator)', 'min': 0, 'max': 16777215, 'srcline': 291, 'srcfile': '/opt/ros/noetic/lib/python3/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'edit_method': '', 'ctype': 'int', 'cconsttype': 'const int'}, {'name': 'Pr', 'type': 'int', 'default': 217, 'level': 0, 'description': 'Pr (Photoreceptor)', 'min': 0, 'max': 16777215, 'srcline': 291, 'srcfile': '/opt/ros/noetic/lib/python3/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'edit_method': '', 'ctype': 'int', 'cconsttype': 'const int'}], 'groups': [], 'srcline': 246, 'srcfile': '/opt/ros/noetic/lib/python3/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'class': 'DEFAULT', 'parentclass': '', 'parentname': 'Default', 'field': 'default', 'upper': 'DEFAULT', 'lower': 'groups'}

min = {}
max = {}
defaults = {}
level = {}
type = {}
all_level = 0

#def extract_params(config):
#    params = []
#    params.extend(config['parameters'])
#    for group in config['groups']:
#        params.extend(extract_params(group))
#    return params

for param in extract_params(config_description):
    min[param['name']] = param['min']
    max[param['name']] = param['max']
    defaults[param['name']] = param['default']
    level[param['name']] = param['level']
    type[param['name']] = param['type']
    all_level = all_level | param['level']

