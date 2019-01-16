"use strict";
//Process image
function processImage(responseText){

  // Reset visibility for animation
  document.getElementsByClassName('balance-index')[0].classList.remove('balance-main-anim');
  document.getElementsByClassName('color-index')[0].classList.remove('color-main-anim');

  document.getElementsByClassName('balance-index')[0].classList.add('balance-main-anim-hide');
  document.getElementsByClassName('color-index')[0].classList.add('color-main-anim-hide');

  document.getElementById('upload-wrapper').classList.add('upload-main-anim-hide');

  var delayInMilliseconds = 500;
  setTimeout(function() {

    document.getElementById('color-wrapper').classList.add('hidden');
    document.getElementById('balance-wrapper').classList.add('hidden');

    document.getElementsByClassName('balance-index')[0].classList.remove('balance-main-anim-hide');
    document.getElementsByClassName('color-index')[0].classList.remove('color-main-anim-hide');
    // Display and hide elements
    if(!document.getElementById('upload-wrapper').classList.contains("hidden")){
      document.getElementsByClassName('dropzone-menu')[0].classList.remove('hidden');
      document.getElementsByClassName('dropzone-menu')[1].classList.remove('hidden');
      document.getElementById('upload-wrapper').classList.add('hidden');
      document.getElementById('color-wrapper').classList.remove('hidden');
      document.getElementById('balance-wrapper').classList.remove('hidden');
      document.getElementsByClassName('balance-index')[0].classList.add('balance-main-anim');
      document.getElementsByClassName('color-index')[0].classList.add('color-main-anim');
    }else{
      document.getElementById('color-wrapper').classList.remove('hidden');
      document.getElementById('balance-wrapper').classList.remove('hidden');
      document.getElementsByClassName('balance-index')[0].classList.add('balance-main-anim');
      document.getElementsByClassName('color-index')[0].classList.add('color-main-anim');
    }

    //Handle response text
    var colorPalette = responseText["color_palette"];

    // Heatmap

    var message = 'Your composition is slightly out of balance, try to add or eliminate an element to compensate properly!';
    document.getElementsByClassName('message-content-balance')[0].innerHTML = message;

    document.getElementById('balance-image').classList.remove('hidden');
    var imageWidth = document.getElementById('balance-image').getElementsByTagName('img')[0].clientWidth;
    var imageHeight = document.getElementById('balance-image').getElementsByTagName('img')[0].clientHeight;

    document.getElementById('heatmap').classList.remove('hidden');
    document.getElementById('heatmap-balanced').classList.remove('hidden');

    document.getElementById('heatmap').width = imageWidth;
    document.getElementById('heatmap').height = imageHeight;
    document.getElementById('heatmap-balanced').width = imageWidth;
    document.getElementById('heatmap-balanced').height = imageHeight;


    var datapoints = [];
    var datapoints_balanced = [];

    for(var i = 0; i < responseText["datapoints"].length; ++i){
      var point = {
					x: responseText["datapoints"][i][0],
					y: responseText["datapoints"][i][1],
					w: responseText["datapoints"][i][2],
					sx: responseText["datapoints"][i][3],
					sy: responseText["datapoints"][i][4]
        }
      datapoints.push(point);

    }


    for(var i = 0; i < responseText["datapoints_balanced"].length; ++i){
      var point = {
          x: responseText["datapoints_balanced"][i][0],
          y: responseText["datapoints_balanced"][i][1],
          w: responseText["datapoints_balanced"][i][2],
					sx: responseText["datapoints_balanced"][i][3],
					sy: responseText["datapoints_balanced"][i][4]
        }
      datapoints_balanced.push(point);

    }
		console.log(datapoints_balanced);
		console.log(datapoints);

    const heatmap = new Heatmap(document.getElementById('heatmap'), datapoints, 0.06);
    heatmap.createHeatmap();

    const heatmapBalanced = new Heatmap(document.getElementById('heatmap-balanced'), datapoints_balanced, 0.06);
    heatmapBalanced.createHeatmap();
    document.getElementById('heatmap-balanced').classList.add('hidden');

		document.getElementById('heatmap').classList.remove('hidden');
		document.getElementById('heatmap-balanced').classList.add('hidden');

		var message = 'Your composition is slightly out of balance, try to add or eliminate an element to compensate properly!';
		document.getElementsByClassName('message-content-balance')[0].innerHTML = message;
		document.getElementsByClassName('message-content-balance')[0].classList.add('message-wrong');
		document.getElementsByClassName('message-content-balance')[0].classList.remove('message-fixed');


    //COLOR PROCESS


    createColorSamples(colorPalette[0], colorPalette[1], colorPalette[2], colorPalette[3], colorPalette[4], colorPalette[5], colorPalette[6], colorPalette[7]);
    createColorPalette(colorPalette[0], colorPalette[1], colorPalette[2], colorPalette[3], colorPalette[4], colorPalette[5], colorPalette[6], colorPalette[7]);
    console.log("Color processed");

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

    // Show tooltips of hex
    $(document).ready(function(){
      $('[data-toggle="tooltip"]').tooltip();
    });


  }, delayInMilliseconds);
}

//Load image
function showImage(file, displayArea){
  var displayArea = document.getElementById(displayArea);
  var imageType = /image.*/;

  if (file.type.match(imageType)) {
      var reader = new FileReader();

      reader.onload = function(e) {
          displayArea.innerHTML = "";

          var img = new Image();
          img.src = reader.result;

          displayArea.appendChild(img);
      }
      reader.readAsDataURL(file);
  }
}
