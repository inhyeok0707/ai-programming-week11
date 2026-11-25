import pytest
from load_scores import load_scores
from helpers import 쓰기


def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5


def test_빈_줄은_건너뛴다():
    with open("임시.csv", "w", encoding="utf-8") as f:
        f.write("name,score\n김하나,88\n\n이두리,90\n\n")
    kept, skipped = load_scores("임시.csv")
    assert kept == [("김하나", 88), ("이두리", 90)]
    assert skipped == []


def test_이름에_쉼표가_있어도_읽는다():
    with open("임시.csv", "w", encoding="utf-8") as f:
        f.write('name,score\n"김, 하나",88\n')
    kept, skipped = load_scores("임시.csv")
    assert kept == [("김, 하나", 88)]


def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")


def test_헤더만_있으면_빈_결과가_나온다():
    kept, skipped = load_scores("empty.csv")
    assert kept == []
    assert skipped == []


@pytest.mark.parametrize("점수, 유효한가", [
    (-1, False),   # 경계 바로 아래
    (0, True),     # ★ 아래쪽 경계
    (1, True),
    (99, True),
    (100, True),   # ★ 위쪽 경계
    (101, False),  # 경계 바로 위
])
def test_점수_경계값(점수, 유효한가):
    쓰기(f"임시.csv", 점수)
    kept, skipped = load_scores("임시.csv")
    assert (len(kept) == 1) == 유효한가

def test_이름이_비면_건너뛰고_기록한다():
    with open("임시.csv", "w", encoding="utf-8") as f:
        f.write("name,score\n,90\n")
    kept, skipped = load_scores("임시.csv")
    assert kept == []
    assert skipped == [(2, ",90", "이름이 비어 있음")]