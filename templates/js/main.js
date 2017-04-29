/**
 * Created by sp41mer on 20.01.17.
 */
const photoParserUrl = '/parse_photos';
var serverResponse;

$(document).ready(function(){
    $('.result_picture_row').hide();
    $('.preloader_row').hide();
    $('.after_click').hide();
    $('.result_row').hide();
    $('.more_row').hide();
    $('.recomend_button__main').click(function(){
        $('.recomend_button__main').hide();
        $('.after_click').show();
    });
    $('.recomend_button__ok').click(function(){
        var accountData = $('.recomend_button__text__input').val();
        $('.recomend_button__text__input').val('');
        $('.after_click').hide();
        $('.preloader_row').show();
        $.post( photoParserUrl, { "account": accountData})
            .done(function( data ) {
                var jsonData = JSON.parse(data);
                serverResponse = jsonData;
                if (jsonData.error==0){
                    $('.preloader_row').hide();
                    $('.result_row').show();
                    $('#result1').text(jsonData.cities[0].replace(/_/g, " "));
                    $('#result2').text(jsonData.cities[1].replace(/_/g, " "));
                    $('#result3').text(jsonData.cities[2].replace(/_/g, " "));
                    $('.more_row').show();
                }
                else {
                    $('.preloader_row').hide();
                    swal("Аккаунт недоступен!", "Возможно, страница закрыта или введена с ошибкой", "error");
                    $('.more_row').hide();
                    $('.result_row').hide();
                    $('.recomend_button__main').show();
                    $('.result_picture_row').hide();
                    $('.picture_row').show();
                }
            });
    });
    $('.more_row__button').click(function(){
        $('.more_row').hide();
        $('.result_row').hide();
        $('.recomend_button__main').show();
        $('.result_picture_row').hide();
        $('.picture_row').show();
    });
    $('.result_button').click(function(){
        var city = $($(this).find('span')[0]).text().replace(/ /g, "_");
        $('.picture_row').hide();
        $('.result_picture_row').show();
        $.each($('.result_picture__img__user'),function(key,value){
            $(value).attr('src', serverResponse.photos[city][key].user)
        });
        $.each($('.result_picture__img__account'),function(key,value){
            $(value).attr('src', serverResponse.photos[city][key].city)
        });
    })
});
