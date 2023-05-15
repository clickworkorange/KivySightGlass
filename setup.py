from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='KivySightGlass',
    version='0.0.1',
    packages=['kivy_sight_glass'],
    include_package_data=True,
    url='https://github.com/clickworkorange/KivySightGlass',
    license='MIT',
    author='clickworkorange',
    author_email='info@clickworkorange.com',
    description='A dynamic bar graph emulating the appearance of liquid inside a sight glass',
    install_requires=["Kivy", "KivyGradient"],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
