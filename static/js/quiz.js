        /**
         * @author 김진회
         * 문제 순서 seq 는 첫번째 문제부터이므로 1로 초기화하여 시작
         * @date 21.08.23
         */
         let seq = 1;
         let countCorrect = 0;
         let quiz = '';
         let category = '';
         let correctAnswer = '';
         let description = '';
         let quizno = '';
         let temp_quiz = '';
         let temp_cate = '';
         let temp_check = '';
         let koQuizno = '';
         let filter = "win16|win32|win64|macintel|mac|"; // PC일 경우 가능한 값
 
         $(document).ready(function () {
             localStorage.clear();
             setQuiz();
             setHtmlByDevice();
         });
 
 
         /**
          * @brief pc로 접속했느냐 폰으로 접속했느냐에 따라 html을 다르게 보여주기 위한 함수
          * @param {}
          * @returns {}
          * @author 김진회
          * @date 21.08.28
          */
         function setHtmlByDevice() {
             //모바일에서 접속했을 경우 <br/>을 추가해 카테고리 를 아래로 내리기
             if (navigator.platform) {
                 if (filter.indexOf(navigator.platform.toLowerCase()) < 0) {
                     /* 모바일에서 접속하셨습니다 */
                     $('#cate-br').html("<br />");
                     // alert("모바일");
                 } else {
                     $('#cate-br').html("&nbsp;");
                 }
             }
 
         }
 
 
         /**
          * @brief 현재 순서에 맞게 퀴즈를 세팅합니다.(ajax)
          * @param {int} no 이번에 세팅해야할 퀴즈 번호
          * @returns {}
          * @author 김진회
          * @date 21.08.23
          */
         function setQuiz(no = 1) {
             $.ajax({
                 dataType: "json",
                 type: "POST",
                 url: "/quiz",
                 data: {
                     "seq": no,
                 },
                 success: function (response) {
                     // console.log(response.quiz);
                     quiz = response.quiz['content']
                     category = response.quiz['category']
                     correctAnswer = response.quiz['answer']
                     description = response.quiz['description']
                     quizno = response.quiz['no']
                     temp_quiz = `${quiz}`
                     temp_cate = `${category}`
                     $('#quiz').html(temp_quiz);
                     $('#category').html(temp_cate);
                     numberOfQuiz(quizno);
                 }
             })
             //현재 풀고 있는 문제 번호를 +1해서 저장
             seq++;
         }
 
         /**
          * @brief 정답을 골랐을 때 맞았는지 틀렸는지와 설명을 띄우고, 점수 합산을 위해 이 정보를 저장합니다.
          * @param {string} selectedAnswer O를 골랐는지 X를 골랐는지에 대한 값
          * @returns {}
          * @author 김진회
          * @date 21.08.24
          */
         function selectAnswer(selectedAnswer) {
             if (seq > 10) {
                 $('#btn-next').html("결과보러가기!");
             }
             if (selectedAnswer === correctAnswer) {
                 countCorrect++;
                 // 모달창에 정답입니다! 문구와 description을 넣어 띄우기
                 temp_check = `정답입니다! <br/><br>`;
                 $('#description').html(temp_check);
                 modalOn()
             } else {
                 // 모달창에 아쉽네요! 문구와 함께 descrirption을 넣어 띄우기
                 temp_check = `아쉽지만 오답이에요! <br/><br>`;
                 $('#description').html(temp_check);
                 modalOn()
             }
         }
 
         /**
          * @brief 다음 문제 버튼 작동 => 다음 문제 세팅 또는 로컬스토리지에 맞춘 개수 저장하고 결과페이지로 보내기
          * @param {}
          * @returns {}
          * @author 김진회
          * @date 21.08.24
          */
         function next() {
             if (seq > 10) {
                 // 10번 문제까지 풀었으면 seq가 11이 되었을 것, 그러면 몇 문제 맞췄는지를 저장하고 result페이지로 보내기
                 localStorage.setItem('countCorrect', countCorrect);
                 location.href = '/result';
             } else {
                 setQuiz(seq);
                 const modal = document.getElementById("modal")
                 modal.style.display = "none"
             }
         }
 
         /**
          * @brief O 또는 X 클릭시 모달창 띄우는 함수
          * @param {}
          * @returns {}
          * @author 김진회
          * @date 21.08.24
          */
         function modalOn() {
             const modal = document.getElementById("modal")
             // const btnModal = document.getElementById("btn-modal")
             // btnModal.addEventListener("click", e => {
             modal.style.display = "flex"
             // })
             const temp_des = `${description}`
             $('#description').append(temp_des);
         }
 
         /**
          * @brief 지금 풀고 있는 퀴즈번호를 한글로 보여주기 (몇 번째)
          * @param {string} no 지금 세팅하는 퀴즈번호 
          * @returns {} 
          * @author 김진회
          * @date 21.08.27
          */
         function numberOfQuiz(no) {
             switch (no) {
                 case "1":
                     koQuizno = '첫';
                     break;
                 case "2":
                     koQuizno = '두';
                     break;
                 case "3":
                     koQuizno = '세';
                     break;
                 case "4":
                     koQuizno = '네';
                     break;
                 case "5":
                     koQuizno = '다섯';
                     break;
                 case "6":
                     koQuizno = '여섯';
                     break;
                 case "7":
                     koQuizno = '일곱';
                     break;
                 case "8":
                     koQuizno = '여덟';
                     break;
                 case "9":
                     koQuizno = '아홉';
                     break;
                 case "10":
                     koQuizno = '열';
                     break;
             }
 
             $('#number-of-quiz').html(koQuizno);
         }