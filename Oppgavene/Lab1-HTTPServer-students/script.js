/*
 * Simple JavaScript Canvas raycaster (untextured).
 *
 * By Guido Krömer <mail@cacodaemon.de>
 *
 */
function Vector2() {
	this.x;
	this.y;
};

var TILE = 48;

function Player(x, y, raycaster) {
	this.x = x;
	this.y = y;
	this.angle = 0;
	this.moveableForward = true;
	this.moveableBackward = true;
	this.raycaster = raycaster;

	this.update = function(delta) {
		if (Key.isDown(Key.UP) && this.moveableForward) {
			this.x += Math.cos(this.angle) * (TILE / 3) * delta;
			this.y += Math.sin(this.angle) * (TILE / 3) * delta;
		}
		if (Key.isDown(Key.DOWN) && this.moveableBackward) {
			this.x -= Math.cos(this.angle) * (TILE / 3) * delta;
			this.y -= Math.sin(this.angle) * (TILE / 3) * delta;
		}
		if (Key.isDown(Key.LEFT)) {
			this.angle -= 0.05;
		}
		if (Key.isDown(Key.RIGHT)) {
			this.angle += 0.05;
		}

		if (this.angle < 0) {
			this.angle += Math.PI * 2;
		}

		if (Key.isDown(113)) {
			Key.reset(113);
			this.raycaster.preciseDistance = !this.raycaster.preciseDistance;
		}
		if (Key.isDown(115)) {
			Key.reset(115);
			this.raycaster.depthShading = !this.raycaster.depthShading;
		}

		this.angle %= Math.PI * 2;
	}
};
Player.prototype = new Vector2();

function Raycaster() {
	this.map = null;
	var COLORS = ['', 'rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)', 'rgb(255, 255, 0)', 'rgb(0, 255, 255)', 'rgb(255, 0, 255)', 'rgb(255, 255, 255)'];
	var INFINITY = 1 / 0;
	var SCR_W = 0;
	var SCR_H = 0;
	var SCR_W_HALF = 0;
	var SCR_H_HALF = 0;
	var WALL_H_FACTOR = 30;
	var WALL_H = 0;
	var RAY_ANGLE = 0;
	var PI_TWO = Math.PI * 2;
	var PI_HALF = Math.PI / 2;
	var VOF = 60 * (Math.PI / 180);
	var VOF_HALF = VOF / 2;
	var TILE_QUATER = TILE / 2;
	this.preciseDistance = true
	this.depthShading = true
	this.player = new Player(TILE * 3, TILE * 3, this);

	this.getColor = function(lineElement) {
		if (!this.depthShading) {
			return COLORS[lineElement.color];
		}

		var dist = lineElement.dist / (TILE_QUATER / 16);
		var factor = Math.ceil(lineElement.north ? 255 - dist * 1.3 : 255 - dist * 1.5);
		return COLORS[lineElement.color].replace('255', factor).replace('255', factor)
	}

	this.init = function (gameManager) {
		this.gameManager = gameManager;
		SCR_W_HALF = (SCR_W = this.gameManager.width) / 2;
		SCR_H_HALF = (SCR_H = this.gameManager.height) / 2;
		RAY_ANGLE = VOF / SCR_W;
		WALL_H = SCR_H * WALL_H_FACTOR;
		this.loadMap();
	}

	this.draw = function(ctx) {
		ctx.fillStyle = "black";
		ctx.fillRect(0, 0, this.gameManager.width, this.gameManager.height);

		var lineElement = {
			y: 0,
			x: 0,
			color: 0,
			north: false,
			dist: 0
		};

		var i = 0;
		for (var rayAngle = -VOF_HALF; rayAngle < VOF_HALF; rayAngle += RAY_ANGLE) {
			var dx = this.player.x + Math.cos(this.player.angle + rayAngle) * 100;
			var dy = this.player.y + Math.sin(this.player.angle + rayAngle) * 100;

			this.getLine(this.player.x, this.player.y, dx, dy, lineElement);
			this.getLine(this.player.x, this.player.y, dx, dy, lineElement);

			if (this.preciseDistance) {
				var vX = this.player.x - lineElement.x;
				var vY = this.player.y - lineElement.y;
				lineElement.dist = Math.sqrt(vX * vX + vY * vY) * Math.cos(rayAngle);
			}

			var wallFactor = SCR_H_HALF / lineElement.dist * TILE_QUATER
            ctx.strokeStyle = this.getColor(lineElement);

            ctx.beginPath();
            ctx.moveTo(i, SCR_H_HALF - wallFactor);
            ctx.lineTo(i, SCR_H_HALF + wallFactor);
            ctx.closePath();
            ctx.stroke();

			if (i == SCR_W_HALF) {
				this.player.moveableForward = lineElement.dist > 10;
			}

			i++;
		}

		this.drawMap(ctx);
	}

	this.getLine = function(x1, y1, x2, y2, lineElement) {
		var dx = Math.abs(x2 - x1);
		var dy = Math.abs(y2 - y1);
		var sx = (x1 < x2) ? 1 : -1;
		var sy = (y1 < y2) ? 1 : -1;
		var err = dx - dy;
		var e2;
		var perviousTileX = 0;
		var perviousTileY = 0;
		var distance = 0;

		while (!((x1 == x2) && (y1 == y2))) {
			e2 = err << 1;
			if (e2 > -dy) {
				err -= dy;
				x1 += sx;
				distance++;
			}
			else if (e2 < dx) {
				err += dx;
				y1 += sy;
				distance++;
			}

			var mapX = Math.floor(x1 / TILE);
			var mapY = Math.floor(y1 / TILE);

			if (this.map[mapY][mapX]) {
				lineElement.y = y1;
				lineElement.x = x1;
				lineElement.color = this.map[mapY][mapX];
				lineElement.north = perviousTileX == mapX;
				lineElement.dist = distance;
				return;
			}
			perviousTileX = mapX;
			perviousTileY = mapY;
		}
	}

	this.update = function(delta) {
		this.player.update(delta);
	}

	this.loadMap = function() {
		this.map = [
			[5, 5, 5, 5, 5, 5, 5, 4, 0, 0, 0, 4, 5, 5, 5, 5, 5, 5, 5, 5],
			[2, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 4],
			[2, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4],
			[2, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 1, 1, 0, 4],
			[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 4],
			[2, 0, 0, 1, 0, 1, 0, 0, 0, 2, 1, 2, 0, 0, 0, 0, 1, 1, 0, 4],
			[2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 4],
			[2, 0, 0, 2, 0, 2, 0, 0, 0, 2, 1, 2, 0, 0, 0, 0, 1, 1, 0, 4],
			[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
			[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
			[2, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
			[2, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
			[2, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 2, 3, 4, 5, 6, 0, 4],
			[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
			[2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 2, 3, 4, 5, 6, 3, 3]
		];
	}

	this.drawMap = function (ctx) {
        ctx.fillStyle = 'BLACK'
       	ctx.fillRect(0, 0, this.map[0].length * 2, this.map.length * 2);

        for (var y = 0; y < this.map.length; y++) {
            for (var x = 0; x < this.map[y].length; x++) {
                if (!this.map[y][x]) {
                    continue;
                }

                ctx.fillStyle = COLORS[this.map[y][x]];
                ctx.fillRect(x*2, y*2, 2, 2);
            }
        }

        ctx.fillStyle = 'WHITE'
        ctx.fillRect((this.player.x / TILE) * 2, (this.player.y / TILE) * 2, 4 ,4)
    }
};
Raycaster.prototype = new GameObject();
