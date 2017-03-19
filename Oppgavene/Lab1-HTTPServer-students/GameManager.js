/*
 * Simple JavaScript game manager.
 *
 * By Guido Krömer <mail@cacodaemon.de>
 *
 */
function GameManager () {
	var canvas = null;
	var ctx = null;
	var delta = 0;
	var lastTimeStamp = null;
	var freePos = -1;
	var gameObjects = new Array();
	this.width = 0;
	this.height = 0;

	this.init = function (canvas) {
		lastTimeStamp = new Date().getTime();
		canvas = canvas;
		ctx = canvas.getContext('2d');
		this.width = canvas.width;
		this.height = canvas.height;

		window.requestAnimFrame = (function(){
		  return  window.requestAnimationFrame       ||
				  window.webkitRequestAnimationFrame ||
				  window.mozRequestAnimationFrame    ||
				  window.oRequestAnimationFrame      ||
				  window.msRequestAnimationFrame     ||
				  function (callback) {
					window.setTimeout(callback, 1000 / 120);
				  };
		})();

		(function animloop(){
		  requestAnimFrame(animloop);
		  timerStart();
			update();
			draw();
			timerEnd();
		})();
	}

	this.addGameObject = function(gameObject) {
		gameObject.init(this);
		if (freePos != -1) {
			gameObjects[this.freePos] = gameObject;
			freePos = -1;
		}
		else {
			gameObjects.push(gameObject);
		}
	};

	this.addGameObjects = function(gameObjects) {
		for (var i = gameObjects.length - 1; i >= 0; i--) {
			this.addGameObject(gameObjects[i]);
		}
	};

	this.removeGameObject = function(gameObject) {
		for (var i = gameObjects.length - 1; i >= 0; i--) {
			if (gameObjects[i] == gameObject) {
				gameObjects.splice(i, 1);
				freePos = i;
				return;
			}
		}
	};

	this.forEachGameObject = function(callBack) {
		for (var i = gameObjects.length - 1; i >= 0; i--) {
			callBack(gameObject[i]);
		}
	};

	var update = function() {
		for (var i = gameObjects.length - 1; i >= 0; i--) {
			gameObjects[i].update(delta);
		}
	};

	var draw = function() {
		for (var i = gameObjects.length - 1; i >= 0; i--) {
			gameObjects[i].draw(ctx);
		}
	};

	var timerStart = function() {
		var date = new Date();
		delta = date.getTime() - this.lastTimeStamp;
		delta *= 0.01;
	};

	var timerEnd = function() {
		this.lastTimeStamp = new Date().getTime();
	};
}
