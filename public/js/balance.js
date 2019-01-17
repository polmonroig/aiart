// HEATMAP CLASS
"use strict";

class Heatmap{

  constructor(canvas, datapoints, blur=0.04){
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
    heatCtx.clearRect(0, 0, this.canvas.offsetWidth, this.canvas.offsetHeight) // Start with a clean canvas

    var maxValue = 100;
    var gradientImage = this.gradientImage();
    heatCtx.filter = `blur(${this.blur*this.canvas.offsetWidth}px)`;

    heatCtx.beginPath();
    // Fill Cells
    for (var i = 0; i < this.datapoints.length; i++) {
        var point = this.datapoints[i];

        var gray = (255 * (point[2] / maxValue)) | 0;
        var r = gradientImage[gray * 4 + 0];
        var g = gradientImage[gray * 4 + 1];
        var b = gradientImage[gray * 4 + 2];
        //var a = gradientImage[gray * 4 + 3];

				// Circle draw
				heatCtx.moveTo(point[0]*this.canvas.offsetWidth, point[1]*this.canvas.offsetHeight);
        heatCtx.fillStyle = 'rgba( 0,0,0,' + (gray / 255) + ')';
        heatCtx.ellipse(point[0]*this.canvas.offsetWidth, point[1]*this.canvas.offsetHeight, point[3]*this.canvas.offsetWidth, point[4]*this.canvas.offsetWidth, 0, 0, 2 * Math.PI);

    }

		 heatCtx.fill();

    // Blur Canvas
    //stackBlurCanvasRGBA(this.canvas.id, 0, 0, this.canvas.offsetWidth, this.canvas.offsetHeight, this.blur);

    // Map blurred canvas to heatmap
    this.colorize(heatCtx, heatCtx, 3, this.canvas.offsetWidth, this.canvas.offsetHeight, true);

  }

}

function balanceButton(){
  document.getElementById('heatmap').classList.add('hidden');
  document.getElementById('heatmap-balanced').classList.remove('hidden');

  var message = 'Image balanced! added an element on <b>bottom left</b> of canvas';
  document.getElementsByClassName('message-content-balance')[0].innerHTML = message;
  document.getElementsByClassName('message-content-balance')[0].classList.remove('message-wrong');
  document.getElementsByClassName('message-content-balance')[0].classList.add('message-fixed');
}

function resetBalanceButton(){
  document.getElementById('heatmap').classList.remove('hidden');
  document.getElementById('heatmap-balanced').classList.add('hidden');

  var message = 'Your composition is slightly out of balance, try to add or eliminate an element to compensate properly!';
  document.getElementsByClassName('message-content-balance')[0].innerHTML = message;
  document.getElementsByClassName('message-content-balance')[0].classList.add('message-wrong');
  document.getElementsByClassName('message-content-balance')[0].classList.remove('message-fixed');
}


// BOOTSTRAP ELEMENTS INIT

$(function(){


  // #1. RANGE SLIDER
  if($('.overlay-slider').length){
    $('.overlay-slider').ionRangeSlider({
      type: "single",
      min: 0,
      max: 100,
      from: 15,
      step: 1,
      onStart: function (data) {
          document.getElementById('balance-image').style.opacity = data['from']/100;
      },
      onChange: function (data) {
          document.getElementById('balance-image').style.opacity = data['from']/100;
      },
    });
  }

});
