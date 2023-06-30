/*
Program: External JS Demo
Date: 9th Dec, 2022
Author: Preston Sodipo
*/


function sales(gender){
	
	var message = "";
	if(gender.toLowerCase().trim() == 'female'){
		message = "Shoes and bags are available for sale"
		
	}else if(gender.toLowerCase().trim() == 'male'){
	message = "Phones are available for sale"

	}else{
		message = "No Product!"
	}
	
	return message;
	
}