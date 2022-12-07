let log = {
    params: {
        sdate: '',
        edate: '',
        page: 1,
        display: 10,
        media: '',
        code: '',
        excel: false
    },
    init: function(){
        let browser = $(window).height();
        let wraper = $("#wraper").height();
        let top = (browser - wraper) / 2;
        $("#wraper").css("margin-top", `${top}px`);
        
        log.setDatePicker();
        log.setDateRange();
        log.getOptions();
        log.getLog();
        log.eventBind();
    },
    eventBind: function(){
        $("#search").click(function(){
            log.setOptions();
            log.getLog();
        });
        $("select").on('change', function() {
            let type = $(this).attr("id");
            log.params[type] =  $(this).val();
        });
        $("#display").on('change', function() {
            log.params['page'] =  1;
            log.params['display'] =  $(this).val();
            log.getLog();
        });
        $("#excel").click(function(){
            log.params['excel'] = true;
            log.getLog();
        });
    },
    setDatePicker: function(){
        let edate = new Date().format();
        let sdate = new Date(edate)['getMonths'](-1);  
    
        let range_date = $("#dateRange").datepicker(
            {type : "range", minDate : new Date().getMonths(-1), maxDate : edate});
    
        range_date.datepicker('setDateRange',  sdate, edate);
    },
    setDateRange: function(){
        let dateRange = $("#dateRange").val();
        let fullDate = dateRange.split(" ~ ");
        log.params["sdate"] = fullDate[0];
        log.params["edate"] = fullDate[1];
    },
    setOptions: function(){
        log.setDateRange();
        let media = $("#media").val();
        let code = $("#code").val();
        log.params["page"] = 1;
        log.params["media"] = media;
        log.params["code"] = code;
    },
    getOptions: function(type){
        let sendData = JSON.stringify(log.params);
        Utils.call('POST', `/options`, sendData, function(res){
            let html = `<option value="">전체</option>\n`;
            let mhtml = html;
            let chtml = html;
            let options = res['options'];
            if(res.success){
                for (let media of options['media']) {
                    mhtml += `<option value="${media}">${media}</option>\n`;
                }
                for (let code of options['code']) {
                    chtml += `<option value="${code}">${code}</option>\n`;
                }
            }else{
                alert(res.message);
            }
            $("#media").html(mhtml);
            $("#code").html(chtml);
        }, false);
    },
    getLog: function(){
        let html = "";
        // console.log("log.params : ", log.params)
        let sendData = JSON.stringify(log.params);
        Utils.call('POST', `/log`, sendData, function(res){
            if(log.params['excel']){
                log.exceldownload(res);
            }else{
                log.setTable(res);
            }
        });
    },
    exceldownload: function(res){
        let header = [], data = [];
        let hlist = [
            '로그일렬번호', '언론사',
            '요청일시',     '반환결과코드',
            '오류메시지',   '반환일시'
        ];
        for(let i=0; i<hlist.length; i++){
            header.push({"text" : hlist[i]});
        }

        data.push(header);

        let picked_list = [];
        for (let [idx, row] of res['list'].entries()) {
            let execelObj = {
                uid : row.uid,
                media : escapeEmpty(row.media),
                request_date : escapeEmpty(row.request_date),
                response_code : row.response_code,
                error_msg : escapeEmpty(row.error_msg),
                response_date : escapeEmpty(row.response_date)
            }
            picked_list.push(execelObj);
        }

        for (let row of picked_list) {
            let rowList = [];
            for (const [key, value] of Object.entries(row)) {
                rowList.push({"text" : value});
            };
            data.push(rowList);
        }

        let tableData = [{"sheetName": "Sheet1", "data": data}];
        let options = {fileName: "api_log"};
        Jhxlsx.export(tableData, options);
        log.params['excel'] = false;
    },
    setTable: function(res){
        // console.log("res : ", res)
        let html = "";
        if(res.success){
            for (let [idx, row] of res['list'].entries()) {
                let request_date = row['request_date'];
                request_date = request_date.replaceAll(' ', '<br/>');
                
                let message = (ObjectUtils.isNotEmpty(
                    row['error_msg'])? row['error_msg'] : "");

                let response_date = row['response_date'];
                response_date = response_date.replaceAll(' ', '<br/>');

                html += `<tr>\n`;
                html += `   <td>${row['uid']}</td>\n`;
                html += `   <td>${row['media']}</td>\n`;
                html += `   <td class="date">${request_date}</td>\n`;
                html += `   <td>${row['response_code']}</td>\n`;
                html += `   <td>${message}</td>\n`;
                html += `   <td class="date">${response_date}</td>\n`;
                html += `</tr>\n`;
            }
            $("#totalCnt").text(res.cnt);

            let lastPage = res.last_page;
            let currentPage = log.params["page"];
            log.pagination(currentPage, lastPage);
        }else{
            alert(res.message);
        }
        $("#log_list").html(html);
    },
    changePage: function(page){
        log.params['page'] = page
        log.getLog();
    },
    pagination: function(currentPage, lastPage){
        let html = ""; 
        let pagePerBlock = 5;

        let pageGroup = Math.ceil(currentPage / pagePerBlock) - 1;
        let start = (pageGroup * pagePerBlock) + 1;
        let last = (pageGroup + 1) * pagePerBlock;

        // 전 페이지 블록으로
        if(start > pagePerBlock){
            html += `<a onclick='log.changePage(${start-pagePerBlock})' class="navi">이전</a>\n`;
        }
        // 중간 페이지
        for(let i=start; i <= last; i++){
            if(i > lastPage) break;
            if(i == currentPage) {
                html += `<a onclick='log.changePage(${i})' class='active'>${i}</a>\n`;
            }else{
                html += `<a onclick='log.changePage(${i})'>${i}</a>\n`;
            }
        }
        // 다음 페이지 블록으로
        if(currentPage + pagePerBlock <= lastPage){
            html += `<a onclick='log.changePage(${last+1})' class="navi">다음</a>\n`;
        }
        $(".pagenation").html(html);
    }
}

