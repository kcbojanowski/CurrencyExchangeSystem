function replaceSet() {
    document.getElementById("divset").style.display="block";
    document.getElementById("divwal").style.display="none";
    document.getElementById("divhis").style.display="none";
}

function replaceWal() {
    document.getElementById("divset").style.display="none";
    document.getElementById("divwal").style.display="block";
    document.getElementById("divhis").style.display="none";
}
function replaceHis() {
    document.getElementById("divset").style.display = "none";
    document.getElementById("divwal").style.display = "none";
    document.getElementById("divhis").style.display = "block";
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
