# ShortDeal

ShortDeal은 콘텐츠 제작사(Producer)와 바이어(Buyer)를 연결하는 B2B 콘텐츠 라이센싱 마켓플레이스입니다. 제작사는 자신의 콘텐츠를 등록하고, 바이어는 관심있는 콘텐츠를 탐색하여 제안(Offer)을 제출할 수 있습니다.

## 주요 기능

### 제작사(Producer)

- **부스(Booth) 관리**: 회사 정보, 로고, 국가, 장르 태그 등을 포함한 전시 공간
- **콘텐츠 스튜디오**: 콘텐츠 등록, 수정, 관리 (포스터, 비디오, 스크린샷, 상세 정보)
- **제안 관리**: 바이어로부터 받은 제안 검토 및 수락/거절
- **LOI 생성**: 제안 수락 시 자동으로 Letter of Intent 생성

### 바이어(Buyer)

- **콘텐츠 탐색**: 장르, 국가별 필터링 및 검색
- **부스 방문**: 제작사 부스에서 콘텐츠 포트폴리오 확인
- **제안 제출**: 관심 콘텐츠에 가격 제안 및 메시지 전송
- **제안 추적**: 제출한 제안의 상태 추적 (대기/수락/거절/만료)

### 공통 기능

- **역할 기반 인증**: 제작사/바이어 구분된 회원가입 및 권한 관리
- **온보딩**: 역할별 맞춤형 프로필 설정
- **알림**: 주요 이벤트(제안 수신, 응답 등) 실시간 알림
- **설정**: 회사 정보, 로고 업데이트

## 기술 스택

### Backend

- **Django 4.2**: 웹 프레임워크
- **Django REST Framework**: RESTful API
- **PostgreSQL**: 데이터베이스
- **JWT**: 인증 (djangorestframework-simplejwt)

### Frontend

- **Django Templates**: 서버사이드 렌더링
- **Bootstrap 5**: UI 프레임워크
- **Vanilla JavaScript**: 클라이언트 인터랙션

### 인프라

- **Gunicorn**: WSGI 서버
- **WhiteNoise**: 정적 파일 서빙
- **Railway**: 배포 플랫폼 (PostgreSQL + Volume 스토리지)

### 개발 도구

- **django-debug-toolbar**: 디버깅
- **django-extensions**: 확장 기능
- **drf-spectacular**: API 문서 자동 생성

## 프로젝트 구조

```text
shortdeal-be/
├── apps/                      # Django 앱
│   ├── accounts/             # 사용자 인증 및 계정 관리
│   ├── booths/               # 제작사 부스
│   ├── contents/             # 콘텐츠 관리
│   ├── offers/               # 제안/거래
│   ├── loi/                  # Letter of Intent
│   ├── notifications/        # 알림
│   └── core/                 # 공통 유틸리티
├── shortdeal/                # 프로젝트 설정
│   ├── settings/
│   │   ├── base.py          # 공통 설정
│   │   ├── local.py         # 로컬 개발
│   │   └── production.py    # 프로덕션
│   └── urls.py              # URL 라우팅
├── templates/                # Django 템플릿
├── static/                   # 정적 파일 (CSS, JS)
├── media/                    # 업로드 파일 (포스터, 비디오 등)
├── docs/                     # 프로젝트 문서
└── requirements.txt          # Python 의존성
```

## 설치 및 실행

### 사전 요구사항

- Python 3.11+
- PostgreSQL 14+
- pip

### 로컬 개발 환경 설정

1. **저장소 클론**

```bash
git clone <repository-url>
cd shortdeal-be
```

2. **가상환경 생성 및 활성화**

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. **의존성 설치**

```bash
pip install -r requirements.txt
```

4. **환경 변수 설정**

`.env` 파일 생성:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/shortdeal
```

5. **데이터베이스 마이그레이션**

```bash
python manage.py migrate
```

6. **슈퍼유저 생성**

```bash
python manage.py createsuperuser
```

7. **개발 서버 실행**

```bash
python manage.py runserver
```

서버는 `http://localhost:8000`에서 실행됩니다.

### 테스트 데이터 생성

개발 환경에서 샘플 데이터를 생성하려면:

```bash
python manage.py shell
# 또는 Django admin에서 직접 생성
```

## 배포

### Railway 배포

프로젝트는 Railway에 배포되어 있습니다:

- **PostgreSQL**: Railway에서 제공하는 관리형 데이터베이스
- **Volume 스토리지**: 미디어 파일 영구 저장 (`/app/media`)
- **환경 변수**: Railway 대시보드에서 관리

배포 설정:

- `shortdeal.settings.production` 사용
- Gunicorn WSGI 서버
- WhiteNoise로 정적 파일 서빙
- PostgreSQL 연결 풀링

자세한 배포 가이드는 [docs/railway-deployment.md](docs/railway-deployment.md)를 참조하세요.

## API 문서

REST API 문서는 다음 엔드포인트에서 확인할 수 있습니다:

- Swagger UI: `/api/schema/swagger-ui/`
- ReDoc: `/api/schema/redoc/`
- OpenAPI Schema: `/api/schema/`

## 문서

프로젝트 문서는 `docs/` 디렉토리에 있습니다:

- [기능 명세서](docs/func-spec.md): 전체 기능 상세 설명
- [데이터베이스 스키마](docs/db-schema.md): ERD 및 테이블 구조
- [API 명세서](docs/api-spec.md): RESTful API 엔드포인트
- [권한 관리](docs/permissions.md): 역할별 접근 권한
- [IA 구조](docs/ia.md): 정보 구조 및 네비게이션
- [Railway 배포 가이드](docs/railway-deployment.md): 배포 설정 및 문제 해결
- [Volume 스토리지 설정](docs/railway-volume-setup.md): 미디어 파일 저장 설정

## 라이선스

이 프로젝트는 비공개 프로젝트입니다.

## 연락처

프로젝트 관련 문의사항은 이슈를 등록해주세요.
