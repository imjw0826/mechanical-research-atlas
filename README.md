# 기계공학 연구 아틀라스

세계 주요 대학과 국내 대학의 기계공학 연구실, 연구 분야, 학회·저널을 탐색하는 한국어 정적 웹사이트입니다.

**웹사이트:** https://imjw0826.github.io/mechanical-research-atlas/

## 로컬 실행

Python 3가 설치된 환경에서 실행합니다.

```sh
python3 -m http.server 8000 --directory site
```

브라우저에서 http://localhost:8000 을 엽니다. 배포된 사이트는 API 키나 별도 서버 없이 동작합니다.

## 구성

- `site/index.html`: 데이터가 포함된 배포용 웹페이지 (`scripts/build_site.py`가 생성)
- `site/template.html`: 화면 템플릿
- `site/data.json`: OpenAlex 집계 데이터 (`scripts/aggregate.py`가 생성)
- `site/pubs/<연구실 id>.json`: 연구실 사이트 게시 논문 전체 목록 (상세 화면에서 필요할 때 불러옴)
- `scripts/`: 교수 명단 생성, OpenAlex 수집, 데이터 집계, 연구실 사이트 논문 정리 스크립트
- `data/`: 수집한 공개 연구 데이터와 조사 기록
  - `data/direct-publications/<대학>-<번호>.json`: 연구실 공식 사이트에서 수집한 논문 목록 (번호는 `roster-<대학>.json` 순서, KAIST는 `kaist-official-roster.json`)
  - `data/direct-publications/<대학>-<번호>.visible.txt` / `.txt`: 수집 근거가 되는 페이지 화면 텍스트
  - `data/direct-publications/progress/`: 대학별 작업 메모

## 연구실 사이트 논문 갱신

```sh
cd scripts
python3 audit_direct_publications.py      # 저장된 화면 텍스트와 대조
python3 catalog_direct_publications.py    # data/direct-publications.md, bibliographies/ 생성
python3 direct_publications_progress.py   # 진행 현황 생성
python3 build_site.py                     # site/index.html, site/pubs/ 생성
```

`parse_visible_text.py`는 브라우저에서 저장한 페이지 텍스트를 인용 항목으로 자동 분리합니다. 자동 분리한 기록은 `extraction: auto_heuristic_v1`과 `status: partial`로 표시합니다.

OpenAlex 데이터를 다시 수집하려면 `.env.example`을 `.env`로 복사하고 본인의 API 키를 입력합니다. `.env`는 Git에서 제외됩니다. 기존 웹사이트를 실행하거나 배포할 때는 필요하지 않습니다.

## 배포

`main` 브랜치에 push하면 GitHub Actions가 `site/index.html`을 GitHub Pages에 자동 배포합니다. 원본 데이터와 조사 스크립트는 저장소에서 확인할 수 있습니다.

## 데이터 해석

조사 범위, 저자 연결의 불확실성, 비공식 명단, 분야 분류 및 집계의 한계는 사이트의 ‘조사 방법과 한계’에서 확인하세요. 학회·저널 등급은 이 조사 안의 지표이며 공식 순위가 아닙니다.
