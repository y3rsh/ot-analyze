# ot-analyze

Github action to analyze Opentrons protocols

## Inputs

## `BASE_DIRECTORY`

**Required** The topmost directory to search for protocols to analyze.

- default directory is protocols
- The action will search this directory and all descendant directories for protocols to analyze.
- Both Python and Protocol Library protocols will be analyzed.

## Outputs

## TODO

## Custom Labware

If your protocol uses custom labware, you must include it in a `custom_labware` directory in the same directory as the protocol. The action will automatically include it in the analysis.

## Example usage

<https://github.com/y3rsh/ot-analyze-test>

 Adding the following to your workflow will analyze your protocols and you may see the results in the Actions tab of your repository.

```yml
 - name: Analyze
        uses: y3rsh/ot-analyze@v1.18
```

Add the the following to your workflow to analyze your protocols and create a pull request with the results.

```yml
- name: Analyze
        uses: y3rsh/ot-analyze@v1.18
- name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          base: ${{ github.head_ref }}
```

## Development

- on Linux, have python 3.10, pip, and make installed
- `make setup` to install dependencies
- uses venv and requirements.txt
