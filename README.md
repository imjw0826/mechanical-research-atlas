# 기계공학 연구 아틀라스

## 1. 프로젝트 소개

세계 주요 대학과 국내 대학의 기계공학 연구실, 연구 분야, 학회·저널을 한곳에서 탐색하는 한국어 정적 웹사이트입니다. 공개 논문 데이터(OpenAlex)와 연구실 공식 사이트의 논문 목록을 모아, 어느 대학의 어떤 연구실이 무슨 연구를 하는지 비교해 볼 수 있게 하는 것이 목적입니다.

## 2. 기술 스택

- **웹사이트:** HTML, CSS, JavaScript (데이터가 포함된 단일 정적 페이지)
- **데이터 수집·가공:** Python 3 스크립트, OpenAlex API
- **배포:** GitHub Pages (GitHub Actions 자동 배포)

## 3. 이용 방법

**웹사이트:** https://imjw0826.github.io/mechanical-research-atlas/

- 대학별 연구실과 연구 분야를 탐색하고, 연구실 상세 화면에서 게시 논문 목록을 확인합니다.
- 분야별 주요 학회·저널을 살펴봅니다. 등급은 이 조사 안의 지표이며 공식 순위가 아닙니다.
- 조사 범위와 집계의 한계는 사이트의 ‘조사 방법과 한계’에서 확인할 수 있습니다.

로컬에서 실행하려면 Python 3만 있으면 됩니다. API 키나 별도 서버는 필요 없습니다.

```sh
git clone https://github.com/imjw0826/mechanical-research-atlas.git
cd mechanical-research-atlas
python3 -m http.server 8000 --directory site
```

브라우저에서 http://localhost:8000 을 엽니다. 데이터를 다시 수집할 때만 `.env.example`을 `.env`로 복사해 OpenAlex API 키를 넣고 `scripts/`의 스크립트를 실행합니다.

## 4. 최근 업데이트

2026-11-15
