## pre-commit SBT

A set of [pre-commit](https://pre-commit.com) hooks which integrate with [SBT](https://www.scala-sbt.org/).

### Why use pre-commit?

If you're not familiar with `pre-commit` and the benefits of having pre-commit hooks, please take a look
at: [pre-commit.com](https://pre-commit.com)

### Why use this project?

Having understood how pre-commit works you may be inspired to create a pre-commit hook which runs a command
like: `sbt <your-command>`, however this might be slow.

Dependent on the size and complexity of your project it can take significant time to run a command, this is
usually because SBT must load your plugins, settings, project definitions, etc. If we were trying to run 3
commands this overhead would happen 3 times. To avoid this overhead developers will usually start SBT and then use the
tool's console as and when needed. This project uses the same approach. Using SBT's network access we can run commands
in SBT without the need to (re-)start SBT.

This project runs SBT commands via the network access. If SBT server isn't running, it will fall back to running a
command via the commandline.

### Available Hooks

- scalafmt (see: [Configuring the scalafmt hook](#configuring-the-scalafmt-hook))

#### Using the scalafmt hook

1) Add the scalafmt plugin to your sbt
   configuration ([scalafmt installation](https://scalameta.org/scalafmt/docs/installation.html#sbt)), and configure the
   plugin with your preferences ([scalafmt config](https://scalameta.org/scalafmt/docs/configuration.html)).
2) Add the following to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/stewartHutchins/pre-commit-sbt
    rev: <version>
    hooks:
      - id: scalafmt
```

3) (optionally) Add the following to your `build.sbt`:

```sbt
ThisBuild / scalafmtFilter := "diff-dirty"
```

This will only format files in your working tree (i.e. the files you're currently working on). If you don't include
this, you may find that all the files in your project get formatted, leading to a confusing working tree or messy git
history.
