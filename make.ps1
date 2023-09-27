<#
.SYNOPSIS
Makefile

.DESCRIPTION
USAGE
    .\make.ps1 <command>

COMMANDS
    init              install Python build tools
    install-dev       install local package in editable mode
    update-deps       update the dependencies
    upgrade-deps      upgrade the dependencies
    lint              run `pre-commit` and `black` and `ruff`
    test              run `pytest`
    build-dist        run `python -m build`
    clean             delete generated content
    help, -?          show this help message
#>
param(
    [Parameter(Position = 0)]
    [ValidateSet("init", "install-dev", "update-deps", "upgrade-deps", "lint", "test", "build-dist", "clean", "help")]
    [string]$Command
)

function Invoke-Help
{
    Get-Help $PSCommandPath
}

function Invoke-Init
{
    python -m pip install --upgrade pip wheel setuptools build
}

function Invoke-Install-Dev
{
    python -m pip install --upgrade --editable ".[dev, tests, docs]"
}

function Invoke-Update-Deps
{
    python -m pip install --upgrade --editable ".[dev, tests, docs]"
    python -m pip install --upgrade pip-tools
    cd requirements
    pip-compile --resolver=backtracking requirements.in --output-file requirements.txt
    pip-compile --resolver=backtracking requirements-dev.in --output-file requirements-dev.txt
    pip-compile --resolver=backtracking requirements-tests.in --output-file requirements-tests.txt
    pip-compile --resolver=backtracking requirements-docs.in --output-file requirements-docs.txt
}

function Invoke-Upgrade-Deps
{
    python -m pip install --upgrade pip-tools pre-commit
    pre-commit autoupdate
    cd requirements
    pip-compile --resolver=backtracking --upgrade requirements.in --output-file requirements.txt
    pip-compile --resolver=backtracking --upgrade requirements-dev.in --output-file requirements-dev.txt
    pip-compile --resolver=backtracking --upgrade requirements-tests.in --output-file requirements-tests.txt
    pip-compile --resolver=backtracking --upgrade requirements-docs.in --output-file requirements-docs.txt
}

function Invoke-Lint
{
    pre-commit run --all-files
    python -m black .
    python -m ruff --fix .
}

function Invoke-Test
{
    python -m pytest
}

function Invoke-Build-Dist
{
    python -m pip install --upgrade build
    python -m build
}

function Invoke-Clean
{
    $folders = @("build", "dist")
    foreach ($folder in $folders)
    {
        if (Test-Path $folder)
        {

            Write-Verbose "Deleting $folder"
            Remove-Item $folder -Recurse -Force
        }
    }
}

switch ($Command)
{
    "init"    {
        Invoke-Init
    }
    "install-dev" {
        Invoke-Install-Dev
    }
    "lint"  {
        Invoke-Lint
    }
    "update-deps"  {
        Invoke-Update-Deps
    }
    "upgrade-deps"  {
        Invoke-Upgrade-Deps
    }
    "test"    {
        Invoke-Test
    }
    "build-dist"    {
        Invoke-Build-Dist
    }
    "clean"    {
        Invoke-Clean
    }
    "help"  {
        Invoke-Help
    }
    default
    {
        Invoke-Init
        Invoke-Install-Dev
    }
}
