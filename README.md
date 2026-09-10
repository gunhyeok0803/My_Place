# 실감 피지컬 컴퓨팅 2주차 — My Place

내 방을 대상으로 방의 구조, 주요 물체, Gaussian Splat 공간을 연결하는 디지털 트윈 과제 저장소입니다.

## 현재 결정

- 공통 대상: 내 방과 방 안의 침대·책상·책장·안마의자
- B 모델 대상: 내 방의 안마의자
- 모델 도구: Blender + AI/MCP 기반 생성 과정 기록
- C 스캔 대상: 강의실이 아닌 내 방으로 진행할 계획
- 다음 주 작업: 내 방 SPZ를 SuperSplat으로 편집하고 안마의자 GLB와 합성

PDF의 C 항목에는 강의실 구석 SPZ가 예시·제출 대상으로 적혀 있으므로, 내 방 SPZ 대체는 교수님께서 허용하신다는 전제로 진행합니다. 필요하면 제출 전에 강의실 스캔을 추가할 수 있도록 계획을 남겨 둡니다.

## 진행 순서

1. Blender에서 안마의자 단일 오브젝트를 AI 기반으로 생성하고, 실제 레퍼런스와 비슷하게 수정합니다.
2. 텍스처를 포함한 `assets/massage-chair.glb`를 export하고 20MB 이하인지 확인합니다.
3. 실제 방의 가로·세로·높이를 측정하고, 침대·책상·책장·안마의자의 대략적인 위치를 기록합니다.
4. 측정값을 바탕으로 `index.html`에 바닥·4개 벽·주요 물체를 박스로 표현하고 GitHub Pages에 게시합니다.
5. Scaniverse에서 내 방을 촬영해 `assets/room.spz`로 export하고 제공된 뷰어에서 확인합니다.
6. 각 단계의 생성·수정·검증 화면을 `evidence/`에 정리합니다.

## 파일 규칙

```text
My_Place/
├─ index.html                  # A: 실제 방 치수를 반영한 박스 방
├─ w02-spz-viewer.html         # C: SPZ 확인용 뷰어
├─ assets/
│  ├─ massage-chair.glb        # B: 안마의자 모델, 20MB 이하
│  └─ room.spz                 # C: 내 방 스캔, 100MB 이하
├─ evidence/
│  ├─ A-room.png
│  ├─ B-blender-ai.png
│  └─ C-room-spz.png
└─ README.md
```

아직 방 치수, GLB, SPZ가 확정되지 않았으므로 현재 저장소에는 결과 파일을 임의로 넣지 않습니다. GitHub Pages의 메인 화면도 `index.html` 제작 후 활성화합니다.

## 학습 기록 방향

결과 자체를 길게 설명하기보다 다음을 짧게 기록합니다.

- 실제 치수와 3D 좌표를 연결한 방법
- 반복되는 벽을 위치·회전값으로 구성한 방법
- AI가 만든 안마의자를 Blender에서 수정한 이유
- Gaussian Splat과 일반 GLB 메시의 차이
- 브라우저 오류 발생 시 Console을 확인하고 해결한 과정

## 체크인 방식

각 단계가 끝날 때 실행 화면, 오류 메시지, Blender/Scaniverse 화면, 파일 크기를 확인한 뒤 다음 단계로 넘어갑니다.

첫 번째 다음 작업은 Blender에서 안마의자 생성 과정을 준비하는 것입니다.
