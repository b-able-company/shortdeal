# ShortDeal - AI Agent Guidelines

## Project Context
- **Type**: B2B Content Marketplace MVP
- **Timeline**: 18 days (12월 15일 마감)
- **Scope**: P0 기능만 (65개)
- **Users**: Producer (제작사), Buyer (바이어), Admin

## Tech Stack
- Django 4.2 + PostgreSQL 14+
- Django REST Framework (DRF)
- JWT Authentication (djangorestframework-simplejwt)
- Bootstrap 5.3 (English UI)
- Docker + docker-compose

## Database Rules
- Django ORM only (no raw SQL)
- PostgreSQL arrays: `ArrayField(CharField(max_length=50))`
- UTC timestamps
- Soft delete: `status` field
- Foreign keys: `CASCADE` default

## API Standards
- Base URL: `/api/v1/`
- JWT: `Authorization: Bearer {token}`
- Response format:
```json
  {
    "success": true,
    "data": {...},
    "message": "...",
    "pagination": {...}  // if list
  }
```
- Pagination: 20/page default
- Currency: USD default

## Permission Patterns
```python
# Import from core/permissions.py
AllowAny              # 공개
IsAuthenticated       # 로그인
IsProducer           # 제작사만
IsBuyer              # 바이어만
IsOwner              # 본인만
IsRelatedParty       # 거래 당사자
IsAdmin              # 관리자만
```

## Business Rules (Critical)
1. **Producer 가입 → Booth 자동 생성** (signal)
2. **동일 콘텐츠 pending 오퍼 1개만** (unique constraint)
3. **Offer 수락 → LOI 자동 생성** (signal)
4. **Email 알림**: Django `send_mail()`
5. **Onboarding 미완료 → 기능 차단**
6. **Soft delete**: `status='deleted'` (물리 삭제 X)

## File Structure
```
shortdeal/
├─ accounts/        # User, auth, onboarding
├─ booths/          # Producer booths
├─ contents/        # Content items
├─ offers/          # Offers
├─ loi/             # LOI documents
├─ core/            # Permissions, utils
└─ shortdeal/       # Settings
```

## Naming
- Models: `PascalCase` (User, Offer)
- Variables: `snake_case` (user_type)
- URLs: `kebab-case` (/my-offers/)
- Files: `snake_case` (offer_views.py)

## DO NOT
- ❌ P0 외 기능 추가
- ❌ Raw SQL
- ❌ 커스텀 User 모델 (AbstractUser 확장만)
- ❌ 조기 최적화
- ❌ GraphQL (REST만)

## References
- DB Schema: docs/db-schema.md
- API Spec: docs/api-spec.md
- Permissions: docs/permissions.md
- Notion IA: docs/ia.md
- Functional Spec: docs/func-spec.md
