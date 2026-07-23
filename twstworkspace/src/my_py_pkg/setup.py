import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'my_py_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ("share/" + package_name + "/launch", glob(os.path.join("launch", "*.launch.py"))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pc',
    maintainer_email='wnehdrjs1114@naver.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'my_node = my_py_pkg.my_node:main',
            'class_pub = my_py_pkg.class_pub:main',
            'class_sub = my_py_pkg.class_sub:main',
            'header_pub = my_py_pkg.header_pub:main',

            'class_sub2 = my_py_pkg.class_sub2:main',
            'time_sub = my_py_pkg.time_sub:main',

            'mv_turtle = my_py_pkg.mv_turtle:main',
            #export ROS_DOMAIN_ID=0
            'qos_test_pub = my_py_pkg.qos_test_pub:main',
            'qos_test_sub = my_py_pkg.qos_test_sub:main',
            'user_int_pub = my_py_pkg.user_int_pub:main',
            'service_server = my_py_pkg.service_server:main',
            'service_thread_server = my_py_pkg.service_thread_server:main',
            'service_client = my_py_pkg.service_client:main',
            'my_param = my_py_pkg.my_param:main',
            'param_async = my_py_pkg.param_async:main',
            'action_server = my_py_pkg.action_server:main',
            'action_client = my_py_pkg.action_client:main',
            'action_thread_server = my_py_pkg.action_thread_server:main',

        ],
    },
)
