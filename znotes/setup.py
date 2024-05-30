from setuptools import setup 

setup(
        author = "Vijay Venkatramani",
        name = 'znotes',
        version = '0.1.0',
        packages= ['znotes'],
        # insatall_requires = ["markdown-to-json>=2.11", "typer>=0.12.3"],
        entry_points = {
            'console_scripts': [
                'znotes = znotes.main:run'
            ]
        }
    )
