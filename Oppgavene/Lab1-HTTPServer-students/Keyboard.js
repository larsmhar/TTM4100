/*
 * Simple JavaScipt keyboard helper.
 * Based upon http://nokarma.org/2011/02/27/javascript-game-development-keyboard-input/index.html
 *
 */
var Key = {
	pressed: [],

	LEFT: 37,
	UP: 38,
	RIGHT: 39,
	DOWN: 40,
	ENTER: 13,
	SPACE: 32,
	PAGE_UP: 33,
	PAGE_DOWN: 34,
	W: 87,
	A: 65,
	S: 83,
	D: 68,

	isDown: function(keyCode) {
		return this.pressed[keyCode];
	},
	reset: function(keyCode) {
		this.pressed[keyCode] = false;
	},
	onKeydown: function(event) {
		this.pressed[event.keyCode] = true;
	},
	onKeyup: function(event) {
		delete this.pressed[event.keyCode];
	}
};

window.addEventListener('keyup', function(event) {
	Key.onKeyup(event);
}, false);

window.addEventListener('keydown', function(event) {
	Key.onKeydown(event);
}, false);
