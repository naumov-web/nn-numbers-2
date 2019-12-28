function parseImg() {
	var canvas = document.getElementById("the_stage");
	var dataURL = canvas.toDataURL('image/jpg');
	$.ajax({
	  type: "POST",
	  url: "/check-image",
	  data:{
		imageBase64: dataURL
	  }
	}).done(function(response) {
	    console.log(response);
	});

}