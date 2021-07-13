function lockScroll(){
    $html = $('html'); 
    $body = $('body'); 
    var initWidth = $body.outerWidth();
    var initHeight = $body.outerHeight();

    var scrollPosition = [
        self.pageXOffset || document.documentElement.scrollLeft || document.body.scrollLeft,
        self.pageYOffset || document.documentElement.scrollTop  || document.body.scrollTop
    ];
    $html.data('scroll-position', scrollPosition);
    $html.data('previous-overflow', $html.css('overflow'));
    $html.css('overflow', 'hidden');
    window.scrollTo(scrollPosition[0], scrollPosition[1]);   

    var marginR = $body.outerWidth()-initWidth;
    var marginB = $body.outerHeight()-initHeight; 
    $body.css({'margin-right': marginR,'margin-bottom': marginB});
} 

function unlockScroll(){
    $html = $('html');
    $body = $('body');
    $html.css('overflow', $html.data('previous-overflow'));
    var scrollPosition = $html.data('scroll-position');
    window.scrollTo(scrollPosition[0], scrollPosition[1]);

    $body.css({'margin-right': 0, 'margin-bottom': 0});
}

$('img.popup-image').css({cursor: 'pointer'}).live('click', function () {
    var img = $(this);
    lockScroll();
    var bigImg = $('<img />').css({
        'max-width': '90%',
        'max-height': '90%',
        'display': 'inline',
        'position': 'fixed',
        'left': '50%',
        'top': '50%',
        'transform': 'translate(-50%, -50%)'
    });
    bigImg.attr({
        src: img.attr('src'),
        alt: img.attr('alt'),
        title: img.attr('title')
    });
    var over = $('<div />').text(' ').css({
        'height': '100%',
        'width': '100%',
        'background': 'rgba(0,0,0,.82)',
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'opacity': 0.0,
        'cursor': 'pointer',
        'z-index': 9999,
        'text-align': 'center'
    }).append(bigImg).bind('click', function () {
    $(this).fadeOut(300, function () {
        $(this).remove();
        unlockScroll();
    });
    }).insertAfter(this).animate({
        'opacity': 1
    }, 300);
});