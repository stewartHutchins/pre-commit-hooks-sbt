## pre-commit SBT
A set of [pre-commit](https://pre-commit.com) hooks which integrate with [SBT](https://www.scala-sbt.org/).


### Available Hooks
- scalafmt - formats scala code using the SBT scalafmt plugin.

### Usage
Add the following to your `.pre-commit-config.yaml` file.
```yaml
- repo: https://github.com/stewartHutchins/pre-commit-sbt
  rev: <version>
  hooks:
  - id: <hook name>
```
(Plugins may also require additional config)
