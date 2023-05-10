'''
FUNCTIONAL TESTS - CLI FLASK
'''


def test_create_command(runner, app_with_db):

    # full command: flask questions create example
    # example - can be diffrent string
    result = runner.invoke(args=['questions', 'create', 'example'])
    assert "Questions collections example are created" in result.output
    assert result.exit_code == 0


def test_questions_count_command(runner, app_with_db):
    # full command: flask question count
    result = runner.invoke(args=['questions', 'count'])
    assert "total 3 questions with total 12 answers" in result.output
    assert result.exit_code == 0


def test_deleteall_command_when_canceled(runner, app_with_db):
    # full command: flask question deleteall
    # y - select 'y' to confirm deleting
    result = runner.invoke(args=['questions', 'deleteall'], input="n")
    assert result.exit_code == 1
    assert result.exception
    assert 'Aborted!' in result.output
    # out, err = capsys.readouterr()
    # assert out == "<class \'SystemExit\'>\n"
    # assert err == ''


def test_deleteall_command_when_confirmed_to_yes(runner, app_with_db, capsys):
    # full command: flask question deleteall
    # y - select 'y' to confirm deleting
    result = runner.invoke(args=['questions', 'deleteall'], input="y")
    assert result.exit_code == 0
    assert not result.exception
    assert "total 3 questions deleted with total 12 answers deleted" in result.output
