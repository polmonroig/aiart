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

	var colorwheel_size = 270;
	var colorsample_size = 40;
	var hsv = rgb2hsv(rgb);
	var top = ((Math.sin((hsv[0]+90) * Math.PI / 180) * hsv[1]) + 100) * colorwheel_size/100/2;
	var left = ((Math.cos((hsv[0]+90) * Math.PI / 180) * hsv[1]) + 100) * colorwheel_size/100/2;
	top = Math.trunc(top)-colorsample_size/2;
	left = Math.trunc(left)-colorsample_size/2;
	return [top, left];
}

function rgb2posSaturated(rgb){

	var colorwheel_size = 270;
	var colorsample_size = 40;
	var hsv = rgb2hsv(rgb);
	hsv[1] = hsv[1]+30 >= 95 ? 95 : hsv[1]+30;
	var top = ((Math.sin((hsv[0]+90) * Math.PI / 180) * hsv[1]) + 100) * colorwheel_size/100/2;
	var left = ((Math.cos((hsv[0]+90) * Math.PI / 180) * hsv[1]) + 100) * colorwheel_size/100/2;
	top = Math.trunc(top)-colorsample_size/2;
	left = Math.trunc(left)-colorsample_size/2;
	return [top, left];
}


function createColorSamples(colorPalette){
	var html = "";

	// Create arrows
	for(var i = 0; i < colorPalette.length/2; i++){
		html += `
						<div class="arrow-container" style="top: ${rgb2posSaturated(colorPalette[i])[0]}px; left:${rgb2posSaturated(colorPalette[i])[1]}px; -webkit-transform: rotate(${rgb2hsv(colorPalette[i])[0]}deg); transform: rotate(${rgb2hsv(colorPalette[i])[0]}deg)">
							<div class="colorsample-arrow" style="border-bottom-width: ${rgb2hsv(colorPalette[i])[1]+20}px"></div>
						</div>
						`
	}

	// Create color circles
	for(var i = 0; i < colorPalette.length/2; i++){
		html += `
						<button class="colorsample-container" style="top: ${rgb2posSaturated(colorPalette[i])[0]}px; left:${rgb2posSaturated(colorPalette[i])[1]}px;" data-placement="top" data-toggle="tooltip" title=${rgb2hex(colorPalette[i])}>
							<div class="colorsample" style="background: ${rgb2hex(colorPalette[i])};"></div>
						</button>
							`
	}

	//class = "color-harmonized hidden"  Class of harmonized buttons

	document.getElementById("colorwheel").innerHTML = html;

	// Show tooltips of hex
	$(document).ready(function(){
		$('[data-toggle="tooltip"]').tooltip();
	});

}


function createCanvasPalette(canvas, colorPalette, colorPositions, radius=0.05){

		var colorCtx = canvas.getContext('2d');

		// Clear canvas
		colorCtx.clearRect(0, 0, canvas.offsetWidth, canvas.offsetHeight);

		for (var i = 0; i < colorPalette.length; i++) {
				var sample = colorPalette[i];
				var position = colorPositions[i];
				colorCtx.strokeStyle = 'white';
				colorCtx.lineWidth = 0.005*canvas.offsetWidth;

				// Circle draw
				//colorCtx.moveTo(position[0]*canvas.offsetWidth, position[1]*canvas.offsetHeight);
				colorCtx.fillStyle = 'rgb('+sample[0]+','+sample[1]+','+sample[2]+')';
				colorCtx.beginPath();
				colorCtx.arc(position[0]*canvas.offsetWidth, position[1]*canvas.offsetHeight, radius*canvas.offsetWidth, 0, 2 * Math.PI);
				colorCtx.closePath();
				colorCtx.fill();
				colorCtx.stroke();
		}

}

function harmonizeButton(){

  var message = 'Color harmonized! check the new color palette and improve your image.';
  document.getElementsByClassName('message-content-color')[0].innerHTML = message;
  document.getElementsByClassName('message-content-color')[0].classList.remove('message-wrong');
  document.getElementsByClassName('message-content-color')[0].classList.add('message-fixed');


		for(var i = 0; i < colorPalette.length/2; i++){
			document.getElementsByClassName('colorsample-arrow')[i].classList.add('hide-arrow-anim');

			document.getElementsByClassName('arrow-container')[i].style = `top: ${rgb2posSaturated(colorPalette[i+5])[0]}px;
																																		 left: ${rgb2posSaturated(colorPalette[i+5])[1]}px;
																																		 -webkit-transform: rotate(${rgb2hsv(colorPalette[i+5])[0]}deg);
																																		 transform: rotate(${rgb2hsv(colorPalette[i+5])[0]}deg)
																																		`

			document.getElementsByClassName('colorsample-arrow')[i].style = `border-bottom-width: ${rgb2hsv(colorPalette[i+5])[1]+20}px;`
			document.getElementsByClassName('colorsample-container')[i].style = `top: ${rgb2posSaturated(colorPalette[i+5])[0]}px;
																																					 left:${rgb2posSaturated(colorPalette[i+5])[1]}px;
																																					 `
			document.getElementsByClassName('colorsample-container')[i].title = `${rgb2hex(colorPalette[i+5])}`;
			document.getElementsByClassName('colorsample')[i].style = `background: ${rgb2hex(colorPalette[i+5])};`

			document.getElementsByClassName('harmonize-btn')[0].disabled = true;
			document.getElementsByClassName('harmonize-reset-btn')[0].disabled = false;
		}
		setTimeout(function() {
			for(var i = 0; i < colorPalette.length/2; i++){
				document.getElementsByClassName('colorsample-arrow')[i].classList.remove('hide-arrow-anim');
			}
		}, 800);

		// Show tooltips of hex
		$(document).ready(function(){
			$('[data-toggle="tooltip"]').tooltip();
		});

}

function resetHarmonizeButton(){

  var message = 'The color palette of the image is not ideal! check the harmnized verison to improve it';
  document.getElementsByClassName('message-content-color')[0].innerHTML = message;
  document.getElementsByClassName('message-content-color')[0].classList.add('message-wrong');
  document.getElementsByClassName('message-content-color')[0].classList.remove('message-fixed');
  document.getElementById('colorwheel').classList.remove('colorwheel-anim-show');

	for(var i = 0; i < colorPalette.length/2; i++){
		document.getElementsByClassName('colorsample-arrow')[i].classList.add('hide-arrow-anim');
		document.getElementsByClassName('arrow-container')[i].style = `top: ${rgb2posSaturated(colorPalette[i])[0]}px;
																																	 left: ${rgb2posSaturated(colorPalette[i])[1]}px;
																																	 -webkit-transform: rotate(${rgb2hsv(colorPalette[i])[0]}deg);
																																	 transform: rotate(${rgb2hsv(colorPalette[i])[0]}deg)
																																	`

		document.getElementsByClassName('colorsample-arrow')[i].style = `border-bottom-width: ${rgb2hsv(colorPalette[i])[1]+20}px;`
		document.getElementsByClassName('colorsample-container')[i].style = `top: ${rgb2posSaturated(colorPalette[i])[0]}px;
																																				 left:${rgb2posSaturated(colorPalette[i])[1]}px;
																																				 `
		document.getElementsByClassName('colorsample-container')[i].title = `${rgb2hex(colorPalette[i])}`;
		document.getElementsByClassName('colorsample')[i].style = `background: ${rgb2hex(colorPalette[i])};`

		document.getElementsByClassName('harmonize-btn')[0].disabled = false;
		document.getElementsByClassName('harmonize-reset-btn')[0].disabled = true;
	}
	setTimeout(function() {
		for(var i = 0; i < colorPalette.length/2; i++){
			document.getElementsByClassName('colorsample-arrow')[i].classList.remove('hide-arrow-anim');
		}
	}, 800);

}
