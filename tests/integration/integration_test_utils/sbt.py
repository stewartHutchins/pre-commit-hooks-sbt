from pathlib import Path


def add_touch_command_to_sbt(project_root: Path, command_name: str) -> None:
    project_root.joinpath("project/TouchCommand.scala").write_text(
        f"""
import sbt.Command

import java.nio.file.{{Files, Paths}}

object TouchCommand {{
  def touchCommand = Command.args("{command_name}", "args") {{ (state, args) =>
    args.map(Paths.get(_).toAbsolutePath).foreach {{ path =>
      println(f"Creating file: $path")
      Files.createFile(path)
    }}
    state
  }}
}}
"""
    )

    project_root.joinpath("build.sbt").write_text(
        """
import TouchCommand._

ThisBuild / organization := "org.example"
ThisBuild / scalaVersion := "2.12.16"
ThisBuild / version      := "0.1.0-SNAPSHOT"

lazy val root = (project in file("."))
  .settings(
    commands ++= Seq(touchCommand)
  )
"""
    )


def add_sleep_command_to_sbt(project_root: Path, command_name: str) -> None:
    project_root.joinpath("project/EchoCommand.scala").write_text(
        f"""
import sbt.Command

object SleepCommand {{
  def sleepCommand = Command.single("{command_name}") {{ (state, arg) =>
    val waitSec = Integer.parseInt(arg)
    Thread.sleep(waitSec * 1000)
    state
  }}
}}
"""
    )

    project_root.joinpath("build.sbt").write_text(
        """
import SleepCommand._

ThisBuild / organization := "org.example"
ThisBuild / scalaVersion := "2.12.16"
ThisBuild / version      := "0.1.0-SNAPSHOT"

lazy val root = (project in file("."))
  .settings(
    commands ++= Seq(sleepCommand)
  )
"""
    )
