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
			}else{
				var thisVal = $(this).val();
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
