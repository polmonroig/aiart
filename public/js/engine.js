"use strict";

var colorPalette = [];
var colorPositions = [];
var datapoints = [];
var datapointsBalanced = [];
var messages = [];
var score = [];

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
		messages = responseText["image_data_messages"];
		score = [70, 56];

		setScore('balance', score[0]);
		setScore('color', score[1]);

    // Heatmap UI
		document.getElementsByClassName('balance-btn')[0].disabled = false;
		document.getElementsByClassName('balance-reset-btn')[0].disabled = true;
		var message = 'Your composition is slightly out of balance, try to add or eliminate an element to compensate properly!';
		setMessage('balance', 'warning', message);

    document.getElementById('heatmap').classList.remove('hidden');

		// Set heatmap canvas inital size
    document.getElementById('heatmap').width = document.getElementById('balance-image').getElementsByTagName('img')[0].clientWidth;
    document.getElementById('heatmap').height = document.getElementById('balance-image').getElementsByTagName('img')[0].clientHeight;

		// Debugging log
		console.log(datapoints);
		console.log(datapointsBalanced);
		console.log(colorPalette);
		console.log(colorPositions);
		console.log(messages);
		console.log(score);

		// Create heapmap
    const heatmap = new Heatmap(document.getElementById('heatmap'), datapoints);
    heatmap.createHeatmap();

		// Set image colorsamples canvas inital size
		document.getElementById('color-image-samples').width = document.getElementById('color-image').getElementsByTagName('img')[0].clientWidth;
		document.getElementById('color-image-samples').height = document.getElementById('color-image').getElementsByTagName('img')[0].clientHeight;

    // Create color samples
    createColorSamples(colorPalette);
    createCanvasPalette(document.getElementById('color-image-samples'), colorPalette.slice(0, 5), colorPositions);

		// Color UI
		document.getElementsByClassName('harmonize-btn')[0].disabled = false;
		document.getElementsByClassName('harmonize-reset-btn')[0].disabled = true;
		var message = 'The color palette of the image is not ideal! check the harmonized verison to improve it';
		setMessage('color', 'warning', message);


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
	document.getElementsByClassName('message-content-' + section)[0].classList.add('message-'+ type == 'message-warning' ? 'message-warning' : 'message-success');
	document.getElementsByClassName('message-content-' + section)[0].classList.remove('message-' + type == 'message-warning' ? 'message-success' : 'message-warning');
}

function setScore(section, localScore, newScore=-1){

	var documentOverviewScore = document.getElementsByClassName(section+'-overview-score')[0];
	var documentScore = document.getElementsByClassName(section+'-score')[0];
	var progress = document.getElementsByClassName(section+'-progress')[0];
	var increment = progress.getElementsByClassName('increment')[0];
	var info = progress.getElementsByClassName('info')[0];
	var barLevel2 = progress.getElementsByClassName('bar-level-2')[0];
	var barLevel3 = progress.getElementsByClassName('bar-level-3')[0];

	var originalScore = section == 'balance' ? score[0] : score[1];
	var initialScore = localScore;

	// Check if function is called to change value or just to set initially
	if(newScore != -1){

		var counter=setInterval(timer, 20);
		function timer(){
			localScore = initialScore < newScore ? localScore+=1 : localScore-=1;
			documentOverviewScore.innerHTML = localScore+'%';

			documentScore.innerHTML = localScore+'%';
			documentOverviewScore.innerHTML = localScore+'%';
			documentScore.innerHTML = localScore+'%';
			increment.innerHTML = initialScore < newScore ? '+'+(localScore-initialScore) : '-'+(initialScore-localScore);
			info.innerHTML = localScore+'/100';
			barLevel2.style.width = localScore+'%';
			barLevel3.style.width = (100/localScore)*originalScore+'%';
			if(localScore == newScore){
				clearInterval(counter);
				return;
			}
		}

		if(initialScore <= newScore){
			increment.classList.remove('negative');
			increment.classList.add('positive');
		}else{
			increment.classList.remove('positive');
			increment.classList.add('negative');
		}
	}else{
		documentOverviewScore.innerHTML = localScore+'%';
		documentScore.innerHTML = localScore+'%';
		increment.innerHTML = '+0';
		info.innerHTML = localScore+'/100';
		barLevel2.style.width = localScore+'%';
		barLevel3.style.width = '100%';

		increment.classList.remove('negative');
		increment.classList.add('positive');
	}

}
