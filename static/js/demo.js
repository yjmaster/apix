$(document).ready(function(){
    $("#textTitle").val(`집배원도, 병문안 차도 ‘휘발유 품절’에 헛걸음…“주유소 문 닫을 판”`);
    $("#textContent").val(`민주노총 공공운수노조 화물연대본부가 안전운임제 유지·확대를 촉구하며 엿새째 총파업을 이어가면서 ‘기름줄’이 끊긴 주유소들이 영업에 차질을 빚는 등 소비자 피해도 가시화되고 있다.

29일 오후 12시19분 우편 배송 오토바이 한 대가 서울 관악구의 한 셀프 주유소로 진입했다. 집배원은 안장에서 내리는 대신 주유기를 바라보며 주위를 한 바퀴 반 돌더니 그대로 진출로로 빠져나갔다. 채 5분도 안되는 시간 동안 오토바이 세 대가 똑같이 주유소에 들어왔다 돌아섰다.
    
이 주유소에 설치된 주유기 두 대엔 모두 ‘휘발유 품절’이란 안내문이 붙어 있었다. 진입로 앞에 설치된 대형 가격 안내판과 주유기 옆에 기대 놓은 노란색 플라스틱 입간판에도 A4용지 한 장에 한 글자씩 인쇄된 ‘품절’ 안내문이 나붙었다. 심지어는 개별 주유 호스 손잡이에도 같은 안내가 부착돼 있었다. 실제로 오토바이 세 대가 헛걸음을 하는 동안 경유를 쓰는 탑차와 승용차 한 대는 정상적으로 기름을 넣었다.
    
한 정유사가 직영하는 이 지점엔 하루 평균 300~350대의 휘발유 차량이 찾아온다. 그러나 전날부터 이날 점심시간까지 급유에 성공한 차는 한 대도 없었다. 휘발유를 비축해둔 탱크가 텅 비어버린 탓이다. 경유는 저장 탱크가 한 대 더 있어 버티고 있지만, 이마저도 이번 주말이면 바닥을 드러낼 것으로 예상된다. 파업에 동참하지 않는 기사들을 통해 대체운송을 한다고 해도 수요 대비 공급이 턱없이 부족한 데다가 직영점은 그마저도 후순위다. 주유소 관계자는 “결국 시간 문제”라며 “(다음 주부턴) 문 닫아야지 별 수 있겠나”고 탄식했다.
    
다른 지역에도 비슷한 사정의 주유소들이 많았다. 송파구의 한 주유소는 일 매출액이 3000만~4000만원에 달하고 차량이 하루 600~700대씩 방문하는 곳이지만 기름 공급이 완전히 끊기면서 손쓸 도리가 없게 됐다. 금천구 소재 한 주유소도 이날 오전 휘발유 재고가 다 떨어졌다. 점심시간쯤 흰색 승용차 한 대가 영문도 모른 채 주유기 앞에 차를 대자 직원이 황급히 달려가 창문 너머로 사정을 설명했다. 이 직원은 “하필 휘발유가 3분의 1 남았을 때 파업이 시작되는 바람에 제때 기름을 못 채웠다”며 난색을 표했다.

적잖은 운전자들이 주유소 문턱에서 품절 표시를 보고 발길을 돌렸다. 아예 대중교통으로 선회하는 사례까지 나타났다. 친언니를 병문안하기 위해 강원도 속초로 향하던 오정자(64)씨는 서초구의 한 주유소 앞에서 차를 멈춰세웠다. 오씨는 “고속도로를 탔다가 기름이 떨어지면 낭패”라며 “차는 집에 다시 가져다 두고 고속버스를 타려 한다”고 말했다.

이날 한국석유공사에 따르면 전국 55개 주유소에서 휘발유 보유 재고가 바닥난 것으로 집계됐다. 화물연대 파업이 시작되고 1주도 채 지나지 않은 점을 고려할 때 이 수는 시간이 지날수록 늘어날 전망이다. 한국주유소협회 관계자는 “평균적인 주유소들은 2주치 정도의 비축분을 가지고 있다”며 “당장 다음 주 정도만 가도 (영업을 못 하는 주유소가) 더 많아질 것”이라고 우려했다.`);
    
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
                    }else{
                        finalText = resText;
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