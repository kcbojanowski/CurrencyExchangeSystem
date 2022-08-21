
function replaceWal() {
    document.getElementById("divhis").style.display="none";
    document.getElementById("divwal").style.display="block";
}
function replaceHis() {
    document.getElementById("divwal").style.display = "none";
    document.getElementById("divhis").style.display = "block";
}

function sell() {
    let content = $('#message-input').val(); // get message content
    let code = $('#UserSelect').val();

    $.ajax({
        url: "/profile",
        type: "POST",
        data: JSON.stringify({
        'amount': content,
        'code': code,
        'type': 'sell'
        }),
        contentType: "application/json",
    })
    .done(function (data){
        $('#message-input').val('1')
    })
    .fail(function (xhr, status, errorThrown){
        alert("Cannot add message")
    })
}
function buy() {
    let content = $('#message-input').val(); // get message content
    let code = $('#UserSelect').val();

    $.ajax({
        url: "/profile",
        type: "POST",
        data: JSON.stringify({
        'content': content,
        'code': code,
        'type': 'buy'
        }),
        contentType: "application/json",
    })
    .done(function (data){
        $('#message-input').val('1')
    })
    .fail(function (xhr, status, errorThrown){
        alert("Cannot add message")
    })
}


$('.slider-top').slick({
   slidesToShow: 1,
   slidesToScroll: 1,
   arrows: false,
   fade: true,
   asNavFor: '.slider-bottom'
 });

 $('.slider-bottom').slick({
   slidesToShow: 3,
   slidesToScroll: 1,
   asNavFor: '.slider-top',
   dots: true,
   focusOnSelect: true,
 });

 $('a[data-slide]').click(function(e) {
   e.preventDefault();
   let slide = $(this).data('slide');
   $('.slider-bottom').slick('slickGoTo', slide - 1);
 });
