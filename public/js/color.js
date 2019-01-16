"use strict";
//Function to convert rgb format to a hsv color
function rgb2hsv (rgb) {
    var rr, gg, bb,
        r = rgb[0] / 255,
        g = rgb[1] / 255,
        b = rgb[2] / 255,
        h, s,
        v = Math.max(r, g, b),
        diff = v - Math.min(r, g, b),
        diffc = function(c){
            return (v - c) / 6 / diff + 1 / 2;
        };

    if (diff == 0) {
        h = s = 0;
    } else {
        s = diff / v;
        rr = diffc(r);
        gg = diffc(g);
        bb = diffc(b);

        if (r === v) {
            h = bb - gg;
        }else if (g === v) {
            h = (1 / 3) + rr - bb;
        }else if (b === v) {
            h = (2 / 3) + gg - rr;
        }
        if (h < 0) {
            h += 1;
        }else if (h > 1) {
            h -= 1;
        }
    }
    return [
        Math.round(h * 360),
        Math.round(s * 100),
        Math.round(v * 100)
    ];
}

//Function to convert rgb format to a hex color
function rgb2hex(rgb){
 return (rgb && rgb.length === 3) ? "#" +
  ("0" + parseInt(rgb[0],10).toString(16)).slice(-2).toUpperCase() +
  ("0" + parseInt(rgb[1],10).toString(16)).slice(-2).toUpperCase() +
  ("0" + parseInt(rgb[2],10).toString(16)).slice(-2).toUpperCase() : '';
}

//Function to convert rgb format to position
function rgb2pos(rgb){
	var colorwheel_size = 202;
	var colorsample_size = 30;
	var hsv = rgb2hsv(rgb);
	var top = ((Math.sin((hsv[0]+230) * Math.PI / 180) * hsv[2]) + 100) * colorwheel_size/100/2;
	var left = ((Math.cos((hsv[0]+230) * Math.PI / 180) * hsv[2]) + 100) * colorwheel_size/100/2;
	top = Math.trunc(top)-colorsample_size/2;
	left = Math.trunc(left)-colorsample_size/2;
	return [top, left];
}


function createColorSamples(rgb_original_1, rgb_original_2, rgb_original_3, rgb_original_4, rgb_harmonized_1, rgb_harmonized_2, rgb_harmonized_3, rgb_harmonized_4){

	var html = `
		<button class="colorsample color-original" style="background: ${rgb2hex(rgb_original_1)}; top: ${rgb2pos(rgb_original_1)[0]}px; left:${rgb2pos(rgb_original_1)[1]}px;" data-placement="top" data-toggle="tooltip" title=${rgb2hex(rgb_original_1)}></button>
		<button class="colorsample color-original" style="background: ${rgb2hex(rgb_original_2)}; top: ${rgb2pos(rgb_original_2)[0]}px; left:${rgb2pos(rgb_original_2)[1]}px; " data-placement="top" data-toggle="tooltip" title=${rgb2hex(rgb_original_2)}></button>
		<button class="colorsample color-original" style="background: ${rgb2hex(rgb_original_3)}; top: ${rgb2pos(rgb_original_3)[0]}px; left:${rgb2pos(rgb_original_3)[1]}px; " data-placement="top" data-toggle="tooltip" title=${rgb2hex(rgb_original_3)}></button>
		<button class="colorsample color-original" style="background: ${rgb2hex(rgb_original_4)}; top: ${rgb2pos(rgb_original_4)[0]}px; left:${rgb2pos(rgb_original_4)[1]}px;" data-placement="top" data-toggle="tooltip" title=${rgb2hex(rgb_original_4)}></button>
    <button class="colorsample color-harmonized hidden" style="background: ${rgb2hex(rgb_harmonized_1)}; top: ${rgb2pos(rgb_harmonized_1)[0]}px; left:${rgb2pos(rgb_harmonized_1)[1]}px;" data-placement="top" data-toggle="tooltip" title=${rgb2hex(rgb_harmonized_1)}></button>
		<button class="colorsample color-harmonized hidden" style="background: ${rgb2hex(rgb_harmonized_2)}; top: ${rgb2pos(rgb_harmonized_2)[0]}px; left:${rgb2pos(rgb_harmonized_2)[1]}px; " data-placement="top" data-toggle="tooltip" title=${rgb2hex(rgb_harmonized_2)}></button>
		<button class="colorsample color-harmonized hidden" style="background: ${rgb2hex(rgb_harmonized_3)}; top: ${rgb2pos(rgb_harmonized_3)[0]}px; left:${rgb2pos(rgb_harmonized_3)[1]}px; " data-placement="top" data-toggle="tooltip" title=${rgb2hex(rgb_harmonized_3)}></button>
		<button class="colorsample color-harmonized hidden" style="background: ${rgb2hex(rgb_harmonized_4)}; top: ${rgb2pos(rgb_harmonized_4)[0]}px; left:${rgb2pos(rgb_harmonized_4)[1]}px;" data-placement="top" data-toggle="tooltip" title=${rgb2hex(rgb_harmonized_4)}></button>
	`;

	document.getElementById("colorwheel").innerHTML = html;
}

function createColorPalette(rgb_original_1, rgb_original_2, rgb_original_3, rgb_original_4, rgb_harmonized_1, rgb_harmonized_2, rgb_harmonized_3, rgb_harmonized_4){


	var html = `
    <div class="color-row color-original">
      <button class="color-row-sample" style="background: ${rgb2hex(rgb_original_1)};"></button>
      <div class="tooltip-fixed">${rgb2hex(rgb_original_1)}</div>
    </div>
    <div class="color-row color-original">
      <button class="color-row-sample" style="background: ${rgb2hex(rgb_original_2)};"></button>
      <div class="tooltip-fixed">${rgb2hex(rgb_original_2)}</div>
    </div>
    <div class="color-row color-original">
      <button class="color-row-sample" style="background: ${rgb2hex(rgb_original_3)};"></button>
      <div class="tooltip-fixed">${rgb2hex(rgb_original_3)}</div>
    </div>
    <div class="color-row color-original">
      <button class="color-row-sample" style="background: ${rgb2hex(rgb_original_4)};"></button>
      <div class="tooltip-fixed">${rgb2hex(rgb_original_4)}</div>
    </div>
    <div class="color-row color-harmonized hidden">
      <button class="color-row-sample" style="background: ${rgb2hex(rgb_harmonized_1)};"></button>
      <div class="tooltip-fixed">${rgb2hex(rgb_harmonized_1)}</div>
    </div>
    <div class="color-row color-harmonized hidden">
      <button class="color-row-sample" style="background: ${rgb2hex(rgb_harmonized_2)};"></button>
      <div class="tooltip-fixed">${rgb2hex(rgb_harmonized_2)}</div>
    </div>
    <div class="color-row color-harmonized hidden">
      <button class="color-row-sample" style="background: ${rgb2hex(rgb_harmonized_3)};"></button>
      <div class="tooltip-fixed">${rgb2hex(rgb_harmonized_3)}</div>
    </div>
    <div class="color-row color-harmonized hidden">
      <button class="color-row-sample" style="background: ${rgb2hex(rgb_harmonized_4)};"></button>
      <div class="tooltip-fixed">${rgb2hex(rgb_harmonized_4)}</div>
    </div>
	`;

	document.getElementById("palette").innerHTML = html;
}


function harmonizeButton(){

  var message = 'Color harmonized! check the new color palette and improve your image.';
  document.getElementsByClassName('message-content-color')[0].innerHTML = message;
  document.getElementsByClassName('message-content-color')[0].classList.remove('message-wrong');
  document.getElementsByClassName('message-content-color')[0].classList.add('message-fixed');


  document.getElementById('colorwheel').classList.add('colorwheel-anim-hide');

  setTimeout(function() {
    document.getElementById('colorwheel').classList.remove('colorwheel-anim-hide');
    document.getElementById('colorwheel').classList.add('colorwheel-anim-show');

    for(var i = 0; i<document.getElementsByClassName('color-original').length; i++){
      document.getElementsByClassName('color-original')[i].classList.add('hidden');
    }

    for(var i = 0; i<document.getElementsByClassName('color-harmonized').length; i++){
      document.getElementsByClassName('color-harmonized')[i].classList.remove('hidden');
    }
  }, 200);


}

function resetHarmonizeButton(){

  var message = 'The color palette of the image is not ideal! check the harmnized verison to improve it';
  document.getElementsByClassName('message-content-color')[0].innerHTML = message;
  document.getElementsByClassName('message-content-color')[0].classList.add('message-wrong');
  document.getElementsByClassName('message-content-color')[0].classList.remove('message-fixed');
  document.getElementById('colorwheel').classList.remove('colorwheel-anim-show');

  for(var i = 0; i<document.getElementsByClassName('color-original').length; i++){
    document.getElementsByClassName('color-original')[i].classList.remove('hidden');
  }

  for(var i = 0; i<document.getElementsByClassName('color-harmonized').length; i++){
    document.getElementsByClassName('color-harmonized')[i].classList.add('hidden');
  }
}
