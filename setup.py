from setuptools import setup, find_packages

setup(
    name='adversarial-bot',
    version='0.0.1',
    description='Simula conversaciones entre un cliente y un chatbot para evaluar su rendimiento.',
    author='Juan Martin Morales',
    author_email='juanm4morales@gmail.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        # Aquí se pueden incluir las dependencias listadas en requirements.txt
    ],
    entry_points={
        'console_scripts': [
            'simulate-conversation=adv_customer.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)