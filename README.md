# 실감 피지컬 컴퓨팅 2주차 — My Place

내 방을 대상으로 방의 구조, 주요 물체, Gaussian Splat 공간을 연결하는 디지털 트윈 과제 저장소입니다.

## 현재 결정

- 공통 대상: 내 방과 방 안의 침대,책상,책장,안마의자,화장대
- B 모델 대상: 내 방의 안마의자
- 모델 도구: Blender + AI/MCP 기반 생성 과정 기록
- C 스캔 대상: 내 방

- 다음 주 작업: 내 방 SPZ를 SuperSplat으로 편집하고 안마의자 GLB와 합성

## 진행 순서

1. Blender에서 안마의자 단일 오브젝트를 AI 기반으로 생성하고 실제 레퍼런스와 비슷하게 수정합니다.
2. 텍스처를 포함한 `assets/massage-chair.glb`를 export하고 20MB 이하인지 확인합니다.
3. 실제 방의 가로·세로·높이를 측정하고, 침대·책상·책장·안마의자의 대략적인 위치를 기록합니다.
4. 측정값을 바탕으로 room_template.html에 바닥·4개 벽·주요 물체를 박스로 표현하고 GitHub Pages에 게시합니다.
5. Scaniverse에서 내 방을 촬영해 `assets/scaniverse_room.spz`로 export하고 제공된 뷰어에서 확인합니다.
6. 각 단계의 생성·수정·검증 화면을 `evidence/`에 정리합니다.

## 파일 규칙

```text
My_Place/
├─ room_template.html          # A: 실제 방 치수를 반영한 박스 방
├─ w02-spz-viewer.html         # C: SPZ 확인용 뷰어
├─ assets/
│  ├─ massage_chair.glb        # B: 안마의자 모델, 20MB 이하
│  └─ scaniverse_room.spz      # C: 내 방 스캔, 100MB 이하
├─ evidence/
└─ README.md
```



