//파일이름이 bot.js인 이유는 그냥 임시이름. 실제로는 메신저봇R에 붙여넣기
function response(room, msg, sender, isGroupChat, replier, imageDB, packageName) {
        // 방 이름이 "필요 코딩 모임"일 때만 FastAPI 서버로 메시지를 전송
        if (room === "필요 코딩 모임") {
            try {
                // FastAPI 서버 URL 설정
                const url = "http://192.168.91.18/reply";
    
                // 메시지를 JSON 형식으로 FastAPI 서버에 POST 요청
                const response = org.jsoup.Jsoup.connect(url)
                    .header("Content-Type", "application/json")
                    .requestBody(JSON.stringify({
                        room: room,
                        msg: msg,
                        sender: sender
                    }))
                    .ignoreContentType(true) // JSON 응답을 허용
                    .post();
    
                // FastAPI 서버에서 받은 응답을 JavaScript로 출력
                const jsonResponse = JSON.parse(response.body().text());
                replier.reply(jsonResponse.response); // FastAPI의 응답으로 답장하기
    
            } catch (error) {
                replier.reply("FastAPI 서버에 연결할 수 없습니다.");
            }
        }
    }