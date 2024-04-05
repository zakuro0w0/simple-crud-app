import pytest
from pydantic import ValidationError
from datetime import datetime
from zoneinfo import ZoneInfo
from app.domain import Task


# fixtureテストデータを共通化する
@pytest.fixture
# fixture関数の名前がテストケースにおける仮引数の名前と一致する
def task() -> Task:
    return Task(title="Test Task", description="This is a test task")


# pytestはtests/ディレクトリ配下の"test_*.py"ファイルに
# 記述された"test_*"関数をテストケースと見なす
def test_task_creation(task: Task):
    """
    Taskモデルのインスタンスが正しく生成されることを確認する。
    """
    assert task.title == "Test Task"
    assert task.description == "This is a test task"


def test_task_default_values(task: Task):
    """
    Taskモデルのデフォルト値が正しく設定されていることを確認する。
    """
    assert task.completed is False
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


def test_task_timezone(task: Task):
    """
    Taskモデルのタイムゾーンが正しく設定されていることを確認する。
    """
    jst = ZoneInfo("Asia/Tokyo")
    assert task.created_at.tzinfo == jst
    assert task.updated_at.tzinfo == jst


def test_task_completed():
    """
    Taskモデルのcompleted属性が正しく設定されることを確認する。
    """
    task = Task(title="Test Task", description="This is a test task", completed=True)
    assert task.completed is True


def test_task_model_validation_error():
    """
    Taskモデルのバリデーションエラーが発生することを確認する。
    """
    with pytest.raises(ValidationError):
        Task(
            title="Test Task",
            description="This is a test task",
            completed="not boolean",
        )
