# 🗂️움짤 저장소 [개인 프로젝트]

<br>

## 👉프로젝트 소개 <br>
- 가지고 있는 움짤들은 많지만 이것들을 공유할 수 없을 때
- 다른 사람들이 가지고 있는 움짤들이 궁금할 때
- 나랑 비슷한 관심사를 가지고 있는 사람들을 구독하고 싶을 때
- 내가 가진 움짤들로 유저들과 이야기를 나누고 싶을 때

💡가지고 있는 움짤들을 공유할 수 있는 사이트, 움짤 저장소 입니다! 🥳

<br>

## 📌프로젝트 ERD
 - [app/customauth/models.py](https://github.com/hoya9802/GifArchive/blob/main/app/customauth/models.py) : 개인정보, 구독자, 프로필 테이블
 - [app/photo/models.py](https://github.com/hoya9802/GifArchive/blob/main/app/photo/models.py) : 카테고리, 움짤, 좋아요 테이블

![Screenshot 2024-10-27 181117](https://github.com/user-attachments/assets/bf61ec9d-61f6-4183-9912-2806c603ba1d)
<br>

## 🛠️기술 스택

### Front-end
<div>
  <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">
  <img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
  <img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white">
  <img src="https://img.shields.io/badge/bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white">
</div>

### Back-end
<div>
  <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">
  <img src="https://img.shields.io/badge/sqlite-003B57?style=for-the-badge&logo=SQLite&logoColor=white">
</div>

### Dev tools
<div>
  <img src="https://img.shields.io/badge/Visual Studio Code-007ACC?style=for-the-badge&logo=Visual Studio Code&logoColor=white">
</div>

<br>

## 📍주요 기능
1. 회원가입 & 로그인
2. SMTP 통신을 통한 패스워드 찾기
3. 움짤 CRUD
4. Q-Function을 이용한 검색기능 구현
5. 댓글기능
6. 원하는 움짤러 구독 & 움짤 좋아요
7. 카테고리
8. 프로필 정보 수정
9. 패스워드 변경

<br>

## 📝기능 상세설명
| **기능** | **상세설명** |
| :--- | :--- |
| 회원가입 & 로그인 | - 이메일을 아이디로 사용 <br> - 닉네임은 겹치지 않게 설정하여 추후에 같은 이름의 움짤 채널이 생성되는 것을 방지 |
| SMTP 통신을 통한 패스워드 찾기 | 회원가입시 입력한 이메일 주소로 비밀번호 초기화할 수 있는 링크를 전송. 그 후, 해당 링크에 접속하면 비밀번호를 재설정 |
| 움짤 CRUD | - 움짤을 메인화면에서 업로드 가능 <br> - 내 프로필에서 내가 지금까지 올린 움짤들을 확인 가능 <br> - 내 프로필에 있는 영상 관리 버튼을 통해 움짤 내용 수정 및 삭제 가능 <br> - 삭제시, 우발적 삭제를 방지하기 위해 한번 더 물어보는 팝업창 생성|
| Q-Function을 이용한 검색기능 구현 | - 움짤은 제목에 해당 단어가 포함되어 있으면 검색가능 <br> - 움짤 채널은 닉네임을 정확하게 임력했을 경우에만 검색창에 노출 |
| 댓글기능 | - DISQUS API를 사용하여 각각의 움짤에 댓글을 작성할 수 있도록 구현 |
| 원하는 움짤러 구독 & 움짤 좋아요 | - 관심있는 움짤러의 채널을 구독할 수 있는 기능 구현(구독 취소도 가능) <br> - 관심있는 움짤에 좋아요를 누를 수 있는 기능(한개의 움짤에는 좋아요를 한번만 누를 수 있음) |
| 카테고리 | - 구독 카테고리는 구독한 움짤러들의 움짤들만 보여주는 기능 <br> - 좋아요 카테고리는 내가 좋아요 누른 움짤들의 목록을 보여주는 기능 <br> - 구독칸 내가 구독한 움짤러들의 프로필과 닉네임들을 보여줌 <br> - 트랜스포머, 동물, 사물, 사람 카테고리는 해당 카테고리에 속한 움짤들만 보여줌  |
| 프로필 정보 수정 | - 처음 회원가입하면 기본 프로필&소개글로 설정 <br> - 원하는 프로필 & 소개글로 변경 가능 <br> - 이메일&닉네임&생년월일&성별&프로필사진 수정 가능|
| 패스워드 변경 | - 기존에 설정했던 비밀번호 변경 가능 <br> - 로그아웃시, 한번 더 확인하는 팝업창 구현 |

<br>

## 🔎기능 미리보기
| **로그인&회원가입** | **패스워드 찾기** | **움짤 CRUD** |
| :---: | :---: | :---: |
| <img src ="https://github.com/user-attachments/assets/a9286197-b029-4a25-ad18-c90dcec6aca8" width="230" height="380" /> | <img src ="https://github.com/user-attachments/assets/ae537f6b-3a9d-4b57-8ef6-4831e78d981c" width="230" height="380"/> | <img src="https://github.com/user-attachments/assets/dfa5b4cc-8bcc-4271-94d6-b2a09064ecda" width="230" height="380" />
| **검색기능** | **댓글** | **구독&좋아요** |
| <img src ="https://github.com/user-attachments/assets/a9103cfd-e9da-4fb0-829d-89cb21dc1e8d" width="230" height="380" /> | <img src ="https://github.com/user-attachments/assets/a1266082-1826-4e82-bbc3-4597291191d3" width="230" height="380"/> | <img src="https://github.com/user-attachments/assets/c9fb2374-a102-4f38-b70b-48de7ecac3a3" width="230" height="380" />
| **카테고리** | **프로필 수정** | **패스워드 변경** |
| <img src ="https://github.com/user-attachments/assets/41f3ee45-15c0-4211-b8bb-bbc6ff46d4ee" width="230" height="380" /> | <img src ="https://github.com/user-attachments/assets/c521483e-68db-4054-9125-2eb4030d1854" width="230" height="380"/> | <img src="https://github.com/user-attachments/assets/262bbaaf-77a6-4ccc-89e7-e266e4de35ce" width="230" height="380" />
