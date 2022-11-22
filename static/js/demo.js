$(document).ready(function(){
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
            let contents = $("#textContent").val().trim();
            let rowCnt = contents.split("\n")
            
            if(type === "keyword"){
                if(title === ""){
                    alert("제목을 입력해주세요");
                    $("#textResult").val("");
                    return false;
                }
            }

            if(contents === ""){
                alert("내용을 입력해주세요");
                $("#textResult").val("");
                return false;
            }

            if(rowCnt < 5){
                alert("5줄 이상 입력해주세요.");
                return false;
            }

            let sendData = JSON.stringify({id_client, title, contents});
            Utils.call('POST', `/v1/${type}`, sendData, function(res){
                if(res.success){
                    let resText = res.extractor;
                    let finalText = "";
                    if(type === "title"){
                        if(resText.length === 2){
                            finalText = `${resText[0]}\n${resText[1]}`;
                        }else{
                            finalText = resText[0];
                        }
                    }else if(type === "keyword"){
                        for(let word of resText){
                            finalText += `${word}, `;
                        }
                        finalText = finalText.slice(0, -2);
                    }
                    $("#textResult").val(finalText);
                }else{
                    $("#textResult").val(res.message);
                }
            })
        }
    })
})