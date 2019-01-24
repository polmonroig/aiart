/*

Main javascript functions to init most of the elements

#1. CHAT APP
#2. CALENDAR INIT
#3. FORM VALIDATION
#4. DATE RANGE PICKER
#5. DATATABLES
#6. EDITABLE TABLES
#7. FORM STEPS FUNCTIONALITY
#8. SELECT 2 ACTIVATION
#9. CKEDITOR ACTIVATION
#10. CHARTJS CHARTS http://www.chartjs.org/
#11. MENU RELATED STUFF
#12. CONTENT SIDE PANEL TOGGLER
#13. EMAIL APP
#14. FULL CHAT APP
#15. CRM PIPELINE
#16. OUR OWN CUSTOM DROPDOWNS
#17. BOOTSTRAP RELATED JS ACTIVATIONS
#18. TODO Application
#19. Fancy Selector
#20. SUPPORT SERVICE
#21. Onboarding Screens Modal
#22. Colors Toggler
#23. Auto Suggest Search
#24. Element Actions

*/

// ------------------------------------
// HELPER FUNCTIONS TO TEST FOR SPECIFIC DISPLAY SIZE (RESPONSIVE HELPERS)
// ------------------------------------

function is_display_type(display_type){
  return ($('.display-type').css('content') == display_type) || ($('.display-type').css('content') == '"'+display_type+'"');
}
function not_display_type(display_type){
  return ($('.display-type').css('content') != display_type) && ($('.display-type').css('content') != '"'+display_type+'"');
}


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
