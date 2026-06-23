from setuptools import find_packages, setup

package_name = 'hexa_simulation'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', [f'resource/{package_name}']),
        (f'share/{package_name}', ['package.xml']),
        (f'share/{package_name}/launch', ['launch/display_rviz.launch.py']),
        (f'share/{package_name}/urdf', ['urdf/hexapode.urdf']),
        (f'share/{package_name}/rviz', ['rviz/hexapode.rviz']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Clement',
    maintainer_email='clement@example.com',
    description='Minimal hexapod RViz simulation.',
    license='Proprietary',
    entry_points={
        'console_scripts': [
            'sim_hexa = hexa_simulation.sim_hexa:main',
                'gui_bridge = hexa_simulation.gui_bridge:main',
            ],
    },
)
