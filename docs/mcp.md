# 한장 — MCP

admin이 BO 대신 MCP 도구로 문항·퀴즈를 넣는 채널. 데이터 경로는 BO와 같다 — 같은 서비스, 같은 테이블.

---

## 1. 위치

`hanjang-be`의 `mcp` 모듈. Streamable HTTP, `POST /mcp`.

```
MCP 클라이언트 --Bearer admin JWT--> POST /mcp --> question/quiz 서비스 --> hanjang-postgres
```

## 2. 인증

- `Authorization: Bearer <admin JWT>`
- JWT는 BO 로그인(아이디·비밀번호)으로 발급한 것
- 수험생 토큰, 토큰 없음 → `401`. admin 아닌 클레임 → `403`

## 3. 도구

| 도구 | 인자 | 결과 |
| --- | --- | --- |
| `list_exam_papers` | `published?` | 시험지 id·제목 목록. 문항 넣을 대상을 고르는 용도 |
| `add_question` | `examPaperId`, `number`, `prompt`, `passageImageUrl?`, `choices[]`, `answer` | 생성된 Question id |
| `add_quiz` | `type: 'ox' \| 'cloze' \| 'word' \| 'history'`, `prompt`, `choices[]`, `answer`, `direction?: 'en-ko' \| 'ko-en'` | 생성된 Quiz id |

발행·수정·삭제는 열지 않는다. 추가만.

## 4. 검증

- `add_question`: `choices` 2~6, `answer`는 choices 안의 값, 같은 `examPaperId + number` 중복 거부
- `add_quiz`: `type = ox`면 choices 정확히 2, `word`면 6, `direction`은 `word`에서만 의미 있음

검증 규칙은 BO 입력 검증과 같은 코드를 쓴다. MCP 전용 규칙을 만들지 않는다.

## 5. 연결 예시

```json
{
  "mcpServers": {
    "hanjang": {
      "url": "https://<be-host>/mcp",
      "headers": { "Authorization": "Bearer <admin JWT>" }
    }
  }
}
```

로컬은 `http://localhost:<port>/mcp`.

## 6. 안 하는 것

- 수험생 데이터(User, ExamSession, Answer) 조회·수정 도구
- 콘텐츠 발행·삭제 도구
- 토큰 발급 도구 — 토큰은 BO 로그인에서만 나온다

## 7. 완료

- `add_question`으로 넣은 문항이 BO 문항 목록에 보인다
- `add_quiz`로 넣은 퀴즈가 발행되면 FO 오늘의 퀴즈에 나온다
- 수험생 토큰으로 호출하면 403
