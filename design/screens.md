status: confirmed
confirmed_at: 2026-09-16

# Screens — 한장

구성은 위→아래 순서. 원문자 번호는 최종 미리보기 폰 프레임의 라벨과 같다 (화면당 최대 5개).

| 순번 | 화면 | slug | 구성 (위→아래) | 상태 프레임 |
|---|---|---|---|---|
| 1 | 로그인 | login | ① Logo(한장 serif) · ② Button(카카오로 시작 primary lg) · ③ Button(전화번호 secondary) · BottomCta · EmptyState · ScreenBody | default·error |
| 2 | 홈 | home | ① AppBar(한장) · ② Card(이어하기+primary 버튼+진행바) · ③ Card(오늘의 퀴즈) · ④ Card(최근 발행) · ⑤ TabBar · ScreenBody · ProgressBar · IsActive · Button | default·empty·loading·error |
| 3 | 자료실 | library | ① AppBar(자료실) · ② Card(회차+star 북마크+primary 풀기) · ③ TabBar · ScreenBody · IconButton · IsActive · Button | default·empty·loading·error·offline |
| 4 | 저장 | saved | ① AppBar(저장) · ② Card(북마크됨+primary 풀기) · ③ TabBar · ScreenBody · IconButton · IsActive · Button | default·empty·loading |
| 5 | 복습 | review | ① AppBar(복습) · ② Card(채점 완료+primary 다시보기) · ③ TabBar · ScreenBody · IsActive · Button | default·empty·loading |
| 6 | 마이 | my | ① AppBar(마이) · ② ListRow(계정 카카오 연결됨) · ③ Button(로그아웃 primary) · ④ TabBar · ScreenBody · IsActive | default |
| 7 | 시험지 | exam | ① NavHeader(뒤로+나가기) · ② Timer(serif 41:58) · ③ PassageImage(지문 contain+펜 밑줄) · ④ Choice(선지 5 정오) · ⑤ BottomCta(제출) · ScreenBody · IconButton · IsCorrect · Button | default·grading·graded·error·offline |
| 8 | 결과 | exam-result | ① NavHeader · ② Card(점수 요약 serif 4/5) · ③ ListRow(문항별 정오) · ④ BottomCta(자료실로) · ScreenBody · IconButton · Button | default |
| 9 | 퀴즈 플레이 | quiz-play | ① NavHeader(뒤로+진행 n/10) · ② ProgressBar · ③ Card(문항 serif) · ④ Choice(선지 6) · ⑤ TfRow(OX 변형) · TfButton · BottomCta(다음 문제) · ScreenBody · IconButton · IsCorrect · Button | default·feedback·error |
| 10 | 퀴즈 결과 | quiz-result | ① NavHeader · ② ScoreRing(8/10) · ③ ListRow(틀린 문항) · ④ BottomCta(홈으로) · ScreenBody · IconButton · Button | default |

## 사용자 수정 이력

| 화면 | 변경 | 원문 | 회차 |
|---|---|---|---|
