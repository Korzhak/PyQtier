import click
import subprocess

from .converter import convert_ui_to_py, convert_qrc_to_py
from .generator import create_project


@click.group()
def cli():
    pass


@cli.command()
def designer():
    """
    Opening qt5-tools designer
    :return: None
    """
    try:
        subprocess.run(['qt5-tools', 'designer'], check=True)
    except FileNotFoundError:
        click.echo("Error: Qt Designer not found. Please ensure qt5-tools is installed.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error launching Qt Designer: {e}")


@cli.command()
@click.argument('project_name')
@click.argument('project_path', required=False)
def startproject(project_name, project_path):
    """
    Creating a project with (pyqtier|pqr) command
    :param project_path: Write a '.' for creating project in current directory
    :param project_name: Name of project (automatically adding to config)
    :return: None
    """
    create_project(project_name, project_path)


@cli.command()
@click.argument('filename', required=False)
@click.option('--autorc', is_flag=True, default=False, help="Auto convert .qrc files after converting .ui files")
def convertui(filename, autorc):
    """
    Auto converting .ui files to .py
    :param filename: [optional] name of file to convert. Converting all of .ui if it didn't pass
    :param autorc: [optional] auto converting .qrc files after converting .ui files
    :return: None
    """
    convert_ui_to_py(filename, autorc)


@cli.command()
@click.argument('filename', required=False)
def convertqrc(filename):
    """
    Auto converting .qrc files to .py
    :param filename: [optional] name of file to convert. Converting all of .qrc if it didn't pass
    :return: None
    """
    convert_qrc_to_py(filename)
