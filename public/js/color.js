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

	// Setting onclick functionality to both arrow and button because Firefox does not detect the click of button properly

	// Create arrows
	for(var i = 0; i < colorPalette.length/2; i++){
		html += `
						<div class="arrow-container" title="${rgb2hex(colorPalette[i])}" onclick="copyToClipboard(this.title, ${i})" style="top: ${rgb2posSaturated(colorPalette[i])[0]}px; left:${rgb2posSaturated(colorPalette[i])[1]}px; -webkit-transform: rotate(${rgb2hsv(colorPalette[i])[0]}deg); transform: rotate(${rgb2hsv(colorPalette[i])[0]}deg)">
							<div class="colorsample-arrow" style="border-bottom-width: ${rgb2hsv(colorPalette[i])[1]+10}px"></div>
						</div>
						`
	}

	// Create color circles
	for(var i = 0; i < colorPalette.length/2; i++){
		html += `
						<button id="colorsample-${i}" class="colorsample-container" value="${rgb2hex(colorPalette[i])}"  style="top: ${rgb2posSaturated(colorPalette[i])[0]}px; left:${rgb2posSaturated(colorPalette[i])[1]}px;">
							<div onclick="copyToClipboard(this.value, ${i})" class="colorsample" style="background: ${rgb2hex(colorPalette[i])};"></div>
						</button>
							`
	}

	// Create color tooltips
	for(var i = 0; i < colorPalette.length/2; i++){
		html += `<div id="tooltip-${i}" class="tooltip-hex" style="top: ${rgb2posSaturated(colorPalette[i])[0]}px; left:${rgb2posSaturated(colorPalette[i])[1]}px;">${rgb2hex(colorPalette[i])}</div>`
	}

	document.getElementById("colorwheel").innerHTML = html;

}

function createImageSamples(colorPalette){
	var colorImageSamples = document.getElementById("color-image-samples");

	// Create color circles
	var html = `<svg viewBox="0,0,${colorImageSamples.width},${colorImageSamples.height}">`;
	for(var i = 0; i < colorPalette.length/2; i++){
		html += `	<circle class="colorsample-image" style="background: ${rgb2hex(colorPalette[i])};" cx="${colorPositions[i][0]*colorImageSamples.width}" cy="${colorPositions[i][1]*colorImageSamples.height}" r="30" stroke="white" stroke-width="3" fill="${rgb2hex(colorPalette[i])}" /> `;
	}
	html += "</svg>";

	colorImageSamples.innerHTML = html;

}


function createCanvasPalette(canvas, colorPalette, colorPositions, radius=0.03){

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
  setMessage('color', 'success', messageList[8]);


		for(var i = 0; i < colorPalette.length/2; i++){
			document.getElementsByClassName('colorsample-arrow')[i].classList.add('hide-arrow-anim');

			document.getElementsByClassName('arrow-container')[i].style = `top: ${rgb2posSaturated(colorPalette[i+(colorPalette.length/2)])[0]}px;
																																		 left: ${rgb2posSaturated(colorPalette[i+(colorPalette.length/2)])[1]}px;
																																		 -webkit-transform: rotate(${rgb2hsv(colorPalette[i+(colorPalette.length/2)])[0]}deg);
																																		 transform: rotate(${rgb2hsv(colorPalette[i+(colorPalette.length/2)])[0]}deg)
																																		`

			document.getElementsByClassName('colorsample-arrow')[i].style = `border-bottom-width: ${rgb2hsv(colorPalette[i+(colorPalette.length/2)])[1]+20}px;`
			document.getElementsByClassName('colorsample-container')[i].style = `top: ${rgb2posSaturated(colorPalette[i+(colorPalette.length/2)])[0]}px;
																																					 left:${rgb2posSaturated(colorPalette[i+(colorPalette.length/2)])[1]}px;
																																					 `

			document.getElementsByClassName('tooltip-hex')[i].style = `top: ${rgb2posSaturated(colorPalette[i+(colorPalette.length/2)])[0]}px;
																																					 left:${rgb2posSaturated(colorPalette[i+(colorPalette.length/2)])[1]}px;
																																					 `
			document.getElementsByClassName('tooltip-hex')[i].innerHTML = `${rgb2hex(colorPalette[i+(colorPalette.length/2)])}`;
			document.getElementsByClassName('colorsample-container')[i].value = `${rgb2hex(colorPalette[i+(colorPalette.length/2)])}`;
			document.getElementsByClassName('arrow-container')[i].title = `${rgb2hex(colorPalette[i+(colorPalette.length/2)])}`;
			document.getElementsByClassName('colorsample')[i].style = `background: ${rgb2hex(colorPalette[i+(colorPalette.length/2)])};`
			document.getElementsByClassName('colorsample-image')[i].setAttribute("fill", rgb2hex(colorPalette[i+(colorPalette.length/2)]));

			// Check if color is changed
			if(colorPalette[i+(colorPalette.length/2)][0] != colorPalette[i][0] || colorPalette[i+(colorPalette.length/2)][1] != colorPalette[i][1] || colorPalette[i+(colorPalette.length/2)][2] != colorPalette[i][2]){
				document.getElementsByClassName('colorsample-image')[i].setAttribute("stroke-width", 8);
				document.getElementsByClassName('colorsample-image')[i].setAttribute("r", 35);
				console.log(colorPalette[i+(colorPalette.length/2)]);
				console.log(colorPalette[i]);
			}

			document.getElementsByClassName('harmonize-btn')[0].disabled = true;
			document.getElementsByClassName('harmonize-reset-btn')[0].disabled = false;
		}
		setTimeout(function() {
			for(var i = 0; i < colorPalette.length/2; i++){
				document.getElementsByClassName('colorsample-arrow')[i].classList.remove('hide-arrow-anim');
			}
		}, 800);

		setScore('color', score[1], 100);
}

function resetHarmonizeButton(){
	setMessage('color', messages['color']['type'], messageList[messages['color']['message']]);
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
		document.getElementsByClassName('tooltip-hex')[i].style = `top: ${rgb2posSaturated(colorPalette[i])[0]}px;
																															 left:${rgb2posSaturated(colorPalette[i])[1]}px;
																															`
		document.getElementsByClassName('tooltip-hex')[i].innerHTML = `${rgb2hex(colorPalette[i])}`;
		document.getElementsByClassName('colorsample-container')[i].value = `${rgb2hex(colorPalette[i])}`;
		document.getElementsByClassName('arrow-container')[i].title = `${rgb2hex(colorPalette[i])}`;
		document.getElementsByClassName('colorsample')[i].style = `background: ${rgb2hex(colorPalette[i])};`
		document.getElementsByClassName('colorsample-image')[i].setAttribute("fill", rgb2hex(colorPalette[i]));

		document.getElementsByClassName('colorsample-image')[i].setAttribute("stroke-width", 3);
		document.getElementsByClassName('colorsample-image')[i].setAttribute("r", 30);


		document.getElementsByClassName('harmonize-btn')[0].disabled = false;
		document.getElementsByClassName('harmonize-reset-btn')[0].disabled = true;
	}
	setTimeout(function() {
		for(var i = 0; i < colorPalette.length/2; i++){
			document.getElementsByClassName('colorsample-arrow')[i].classList.remove('hide-arrow-anim');
		}
	}, 800);

	setScore('color', 100, score[1]);
}

// Copies passed value to the clipboard, it creates a temporary input
function copyToClipboard(value, elementIndex){

	var tempInput = document.createElement("input");
	tempInput.style = "position: absolute; left: -1000px; top: -1000px";
	tempInput.value = value;
	document.body.appendChild(tempInput);
	tempInput.select();
	document.execCommand("copy");
	document.body.removeChild(tempInput);
	console.log("Copied: "+value);
	var tooltipValue = document.getElementById('tooltip-'+elementIndex).innerHTML;
	document.getElementById('tooltip-'+elementIndex).innerHTML = 'Copied to clipboard!';
	document.getElementById('colorsample-'+elementIndex).classList.add('colorsample-clicked');

	setTimeout(function() {
		document.getElementById('tooltip-'+elementIndex).innerHTML = tooltipValue;
		document.getElementById('colorsample-'+elementIndex).classList.remove('colorsample-clicked');
	}, 800);

}
