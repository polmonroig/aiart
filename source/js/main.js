
// ------------------------------------
// HELPER FUNCTIONS TO TEST FOR SPECIFIC DISPLAY SIZE (RESPONSIVE HELPERS)
// ------------------------------------

function is_display_type(display_type){
  return ($('.display-type').css('content') == display_type) || ($('.display-type').css('content') == '"'+display_type+'"');
}
function not_display_type(display_type){
  return ($('.display-type').css('content') != display_type) && ($('.display-type').css('content') != '"'+display_type+'"');
}

// Scroll-up button
$(document).ready(function(){

	// hide #back-top first
	$("#scroll-up").hide();

	// fade in #back-top
	$(function () {
		$(window).scroll(function () {
			if ($(this).scrollTop() > 100) {
				$('#scroll-up').fadeIn();
			} else {
				$('#scroll-up').fadeOut();
			}
		});

		// scroll body to 0px on click
		$('#scroll-up').click(function () {
			$('body,html').animate({
				scrollTop: 0
			}, 400);
			return false;
		});
	});

});

// Initiate on click and on hover sub menu activation logic
function os_init_sub_menus(){

  // INIT MENU TO ACTIVATE ON HOVER
  var menu_timer;
  $('.menu-activated-on-hover').on('mouseenter', 'ul.main-menu > li.has-sub-menu', function(){
    var $elem = $(this);
    clearTimeout(menu_timer);
    $elem.closest('ul').addClass('has-active').find('> li').removeClass('active');
    $elem.addClass('active');
  });

  $('.menu-activated-on-hover').on('mouseleave', 'ul.main-menu > li.has-sub-menu', function(){
    var $elem = $(this);
    menu_timer = setTimeout(function(){
      $elem.removeClass('active').closest('ul').removeClass('has-active');
    }, 30);
  });

  // INIT MENU TO ACTIVATE ON CLICK
  $('.menu-activated-on-click').on('click', 'li.has-sub-menu > a', function(event){
    var $elem = $(this).closest('li');
    if($elem.hasClass('active')){
      $elem.removeClass('active');
    }else{
      $elem.closest('ul').find('li.active').removeClass('active');
      $elem.addClass('active');
    }
    return false;
  });

}

$(function(){

  // #11. MENU RELATED STUFF

  // INIT MOBILE MENU TRIGGER BUTTON
  $('.mobile-menu-trigger').on('click', function(){
    $('.menu-mobile .menu-and-user').slideToggle(200, 'swing');
    return false;
  });



  os_init_sub_menus();

  // #12. CONTENT SIDE PANEL TOGGLER

  $('.content-panel-toggler, .content-panel-close, .content-panel-open').on('click', function(){
    $('.all-wrapper').toggleClass('content-panel-active');
  });



  // #16. OUR OWN CUSTOM DROPDOWNS
  $('.os-dropdown-trigger').on('mouseenter', function(){
    $(this).addClass('over');
  });
  $('.os-dropdown-trigger').on('mouseleave', function(){
    $(this).removeClass('over');
  });



  // #21. Onboarding Screens Modal

  $('.onboarding-modal.show-on-load').modal('show');
  if($('.onboarding-modal .onboarding-slider-w').length){
    $('.onboarding-modal .onboarding-slider-w').slick({
      dots: true,
      infinite: false,
      adaptiveHeight: true,
      slidesToShow: 1,
      slidesToScroll: 1
    });
    $('.onboarding-modal').on('shown.bs.modal', function (e) {
      $('.onboarding-modal .onboarding-slider-w').slick('setPosition');
    })
  }



});
