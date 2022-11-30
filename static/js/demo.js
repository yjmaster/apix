$(document).ready(function(){
    $("#textTitle").val(`카타르 월드컵 광화문광장 거리 응원 이뤄질까…서울시 '고심'`);
    $("#textContent").val(`대한민국 축구 대표팀의 2022 카타르 월드컵 예선전 경기를 앞두고 서울시가 광화문광장 거리 응원 승인 여부를 고심하고 있다. 지난달 말 이태원 참사를 계기로 거리 응원으로 인파가 몰리게 될 경우 안전 문제에 대한 우려가 높아졌기 때문이다.

21일 서울시에 따르면 시는 22일 오후 광화문광장자문단 회의를 열어 응원단 ‘붉은악마’ 측이 신청한 광장 사용 허가 여부를 최종 결정한다.

앞서 붉은악마는 최근 서울시·종로구에 이달 23일부터 12월 3일까지 기간 동안 광화문광장에서 거리 응원을 위한 안전계획서를 제출했다. 이에 종로구는 이날 화재 예방과 인명피해 방지 조치, 안전 관리 인력 확보와 배치, 비상시 대응 요령 등을 집중적으로 살핀 뒤 심의 결과를 시로 통보하기로 했다.

붉은 악마는 사용 허가가 나면 대표팀의 월드컵 조별리그 경기가 예정된 11월 24일과 28일, 12월 2일 광화문광장에서 거리 응원을 펼칠 계획이다.

붉은악마 측이 예상한 참여 인원은 24일과 28일 8000명, 12월 2일 1만 명이며 안전 관리를 최우선으로 고려해 거리 응원을 추진할 방침이다.

사용 승인 심의에 앞서 붉은악마와 서울시 측은 18일 교통·안전관리 대책을 논의했다. 이 자리에서는 거리 응원 당일 광화문역 지하철 무정차 통과, 광화문역 외 인근 지하철역 분산 이용 유도, 필요 시 일부 차로 점용 방안 등이 거론된 것으로 알려졌다.

앞서 이달 초 대한축구협회는 "참사가 난 지 한 달이 되지 않은 시점에 거리 응원을 하는 게 국민 정서에 맞지 않는다"며 거리 응원을 취소한 바 있다.

시 관계자는 "군중 밀집으로 인한 참사를 겪은 만큼 안전을 최우선으로 고려할 계획"이라며 "안전관리 계획을 꼼꼼히 살펴 승인 여부를 결정할 방침"이라고 말했다. 경기가 심야 시간대 끝나기 때문에 지하철 연장 운행, 심야 버스 추가 등 응원 참가자의 귀가 대책도 해결해야 할 문제다.`);

    let browser = $(window).height();
    let wraper = $("#wraper").height();
    let top = (browser - wraper) / 2;

    $("#wraper").css("margin-top", `${top}px`);
    $("#extraction").click(function(e) {
        let btn = $(e.target);
        if(btn.prop('tagName') === "BUTTON"){
            $("#textResult").val("");

            let type = btn.attr("name");
            if(type === "reset"){
                $("#textTitle").val("");
                $("#textContent").val("");
                return false;
            }

            let id_client = "8C131969-5015-D02E-CCF1-EB4624C93692";
            let title = $("#textTitle").val().trim();
            let content = $("#textContent").val().trim();
            let rowCnt = content.split("\n").length;

            if(type === "keyword"){
                if(title === ""){
                    alert("제목을 입력해주세요");
                    $("#textResult").val("");
                    return false;
                }
            }

            if(content === ""){
                alert("내용을 입력해주세요");
                $("#textResult").val("");
                return false;
            }

            if(rowCnt < 5){
                alert("5줄 이상 입력해주세요.");
                return false;
            }

            let sendData = JSON.stringify({id_client, title, content});
            Utils.call('POST', `/v1/${type}`, sendData, function(res){
                if(res.success){
                    let resText = res.extractor;
                    let finalText = "";
                    if(type === "title" || type === "subTitle"){
                        for(let text of resText){
                            finalText += `${text}\n`;
                        }
                    }else if(type === "keyword"){
                        for(let word of resText){
                            finalText += `${word}, `;
                        }
                        finalText = finalText.slice(0, -2);
                    }
                    finalText = finalText.trim();
                    $("#textResult").val(finalText);
                }else{
                    $("#textResult").val(res.message);
                }
            })
        }
    })
})