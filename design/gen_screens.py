#!/usr/bin/env python3
"""design/od/screens/*.html 생성기 — screens.md 구성표대로."""
import os

ROOT = os.path.join(os.path.dirname(__file__), "od", "screens")
os.makedirs(ROOT, exist_ok=True)

def icon(name, size=24):
    return (f'<svg class="icon" data-icon="{name}" width="{size}" height="{size}">'
            f'<use href="../icons.svg#i-{name}"/></svg>')

def head(title):
    return (f'<!DOCTYPE html>\n<html lang="ko">\n<head>\n<meta charset="UTF-8">\n'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            f'<title>한장 — {title}</title>\n'
            f'<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;600;700&family=Noto+Serif+KR:wght@600;700&display=swap" rel="stylesheet">\n'
            f'<link rel="stylesheet" href="../tokens.css">\n'
            f'<link rel="stylesheet" href="../components.css">\n</head>\n<body>\n')

def appbar(title, action=None):
    act = (f'<div class="app-bar-actions"><button class="icon-button icon-button-md" '
           f'aria-label="{action[1]}">{icon(action[0])}</button></div>' if action
           else '<div class="app-bar-actions"></div>')
    return (f'<header class="app-bar"><div class="app-bar-actions"></div>'
            f'<h1 class="app-bar-title t-h3">{title}</h1>{act}</header>')

def navheader(title, center="", exits=True):
    right = (f'<div class="nav-header-actions"><button class="icon-button icon-button-md" '
             f'aria-label="나가기">{icon("door-open")}</button></div>' if exits
             else '<div class="nav-header-actions"></div>')
    return (f'<header class="nav-header"><button class="icon-button icon-button-md" '
            f'aria-label="뒤로">{icon("chevron-left")}</button>'
            f'<div class="nav-header-center">{center}</div>'
            f'<h1 class="nav-header-title t-h3">{title}</h1>{right}</header>')

TABS = [("home","홈"),("library","자료실"),("bookmark","저장"),("history","복습"),("user","마이")]
def tabbar(active):
    items = "".join(
        f'<button class="tab-bar-item{" is-active" if label==active else ""}" aria-label="{label}">'
        f'{icon(i)}<span class="t-caption">{label}</span></button>' for i, label in TABS)
    return f'<nav class="tab-bar">{items}</nav>'

def card(title, desc="", meta="", action_icon=None, primary=None):
    a = (f'<button class="icon-button icon-button-md card-action" aria-label="북마크">'
         f'{icon(action_icon)}</button>') if action_icon else ''
    if primary:
        a += f'<button class="button button-primary button-md">{primary}</button>'
    d = f'<p class="card-desc t-body-sm">{desc}</p>' if desc else ''
    m = f'<p class="card-meta t-caption">{meta}</p>' if meta else ''
    return (f'<div class="card"><div class="card-row"><div>'
            f'<h2 class="card-title t-body">{title}</h2>{d}{m}</div>{a}</div></div>')

def bottomcta(label, loading=False):
    cls = "button button-primary button-lg button-full"
    if loading: cls += " is-loading"
    return f'<div class="bottom-cta"><button class="{cls}">{label}</button></div>'

def listrow(title, meta=""):
    m = f'<span class="list-row-meta t-caption">{meta}</span>' if meta else ''
    return f'<div class="list-row"><span class="list-row-title t-body">{title}</span>{m}</div>'

def choices(n=5, correct=None, wrong=None, words=None):
    labels = words or ["첫 번째 선지","두 번째 선지","세 번째 선지","네 번째 선지","다섯 번째 선지","여섯 번째 선지"][:n]
    out = ['<div class="choice-list">']
    for i in range(n):
        cls, mark = "choice", ""
        if correct is not None and i == correct:
            cls += " is-correct"; mark = '<span class="choice-mark">✓ 정답</span>'
        elif wrong is not None and i == wrong:
            cls += " is-wrong"; mark = '<span class="choice-mark">내 선택</span>'
        out.append(f'<button class="{cls}"><span class="choice-index t-label">{i+1}</span>'
                   f'<span class="choice-text t-body">{labels[i]}</span>{mark}</button>')
    out.append('</div>')
    return "".join(out)

def screen(body, tab=None, cta=None, extra=""):
    cls = "screen-body"
    if cta and tab: cls += " screen-body--has-cta-tab-bar"
    elif cta: cls += " screen-body--has-cta"
    elif tab: cls += " screen-body--has-tab-bar"
    return (f'<main class="screen">{body}<div class="{cls}">{extra}</div>'
            f'{cta or ""}{tabbar(tab) if tab else ""}</main>\n</body>\n</html>')

def empty_state(msg, btn):
    return (f'<div class="empty-state"><div class="empty-state-icon">{icon("inbox",24)}</div>'
            f'<p class="empty-state-desc t-body">{msg}</p>'
            f'<button class="button button-primary button-md empty-state-action">{btn}</button></div>')

def loading_cards(n=3):
    return "".join('<div class="skeleton-card"><div class="skeleton-line"></div>'
                   '<div class="skeleton-line skeleton-line-sm"></div></div>' for _ in range(n))

def error_state(msg="불러오지 못했어요"):
    return (f'<div class="error-state"><div class="error-state-icon">{icon("alert-circle",24)}</div>'
            f'<p class="error-state-desc t-body">{msg} 다시 시도할 수 있어요</p>'
            f'<button class="button button-secondary button-md error-state-action">다시 시도</button></div>')

OFFLINE = ('<div class="offline-banner"><span class="t-caption">'
           '오프라인 — 마지막으로 저장된 내용을 보여줘요</span></div>')

files = {}
def put(slug, state, content):
    files[f"{slug}-{state}.html"] = content

def common_states(slug, header, tab, extra, cta=None, long_marker=None):
    """필수 상태: empty·loading·error·long-title·many-items·text-120"""
    put(slug, "empty", head(slug) + screen(header, tab=tab, cta=cta,
        extra=empty_state("표시할 내용이 없어요", "새로고침")))
    put(slug, "loading", head(slug) + screen(header, tab=tab, cta=cta, extra=loading_cards()))
    put(slug, "error", head(slug) + screen(header, tab=tab, cta=cta, extra=error_state()))
    long = extra.replace("수능 국어", "수능 국어 영역 전체 범위 모의고사 기출 문제집", 1) \
        if "수능 국어" in extra else extra + card("아주 긴 제목의 시험지 카드 예시 텍스트입니다 정말로 깁니다")
    put(slug, "long-title", head(slug) + screen(header, tab=tab, cta=cta, extra=long))
    many = extra + card("추가 회차 2025 3월 모의평가 국어", "기출", "80분 · 45문항", "star") \
        + card("추가 회차 2024 9월 모의평가 국어", "기출", "80분 · 45문항", "star")
    put(slug, "many-items", head(slug) + screen(header, tab=tab, cta=cta, extra=many))
    put(slug, "text-120", head(slug) + screen(header, tab=tab, cta=cta, extra=extra))

# ── login ──
login_body = ('<div class="empty-state"><div class="logo t-display">한장</div>'
              '<p class="empty-state-desc t-body">시험지 한 장을 펼쳐 시간 안에 풉니다</p></div>')
login_cta = ('<div class="bottom-cta"><button class="button button-primary button-lg button-full">카카오로 시작</button>'
             '<button class="button button-secondary button-lg button-full">전화번호로 시작</button></div>')
put("login", "default", head("로그인") + screen("", cta=login_cta, extra=login_body))
common_states("login", "", None, login_body, cta=login_cta)

# ── home ──
home_extra = (
    '<div class="card"><div class="card-row"><div>'
    '<h2 class="card-title t-body">이어하기</h2>'
    '<p class="card-desc t-body-sm">2025학년도 수능 국어</p>'
    '<p class="card-meta t-caption">남은 시간 42:10</p></div>'
    f'<button class="button button-primary button-md card-action">이어하기</button></div>'
    '<div class="progress-bar"><div class="progress-bar-fill"></div></div></div>'
    + card("오늘의 퀴즈", "OX · 빈칸 · 영단어 · 한국사", "10문제 세트")
    + card("최근 발행", "2025 9월 모의평가 국어", "외 2회차"))
put("home", "default", head("홈") + screen(appbar("한장"), tab="홈", extra=home_extra))
common_states("home", appbar("한장"), "홈", home_extra)
files["home-empty.html"] = head("홈") + screen(appbar("한장"), tab="홈",
    extra=empty_state("진행 중인 시험이 없어요", "자료실에서 고르기"))

# ── library ──
lib_cards = (card("2025학년도 수능 국어", "화법·언어·독서·문학", "80분 · 45문항", "star", primary="풀기")
             + card("2025 9월 모의평가 국어", "한국교육과정평가원", "80분 · 45문항", "star")
             + card("2024학년도 수능 국어", "기출", "80분 · 45문항", "star")
             + card("2025 6월 모의평가 국어", "한국교육과정평가원", "80분 · 45문항", "star"))
put("library", "default", head("자료실") + screen(appbar("자료실"), tab="자료실", extra=lib_cards))
common_states("library", appbar("자료실"), "자료실", lib_cards)
files["library-empty.html"] = head("자료실") + screen(appbar("자료실"), tab="자료실",
    extra=empty_state("아직 발행된 시험지가 없어요", "새로고침"))
put("library", "offline", head("자료실") + screen(appbar("자료실") + OFFLINE, tab="자료실", extra=lib_cards))

# ── saved ──
saved_cards = card("2025 9월 모의평가 국어", "북마크됨", "80분 · 45문항", "star", primary="풀기")
put("saved", "default", head("저장") + screen(appbar("저장"), tab="저장", extra=saved_cards))
common_states("saved", appbar("저장"), "저장", saved_cards)
files["saved-empty.html"] = head("저장") + screen(appbar("저장"), tab="저장",
    extra=empty_state("저장한 시험지가 없어요", "자료실에서 고르기"))

# ── review ──
rev_cards = (card("2025 9월 모의평가 국어", "채점 완료", "정답 4/5 · 어제", primary="다시 보기")
             + card("2024학년도 수능 국어", "채점 완료", "정답 3/5 · 3일 전"))
put("review", "default", head("복습") + screen(appbar("복습"), tab="복습", extra=rev_cards))
common_states("review", appbar("복습"), "복습", rev_cards)
files["review-empty.html"] = head("복습") + screen(appbar("복습"), tab="복습",
    extra=empty_state("아직 채점한 시험이 없어요", "시험지 풀기"))

# ── my ──
my_extra = (listrow("계정", "카카오 연결됨") + listrow("앱 버전", "1.0.0")
            + '<button class="button button-primary button-lg button-full">로그아웃</button>')
put("my", "default", head("마이") + screen(appbar("마이"), tab="마이", extra=my_extra))
common_states("my", appbar("마이"), "마이", my_extra)

# ── exam ──
exam_head = navheader("국어", '<span class="timer t-h1">41:58</span>')
exam_img = ('<div class="passage-image"><p class="t-body-sm">[지문] 다음 글을 읽고 물음에 답하시오. '
            '세부 내용은 지문 이미지로 제공된다.</p></div>')
exam_extra = exam_img + choices(5, correct=1)
put("exam", "default", head("시험지") + screen(exam_head, cta=bottomcta("제출"), extra=exam_extra))
put("exam", "grading", head("시험지") + screen(exam_head, cta=bottomcta("제출", loading=True), extra=exam_extra))
put("exam", "graded", head("시험지") + screen(exam_head, cta=bottomcta("제출"),
    extra=exam_img + choices(5, correct=1, wrong=2)))
put("exam", "offline", head("시험지") + screen(exam_head + OFFLINE, cta=bottomcta("제출"), extra=exam_extra))
common_states("exam", exam_head, None, exam_extra, cta=bottomcta("제출"))

# ── exam-result ──
res_extra = ('<div class="card"><div class="card-row"><div>'
             '<h2 class="card-title t-h1">정답 4/5</h2>'
             '<p class="card-desc t-body-sm">2025 9월 모의평가 국어</p></div></div></div>'
             + listrow("1번 문항", "정답") + listrow("2번 문항", "오답 — ④ 선택")
             + listrow("3번 문항", "정답") + listrow("4번 문항", "정답") + listrow("5번 문항", "정답"))
put("exam-result", "default", head("결과") + screen(navheader("결과", exits=False),
    cta=bottomcta("자료실로"), extra=res_extra))
common_states("exam-result", navheader("결과", exits=False), None, res_extra, cta=bottomcta("자료실로"))

# ── quiz-play ──
quiz_head = navheader("영단어 퀴즈", '<span class="t-label">3 / 10</span>')
quiz_extra = ('<div class="progress-bar"><div class="progress-bar-fill"></div></div>'
              '<div class="card"><span class="t-caption">EN → KO</span>'
              '<h2 class="card-title t-h1">"apple"을 뜻하는 것은?</h2>'
              '<p class="card-desc t-body-sm">다음 중 알맞은 뜻을 고르세요</p></div>'
              + choices(6, correct=1, words=["바나나","사과","포도","복숭아","귤","수박"])
              + '<div class="tf-row"><button class="tf-button is-correct">O</button>'
                '<button class="tf-button">X</button></div>')
put("quiz-play", "default", head("퀴즈 플레이") + screen(quiz_head, cta=bottomcta("다음 문제"), extra=quiz_extra))
put("quiz-play", "feedback", head("퀴즈 플레이") + screen(quiz_head, cta=bottomcta("다음 문제"),
    extra=quiz_extra.replace('is-correct">O', 'is-selected">O')))
common_states("quiz-play", quiz_head, None, quiz_extra, cta=bottomcta("다음 문제"))

# ── quiz-result ──
qres_extra = ('<div class="score-ring"><div class="t-display">8/10</div>'
              '<p class="t-caption">정답</p></div>'
              + listrow("apple — 사과", "오답: 바나나 선택")
              + listrow("run — 달리다", "오답: 걷다 선택"))
put("quiz-result", "default", head("퀴즈 결과") + screen(navheader("퀴즈 결과", exits=False),
    cta=bottomcta("홈으로"), extra=qres_extra))
common_states("quiz-result", navheader("퀴즈 결과", exits=False), None, qres_extra, cta=bottomcta("홈으로"))

# 시험지-error는 common_states가 생성함 (error_state 교체) — default 마크업 유지 위해 덮어씀
files["exam-error.html"] = head("시험지") + screen(exam_head, cta=bottomcta("제출"),
    extra=error_state("채점에 실패했어요"))
files["quiz-play-error.html"] = head("퀴즈 플레이") + screen(quiz_head, cta=bottomcta("다음 문제"),
    extra=error_state("문제를 불러오지 못했어요"))

for name, content in files.items():
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(content)
print(f"wrote {len(files)} files")
