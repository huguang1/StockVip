function right_criclefn(num) {
	var degree = num * 3.6;
	if(degree > 360) degree = 360;
	if(degree < 0) degree = 0;

	$({
		property: 0
	}).animate({
		property: 100
	}, {
		duration: 600,
		step: function() {
			var deg = this.property / 100 * degree;
			var percent = parseInt(this.property / 100 * num) + 1;
			if(deg <= 180) {
				$(".right_circle_content .right").css("-webkit-transform", "rotate(" + deg + "deg)");
				$(".right_circle_content .mask span").text(percent);
			} else {
				$(".right_circle_content .cricle").css("background-color", "#ffae00");
				$(".right_circle_content .mask").css("color", "#ffae00");
				deg = deg - 180;
				$(".right_circle_content .right").css("-webkit-transform", "rotate(" + 180 + "deg)");
				$(".right_circle_content .left").css("-webkit-transform", "rotate(" + deg + "deg)");
				$(".right_circle_content .mask span").text(percent);
			}
		}
	});

}


function left_criclefn(num) {
	var degree = num * 3.6;
	if(degree > 360) degree = 360;
	if(degree < 0) degree = 0;

	$({
		property: 0
	}).animate({
		property: 100
	}, {
		duration: 600,
		step: function() {
			var deg = this.property / 100 * degree;
			var percent = parseInt(this.property / 100 * num) + 1;
			if(deg <= 180) {
				$(".left_circle_content .right").css("-webkit-transform", "rotate(" + deg + "deg)");
				$(".left_circle_content .mask span").text(percent);
			} else {
				$(".left_circle_content .cricle").css("background-color", "#00ffff");
				$(".left_circle_content .mask").css("color", "#00ffff");
				deg = deg - 180;
				$(".left_circle_content .right").css("-webkit-transform", "rotate(" + 180 + "deg)");
				$(".left_circle_content .left").css("-webkit-transform", "rotate(" + deg + "deg)");
				$(".left_circle_content .mask span").text(percent);
			}
		}
	});

}