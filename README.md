# My Place — 실감 피지컬 컴퓨팅

내 방을 3D로 재현하고, 방 안의 실물을 센서와 연결하는 디지털 트윈 과제 저장소입니다.

**🔗 [브라우저에서 보기](https://gunhyeok0803.github.io/My_Place/splat-twin.html)**

## 개요

| | 내용 |
|---|---|
| 대상 공간 | 내 방 (약 4.5 × 2.5 m, 천장 2.17 m) |
| 대상 물체 | 의자 · 책상 · 안마의자 |
| 접근 | 박스 모델 → Gaussian Splat 스캔 → 센서 연동 |

세 물체에 붙일 예상 기능은 각각 **의자 = 자세 교정 알림**, **책상 = 적치 알림**, **안마의자 = 전원 감지**입니다.

## 진행 현황

| 주차 | 내용 | 산출물 | 상태 |
|---|---|---|---|
| 2주차 | 방 치수 측정 · 박스 방 · 안마의자 모델링 | `room-template.html`, `massage_chair_model.glb` | ✅ |
| 3주차 | 방 스캔 · SuperSplat 정리 · 브라우저 배포 | `splat-twin.html`, `assets/room.spz` | ✅ |
| 4주차 | 의자 분리 후 공간에 배치 | `assets/chair.spz` | ⬜ |
| 5주차 | 센서 → MQTT → 오브젝트 연동 | — | ⬜ |
| 6주차 | Propasal | — | ⬜ |

---

### 2주차 — 박스 방과 물체 모델

실제 방의 가로·세로·높이를 재고 바닥·벽·주요 가구를 박스로 세웠습니다. 안마의자는 Blender에서 AI 기반으로 생성한 뒤 실제 모습에 맞게 수정했습니다.

- `room-template.html` — 실측 치수를 반영한 박스 방
- `assets/massage_chair_model.glb` — 안마의자 모델 (0.16 MB)

### 3주차 — 공간 스캔과 정리

Scaniverse로 촬영한 방을 SuperSplat에서 정리하고 Spark로 브라우저에 띄웠습니다.

| | 스플랫 개수 | 크기 |
|---|---|---|
| 정리 전 | 404,041 | 8.60 MB |
| 정리 후 | **346,372** | **7.14 MB** |

정리 내용 — 원거리 잡티 제거 · 바닥 정렬(기울기 0.58°, y = 0) · 불필요 영역 자르기


> 각 주차의 상세 과정과 근거는 제출한 PDF에 정리되어 있습니다.

---

## 파일 구조

```text
My_Place/
├─ splat-twin.html              # 메인 뷰어 (스플랫 배경 + 오브젝트 + MQTT)
├─ room-template.html           # 2주차 박스 방
├─ assets/
│  ├─ room.spz                  # 정리한 방 스캔 (SPZ v3)
│  ├─ room-before.spz           # 정리 전 원본
│  └─ massage_chair_model.glb   # 안마의자 모델
├─ evidence/                    # 단계별 증빙 스크린샷
└─ README.md
