# 기계공학 연구 트렌드와 대학원 연구 주제 추천

작성일 2026-11-17 · 기계공학 연구 아틀라스(13개 대학, 815개 연구실, 연구실 공식 사이트 게시 논문 약 5만 2천 건)를 바탕으로 정리했습니다.

보기 좋은 화면: [trend.html](trend.html) · 아틀라스 본 사이트: [index](./)

## 읽기 전에

- **프로젝트 데이터**라고 표시한 내용은 이 아틀라스가 연구실 공식 사이트에서 수집한 논문 제목에서 뽑았습니다. 제목과 연구실은 수집 기록 그대로지만, 자동 추출이라 게재 학술지는 적지 않았습니다.
- **웹 확인**이라고 표시한 논문은 2026년 11월에 검색으로 제목·학술지·연도를 확인했습니다. 대부분 대학 보도자료와 뉴스 기사를 통한 확인이라, 인용하기 전에 원문을 직접 확인하세요.
- **고전**이라고 표시한 논문은 분야에서 널리 인용되는 기준 논문입니다. 서지 정보는 제 지식에 근거해 적었고 이번에 따로 검증하지 않았습니다.
- 논문 순위나 "가장 유명한 논문"의 공식 목록은 없습니다. 아래 목록은 대표 사례이지 전수 조사가 아닙니다.

---

## 1. 큰 흐름: 프로젝트 데이터가 보여주는 것

### 1-1. AI가 기계공학 논문 제목에 들어오는 속도

수집한 논문 제목 가운데 AI 관련 단어(machine learning, neural network, reinforcement learning, generative, LLM 등)가 들어간 비율입니다.

| 연도 | 2017 | 2019 | 2021 | 2023 | 2025 | 2026 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| AI 관련 제목 비율 | 1.3% | 4.6% | 7.4% | 8.0% | 9.8% | 11.3% |

같은 기간 다른 주제의 비율은 거의 그대로입니다. 로봇은 4~5%대, 열·열전달은 4~5%대, 바이오는 7~9%대를 유지했습니다. 즉 AI는 새 분야로 따로 커지기보다 기존 분야(열, 바이오, 재료, 설계) 안으로 들어오고 있습니다. 수소 관련 제목은 0.5%(2017)에서 2%대(2024~2025)로 늘었습니다.

### 1-2. 연구실 분포

아틀라스의 분야 분류(OpenAlex 주제 기반 자동 분류)로 본 연구실 수입니다.

| 분야 | 연구실 수 |
| --- | ---: |
| 열·에너지 | 132 |
| 재료·나노공학 | 105 |
| 바이오·의공학 | 99 |
| 유체역학·항공 | 86 |
| 로보틱스·자율시스템 | 77 |
| 고체역학·구조 | 51 |
| 동역학·제어·음향 | 46 |
| 설계·제조 | 39 |
| AI·계산과학 | 29 |

열·에너지와 바이오는 연구실 수가 많은 축에 듭니다. "AI·계산과학"을 주 분야로 하는 연구실은 적지만, 1-1에서 본 것처럼 AI를 도구로 쓰는 연구실은 훨씬 많습니다. 대학원 지원에서는 "AI 연구실"을 찾기보다, 관심 분야 연구실 중에 AI를 쓰는 곳을 찾는 편이 선택지가 넓습니다.

### 1-3. 분야별로 많이 실리는 학술지 (프로젝트 데이터, 2022년 이후 OpenAlex 집계)

- **바이오·의공학:** Nature Communications, Advanced Materials, Advanced Healthcare Materials, Advanced Science, Science Advances, PNAS, Lab on a Chip
- **열·에너지:** Applied Energy, Combustion and Flame, Proceedings of the Combustion Institute, Applied Thermal Engineering, Energy, International Journal of Hydrogen Energy, International Journal of Heat and Mass Transfer, Journal of Power Sources

---

## 2. 요즘 대표 논문

### 2-1. 로봇

| 논문 | 왜 중요한가 | 구분 |
| --- | --- | --- |
| SONIC: Supersizing Motion Tracking for Natural Humanoid Whole-Body Control (NVIDIA, Science Robotics 2026) | 모션캡처 700시간 분량으로 학습한 휴머노이드 전신 제어 모델. 휴머노이드 제어가 "데이터를 키우는" 방향으로 간다는 것을 보여줌 | 웹 확인 |
| BeyondMimic (Stanford, Science Robotics) | 사람 동작 시연에서 옆돌기·발차기 같은 전신 동작을 학습하는 공개 프레임워크 | 웹 확인 |
| π0.5: A Vision-Language-Action Model with Open-World Generalization (Physical Intelligence, CoRL 2025) | 처음 보는 집에서 주방·침실 정리를 수행. 시각-언어-행동(VLA) 모델의 대표 사례 | 웹 확인 |
| Champion-level drone racing using deep reinforcement learning (Kaufmann 외, Nature 2023) | 강화학습 드론이 사람 챔피언을 이김 | 고전 |
| Learning agile and dynamic motor skills for legged robots (Hwangbo 외, Science Robotics 2019) | 시뮬레이션 학습을 실제 4족 로봇에 옮기는 방법의 출발점 | 고전 |

프로젝트 데이터에서도 같은 흐름이 보입니다. ETH Marco Hutter 연구실의 "A robot operating system framework for using large language models in embodied AI"(2026), KAIST 오현동 교수 연구실의 "RAPID: Robust and agile planner using inverse reinforcement learning for vision-based drone navigation"(2025)이 그 예입니다.

### 2-2. 재료·역학

| 논문 | 왜 중요한가 | 구분 |
| --- | --- | --- |
| Thermal conductivity of boron arsenide above 2100 W/mK at room temperature (Houston 등, Materials Today 2025) | 이론 상한(약 1,360 W/mK)을 넘는 열전도도를 보고. 반도체 방열 소재 후보 | 웹 확인 |
| Scaling deep learning for materials discovery, GNoME (Merchant 외, Nature 2023) | 그래프 신경망으로 안정한 결정 구조 후보 수십만 개를 예측 | 웹 확인 |
| An autonomous laboratory for the accelerated synthesis of novel materials, A-Lab (Szymanski 외, Nature 2023) | AI와 로봇이 합성 실험을 자동 수행. 다만 결과 분석의 신뢰성을 두고 논쟁이 있음 | 웹 확인 |

프로젝트 데이터에서는 메타물질 설계에 생성 모델을 쓰는 논문이 눈에 띕니다. ETH Dennis Kochmann 연구실의 "Algebraic language models for inverse design of metamaterials via diffusion transformers"(2026), KAIST 유승화 교수 연구실의 "Enhancing Specific Stiffness of Nano-Architected Materials through Generative AI and Active Learning"(2026), POSTECH 노준석 교수 연구실의 "Learning nonlocal interactions in large-scale heterogeneous metamaterials through scientific machine learning"(2026)이 있습니다.

### 2-3. 에너지·열

| 논문 | 왜 중요한가 | 구분 |
| --- | --- | --- |
| Achieving kilowatt-scale elastocaloric cooling by a multi-cell architecture (HKUST 등, Nature 2025) | 냉매 없이 형상기억합금의 변형으로 냉각하는 장치가 처음 kW급(1,284 W)에 도달 | 웹 확인 |
| Thermophotovoltaic efficiency of 40% (LaPotin 외, Nature 2022) | 고온 열을 빛으로 받아 전기로 바꾸는 열광전지가 효율 41.1% 달성. 열 배터리의 핵심 부품 | 웹 확인 |
| MIT 창문 크기 수동형 대기 수분 수확 패널 (Nature Water 2025) | 전력 없이 데스밸리에서 하루 최대 160 mL의 물을 수확 | 웹 확인 |
| Passive radiative cooling below ambient air temperature under direct sunlight (Raman 외, Nature 2014) | 햇빛 아래에서 전력 없이 주변보다 차갑게 만드는 복사냉각의 출발점 | 고전 |

### 2-4. 바이오

| 논문 | 왜 중요한가 | 구분 |
| --- | --- | --- |
| Imaging-guided deep tissue in vivo sound printing (Davoodi 외, Caltech, Science 2025) | 집속 초음파로 몸속 깊은 곳에 하이드로젤을 직접 인쇄. 초음파가 국소 온도를 약 5°C 올려 가교제를 방출시킴 | 웹 확인 |
| 웨어러블 초음파 심박조율기 (USC·MIT 등, Nature Biomedical Engineering 2026) | 수술 없이 피부에 붙이는 초음파 패치로 심장 박동을 조절. 쥐 실험 단계 | 웹 확인 |
| Bioadhesive ultrasound for long-term continuous imaging of diverse organs (Wang 외, Science 2022) | 피부에 붙여 48시간 연속 촬영하는 초음파 패치 | 고전 |
| 3D bioprinting of collagen to rebuild components of the human heart (Lee 외, Science 2019) | 콜라겐으로 심장 구성 요소를 인쇄하는 FRESH 기법 | 고전 |

---

## 3. 바이오엔지니어링 연구 주제

기계공학과에서 하는 바이오 연구는 크게 다섯 갈래입니다. 각 갈래에 프로젝트 데이터의 최근 논문 제목을 예로 붙였습니다.

### 3-1. 웨어러블·이식형 바이오전자

몸에 붙이거나 넣는 기기로 측정하고 치료합니다. 접착, 유연 소재, 무선 전력이 핵심 기술입니다.

- MIT Xuanhe Zhao: "Adhesive nonfibrotic bioelectronic interfaces on diverse peripheral nerves for long-term functional neuromodulation"(2025), "Hand tracking using wearable wrist imaging"(2026)
- MIT Giovanni Traverso: "Bioresorbable batteries for transient ingestible bioelectronics"(2026), "Towards intelligent and miniaturized drug delivery devices"(2026)
- Harvard Shriya Srinivasan: "Gastrointestinal neuromuscular interfaces: Bioelectronic device design for gastrointestinal motility"(2025)
- KAIST 박형순: "Wearable Hyperspectral Photoplethysmography allows Continuous Monitoring of Exercise-Induced Hypertension"(2025)

### 3-2. 초음파·광음향 영상과 치료

기계공학의 음향·진동 지식이 그대로 쓰이는 분야입니다. 한국에서는 POSTECH 김철홍 교수 연구실이 대표적입니다.

- POSTECH 김철홍: "Fabrication of optically transparent ultrasound transducers to integrate light and sound in multimodal biomedical systems"(2026), "A Three-Dimensional Photoacoustic and Ultrasound Automated Breast Volume Scanner for Breast Cancer Patients"(2025)
- ETH Outi Supponen: "Cyclic jetting enables microbubble-mediated drug delivery"(2025)

### 3-3. 생체역학과 웨어러블 로봇

- Harvard Conor Walsh: "Personalized ML-based wearable robot control improves impaired arm function"(2025), "Minimal-calibration multimodal wearable sensing for long-duration three-dimensional shoulder kinematics"(2026)
- 관련 고전: Slade 외, "Personalizing exoskeleton assistance while walking in the real world"(Nature 2022)

### 3-4. 기계생물학(mechanobiology)과 장기 칩

세포가 힘과 강성에 어떻게 반응하는지 연구하고, 미세유체 칩 위에 장기 기능을 재현합니다.

- Stanford Ovijit Chaudhuri: "Substrate stress relaxation regulates monolayer fluidity and leader cell formation for collectively migrating epithelia"(2025)
- 서울대 전누리 교수 연구실(멀티스케일 의기계공학 연구실)이 미세유체·장기 칩을 다룹니다.

### 3-5. 살아 있는 재료와 바이오하이브리드 로봇

- Harvard David Weitz: "Implantable living materials autonomously deliver therapeutics using contained engineered bacteria"(2026)
- ETH Robert Katzschmann: "Multicellular muscle-tendon bioprinting of mechanically optimized musculoskeletal bioactuators with enhanced force transmission"(2025)
- MIT Ritu Raman: 빛에 반응하는 근육 세포로 움직이는 종이 두께의 수영 로봇(Advanced Functional Materials 2026, 웹 확인)

---

## 4. 열역학·열공학 연구 주제

### 4-1. 전자기기와 AI 데이터센터 냉각

AI 연산량이 늘면서 칩과 데이터센터의 발열이 가장 급한 열 문제가 됐습니다. 고열전도 소재, 2상 냉각(비등), 폐열 재활용이 주제입니다.

- KAIST 강준상: "Isotope Enriched Cubic Boron Arsenide with Ultrahigh Thermal Conductivity"(2025)
- POSTECH 조항진 교수 연구실이 비등 열전달을, KAIST 남영석 교수 연구실이 열관리를 다룹니다.
- 산업 동향(웹 확인): 제올라이트·콘크리트 열 배터리로 데이터센터 폐열을 저장하거나 냉각에 쓰는 연구가 2026년에 여러 건 보도됐습니다. 대부분 모델링이나 시제품 단계입니다.

### 4-2. 냉매 없는 고체 냉각과 히트펌프

탄성열량·압력열량 효과를 이용해 온실가스 냉매 없이 냉각합니다. 2025년 Nature의 kW급 탄성열량 장치가 대표 성과입니다.

- 서울대 김민수 교수 연구실(냉동시스템 및 컨트롤)이 냉동·공조 시스템을 다룹니다.

### 4-3. 열 저장과 열-전기 변환

재생에너지 전기를 고온 열로 저장했다가 다시 전기로 꺼내는 열 배터리, 열광전지, 열전소자입니다.

- NUS Shin Sunmi: "High performance wearable thermoelectric coolers with 3D structural thermoelectric pillars"(2026)
- NUS Liu Chang: "Modulating thermo-diffusion/galvanic coupling via ion speciation engineering enables high-performance ionic thermoelectric cells"(2026)
- POSTECH 진현규 교수 연구실이 열전 소재·소자를, KAIST 이봉재 교수 연구실이 복사 열전달을 다룹니다.

### 4-4. 수소·암모니아 연소와 탈탄소 공정

- Imperial Andrea Giusti: "Investigation of differential diffusion and strain coupling in large eddy simulations of hydrogen-air flames"(2026), "Low-NOx hydrogen combustion via water-based bubbles"(2025)
- ETH André Bardow: "Autothermal methane pyrolysis: scalable heat integration for hydrogen and graphite production"(2026)
- ETH Russell McKenna: "Realistic roles for hydrogen in the future energy transition"(2025)
- 서울대 송한호·민경덕 교수 연구실이 연소·동력 시스템을 다룹니다.

### 4-5. 물과 탄소: 담수화, 대기 수분 수확, 탄소 포집

- MIT John Lienhard: "Energy Efficiency and Sustainability of Desalination"(2026)
- MIT Xuanhe Zhao: "Long-term stability of moisture-capturing hydrogels by preventing metal-mediated degradation"(2026)
- MIT Betar Gallant: "Thermodynamic Modeling of Aqueous Amine-Electrolyte Solvents for CO2 Absorption"(2025)
- Harvard Michael Aziz: "Direct Air Capture of CO2 in an Electrochemical Hybrid Flow Cell With a Spatially Isolated Phenazine Electrode"(2025)

### 4-6. 복사냉각과 도시 열 환경

- POSTECH 노준석: "Flexible self-cleaning Janus emitter for transparent radiative cooling in enclosed spaces"(2025)
- ETH Jan Carmeliet: "Asymmetric global urban cooling potential demands accelerated and context-specific actions"(2026)

---

## 5. 기계공학에서 유명한 AI 논문

### 5-1. 물리 법칙을 아는 신경망 (시뮬레이션 대체·가속)

| 논문 | 한 줄 설명 | 구분 |
| --- | --- | --- |
| Physics-informed neural networks (Raissi, Perdikaris, Karniadakis, Journal of Computational Physics 2019) | 미분방정식을 손실 함수에 넣어 학습하는 PINN. 기계공학에서 가장 많이 인용되는 AI 논문 중 하나 | 고전 |
| Learning nonlinear operators via DeepONet (Lu 외, Nature Machine Intelligence 2021) | 함수에서 함수로 가는 사상(연산자)을 학습 | 고전 |
| Fourier Neural Operator for Parametric Partial Differential Equations (Li 외, ICLR 2021) | 한 번 학습하면 여러 조건의 해를 빠르게 예측 | 고전 |
| Discovering governing equations from data by sparse identification of nonlinear dynamical systems, SINDy (Brunton, Proctor, Kutz, PNAS 2016) | 데이터에서 지배방정식을 찾아냄 | 고전 |
| Machine Learning for Fluid Mechanics (Brunton, Noack, Koumoutsakos, Annual Review of Fluid Mechanics 2020) | 유체역학과 기계학습의 접점을 정리한 표준 리뷰 | 고전 |
| Machine learning–accelerated computational fluid dynamics (Kochkov 외, PNAS 2021) | 거친 격자 CFD를 학습으로 보정해 가속 | 고전 |
| Learning to Simulate Complex Physics with Graph Networks (Sanchez-Gonzalez 외, ICML 2020) | 그래프 신경망으로 유체·입자 시뮬레이션을 학습 | 고전 |
| Learning PDE Solvers with Physics and Data: A Unifying View of PINNs and Neural Operators (Dai 외, IJCAI 2026 서베이) | PINN과 신경 연산자를 한 틀로 정리한 최신 서베이. 입문용으로 적합 | 웹 확인 |

2026년 리뷰들이 공통으로 지적하는 미해결 문제는 학습 범위 밖 조건에서의 신뢰성입니다. 이 부분이 대학원 연구 주제가 됩니다.

### 5-2. 로봇 학습

| 논문 | 한 줄 설명 | 구분 |
| --- | --- | --- |
| Diffusion Policy: Visuomotor Policy Learning via Action Diffusion (Chi 외, RSS 2023) | 확산 모델로 로봇 동작을 생성. 이후 조작 연구의 기본 구조가 됨 | 고전 |
| RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control (Google DeepMind, CoRL 2023) | 언어·시각 모델을 로봇 제어로 확장한 VLA의 출발점 | 고전 |
| π0.5 (Physical Intelligence, CoRL 2025), SONIC (NVIDIA, Science Robotics 2026) | 2-1 참조 | 웹 확인 |
| Experiment-free exoskeleton assistance via learning in simulation (Luo 외, Nature 2024) | 시뮬레이션 학습만으로 외골격 로봇 보조 제어기를 만듦. 바이오와 AI가 만나는 사례 | 고전 |

### 5-3. 재료·설계·제조

| 논문 | 한 줄 설명 | 구분 |
| --- | --- | --- |
| GNoME (Nature 2023), A-Lab (Nature 2023) | 2-2 참조 | 웹 확인 |
| MatterGen (Microsoft, Nature 2025) | 원하는 물성을 조건으로 무기 결정 구조를 생성. 게재 정보는 이번 검색에서 확인하지 못함 | 고전 |
| Deep Generative Models in Engineering Design: A Review (Regenwetter, Nobari, Ahmed, Journal of Mechanical Design 2022) | 설계 분야 생성 모델 리뷰 | 고전 |
| Text2CAD-Bench, MUSE, CADTestBench (arXiv 2026) | LLM이 CAD 모델을 만드는 능력을 재는 벤치마크. 복잡한 형상은 아직 잘 못 만든다는 결론 | 웹 확인 |

프로젝트 데이터의 관련 논문: MIT Faez Ahmed "DesignQA: A Multimodal Benchmark for Evaluating Large Language Models' Understanding of Engineering Documentation"(2025), ETH Kristina Shea "Expanding the Generative Power of Large Language Models for Design through Formal Design Grammars and Languages"(2025), NTU Moon Seung Ki "Leveraging Vision-Language Models for Manufacturing Feature Recognition in CAD Designs"(2025), MIT Markus Buehler "Automating alloy design and discovery with physics-aware multimodal multiagent AI"(2025).

### 5-4. 에너지·열 분야의 AI

| 논문 | 한 줄 설명 | 구분 |
| --- | --- | --- |
| Data-driven prediction of battery cycle life before capacity degradation (Severson 외, Nature Energy 2019) | 초기 사이클 데이터로 배터리 수명을 예측 | 고전 |
| Magnetic control of tokamak plasmas through deep reinforcement learning (Degrave 외, Nature 2022) | 강화학습으로 핵융합 플라즈마 형상을 제어 | 고전 |

프로젝트 데이터의 관련 논문: Imperial Huizhi Wang "Mechanism-traced diagnosis of lithium inventory loss for lithium-ion batteries using physics-driven machine learning"(2025), NUS Zhang Huangwei "Development of compact mechanism for lithium-ion battery venting gas fires using Cantera ordinary differential equation neural network algorithm"(2025), Imperial Ricardo Martinez-Botas "Evolutionary design of radial fins for forced and natural convection using generative methods"(2026), Harvard Petros Koumoutsakos "Prediction of Extreme Events in Multiscale Simulations of Geophysical Turbulence using Reinforcement Learning"(2026).

---

## 6. 추천 연구 주제

바이오, 열역학, AI에 관심이 있다는 점을 기준으로, 세 분야가 겹치는 곳을 먼저 골랐습니다. 앞쪽일수록 세 관심사가 많이 겹칩니다.

### 추천 1. 생체 열전달과 초음파 치료 (바이오 × 열)

몸속에서 열이 어떻게 퍼지는지가 치료 성능을 좌우하는 주제입니다. 집속 초음파 가열, 온열 치료, 장기 냉동 보존과 해동이 여기에 속합니다. 2025년 Science의 체내 초음파 인쇄도 "국소적으로 5°C 올리기"라는 열 문제가 핵심입니다. 열전달 수업 내용이 그대로 쓰이고, 실험과 시뮬레이션 양쪽으로 갈 수 있습니다.

- 시작점: Davoodi 외(Science 2025), POSTECH 김철홍 교수 연구실 논문
- AI 접점: 생체 열전달 방정식을 PINN이나 신경 연산자로 풀어 환자별 온도 분포를 빠르게 예측

### 추천 2. 웨어러블 열관리와 체온 조절 기기 (바이오 × 열 × 재료)

피부에 붙이는 열전 냉각기, 체온으로 발전하는 소자, 땀과 열을 다루는 섬유입니다. 기기 하나를 직접 만들어 측정까지 하는 연구라 학부생이 결과를 내기 좋습니다.

- 시작점: NUS Shin Sunmi "High performance wearable thermoelectric coolers with 3D structural thermoelectric pillars"(2026), POSTECH 진현규 교수 연구실

### 추천 3. 열유체 문제의 과학 기계학습 (열 × AI)

CFD나 열해석을 신경 연산자로 대체하거나 가속하는 연구입니다. 방열판, 배터리 팩, 연소기 설계가 적용 대상입니다. 5-1의 미해결 문제(학습 범위 밖 신뢰성)가 그대로 논문 주제가 됩니다. 코딩과 수치해석을 좋아하면 맞습니다.

- 시작점: Raissi 외(2019), Li 외(2021), Dai 외 서베이(2026)
- 관련 연구실: Harvard Koumoutsakos, Imperial Martinez-Botas, 서울대 김도년 교수(AI주도 시뮬레이션 및 설계 연구실)

### 추천 4. AI 데이터센터와 반도체 냉각 (열)

수요가 가장 빠르게 늘어나는 열 문제입니다. 비등·2상 냉각, 고열전도 소재, 칩 패키지 열설계가 세부 주제입니다. 한국 반도체 산업과 바로 연결됩니다.

- 시작점: 붕소 비소 열전도도 논문(Materials Today 2025), KAIST 강준상·남영석 교수 연구실, POSTECH 조항진 교수 연구실

### 추천 5. 웨어러블 초음파와 바이오전자 (바이오)

2022년 이후 Science와 Nature 계열에 꾸준히 실리는 주제입니다. 음향, 접착 역학, 유연 소재가 필요합니다.

- 시작점: Wang 외(Science 2022), MIT Zhao 연구실, POSTECH 김철홍 교수 연구실

### 추천 6. 웨어러블 로봇의 학습 기반 제어 (바이오 × AI)

외골격·소프트 슈트를 사람마다 맞추는 제어기를 강화학습과 시뮬레이션으로 만듭니다.

- 시작점: Luo 외(Nature 2024), Harvard Walsh 연구실 논문(2025), KAIST 박형순 교수 연구실

### 추천 7. 냉매 없는 고체 냉각 (열역학)

열역학 사이클 자체를 새로 설계하는 주제라 열역학을 가장 깊게 씁니다. 재료 피로와 시스템 효율이 남은 과제입니다.

- 시작점: HKUST kW급 탄성열량 장치(Nature 2025), 서울대 김민수 교수 연구실

### 추천 8. 수소·암모니아 연소 (열 × 유체)

산업 수요가 분명하고 국내 연구실이 많습니다. 실험 연소와 대규모 수치해석(LES)으로 갈립니다.

- 시작점: Imperial Giusti 연구실 논문, 서울대 송한호·민경덕 교수 연구실, KAIST 배충식 교수 연구실

---

## 7. 주제를 고르는 방법

1. **6장에서 두세 개를 고르고, 각 주제의 "시작점" 논문을 초록과 그림만 먼저 읽습니다.** 그림이 재미있는 쪽이 맞는 주제입니다.
2. **실험형인지 계산형인지 정합니다.** 추천 1·2·4·5는 장치를 만들고 측정하는 비중이 크고, 추천 3은 계산 위주, 추천 6·8은 연구실에 따라 갈립니다.
3. **아틀라스에서 해당 연구실의 최근 3년 논문 목록을 봅니다.** 연구실 이름이나 소개 글보다 최근 논문 제목이 실제로 하는 일을 정확히 보여줍니다.
4. **학부 과목과 연결합니다.** 열전달, 유체역학, 수치해석, 기계학습 기초 가운데 부족한 과목을 대학원 전에 채웁니다. 추천 3은 Python과 PyTorch가 필수입니다.
5. **학부 연구생이나 인턴으로 한 학기 해 봅니다.** 주제 적합성은 해 봐야 알 수 있습니다.

---

## 출처

**웹 확인에 쓴 자료 (2026년 11월 검색)**

- [SONIC: Supersizing Motion Tracking for Natural Humanoid Whole-Body Control](https://www.citedrive.com/en/discovery/sonic-supersizing-motion-tracking-for-natural-humanoid-whole-body-control/)
- [Nvidia's SONIC Teaches Humanoids to Move](https://aibusiness.com/robotics/nvidia-s-sonic-teaches-humanoids-move)
- [Humanoid robot does cartwheels and flip kicks (BeyondMimic)](https://connectsci.au/news/news-parent/9997/Humanoid-robot-does-cartwheels-and-flip-kicks)
- [π0.5: A Vision-Language-Action Model with Open-World Generalization](https://mlanthology.org/corl/2025/black2025corl-visionlanguageaction)
- [UH Researchers Help Break Thermal Conductivity Barrier with Boron Arsenide Discovery](https://www.uh.edu/news-events/stories/2025/october/10212025-boron-arsenide-thermal-conductivity.php)
- [HKUST Develops World's First Kilowatt-Scale Elastocaloric Green Cooling Device](https://hkust.edu.hk/news/hkust-develops-worlds-first-kilowatt-scale-elastocaloric-green-cooling-device)
- [Achieving kilowatt-scale elastocaloric cooling by a multi-cell architecture](https://ideas.repec.org/a/nat/nature/v639y2025i8053d10.1038_s41586-024-08549-9.html)
- [Thermophotovoltaic cells top 40 percent efficiency](https://physicsworld.com/a/thermophotovoltaic-cells-top-40-percent-efficiency)
- [Window-sized device taps the air for safe drinking water (MIT News)](https://news.mit.edu/2025/window-sized-device-taps-air-safe-drinking-water-0611)
- [Imaging-guided deep tissue in vivo sound printing (Science 2025)](https://www.gao.caltech.edu/uploads/2/6/7/2/26723767/science.adt0293.pdf)
- [3D Printing In Vivo Using Sound](https://www.chemistry.ucla.edu/news/3d-printing-in-vivo-using-sound/)
- [A pacemaker without surgery? USC Viterbi ultrasound breakthrough](https://viterbischool.usc.edu/?p=84523)
- [MIT 근육 세포 수영 로봇 (ScienceDaily, 2026-10)](https://sciencedaily.com/releases/2026/10/261022081308.htm)
- [Millions of new materials discovered with deep learning (GNoME)](https://deepmind.google/blog/millions-of-new-materials-discovered-with-deep-learning/)
- [A Survey of AI for Materials Science](https://arxiv.org/pdf/2506.20743)
- [Learning PDE Solvers with Physics and Data (IJCAI 2026)](https://www.ijcai.org/proceedings/2026/868)
- [Partial Differential Equations in the Age of Machine Learning](https://www.alphaxiv.org/abs/2603.07655)
- [Text2CAD-Bench](https://arxiv.org/abs/2605.18430)
- [Foundation Models for Automatic CAD Generation](https://arxiv.org/abs/2607.05573)
- [New Method of Data Center Cooling Could Dramatically Decrease Electricity Use (NYU)](https://engineering.nyu.edu/news/new-method-data-center-cooling-could-dramatically-decrease-electricity-use)
- [Top Mechanical Engineering Research Areas in 2026 (ASME)](https://www.asme.org/topics-resources/content/top-mechanical-engineering-research-areas-in-2026)

**프로젝트 데이터**

- 연구실 공식 사이트 게시 논문: `data/direct-publications/` (제목이 있는 기록 약 4만 8천 건으로 비율 계산)
- 분야 분류와 학술지 집계: `site/data.json` (OpenAlex, 2022년 이후)
