"use strict";

// Main function called by response text
function processImage(responseText){

  // Reset visibility of wrappers for initial animation
  document.getElementsByClassName('balance-index')[0].classList.remove('balance-main-anim');
  document.getElementsByClassName('color-index')[0].classList.remove('color-main-anim');
  document.getElementsByClassName('balance-index')[0].classList.add('balance-main-anim-hide');
  document.getElementsByClassName('color-index')[0].classList.add('color-main-anim-hide');
  document.getElementById('upload-wrapper').classList.add('upload-main-anim-hide');

	// Delay functions to allow animation to complete
  var delayInMilliseconds = 500;
  setTimeout(function() {

    document.getElementById('color-wrapper').classList.add('hidden');
    document.getElementById('balance-wrapper').classList.add('hidden');
    document.getElementsByClassName('balance-index')[0].classList.remove('balance-main-anim-hide');
    document.getElementsByClassName('color-index')[0].classList.remove('color-main-anim-hide');

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


    // Handle response text
    var colorPalette = responseText["color_palette"];
    var colorPositions = responseText["color_positions"];
		var datapoints = responseText["datapoints"];
		var datapointsBalanced = responseText["datapoints_balanced"];

    // Heatmap UI
		document.getElementById('heatmap').classList.remove('hidden');
		document.getElementById('heatmap-balanced').classList.remove('hidden');

		var message = 'Your composition is slightly out of balance, try to add or eliminate an element to compensate properly!';
		document.getElementsByClassName('message-content-balance')[0].innerHTML = message;
		document.getElementsByClassName('message-content-balance')[0].classList.add('message-wrong');
		document.getElementsByClassName('message-content-balance')[0].classList.remove('message-fixed');

    document.getElementById('heatmap').classList.remove('hidden');
    document.getElementById('heatmap-balanced').classList.remove('hidden');

		// Set heatmap canvas inital size
		var imageWidth = document.getElementById('balance-image').getElementsByTagName('img')[0].clientWidth;
		var imageHeight = document.getElementById('balance-image').getElementsByTagName('img')[0].clientHeight;
    document.getElementById('heatmap').width = imageWidth;
    document.getElementById('heatmap').height = imageHeight;
    document.getElementById('heatmap-balanced').width = imageWidth;
    document.getElementById('heatmap-balanced').height = imageHeight;

		// Debugging log
		console.log(datapoints);
		console.log(datapointsBalanced);
		console.log(colorPalette.slice(0, 5));
		console.log(colorPositions);

		// Create heapmap
    const heatmap = new Heatmap(document.getElementById('heatmap'), datapoints);
    heatmap.createHeatmap();

    const heatmapBalanced = new Heatmap(document.getElementById('heatmap-balanced'), datapointsBalanced);
    heatmapBalanced.createHeatmap();
		document.getElementById('heatmap-balanced').classList.add('hidden');

		// Set image colorsamples canvas inital size
		var colorImageWidth = document.getElementById('color-image').getElementsByTagName('img')[0].clientWidth;
		var colorImageHeight = document.getElementById('color-image').getElementsByTagName('img')[0].clientHeight;
		document.getElementById('color-image-samples').width = colorImageWidth;
		document.getElementById('color-image-samples').height = colorImageHeight;

    // Create color samples
    createColorSamples(colorPalette);
    createCanvasPalette(document.getElementById('color-image-samples'), colorPalette.slice(0, 5), colorPositions);
    console.log("Color processed");

		// Color UI
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
