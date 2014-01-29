function checkboxChecked(selector) {
    var allVals = [];
    $(selector).each(function() {
        allVals.push($(this).val());
    });
    return allVals;
}

function GridBase(){
	var thisClass = this;
	
	this.seperateElement = function(id,val){
		var tagName = $(id).prop("tagName");
		var name = $(id).attr("name");
		if(tagName !== undefined){
			switch (tagName)
			{
				
				case "SPAN":
				{
					$(id).text(val);
				}
				case "INPUT":
					var type = $(id).prop("type")
					if(type == "text")
						$(id).val(val);
					else if(type == 'checkbox')
						thisClass.checkboxVal(id,val);
				case "SELECT":
				{
					$(id).find('option:selected').removeAttr("selected");
					if($(id).next().hasClass('ui-multiselect')){
						thisClass.multipleVal(id,val);
					}else{
						$(id).val(val);
					}
				}
				default:
				{
					$(id).val(val);
				}
			}
		}
	}
	
	this.seperateView = function(id,val){
		var tagName = $("#ele_"+id).prop("tagName");
		var name = $("#ele_"+id).attr("name");
		var val;
		if(tagName !== undefined){
			if(tagName == "SPAN")				
			{
				$("#textView_"+id).text(value);
			}else if(tagName == "INPUT"){
				var type = $("#ele_"+id).prop("type")
				if(type == "text"){
					$("#textView_"+id).text(val);
				}
				else if(type == 'checkbox'){
					$("#textView_"+id).text('True');
					if(val == 0){
						$("#textView_"+id).text('False');
					}
				}
			}else if(tagName == "SELECT"){
				if($("#ele_"+id).next().hasClass('ui-multiselect')){
					$("#textView_"+id).text(val);
				}else{
					value = $("#ele_"+id).find('option:selected').text();
					$("#textView_"+id).text(value);
				}
			}
		}
	}
	
	this.multipleVal = function(id,val){
		var attrid = $(id).attr("id");
		$.each(val.split(","), function(i,e){
		    $("#"+attrid+" option[value='" + e + "']").prop("selected", true);
		});
	}
	
	this.checkboxVal = function(id,val){
		if(val==0){
			$(id).prop('checked', false);
		}else if(val==1){
			$(id).prop('checked', true);
		}
	}
	
	this.UIHover = function(id){
		$(id).hover(function(){
			$(this).addClass('ui-state-hover');
		}, function(){
			$(this).removeClass('ui-state-hover');
		});
	}
	
	this.oData = function(odata){
		$("[id^='ele_']").each(function(){
			var attrName = $(this).attr("name");
			var thisType = $(this).attr("type");
			
			var thisVal;

			if(thisType == 'checkbox'){
				if($(this).prop('checked')){
					thisVal = 1;
				}else{
					thisVal = 0;
				}
			/*
			}else if(thisType==undefined){
				if($(this).is('select')){
					if($(this).next().hasClass('ui-multiselect')){
						var attrId = $(this).attr("id");
						thisVal = checkboxChecked("input[name='multiselect_"+attrId+"']:checked");
					}else{
						thisVal = $(this).val();
					}
				}else{
					thisVal = $(this).val();
				}
				*/
			}else{
				thisVal = $(this).val();
			}
			
			if(attrName !== undefined){
				var data = {};
				if(thisVal !== null){
					if(typeof thisVal == 'object'){
						data[attrName] = thisClass.objToStr(thisVal);
					}else{
						data[attrName] = thisVal;
					}
				}
			}
			
			$.extend(odata, data);
		})
		
		return odata;
	}
	
	this.objToStr = function(obj){
		var str = '';
		for(var i=0; i<obj.length;i++){
			str += obj[i];
			if(i !== obj.length-1)
				str += ',';
		}
		return str;
	}
	
	this.strToObj = function(str){
		var obj = [];
		obj = str.split(",");
		return obj;
	}
}

function EDITPROFILE(url) {
	var thisClass = this;

	this.getData = function() {
		$.getJSON( url,
			{	class: 'USERLIST',
				'method': 'editData'},
			function(result){
				$.each(result, function(ini,val){
					thisClass.seperateElement($("#edit_"+ini), val);
				});

		});
	}
	
	this.seperateElement = function(id,val){
		var tagName = $(id).prop("tagName");
		var name = $(id).attr("name");
		if(tagName !== undefined){
			switch (tagName)
			{
				case "SPAN":
				{
					$(id).text(val);
				}
				case "INPUT":
					var type = $(id).prop("type")
					if(type == "text")
						$(id).val(val);
					else if(type == 'checkbox')
						thisClass.checkboxVal(id,val);
				case "SELECT":
				{
					$(id).find('option:selected').removeAttr("selected");
					if($(id).next().hasClass('ui-multiselect')){
						thisClass.multipleVal(id,val);
					}else{
						$(id).val(val);
					}
				}
			}
		}
	}
	
	this.hideEditTable = function(){
		$('#edit_profile').modal('hide');
	}
	
	this.oEditData = function(odata){
		$("[id^='edit_']").each(function(){
			var attrName = $(this).attr("name");
			var thisType = $(this).attr("type");
			
			var thisVal;
			if(thisType == 'checkbox'){
				if($(this).prop('checked')){
					thisVal = 1;
				}else{
					thisVal = 0;
				}
			}else{
				
				thisVal = $(this).val();
			}
			
			if(attrName !== undefined){
				var data = {};
				if(thisVal !== null){
					if(typeof thisVal == 'object'){
						data[attrName] = thisClass.objToStr(thisVal);
					}else{
						data[attrName] = thisVal;
					}
				}
			}
			
			$.extend(odata, data);
		});
	}
	
	this.save = function(){
		var odata;

		odata = {'class' :  'USERLIST', 'method' : "save" };
		thisClass.oEditData(odata);

		$.post(url,odata,
			function(result){
				thisClass.hideEditTable();
			});
	}
	
	this.selectEditSalutation = function(){
		var html ='';
		$.ajax({
			url: url,
			type: 'GET',
			data: { class: 'USERLIST',
					method: 'getSalutation'
			},
			success: function(res){
				$.each(res, function(ini ,val){
						html += "<option value='"+val.id+"'>"+val.selectionname+"</option>";
				});
				$("#edit_salutation").append(html);
			}	
		});
	}
	
    this.initValidateForm = function(){
		  $("#edit_profile_form").validate({              
		    rules: {
		      	firstname:{
		      		required: true,
		      	},
	          	password : {
					minlength : 6,
	            },
	            re_password : {
	                minlength : 5,
	                equalTo : "#edit_password"
	            },
		      	firstname:{
		      		required: true,
		      	},
		      	dob :{
	            	required: true,
	            },
                  mobilephone:{
			      	required: false,
			      	number: true,
			      	rangelength: [4, 20]
			      },
			      homephone:{
			      	required: false,
			      	number: true,
			      	rangelength: [4, 20]
			      },
			      officephone:{
			      	required: false,
			      	number: true,
			      	rangelength: [4, 20]
			      },
		    },
			 invalidHandler: function(event, validator) {
			// 'this' refers to the form
				thisClass.submitForm = false;
			}
		  });
    }

	this.initValidateFormEvent = function(){
		thisClass.submitForm = true;
	  	$("#edit_profile_form").validate().form();
	}
	
	this.iniControl = function(){
		$("#edit-profile-submit").click(function(){
        	thisClass.initValidateFormEvent();
            if(thisClass.submitForm){
				thisClass.save();
			}
		});
		
		$( "#edit_dob").datepicker({ dateFormat: 'dd-mm-yy' });
		
	  	$('.modal .form-control, .modal input[type="checkbox"]').attr('disabled', 'disabled');
		$("#edit-profile-submit").attr('disabled', 'disabled');
		
	  	$('#editProfileBtn').click(function(){
		  	$('.modal .form-control, .modal input[type="checkbox"]').removeAttr('disabled', 'disabled');
		  	$('#edit-profile-submit').removeAttr('disabled', 'disabled');
		  	$('#edit_user').attr('disabled', 'disabled');
  	  	});
  	  	
  	  	$(".btnEditProfile").click(function(){
  	  		$('.modal .form-control, .modal input[type="checkbox"]').attr('disabled', 'disabled');
  	  		$("#edit-profile-submit").attr('disabled', 'disabled');
  	  	});
		
		thisClass.getData();
		thisClass.selectEditSalutation(); 
		thisClass.initValidateForm();
	}
	
}


var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


