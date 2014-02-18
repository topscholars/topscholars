(function($) {
	
	$.fn.hashtags = function(options) {
		/**
		* Merge Options with defaults
		*/

		options = $.extend(true, {
			// default options here
			autocompleteURL: null,
			minLength: 2,
            refresh: false
		}, options || {});
			
		if (options.refresh) {
		    doTag($(this));
		}
		else {
		    wrapControl($(this));
		    doTag($(this));
		    textareaKeyDown($(this));
		    textareaKeyUp($(this));

		    bindAutocomplete($(this));
		}
							
		function wrapControl(element){
			//add hash
			element.wrap('<div class="jqueryHashtags"><div class="highlighter"></div></div>').unwrap().before('<div class="highlighter"></div>').wrap('<div class="typehead"></div></div>');
			element.addClass("theSelector");
			element.autosize({append: "\n"});
			
			element.parent().prev().on('click', function() {
				element.parent().find(".theSelector").focus();
			});
		}
		
		function doTag(element){
			var str = element.val();
			element.parent().parent().find(".highlighter").css("width", element.css("width"));

			var currentcarret = element.prop("selectionStart");
			if (currentcarret != 0) {
			    var result = /\S+$/.exec(element.val().slice(0, currentcarret));
			    if ((result != null) && (result[0] != null) && (result[0].indexOf('#') == 0)) {
			        str = [str.slice(0, result.index), '<span class="hashtagPosition"></span>', str.slice(result.index)].join('');
			    }
			}
			
			str = str.replace(/\n/g, '<br>');
			if(!str.match(/(http|ftp|https):\/\/[\w-]+(\.[\w-]+)+([\w.,@?^=%&amp;:\/~+#-]*[\w@?^=%&amp;\/~+#-])?#([a-zA-Z0-9]+)/g)) {
				if(!str.match(/#([a-zA-Z0-9]+)#/g)) {
					str = str.replace(/#([a-zA-Z0-9\.]+)/g,'<span class="hashtag">#$1</span>');
				}else{
					str = str.replace(/#([a-zA-Z0-9\.]+)#([a-zA-Z0-9]+)/g,'<span class="hashtag">#$1</span>');
				}
			}
	
			element.parent().parent().find(".highlighter").html(str);
			element.parent().parent().find(".highlighter").find("span").each(function(){
			    var value = $(this).html();
			    var match = false;
				for (key in options.autocompleteURL) {
			        if(value == options.autocompleteURL[key].value) {
			        	match = true;
			        	break;
			        }
			    }
			    
			    if(!match) {
			    	str = str.replace('<span class="hashtag">' + value + '</span>',value);
			    }
			});

			element.parent().parent().find(".highlighter").html(str);
			////add space condition
			//for (key in options.autocompleteURL) {
			//	if(options.autocompleteURL[key].value.search(" ") >-1){
	    	//		findAndReplace(options.autocompleteURL[key].value, function(text){
			//			return '<span class="hashtag">' + text + '</span>';
			//		});
			//	}
		    //}
		    
		}

		function findAndReplace(searchText, replacement, searchNode) {
		    if (!searchText || typeof replacement === 'undefined') {
		        // Throw error here if you want...
		        return;
		    }
		    var regex = typeof searchText === 'string' ?
		                new RegExp(searchText, 'g') : searchText,
		        childNodes = (searchNode || document.body).childNodes,
		        cnLength = childNodes.length,
		        excludes = 'html,head,style,title,link,meta,script,object,iframe';

		    while (cnLength--) {
		        var currentNode = childNodes[cnLength];
		        if (currentNode.nodeType === 1 &&
		            (excludes + ',').indexOf(currentNode.nodeName.toLowerCase() + ',') === -1) {
		            arguments.callee(searchText, replacement, currentNode);
		        }
		        if (currentNode.nodeType !== 3 || !regex.test(currentNode.data) ) {
		            continue;
		        }
		        var parent = currentNode.parentNode,
		            frag = (function(){
		                var html = currentNode.data.replace(regex, replacement),
		                    wrap = document.createElement('div'),
		                    frag = document.createDocumentFragment();
		                wrap.innerHTML = html;
		                while (wrap.firstChild) {
		                    frag.appendChild(wrap.firstChild);
		                }
		                return frag;
		            })();
		        parent.insertBefore(frag, currentNode);
		        parent.removeChild(currentNode);
		    }
		}
		
		function textareaKeyDown(element){
			element.keydown(function(event) {
				if(event.keyCode == 40){
					if(localStorage.hashTagTextKeyDown == undefined){
						localStorage.hashTagText = $(this).val();
						localStorage.hashTagTextKeyDown = true;
					}
				}
			});
		}
		
		function textareaKeyUp(element){
			element.keyup(function(event) {
				doTag(element);
			});
		}
		
		function _leftMatch(string, area) {
	        return string.substring(0, area.selectionStart).match(/[\#\w]+$/);
	    }
	    
	    function _setCursorPosition(area, pos) {
	        if (area.setSelectionRange) {
	            area.setSelectionRange(pos, pos);
	        } else if (area.createTextRange) {
	            var range = area.createTextRange();
	            range.collapse(true);
	            range.moveEnd('character', pos);
	            range.moveStart('character', pos);
	            range.select();
	        }
	    }
			    
		function bindAutocomplete(element){
			element.bind('transformToTag', function(event, id) {
				doTag(element);
				
				// close autocomplete
				if(options.autocompleteURL) {
					element.autocomplete( "close" );
				}
			});
						
			if(options.autocompleteURL != false) {
				element.autocomplete({
					minLength:options.minLength,
					source: function( request, response ) {	
						
						var end = element.getSelection().end;
						var result = request.term.slice(0, end);
						
						var arr = result.split(' ');
						var term = arr[arr.length-1];
 						if (term.length > options.minLength) {
 							var firstchar = term.substring(0,1);
 							if(firstchar == '#') {
 								response($.ui.autocomplete.filter(
			                    options.autocompleteURL, term));
 							}
 						}

					    var offset = $(".hashtagPosition:last").offset();
					    if(offset != null)
					        $(".ui-autocomplete:visible").css({ 'position': 'absolute', 'width': 'auto', 'z-index': '2000', 'left': offset.left, 'top': offset.top + 16 });
					    else
					        $(".ui-autocomplete:visible").css({ 'position': 'absolute', 'width': 'auto', 'z-index': '2000', 'left': '0', 'top': '16' });
					    $(".hashtagPosition").remove();
					},
					
					select: function( event, ui ) {
						var beg;
			            var m = _leftMatch(this.value, this)[0];
			            
			            if(localStorage.hashTagText == undefined){
			            	beg = this.value.substring(0, this.selectionStart - m.length);
			            }else{
			            	beg = localStorage.hashTagText.substring(0, localStorage.hashTagText.length - m.length+1);
			            	localStorage.removeItem('hashTagText'); 
			            	localStorage.removeItem('hashTagTextKeyDown');
			            }
			            this.value = beg + ui.item.value + this.value.substring(this.selectionStart, this.value.length);
			         
			            var pos = beg.length + ui.item.value.length;
			            _setCursorPosition(this, pos);
						$(this).trigger('transformToTag', [ui.item.id]);
						
						return false;
					},
				});
			}
		}
	}
	
	
	
})(jQuery);