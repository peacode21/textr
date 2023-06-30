/*
Program: Week 4 Mini Project
Date: 10th Dec, 2022
Author: Preston Sodipo
*/


function grade(scores){
	var message = "";
	document.getElementById('english').style.border ='1px solid grey';
	document.getElementById('egrade').style.border ='1px solid grey';
	document.getElementById('maths').style.border ='1px solid grey';
	document.getElementById('mgrade').style.border ='1px solid grey';
	document.getElementById('chemistry').style.border ='1px solid grey';
	document.getElementById('cgrade').style.border ='1px solid grey';
	document.getElementById('biology').style.border ='1px solid grey';
	document.getElementById('bgrade').style.border ='1px solid grey';
	document.getElementById('french').style.border ='1px solid grey';
	document.getElementById('fgrade').style.border ='1px solid grey';
	if(scores.trim() < 40){
		message = "F";
		
	}else if(scores.trim() >= 40 && scores.trim() < 45){
	message = "E";

	}else if(scores.trim() >= 45 && scores.trim() < 50){
	message = "D";

	}else if(scores.trim() >= 50 && scores.trim() < 60){
	message = "C";

	}else if(scores.trim() >= 60 && scores.trim() < 69){
	message = "B";

	}else if(scores.trim() >= 70 && scores.trim() <= 100){
	message = "A";

	}else{
		message = "Input a valid number";
	
	}
	var grade = "";
	return message;
	
}