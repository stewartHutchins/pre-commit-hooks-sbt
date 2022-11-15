Feature: scalafmt
  Code should be formatted by scalafmt

  Background:
    Given an sbt project with scalafmt configured

  Scenario: scala code is formatted
    Given there is an unformatted scala file src/main/scala/Main.scala
    When I run pre-commit
    Then the code in src/main/scala/Main.scala should be formatted

  Scenario: only code in the working tree is formatted
    Given there is an unformatted scala file src/main/scala/Main1.scala
    And there is an unformatted scala file src/main/scala/Main2.scala
    And the file src/main/scala/Main1.scala is in the commit history
    When I run pre-commit
    Then the code in src/main/scala/Main2.scala should be formatted
    And the code in the code in src/main/scala/Main1.scala should not be formatted
