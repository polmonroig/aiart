//Process image
function processImage(responseText){

  var delayInMilliseconds = 1500; //1 second

  setTimeout(function() {

    // Display and hide elements
    if(!document.getElementById('upload-wrapper').classList.contains("hidden")){
      document.getElementsByClassName('dropzone-menu')[0].classList.remove('hidden');
      document.getElementsByClassName('dropzone-menu')[1].classList.remove('hidden');
      document.getElementById('upload-wrapper').classList.add('hidden');
      document.getElementById('color-wrapper').classList.remove('hidden');
      document.getElementById('balance-wrapper').classList.remove('hidden');
    }

    //Handle response text
    var colorPalette = responseText["color_palette"];

    // HEATMAP PROCESS

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
          v: responseText["datapoints"][i][2],
          r: responseText["datapoints"][i][3]
        }
      datapoints.push(point);
    }

    for(var i = 0; i < responseText["datapoints_balanced"].length; ++i){
      var point = {
          x: responseText["datapoints_balanced"][i][0],
          y: responseText["datapoints_balanced"][i][1],
          v: responseText["datapoints_balanced"][i][2],
          r: responseText["datapoints_balanced"][i][3]
        }
      datapoints_balanced.push(point);
    }

    const heatmap = new Heatmap(document.getElementById('heatmap'), datapoints, 0.08);
    heatmap.createHeatmap();

    const heatmapBalanced = new Heatmap(document.getElementById('heatmap-balanced'), datapoints_balanced, 0.08);
    heatmapBalanced.createHeatmap();
    document.getElementById('heatmap-balanced').classList.add('hidden');


    //COLOR PROCESS

    var message = 'The color palette of the image is not ideal! check the harmnized verison to improve it';
    document.getElementsByClassName('message-content-color')[0].innerHTML = message;

    createColorSamples(colorPalette[0], colorPalette[1], colorPalette[2], colorPalette[3], colorPalette[4], colorPalette[5], colorPalette[6], colorPalette[7]);
    createColorPalette(colorPalette[0], colorPalette[1], colorPalette[2], colorPalette[3], colorPalette[4], colorPalette[5], colorPalette[6], colorPalette[7]);
    console.log("Color processed");

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
