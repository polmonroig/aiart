"use strict";

var colorPalette = [];
var colorPositions = [];
var datapoints = [];
var datapointsBalanced = [];

// Main function called by response text
function processImage(responseText){

  // Reset visibility of wrappers for initial animation
	document.getElementsByClassName('overview-index')[0].classList.remove('overview-main-anim');
	document.getElementsByClassName('overview-index')[0].classList.add('overview-main-anim-hide');
	document.getElementsByClassName('balance-index')[0].classList.remove('balance-main-anim');
	document.getElementsByClassName('balance-index')[0].classList.add('balance-main-anim-hide');
  document.getElementsByClassName('color-index')[0].classList.remove('color-main-anim');
	document.getElementsByClassName('color-index')[0].classList.add('color-main-anim-hide');

  document.getElementById('upload-wrapper').classList.add('upload-main-anim-hide');

	// Delay functions to allow animation to complete
  var delayInMilliseconds = 500;
  setTimeout(function() {

		document.getElementById('overview-wrapper').classList.add('hidden');
		document.getElementById('balance-wrapper').classList.add('hidden');
		document.getElementById('color-wrapper').classList.add('hidden');
    document.getElementsByClassName('overview-index')[0].classList.remove('overview-main-anim-hide');
    document.getElementsByClassName('balance-index')[0].classList.remove('balance-main-anim-hide');
    document.getElementsByClassName('color-index')[0].classList.remove('color-main-anim-hide');

    if(!document.getElementById('upload-wrapper').classList.contains("hidden")){
      document.getElementsByClassName('dropzone-menu')[0].classList.remove('hidden');
      document.getElementsByClassName('dropzone-menu')[1].classList.remove('hidden');
      document.getElementById('upload-wrapper').classList.add('hidden');
			document.getElementById('overview-wrapper').classList.remove('hidden');
			document.getElementById('balance-wrapper').classList.remove('hidden');
      document.getElementById('color-wrapper').classList.remove('hidden');
      document.getElementsByClassName('overview-index')[0].classList.add('overview-main-anim');
      document.getElementsByClassName('balance-index')[0].classList.add('balance-main-anim');
      document.getElementsByClassName('color-index')[0].classList.add('color-main-anim');
    }else{
      document.getElementById('overview-wrapper').classList.remove('hidden');
			document.getElementById('balance-wrapper').classList.remove('hidden');
			document.getElementById('color-wrapper').classList.remove('hidden');
      document.getElementById('balance-wrapper').classList.remove('hidden');
      document.getElementsByClassName('overview-index')[0].classList.add('overview-main-anim');
      document.getElementsByClassName('balance-index')[0].classList.add('balance-main-anim');
      document.getElementsByClassName('color-index')[0].classList.add('color-main-anim');
    }


    // Handle response text
    colorPalette = responseText["color_palette"];
    colorPositions = responseText["color_positions"];
		datapoints = responseText["datapoints"];
		datapointsBalanced = responseText["datapoints_balanced"];

    // Heatmap UI
		document.getElementsByClassName('balance-btn')[0].disabled = false;
		document.getElementsByClassName('balance-reset-btn')[0].disabled = true;
		var message = 'Your composition is slightly out of balance, try to add or eliminate an element to compensate properly!';
		setMessage('balance', 'wrong', message);

    document.getElementById('heatmap').classList.remove('hidden');

		// Set heatmap canvas inital size
		var imageWidth = document.getElementById('balance-image').getElementsByTagName('img')[0].clientWidth;
		var imageHeight = document.getElementById('balance-image').getElementsByTagName('img')[0].clientHeight;
    document.getElementById('heatmap').width = imageWidth;
    document.getElementById('heatmap').height = imageHeight;

		// Debugging log
		console.log(datapoints);
		console.log(datapointsBalanced);
		console.log(colorPalette);
		console.log(colorPositions);
		console.log(responseText["image_data_messages"]);

		// Create heapmap
    const heatmap = new Heatmap(document.getElementById('heatmap'), datapoints);
    heatmap.createHeatmap();

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
		document.getElementsByClassName('harmonize-btn')[0].disabled = false;
		document.getElementsByClassName('harmonize-reset-btn')[0].disabled = true;
		var message = 'The color palette of the image is not ideal! check the harmonized verison to improve it';
		setMessage('color', 'wrong', message);


  }, delayInMilliseconds);
}

//Load image from user
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

// Sets the first found class element to the desired message
function setMessage(section, type, message){

	document.getElementsByClassName('message-content-' + section)[0].innerHTML = message;
	document.getElementsByClassName('message-content-' + section)[0].classList.add('message-'+ type == 'message-wrong' ? 'message-wrong' : 'message-success');
	document.getElementsByClassName('message-content-' + section)[0].classList.remove('message-' + type == 'message-wrong' ? 'message-success' : 'message-wrong');
}
