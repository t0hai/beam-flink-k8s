from invoke import Context, Result, task


@task
def lint_pep8(ctx):
    """Lint pep8 compliance with flake8

    Args:
        ctx (invoke.Context): invoke Context
    """
    print("Linting with flake8")
    ctx.run("flake8")


@task
def lint_types(ctx):
    """Lint types with mypy

    Args:
        ctx (invoke.Context): invoke Context
    """
    print("Linting with mypy")
    ctx.run("mypy")


@task
def lint_format(ctx):
    """Lint format with black

    Args:
        ctx (invoke.Context): invoke Context
    """
    print("Linting with black")
    ctx.run("black --check .")


@task
def lint_imports(ctx):
    """Lint imports with isort

    Args:
        ctx (invoke.Context): invoke Context
    """
    print("Linting imports with isort")
    ctx.run("isort **/*.py -c --atomic")


@task
def test(ctx):
    """Test with pytest

    Args:
        ctx (invoke.Context): invoke Context
    """
    print("Testing with pytest")
    ctx.run("pytest")


@task
def format(ctx):
    """Format code with black

    Args:
        ctx (invoke.Context): invoke Context
    """
    print("Formatting with black")
    ctx.run("black .")


@task
def sort_imports(ctx):
    """Sort imports with isort

    Args:
        ctx (invoke.Context): invoke Context
    """
    print("Sort imports with isort")
    ctx.run("isort **/*.py --atomic")


@task
def lint_commits(ctx, start=None, stop=None):
    """Lint commits with gitlint. Supply either a range or lint latest commit.

    Args:
        ctx (invoke.Context): invoke Context
        start (str, optional): Start commit ref. Defaults to None.
        stop (str, optional): End commit ref. Defaults to None.
    """
    print("Linting commits with gitlint")
    if start and stop:
        print(f"Commit range: {start}..{stop}")
        # --ignore-stdin flag is needed because of this issue:
        # https://github.com/jorisroovers/gitlint/issues/91
        ctx.run(f'gitlint --ignore-stdin --commits "{start}..{stop}"')
    else:
        print("Linting latest commit")
        ctx.run("gitlint --ignore-stdin")


@task(pre=[lint_format, lint_types, lint_pep8, lint_imports, lint_commits])
def lint(ctx):
    """Perform all linting tasks

    Args:
        ctx (invoke.Context): invoke Context
    """
    pass


@task
def docker_build(ctx):
    """Build docker image
    Args:
        ctx (invoke.Context): invoke Context
    """
    print("docker build")
    ctx.run("docker build -t lambdas-enrichment .")


@task(pre=[docker_build])
def docker_run(ctx):
    """Run docker container (in detached mode)
    Args:
        ctx (invoke.Context): invoke Context
    """
    print("docker run")
    ctx.run(
        "docker run -p 9000:8080 --env-file .env --rm --name lambda -d lambdas-enrichment"
    )


@task
def docker_test(ctx):
    """Test docker container locally (needs curl to be installed)
    Args:
        ctx (invoke.Context): invoke Context
    """
    print("sending test payload to container")
    # TODO: create a more realistic payload
    ctx.run(
        """
        curl -s -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" \
            -d '{"requestId": "foo-bar", "Records": []}'
        """
    )


@task
def docker_stop(ctx):
    """Stop docker container
    Args:
        ctx (invoke.Context): invoke Context
    """
    print("docker stop")
    ctx.run("docker stop lambda")
