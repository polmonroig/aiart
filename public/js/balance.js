// HEATMAP CLASS
"use strict";

class Heatmap{

  constructor(canvas, datapoints, blur=0.12){
    this.canvas = canvas;
		this.blur = blur;

		// datapoints array oder: [0] = x   [1] = y   [2] = w   [3] = sx   [4] = sy
		this.datapoints = datapoints;

    this.gradient = {
        0.0: "rgba(50,50,160,1)",
        0.2: "rgba(50,50,200,1)",
        0.4: "rgba(000,255,255,1)",
        0.6: "rgba(000,255,000,1)",
        0.8: "rgba(255,255,000,1)",
        1.0: "rgba(255,000,000,1)"
    };

  }

  gradientImage(){
    var canvas = document.createElement("canvas");
    canvas.width = 1;
    canvas.height = 256;
    var ctx = canvas.getContext("2d");
    var grad = ctx.createLinearGradient(0, 0, 1, 256);

    for (var x in this.gradient) {
        grad.addColorStop(x, this.gradient[x]);
    }

    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 1, 256);

    return ctx.getImageData(0, 0, 1, 256).data;
  }

  colorize(sourceCtx, destCtx, channel, width, height, alpha){
    var blurImageData = sourceCtx.getImageData(0, 0, width, height);
    var blurImageDataPlain = blurImageData.data;
    var gradientImage = this.gradientImage();

    for (var i = 0; i < blurImageDataPlain.length; i += 4) {

				var gray = blurImageDataPlain[i + channel];
        var r = gradientImage[gray * 4 + 0];
        var g = gradientImage[gray * 4 + 1];
        var b = gradientImage[gray * 4 + 2];
        var a = gradientImage[gray * 4 + 3];

        blurImageDataPlain[i] = r;
        blurImageDataPlain[i + 1] = g;
        blurImageDataPlain[i + 2] = b;
        blurImageDataPlain[i + 3] = alpha ? a : 255;
    }
    destCtx.putImageData(blurImageData, 0, 0);
  }

  createHeatmap(){

    var heatCtx = this.canvas.getContext('2d');
    heatCtx.clearRect(0, 0, this.canvas.width, this.canvas.height) // Start with a clean canvas

    var gradientImage = this.gradientImage();
    //heatCtx.filter = `blur(${this.blur*this.canvas.offsetWidth}px)`; This blur is NOT compatible with retina display devices
		var maxValue = 1.5;

		// Prefill canvas with black
		heatCtx.fillStyle = "rgba(0,0,0,1)";
		heatCtx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Fill Cells
    for (var i = 0; i < this.datapoints.length; i++) {
        var point = this.datapoints[i];
				// Circle draw
				heatCtx.fillStyle = 'rgba(' + Math.floor((point[2])*255) + ',0,0,1)';
				heatCtx.beginPath();
				//heatCtx.moveTo(point[0]*this.canvas.width, point[1]*this.canvas.height);
        heatCtx.ellipse(point[0]*this.canvas.width, point[1]*this.canvas.height, point[3]*this.canvas.width, point[4]*this.canvas.width, 0, 0, 2 * Math.PI);
				heatCtx.fill();
    }
    // Blur Canvas
    stackBlurCanvasRGBA(this.canvas.id, 0, 0, this.canvas.width, this.canvas.height, this.blur*this.canvas.width); // This blur is compatible with retina display devices

    // Map blurred canvas to heatmap
    this.colorize(heatCtx, heatCtx, 0, this.canvas.width, this.canvas.height, true);

  }

}

function balanceButton(){
	const heatmapBalanced = new Heatmap(document.getElementById('heatmap'), datapointsBalanced);
	heatmapBalanced.createHeatmap();

  setMessage('balance', 'success', messageList[7]);

	document.getElementsByClassName('balance-btn')[0].disabled = true;
	document.getElementsByClassName('balance-reset-btn')[0].disabled = false;

	setScore('balance', score[0], 100);
}

function resetBalanceButton(){
	const heatmap = new Heatmap(document.getElementById('heatmap'), datapoints);
	heatmap.createHeatmap();

  setMessage('balance',messages['composition']['type'], messageList[messages['composition']['message']]);

	document.getElementsByClassName('balance-btn')[0].disabled = false;
	document.getElementsByClassName('balance-reset-btn')[0].disabled = true;

	setScore('balance', 100, score[0]);
}


// BOOTSTRAP ELEMENTS INIT

$(function(){


  // #1. RANGE SLIDER
  if($('.overlay-slider').length){
    $('.overlay-slider').ionRangeSlider({
      type: "single",
      min: 0,
      max: 100,
      from: 85,
      step: 1,
      onStart: function (data) {
          document.getElementById('heatmap').style.opacity = data['from']/100;
      },
      onChange: function (data) {
          document.getElementById('heatmap').style.opacity = data['from']/100;
      },
    });
  }

});
