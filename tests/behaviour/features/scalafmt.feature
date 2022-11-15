Feature: scalafmt
  Code should be formatted by scalafmt

  Background:
    Given an sbt project with scalafmt configured

  Scenario: scala code is formatted
    Given there is an unformatted scala file in src/
    When I run pre-commit
    Then the code should be formatted
