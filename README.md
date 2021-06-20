# 군부대 식단 API
본 코드는 공공데이터 포털에서 제공한 군부대 식단 api를 재가공하여
개발자가 다른 어플이나 서비스에 이용할 때 
조금 더 사용하기 편하라고 개발한 api 서비스 입니다.

http 방식에서 post 방식으로 변경

AWS에서 작동하는 컴퓨팅 속도 향상

API 엔드포인트 : https://고유값.execute-api.us-east-1.amazonaws.com/default/army-memu

고유값을 원하시면 eric71804122@gmail.com으로 연락주시면 api 사용할 수 있도록 도와드리겠습니다.

query string 요청 값
army=7369&start=2021-06-20&end=2021-06-20

army 값은 부대번호 입력(급양대 부대번호)

start는 검색 원하는 시작 날짜 입력

end는 검색 원하는 종료 날짜 입력