#!/usr/bin/env python3

"""generate-deployments"""

import importlib.metadata
import logging
from argparse import ArgumentParser
from argparse import Namespace as Args
from pathlib import Path
from shutil import copytree
from sys import stdout
from typing import Sequence, Union

from jinja2 import Environment, FileSystemLoader
from markdown import markdown

from .common import (
    LOG_LEVELS,
    create_hash,
    read_file,
    render,
    save_file,
    verify_password,
)

LOGGER_FORMAT = '[%(asctime)s] [%(levelname)-8s] [%(filename)-15s @'\
                ' %(funcName)-15s:%(lineno)4s] %(message)s'

# configure logging
logging.basicConfig(level=logging.INFO, format=LOGGER_FORMAT, stream=stdout)

logger = logging.getLogger("pcba_helper")
logger.setLevel(logging.DEBUG)


def does_exist(parser: ArgumentParser, arg: str) -> Path:
    if not Path(arg).resolve().exists():
        parser.error(f"{Path(arg).resolve()} does not exist")
    else:
        return Path(arg)


def parse_args(argv: Union[Sequence[str], None] = None) -> Args:
    """Multi command argument parser"""
    parser = ArgumentParser(__doc__)
    parser.add_argument(
        "--verbose", "-v",
        default=0,
        action="count",
        help="Set level of verbosity, default is CRITICAL",
    )

    parser.add_argument(
        "root",
        type=Path,
        help="Root directory with all files",
    )

    parser.add_argument(
        "--output",
        default=Path("deploy"),
        type=Path,
        help="Target directory for rendered files",
    )

    parser.add_argument(
        "--ibom-file",
        default="bom/ibom.html",
        type=Path,
        help="iBOM file",
    )

    parser.add_argument(
        "--username",
        default="John",
        help="Username for secure login",
    )

    parser.add_argument(
        "--password",
        default="secret",
        help="Password for secure login",
    )

    return parser.parse_args(argv)


def extract_version() -> str:
    """Returns version of installed package or the one of version.py"""
    try:
        from .version import __version__

        return f"{__version__}-dev"
    except ImportError:
        return importlib.metadata.version("pcba_helper")


def main() -> int:
    """Entry point for everything else"""
    args = parse_args()

    log_level = LOG_LEVELS[min(args.verbose, max(LOG_LEVELS.keys()))]
    logger.setLevel(level=log_level)
    logger.debug(f"{args}, {log_level}")

    repo_root = args.root.resolve()
    deploy_location = args.output.resolve()
    ibom_file = (repo_root / args.ibom_file).resolve()
    logger.debug(f"Repo root: {repo_root}")
    logger.debug(f"Deploy location: {deploy_location}")
    logger.debug(f"iBOM: {ibom_file}")

    _template_folder = (Path(__file__).parent / "templates").resolve()
    _overview_template = "overview.php.template"
    _php_index_template = "index.php.template"
    _php_auth_template = "auth.php.template"
    _php_template = "base.php.template"
    _env = Environment(
        loader=FileSystemLoader(searchpath=_template_folder),
        keep_trailing_newline=True
    )

    kicad_files = [x for x in repo_root.glob("*.kicad_pro") if x.is_file()]
    assert len(kicad_files) == 1
    logger.debug(f"Found KiCAD project file: {kicad_files[0]}")
    project_name = kicad_files[0].stem

    content = {
        "title": project_name,
        "schematic_name": f"{project_name}.pdf"
    }

    # render overview page, default after successful login
    save_file(
        filename=Path(f"{deploy_location}/overview.php"),
        content=render(env=_env, template=_overview_template, content=content),
    )

    # render changelog page
    html_changelog = markdown(read_file(filename=Path(f"{repo_root}/changelog.md")))
    save_file(
        filename=Path(f"{deploy_location}/changelog.php"),
        content=render(env=_env, template=_php_template, content={"content": html_changelog}),
    )

    # render ibom page
    html_ibom = read_file(filename=ibom_file)
    save_file(
        filename=Path(f"{deploy_location}/ibom.php"),
        content=render(env=_env, template=_php_template, content={"content": html_ibom}),
    )

    # render landing index page providing login form
    save_file(
        filename=Path(f"{deploy_location}/index.php"),
        content=render(env=_env, template=_php_index_template, content={"no_login": True}),
    )

    password = args.password
    php_hash = create_hash(password=password)
    logger.debug(f"Hash for specified password: {php_hash}")
    is_valid = verify_password(password=password, hash=php_hash)
    logger.debug(f"Password valid: {is_valid}")
    assert is_valid

    # render auth file with custom password
    save_file(
        filename=Path(f"{deploy_location}/php/auth.php"),
        content=render(env=_env, template=_php_auth_template, content={"generated_password_hash": php_hash, "username": args.username}),
    )

    # copy php folder and the files contained
    copytree(
        src=_template_folder / "php",
        dst=Path(f"{deploy_location}/php"),
        dirs_exist_ok=True
    )

    # copy static folder and the files contained
    copytree(
        src=_template_folder / "static",
        dst=Path(f"{deploy_location}/static"),
        dirs_exist_ok=True
    )

    return 0


if __name__ == "__main__":
    main()
