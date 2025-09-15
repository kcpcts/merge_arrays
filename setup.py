from setuptools import setup

package_name = 'merge_arrays'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Krish',
    maintainer_email='kchauhan5@wisc.edu',
    description='A simple ROS 2 package that merges arrays.',
    license='NONE',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'merge_arrays_node = merge_arrays.merge_arrays_node:main',
        ],
    },
)
