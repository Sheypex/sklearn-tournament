import click

import sklearn_tournament

from sklearn_tournament import commons, distributions, model, tournament  # noqa: F401

###############################
# lib definitions and exports #
###############################
rc = commons.rc

# PickleOut = namedtuple("PickleOut", ["longname", "regr", "test_confidence", "polyDeg", "full_confidence", "unknown_confidence", "train_confidence", "bonusPickleInfo"]) # noqa
################################
# cli for standalone execution #
################################
context_settings = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=context_settings)
@click.version_option(sklearn_tournament.__version__, "--version")
def cli():
    pass


@cli.command()
@click.argument("arg")
@click.option(
    "--repeat", metavar="N", type=int, default=1, help="Repeat N times (optional)."
)
def echo(arg, repeat):
    for _ in range(repeat):
        click.echo(arg)


def main():
    cli()


if __name__ == "__main__":
    main()
