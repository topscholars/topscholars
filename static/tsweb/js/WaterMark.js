function Watermark(id, text, css)
{
	//init, set watermark text and class
	if ($('#' + id).val().length == 0){
		$('#' + id).addClass(css);
		$('#' + id).val(text);
	}
 
	//if blur and no value inside, set watermark text and class again.
 	$('#' + id).blur(function(){
  		if ($(this).val().length == 0){
    		$(this).addClass(css);
    		$(this).val(text);
		}
 	});
 
	//if focus and text is watermrk, set it to empty and remove the watermark class
	$('#' + id).focus(function(){
		if($(this).val() == text)
			$(this).val('');
    	$(this).removeClass(css);
 	});
 }
