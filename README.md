# [Assignment 4] 8PERCENT  

## 팀원  
| **이름** | **Github Link** |
|:------|:-------------|
| 강대훈 | https://github.com/daehoon12 |
| 김훈태 | https://github.com/kim-hoontae |
| 이무현 | https://github.com/PeterLEEEEEE |


## 과제  안내

### API 목록

---

- 거내역 조회 API
- 입금 API
- 출금 API

### 주요 고려 사항은 다음과 같습니다.

---

- 계좌의 잔액을 별도로 관리해야 하며, 계좌의 잔액과 거래내역의 잔액의 무결성의 보장
- DB를 설계 할때 각 칼럼의 타입과 제약

### 구현하지 않아도 되는 부분은 다음과 같습니다.

---

- 문제와 관련되지 않은 부가적인 정보. 예를 들어 사용자 테이블의 이메일, 주소, 성별 등
- 프론트앤드 관련 부분

### 제약사항은 다음과 같습니다.

---

- (**8퍼센트가 직접 로컬에서 실행하여 테스트를 원하는 경우를 위해**) 테스트의 편의성을 위해 mysql, postgresql 대신 sqllite를 사용해 주세요.

### 상세설명

---

**1)** 거래내역 조회 **API**

- 아래와 같은 조회 화면에서 사용되는 API를 고려하시면 됩니다.
    
    ![image](https://lh6.googleusercontent.com/PdtI4YvVu3biJ0TyEGCHVrR0fAPOQsILYHEczQHmR3UMKEINxlIjjp_-3gOGu5yGh3YXpxbegNYqNCEosUosq3nKRTMpte6ZiRUccX8iRlD5rxLJ1HWFy6E2HcMFMIMGZO7eVQl5)
    

거래내역 API는 다음을 만족해야 합니다.

- 계좌의 소유주만 요청 할 수 있어야 합니다.
- 거래일시에 대한 필터링이 가능해야 합니다.
- 출금, 입금만 선택해서 필터링을 할 수 있어야 합니다.
- Pagination이 필요 합니다.
- 다음 사항이 응답에 포함되어야 합니다.
    - 거래일시
    - 거래금액
    - 잔액
    - 거래종류 (출금/입금)
    - 적요

**2)** 입금 **API**

입금 API는 다음을 만족해야 합니다.

- 계좌의 소유주만 요청 할 수 있어야 합니다.

**3)** 출금 **API**

출금 API는 다음을 만족해야 합니다.

- 계좌의 소유주만 요청 할 수 있어야 합니다.
- 계좌의 잔액내에서만 출금 할 수 있어야 합니다. 잔액을 넘어선 출금 요청에 대해서는 적절한 에러처리가 되어야 합니다.

**4)** 가산점

다음의 경우 가산점이 있습니다.

- Unit test의 구현
- Functional Test 의 구현 (입금, 조회, 출금에 대한 시나리오 테스트)
- 거래내역이 1억건을 넘어갈 때에 대한 고려
    - 이를 고려하여 어떤 설계를 추가하셨는지를 README에 남겨 주세요.


## 사용한 기술 스택

Back-end : <img src="https://img.shields.io/badge/Python 3.8-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Django 3.2-092E20?style=for-the-badge&logo=Django&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/sqlite-0064a5?style=for-the-badge&logo=sqlite&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/AWS_EC2-232F3E?style=for-the-badge&logo=Amazon&logoColor=white"/>&nbsp;
<p>
Tool : <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white"/>
</p>

## 모델링  

<img width="772" alt="스크린샷 2021-11-12 오전 3 26 36" src="https://user-images.githubusercontent.com/78228444/141350250-cf0f31b4-3905-46e9-ac6b-e390f516ad4d.png">


## 파일 구조  
- `./config`
  - `./__init__.py`    
  - `./asgi.py`
  - `./settings.py`
  - `./urls.py`
  - `./wsgi.py`
- `./users`
  - `./migration`
  - `./__init__.py`
  - `./admin.py`
  - `./apps.py`
  - `./models.py`
  - `./tests.py`
  - `./urls.py`
  - `./utils.py`
  - `./views.py`
- `./account`
  - `./migration`
  - `./__init__.py`
  - `./admin.py`
  - `./apps.py`
  - `./filtering.py`
  - `./models.py`
  - `./tests.py`
  - `./urls.py`
  - `./views.py`
- `./.gitignore`
- `./manage.py`
- `./requirements.txt`

## Endpoint  
![image](https://user-images.githubusercontent.com/78228444/140987466-18431ef6-5278-4cb6-a598-dfd439d9fd3d.png)


## 구현기능  

### 계좌 생성
- ```계좌생성 성공시``` : status_code : 200

```
- JSON
{
    "MESSAGE": "SUCCESS",
}
```

- ```계좌생성 실패시``` : 
1. 비밀번호가 숫자 4자리 아닐시 status_code : 400, 
2. 키에러가 발생했을시 status_code : 400
```
- JSON
{
    "MESSAGE":"숫자 4자리를 입력해주세요.",
    "MESSAGE": "KEY_ERROR"
    
}

``` 

### 입금 API
- ```입금 성공시``` : status 201,
```
{
}
``` 

- ```입금 실패시``` : status 404, 
``` 
{
}
```

### 출금 API
- ```출금 성공시``` : status 201,
``` 
{
}
```
- ```출금 실패시``` : status 404,
``` 
{
}
```


# Reference
이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 8퍼센트에서 출제한 과제를 기반으로 만들었습니다.
