from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'ros2_nav_lecture'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'maps'), glob(os.path.join('maps', '*'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='student',
    maintainer_email='student@proboticists.org',
    description='ROS 2 Gazebo and Nav2 Lecture Workspace',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'simple_navigator = ros2_nav_lecture.simple_navigator:main',
            'patrol_challenge = ros2_nav_lecture.patrol_challenge:main',
            'patrol_challenge_solution = ros2_nav_lecture.patrol_challenge_solution:main',
            'obstacle_avoidance = ros2_nav_lecture.obstacle_avoidance:main',
        ],
    },
)
