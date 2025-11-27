# **ShortDeal Permission & Role System**

**Version:** 1.0

**Date:** 2024-11-27

**Based on:** Information Architecture - 역할별 접근 권한 매트릭스

---

## **1. Role Definitions**

### **1.1 Role Types**

```python
USER_ROLES = {
    "producer": {
        "description": "Content producer / seller",
        "onboarding": True,
        "booth_required": True,
    },
    "buyer": {
        "description": "Content buyer / platform",
        "onboarding": True,
        "booth_required": False,
    },
    "admin": {
        "description": "Platform administrator",
        "onboarding": False,
        "booth_required": False,
    },
}

```

### **1.2 Role Assignment**

- **회원가입 시 선택**: Producer 또는 Buyer (AUTH-001)
- **변경 불가**: 가입 후 역할 변경 불가
- **Admin**: 직접 DB에서 수동 할당 (가입 불가)

---

## **2. Permission Matrix**

### **2.1 공개 리소스 (AllowAny)**

| 리소스 | URL | 비로그인 | Producer | Buyer | Admin |
| --- | --- | --- | --- | --- | --- |
| 회원가입 | `/join` | ✅ | ❌ | ❌ | ❌ |
| 로그인 | `/login` | ✅ | ❌ | ❌ | ❌ |
| 콘텐츠 브라우징 | `/browse` | ✅ | ✅ | ✅ | ✅ |
| 콘텐츠 상세 | `/content/:id` | ✅ | ✅ | ✅ | ✅ |
| 제작사 부스 | `/booth/:slug` | ✅ | ✅ | ✅ | ✅ |

---

### **2.2 인증 필요 (IsAuthenticated)**

| 리소스 | Producer | Buyer | Admin |
| --- | --- | --- | --- |
| 내 프로필 | ✅ | ✅ | ✅ |
| 계정 설정 | ✅ | ✅ | ✅ |
| 비밀번호 변경 | ✅ | ✅ | ✅ |
| LOI 문서함 | ✅ (본인) | ✅ (본인) | ❌ |

---

### **2.3 Producer 전용**

| 리소스 | URL | Permission |
| --- | --- | --- |
| 온보딩 | `/onboarding/producer` | IsProducer + !is_onboarded |
| 콘텐츠 관리 | `/studio/contents` | IsProducer + is_onboarded |
| 콘텐츠 업로드 | `/studio/contents/new` | IsProducer + is_onboarded |
| 콘텐츠 수정 | `/studio/contents/:id/edit` | IsProducer + IsOwner |
| 콘텐츠 삭제 | `/studio/contents/:id/delete` | IsProducer + IsOwner |
| 받은 오퍼 목록 | `/studio/offers` | IsProducer |
| 오퍼 상세 | `/studio/offers/:id` | IsProducer + IsOwner |
| 오퍼 수락/거절 | `/studio/offers/:id/accept` | IsProducer + IsOwner |

---

### **2.4 Buyer 전용**

| 리소스 | URL | Permission |
| --- | --- | --- |
| 온보딩 | `/onboarding/buyer` | IsBuyer + !is_onboarded |
| 오퍼 작성 | `/content/:id/offer` | IsBuyer |
| 내 오퍼 목록 | `/my/offers` | IsBuyer |
| 오퍼 상세 | `/my/offers/:id` | IsBuyer + IsOwner |

---

### **2.5 Admin 전용**

| 리소스 | URL | Permission |
| --- | --- | --- |
| 관리자 대시보드 | `/admin` | IsAdmin |
| 사용자 관리 | `/admin/users` | IsAdmin |
| 콘텐츠 모니터링 | `/admin/contents` | IsAdmin |
| 오퍼 모니터링 | `/admin/offers` | IsAdmin |

---

## **3. Django Permission Classes**

### **3.1 기본 클래스**

```python
# permissions.py

from rest_framework import permissions

class IsProducer(permissions.BasePermission):
    """제작사만 허용"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.user_type == 'producer'
        )

class IsBuyer(permissions.BasePermission):
    """바이어만 허용"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.user_type == 'buyer'
        )

class IsAdmin(permissions.BasePermission):
    """관리자만 허용"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.user_type == 'admin'
        )

class IsOnboarded(permissions.BasePermission):
    """온보딩 완료 사용자만"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.is_onboarded
        )

class IsOwner(permissions.BasePermission):
    """본인 리소스만 접근"""
    def has_object_permission(self, request, view, obj):
        # obj가 user 필드를 가진 경우
        if hasattr(obj, 'user'):
            return obj.user == request.user
        # obj가 producer_id 필드를 가진 경우
        if hasattr(obj, 'producer'):
            return obj.producer == request.user
        # obj가 buyer_id 필드를 가진 경우
        if hasattr(obj, 'buyer'):
            return obj.buyer == request.user
        return False

class IsRelatedParty(permissions.BasePermission):
    """거래 당사자만 (Producer 또는 Buyer)"""
    def has_object_permission(self, request, view, obj):
        # LOI, Offer 등에서 사용
        return (
            obj.producer == request.user or
            obj.buyer == request.user
        )

```

---

### **3.2 View에서 사용 예시**

```python
# contents/views.py

class ContentListView(generics.ListAPIView):
    """콘텐츠 목록 - 공개"""
    queryset = Content.objects.filter(status='public')
    serializer_class = ContentSerializer
    permission_classes = [permissions.AllowAny]

class ContentCreateView(generics.CreateAPIView):
    """콘텐츠 업로드 - 제작사만"""
    serializer_class = ContentSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsProducer,
        IsOnboarded,
    ]

class ContentUpdateView(generics.UpdateAPIView):
    """콘텐츠 수정 - 제작사 + 본인"""
    serializer_class = ContentSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsProducer,
        IsOwner,
    ]

class OfferCreateView(generics.CreateAPIView):
    """오퍼 제출 - 바이어만"""
    serializer_class = OfferSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsBuyer,
    ]

class OfferAcceptView(generics.UpdateAPIView):
    """오퍼 수락 - 제작사 + 본인"""
    permission_classes = [
        permissions.IsAuthenticated,
        IsProducer,
        IsRelatedParty,  # producer만 해당 오퍼 수락 가능
    ]

```

---

## **4. Business Rules**

### **4.1 온보딩 체크**

```python
# middleware or decorator
def require_onboarding(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_onboarded:
            return redirect('/onboarding/')
        return view_func(request, *args, **kwargs)
    return wrapper

```

### **4.2 역할별 리다이렉트**

```python
# 로그인 후 리다이렉트
def get_post_login_redirect(user):
    if not user.is_onboarded:
        if user.user_type == 'producer':
            return '/onboarding/producer'
        elif user.user_type == 'buyer':
            return '/onboarding/buyer'

    if user.user_type == 'producer':
        return '/studio/contents'
    elif user.user_type == 'buyer':
        return '/browse'
    elif user.user_type == 'admin':
        return '/admin'

```

### **4.3 Queryset 필터링**

```python
# 역할별 데이터 필터링
class ContentViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user

        if self.action in ['list', 'retrieve']:
            # 공개 콘텐츠만
            return Content.objects.filter(status='public')

        if user.user_type == 'producer':
            # 제작사는 본인 콘텐츠만
            return Content.objects.filter(producer=user)

        return Content.objects.none()

```

---

## **5. 요약**

### **5.1 Permission 조합 패턴**

| 패턴 | 조합 | 사용 예 |
| --- | --- | --- |
| 공개 | `AllowAny` | 콘텐츠 브라우징 |
| 로그인 | `IsAuthenticated` | 프로필 |
| 제작사 | `IsAuthenticated + IsProducer` | 콘텐츠 업로드 |
| 제작사 + 온보딩 | `IsAuthenticated + IsProducer + IsOnboarded` | 콘텐츠 관리 |
| 제작사 + 본인 | `IsAuthenticated + IsProducer + IsOwner` | 콘텐츠 수정 |
| 바이어 | `IsAuthenticated + IsBuyer` | 오퍼 제출 |
| 당사자 | `IsAuthenticated + IsRelatedParty` | LOI 조회 |
| 관리자 | `IsAuthenticated + IsAdmin` | 대시보드 |

### **5.2 Django Settings**

```python
# settings.py

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

```

---