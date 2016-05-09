function setBackTop() {
    var mainFloating = $('#main-floating');
    var backTopFloating = $('#back-top-floating');

    backTopFloating.bind('click', function() {
       $('body').animate({
           scrollTop: 0
       }, 500);
    });

    $(window).scroll(function() {
        var sTop = $('body').scrollTop() || $('html').scrollTop();

        if (sTop > 500) {
            mainFloating.hide();
            backTopFloating.show();
        } else {
            mainFloating.show();
            backTopFloating.hide();
        }
    });
}

$(document).ready(function() {
    Materialize.updateTextFields();
    setBackTop();
});