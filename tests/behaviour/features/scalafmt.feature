Feature: scalafmt
  Code should be formatted by scalafmt

  Background:
    Given a sbt project with scalafmt

  Scenario: scala code is formatted
    Given there is unformatted code in src/main/scala/Main.scala
    And I git add src/main/scala/Main.scala
    When I run pre-commit
    Then the code in src/main/scala/Main.scala should be formatted

  Scenario: sbt code is formatted
    Given there is unformatted code in build.sbt
    And I git add build.sbt
    When I run pre-commit
    Then the code in build.sbt should be formatted

  Scenario: only staged code is formatted
    Given there is unformatted code in src/main/scala/Main1.scala
    And the file src/main/scala/Main1.scala is in the commit history
    And there is unformatted code in src/main/scala/Main2.scala
    And I git add src/main/scala/Main2.scala
    And there is unformatted code in src/main/scala/Main3.scala
    When I run pre-commit
    Then the code in src/main/scala/Main2.scala should be formatted
    And the code in the code in src/main/scala/Main1.scala should not be formatted
    And the code in the code in src/main/scala/Main3.scala should not be formatted
