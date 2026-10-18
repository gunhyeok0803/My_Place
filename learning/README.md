# 학습 기록 — Claude를 학습 튜터로

자세 습관 알림 의자 트윈을 만들며 처음인 것 ①~⑧을 Claude로 배운 기록이다. 최종 발표 "AI로 배운 것"과 AI 사용 내역의 근거가 된다.

- 계획: [ai-study-plan.md](../proposal/ai-study-plan.md) · 튜터 지침: [CLAUDE.md](../CLAUDE.md) (Claude Code) · 설정 기록: [00-setup](00-setup/README.md)
- **배운 것 = 처음 내 설명과 배운 뒤 내 설명의 차이 + 그 지식으로 내린 결정**

## 진행 현황

| 칸 | 주차 | 상태 | 학습 노트 |
|---|---|---|---|
| 0 초기 셋팅 (A 배선 · B 방석 부착) | 부품 도착 후 · B는 ① 확인 뒤 | 시작 전 | [순서](00-setup/hardware-setup.md) — "0번 시작" |
| ① 압력센서 회로 · ADC | 9주 (10/27~) | 시작 전 | [노트](01-circuit-adc/README.md) |
| ② 3D 압력 색상 지도 | 10주 (11/3~) | 시작 전 | [노트](02-color-map/README.md) |
| ③ 비율 + 기준값 판정 | 10주 (11/3~) | 시작 전 | [노트](03-ratio-judgment/README.md) |
| ④ 측정 기록 · 분포 비교 | 11주 (11/10~) | 시작 전 | [노트](04-recording-distribution/README.md) |
| ⑤ 깜빡임 방지 · 센서 확인 | 11주 (11/10~) | 시작 전 | [노트](05-debounce-sensor-check/README.md) |
| ⑥ 나쁜 자세 알림 | 12주 (11/17~) | 시작 전 | [노트](06-posture-alert/README.md) |
| ⑦ 오늘의 자세 시간 | 12주 (11/17~) | 시작 전 | [노트](07-daily-posture-time/README.md) |
| ⑧ MQTT 재연결 | 13주 (11/24~) | 시작 전 | [노트](08-mqtt-reconnect/README.md) |

상태는 `시작 전 → 진행 중 → 완료`로 바꾼다.

## 칸 하나를 배우는 순서와 캡처

| 단계 | 하는 일 | 캡처 파일 |
|---|---|---|
| ① 시작 전 설명 | AI 없이 지금 아는 만큼 3줄 | `YYYY-MM-DD_1-before.png` |
| ② 개념 · 힌트 | 정답 대신 원리, 힌트는 한 단계씩 | `YYYY-MM-DD_2-hint.png` |
| ③ 미니 프로젝트 | 30분 직접 만들고 Claude가 리뷰 | `YYYY-MM-DD_3-mini.png` |
| ④ 거꾸로 설명 | 내가 설명하고 틀린 곳만 지적받기 | `YYYY-MM-DD_4-teachback.png` |
| ⑤ 적용 · 노트 | 본 프로젝트에 넣고 결정과 이유 기록 | `YYYY-MM-DD_5-applied.png` (영상은 `.mp4`) |

- 캡처에 이메일 · 계정 정보가 보이면 잘라 낸다.
- 캡처와 함께 Claude 세션 기록(내보내기 파일)을 그 칸 폴더에 남긴다.
