function parseImg() {
	var canvas = document.getElementById("the_stage");
	var dataURL = canvas.toDataURL('image/jpg');
	$('.btn-parse').attr('disabled', 'disabled');
	$.ajax({
	  type: "POST",
	  url: "/check-image",
	  data:{
		imageBase64: dataURL
	  },
		success: function (response) {

			$('.found-digit > span').text(response.label);
			$('.found-digit-percent > span').text(response.probability);
			$('.btn-parse').attr('disabled', null);
		}
	});

}