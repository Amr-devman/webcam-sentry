function toggle_visibility(){
	if ($("#my_camera").is(":visible")){
		document.getElementById('toggle_button').value = "Show webcam" 
	}
	else if($("#my_camera").is(":hidden")){
		document.getElementById('toggle_button').value = "Hide webcam" 
	}	
	$("#my_camera").toggle()
}