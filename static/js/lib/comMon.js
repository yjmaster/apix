

/*스크롤바*/
(function ($) {
    $(window).on("load", function () {
        $(".scroll").mCustomScrollbar();
    });
})(jQuery);
/*//스크롤바*/


/*AI추천 샘플용*/
$(document).ready(function ($) {
    $('.btn_recommend').click(function () {
    $('.title_sample_txt').addClass('active');

    });
    
    $('.btn_recommend02').click(function () {
    $('.data-div02').addClass('active');

    });
    
    $('.btn_recommend03').click(function () {
    $('.category_list_box').addClass('active')
    $('.img_group_list').addClass('active');

    });
    
    $('.btn_recommend04').click(function () {
    $('.relation_arti_list').addClass('active')
    $('.img_group_list03').addClass('active');

    });
    
    $('.btn_recommend05').click(function () {
    $('.recommend_photo_area').addClass('active');
    $('.upload_ico_box').css('display','none');

    });
});
/*//AI추천 샘플용*/


/*글로벌서치 윈도우팝업 20210416*/

function popup() {
    window.open("global_search_winpop.html", "#winpop04", "width=1600, height=900, left=0, top=0");
}
/*//글로벌서치  윈도우팝업*/
