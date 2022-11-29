$(document).ready(function(){
    let log = {
        init: function(){
            let browser = $(window).height();
            let wraper = $("#wraper").height();
            let top = (browser - wraper) / 2;
        
            $("#wraper").css("margin-top", `${top}px`);
        
            let edate = new Date().format();
            let sdate = new Date(edate)['getMonths'](-1);  
        
            let range_date = $("#dateRange").datepicker(
                {type : "range", minDate : new Date().getMonths(-1), maxDate : edate});
        
            range_date.datepicker('setDateRange',  sdate, edate);

        }
    }
    log.init();
});